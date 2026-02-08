from langchain_core.runnables import RunnableParallel, RunnableBranch, RunnableLambda
from langchain_layer.intent.intent_chain import intent_chain
from langchain_layer.chains.customer_chain import customer_chain
from langchain_layer.chains.finance_chain import finance_chain
from llm.groq_llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_layer.agent.decision_agent import decision_agent

def decision_with_agent(state: dict):
    """
    Uses agent to make final decision and store memory.
    """
    customer_id = state.get("customer_id")

    prompt = f"""
    Based on customer risk and financial exposure,
    make a business decision.

    Customer ID: {customer_id}

    Actions:
    - Decide what should be done
    - Store decision into memory with confidence score
    """

    result = decision_agent.invoke({
        "messages": [("user", prompt)]
    })

    return result["messages"][-1].content


llm = get_llm()
parser = StrOutputParser()

parallel_chain = RunnableParallel(
    customer=customer_chain,
    finance=finance_chain
)

summary_chain = (
    ChatPromptTemplate.from_template(
        "Summarize the business query:\n{query}"
    )
    | llm
    | parser
)

decision_chain = RunnableLambda(decision_with_agent)

conditional_chain = RunnableBranch(
    (lambda x: x["task"] == "decision", decision_chain),
    (lambda x: x["task"] == "analysis", parallel_chain),
    summary_chain
)

final_chain = (
    intent_chain
    | RunnableLambda(
        lambda intent: {
            "task": intent["task"],
            "customer_id": intent["customer_id"],
            "query": intent
        }
    )
    | conditional_chain
)


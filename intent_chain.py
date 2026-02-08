from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from llm.groq_llm import get_llm

from langchain_layer.intent.schema import BusinessIntent

llm = get_llm()

intent_prompt = ChatPromptTemplate.from_template("""
Analyze the business query below and extract intent.

Query:
{query}
""")

intent_chain = (
    intent_prompt
    | llm.with_structured_output(BusinessIntent)
    | RunnableLambda(lambda x: x.model_dump())
)
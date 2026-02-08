from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from llm.groq_llm import get_llm
from langchain_layer.db.sql_tools import get_financial_exposure

llm = get_llm()
parser = StrOutputParser()

prompt = ChatPromptTemplate.from_template("""
Analyze financial exposure based on the data below.

Financial Data:
{finance_data}

Provide a brief financial insight.
""")

finance_chain = (
    RunnableLambda(
        lambda _: {
            "finance_data": get_financial_exposure.run({})
        }
    )
    | prompt
    | llm
    | parser
)
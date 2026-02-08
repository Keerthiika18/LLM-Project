from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from llm.groq_llm import get_llm

from langchain_layer.db.sql_tools import get_customer_risk_profile

llm = get_llm()
parser = StrOutputParser()

prompt = ChatPromptTemplate.from_template("""
Analyze customer risk based on the data below.

Customer Data:
{customer_data}

Provide a short risk summary.
""")

customer_chain = (
    RunnableLambda(
        lambda x: {
            "customer_data": get_customer_risk_profile.run(x["customer_id"])
        }
    )
    | prompt
    | llm
    | parser
)
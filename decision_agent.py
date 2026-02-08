from langchain.agents import create_agent
from llm.groq_llm import get_llm
from langchain_layer.db.sql_tools import (
    get_customer_risk_profile,
    get_financial_exposure,
    store_decision_memory
)

llm = get_llm()

tools = [
    get_customer_risk_profile,
    get_financial_exposure,
    store_decision_memory
]

decision_agent = create_agent(
    llm,
    tools=tools
)
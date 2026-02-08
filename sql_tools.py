import sqlite3
from langchain.tools import tool

DB_PATH = "data/processed/enterprise_intelligence.db"

@tool
def get_customer_risk_profile(customer_id: str) -> str:
    """
    Fetch customer churn, usage, billing, and support risk profile.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT
        c.customer_id,
        c.churn_flag,
        c.tenure_months,
        s.usage_intensity_score,
        b.monthly_charges,
        sp.support_tickets_count,
        sp.escalations
    FROM customers c
    JOIN services_usage s ON c.customer_id = s.customer_id
    JOIN billing_financials b ON c.customer_id = b.customer_id
    JOIN support_experience sp ON c.customer_id = sp.customer_id
    WHERE c.customer_id = ?
    """

    cursor.execute(query, (customer_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return "Customer not found"

    return str({
        "customer_id": row[0],
        "churn_flag": row[1],
        "tenure_months": row[2],
        "usage_intensity_score": row[3],
        "monthly_charges": row[4],
        "support_tickets_count": row[5],
        "escalations": row[6],
    })


@tool
def get_financial_exposure() -> str:
    """
    Returns total monthly revenue and average customer charges.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = """
    SELECT
        SUM(monthly_charges) AS total_monthly_revenue,
        AVG(monthly_charges) AS avg_monthly_charge
    FROM billing_financials
    """

    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()

    return str({
        "total_monthly_revenue": row[0],
        "avg_monthly_charge": row[1]
    })

@tool
def store_decision_memory(customer_id: str, summary: str, confidence: float) -> str:
    """
    Store final business decision into enterprise memory.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO decision_memory (customer_id, decision_summary, confidence_score)
        VALUES (?, ?, ?)
    """, (customer_id, summary, confidence))

    conn.commit()
    conn.close()

    return "Decision stored successfully"
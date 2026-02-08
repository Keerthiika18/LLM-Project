import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "data.csv"
DB_PATH = BASE_DIR / "data" / "processed" / "enterprise_intelligence.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS billing_financials;
DROP TABLE IF EXISTS services_usage;
DROP TABLE IF EXISTS support_experience;
DROP TABLE IF EXISTS decision_memory;

CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    gender TEXT,
    senior_citizen INTEGER,
    partner INTEGER,
    dependents INTEGER,
    tenure_months INTEGER,
    contract_type TEXT,
    churn_flag INTEGER
);

CREATE TABLE billing_financials (
    customer_id TEXT,
    monthly_charges REAL,
    total_charges REAL,
    payment_method TEXT,
    paperless_billing INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE services_usage (
    customer_id TEXT,
    internet_service TEXT,
    online_security INTEGER,
    tech_support INTEGER,
    streaming_services INTEGER,
    device_protection INTEGER,
    usage_intensity_score REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE support_experience (
    customer_id TEXT,
    support_tickets_count INTEGER,
    avg_resolution_time REAL,
    satisfaction_score REAL,
    escalations INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE decision_memory (
    memory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id TEXT,
    decision_type TEXT,
    decision_summary TEXT,
    risk_level TEXT,
    confidence_score REAL,
    market_context TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")

df = pd.read_csv(RAW_DATA_PATH)
df.columns = df.columns.str.strip()

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)

def yes_no(val):
    return 1 if val == "Yes" else 0

customers_df = pd.DataFrame({
    "customer_id": df["customerID"],
    "gender": df["gender"],
    "senior_citizen": df["SeniorCitizen"],
    "partner": df["Partner"].apply(yes_no),
    "dependents": df["Dependents"].apply(yes_no),
    "tenure_months": df["tenure"],
    "contract_type": df["Contract"],
    "churn_flag": df["Churn"].apply(yes_no)
})

customers_df.to_sql("customers", conn, if_exists="append", index=False)

billing_df = pd.DataFrame({
    "customer_id": df["customerID"],
    "monthly_charges": df["MonthlyCharges"],
    "total_charges": df["TotalCharges"],
    "payment_method": df["PaymentMethod"],
    "paperless_billing": df["PaperlessBilling"].apply(yes_no)
})

billing_df.to_sql("billing_financials", conn, if_exists="append", index=False)

usage_score = (
    df["StreamingTV"].apply(yes_no) +
    df["StreamingMovies"].apply(yes_no) +
    df["TechSupport"].apply(yes_no) +
    df["OnlineSecurity"].apply(yes_no)
)

usage_score = usage_score / usage_score.max()

services_df = pd.DataFrame({
    "customer_id": df["customerID"],
    "internet_service": df["InternetService"],
    "online_security": df["OnlineSecurity"].apply(yes_no),
    "tech_support": df["TechSupport"].apply(yes_no),
    "streaming_services": (
        df["StreamingTV"].apply(yes_no) + df["StreamingMovies"].apply(yes_no)
    ),
    "device_protection": df["DeviceProtection"].apply(yes_no),
    "usage_intensity_score": usage_score
})

services_df.to_sql("services_usage", conn, if_exists="append", index=False)

support_df = pd.DataFrame({
    "customer_id": df["customerID"],
    "support_tickets_count": (df["tenure"] < 12).astype(int) * 3,
    "avg_resolution_time": 24 + (df["tenure"] < 6).astype(int) * 12,
    "satisfaction_score": 5 - (df["Churn"] == "Yes").astype(int) * 2,
    "escalations": (df["Churn"] == "Yes").astype(int)
})

support_df.to_sql("support_experience", conn, if_exists="append", index=False)

for table in ["customers", "billing_financials", "services_usage", "support_experience"]:
    count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {count} rows")
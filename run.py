import streamlit as st
from langchain_layer.orchestration.main_chain import final_chain

st.set_page_config(
    page_title="LangChain Enterprise AI",
    layout="centered"
)

st.title("LangChain Enterprise AI System")
st.write("Analyze customer risk and make business decisions using LangChain")

# User input
query = st.text_input(
    "Enter your business query:",
    placeholder="Make a decision for churn risk customer 7795-CFOCW"
)

# Button
if st.button("Run Analysis"):
    if query.strip() == "":
        st.warning("Please enter a query.")
    else:
        with st.spinner("Processing..."):
            result = final_chain.invoke({
                "query": query
            })

        st.success("Done")

        # Neat output
        st.subheader("Final Response")
        st.markdown(
            f"""
            ---
            **Query:**  
            {query}

            **Response:**  
            {result}
            ---
            """
        )

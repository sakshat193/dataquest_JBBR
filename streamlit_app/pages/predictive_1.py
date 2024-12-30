import streamlit as st

st.title("Predictive Models - Page 1")
st.subheader("Model 1")
st.write("Description and functionality of Model 1.")
if st.button("Run Model 1"):
    st.success("Model 1 executed!")

st.subheader("Model 2")
st.write("Description and functionality of Model 2.")
if st.button("Run Model 2"):
    st.success("Model 2 executed!")

if st.button("Go to Predictive Models 2"):
    st.experimental_set_query_params(page="Predictive Models 2")

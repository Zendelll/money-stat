import streamlit as st
from utils.db import change_limit
from utils.sidebar import sidebar_nav
from utils.constants import CATEGORIES

st.set_page_config(page_title="Change limit", page_icon="⚙️")
sidebar_nav()

st.title("⚙️ Change limit")

st.subheader("Change category limit:")
category = st.selectbox("Category", CATEGORIES)
amount = st.number_input("Limit (€)", step=0.1, format="%.2f", value=0.0)

if st.button("Change!"):
    if amount < 0:
        st.error("Please enter a valid amount.")
    else:
        change_limit("vlada", category, amount)
        st.success(f"✅ Changed {category} limit to {amount:.2f}€!")
        st.rerun()
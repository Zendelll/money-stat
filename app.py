import streamlit as st
from utils.db import add_transaction, get_user
from utils.sidebar import sidebar_nav
from utils.constants import CATEGORIES

st.set_page_config(page_title="Add Expense", page_icon="➕")
sidebar_nav()

st.title("➕ Add Expense")

user_id = "vlada"
user_data = get_user(user_id)

st.subheader("Enter new expense:")
amount = st.number_input("Amount (€)", step=0.1, format="%.2f", value=0.0)
category = st.selectbox("Category", CATEGORIES)
comment = st.text_input("Comment (optional)")
new_month = st.checkbox("Is it a salary (start of new month)?", True)

if st.button("Add Expense"):
    if amount <= 0:
        st.error("Please enter a valid amount.")
    else:
        add_transaction(user_id, amount, category, comment, new_month)
        st.success(f"✅ Added {amount:.2f}€ to {category}!")
        st.rerun()

st.divider()

if user_data:
    st.subheader(f"**{user_data['balance']:.2f}€** -> **{user_data['predicted_savings']:.2f}€**")
    limits = user_data["limits"]
    for category in CATEGORIES:
        if category in limits:
            info = limits[category]
            color = "<span style='color:red'>" if info['spent'] > info['limit'] else ""
            st.markdown(f"**{category}**: {color}**{info['spent']:.2f}€**</span> / **{info['limit']:.2f}€**", unsafe_allow_html=True)


else:
    st.warning("No user data found.")
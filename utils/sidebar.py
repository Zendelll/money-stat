import streamlit as st

pages = {
    "add": {"label": "➕ Add Expense", "file": "app.py"},
    "edit": {"label": "⚙️ Edit Profile", "file": "pages/edit_user.py"},
}

def sidebar_nav():
    st.markdown("""<style>div[data-testid="stSidebarNav"] {display: none;}</style>""", unsafe_allow_html=True)
    with st.sidebar:
        for page in pages.values():
            st.page_link(page["file"], label=page["label"])

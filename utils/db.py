from supabase import create_client, Client
import streamlit as st
from utils.constants import DEFAULT_LIMITS
import time

# Подключение к Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

def create_user(user_id: str):
    """
    Создание нового пользователя с пустыми лимитами и 0 балансом.
    """
    data = {
        "id": user_id,
        "balance": 0.0,
        "limits": DEFAULT_LIMITS,
        "month_id": 1,
        "predicted_savings": 0
    }
    supabase.table("users").insert(data).execute()

def get_user(user_id: str):
    """
    Получить данные пользователя.
    """
    response = supabase.table("users").select("*").eq("id", user_id).single().execute()
    return response.data

def change_predicted_savings(user_id: str):
    user = get_user(user_id)
    limits = user["limits"]
    predicted_savings = user["balance"]
    for category, limit in limits.items():
        predicted_savings -= 0 if float(limit["spent"]) > float(limit["limit"]) else (float(limit["limit"])-float(limit["spent"]))
    supabase.table("users").update({"predicted_savings": predicted_savings}).eq("id", user_id).execute()

def add_transaction(user_id: str, amount: float, category: str, comment: str = "", new_month: bool = False):
    """
    Добавление траты и обновление лимита пользователя.
    """

    user = get_user(user_id)
    if not user:
        raise ValueError("Пользователь не найден")
    if category == "💸 Salary":
        supabase.table("users").update({"month_id": user["month_id"]+1}).eq("id", user_id).execute()
        user = get_user(user_id)

    # 3. Добавляем трату в таблицу transactions
    transaction = {
        "user_id": user_id,
        "amount": amount,
        "type": category,
        "comment": comment,
        "month_id": user["month_id"],
    }
    supabase.table("transactions").insert(transaction).execute()

    # 4. Обновляем лимиты
    limits = user["limits"]
    if category == "💸 Salary":
        new_balance = user["balance"] + amount
        if new_month:
            for limit_name in limits.keys():
                limits[limit_name]["spent"] = 0.0
    else:
        if category not in limits:
            limits[category] = {"limit": 0.0, "spent": 0.0}
        limits[category]["spent"] += amount
        new_balance = user["balance"] - amount
    supabase.table("users").update({
        "balance": new_balance,
        "limits": limits,
        "month_id": user["month_id"]
    }).eq("id", user_id).execute()
    change_predicted_savings(user_id)



def change_limit(user_id: str, category: str, limit: float):
    user = get_user(user_id)
    limits = user["limits"]
    if category not in limits:
        limits[category] = {"limit": limit, "spent": 0.0}
    else:
        limits[category]["limit"] = limit
    supabase.table("users").update({"limits": limits}).eq("id", user_id).execute()
    change_predicted_savings(user_id)
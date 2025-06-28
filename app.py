import streamlit as st
from datetime import date
import pandas as pd
import uuid
import os

# ファイル名（申請内容をCSVに保存）
CSV_FILE = "yukyu申請一覧.csv"

# データ保存処理
def save_data(name, dept, leave_date, reason):
    row = {
        "申請ID": str(uuid.uuid4())[:8],
        "氏名": name,
        "所属": dept,
        "申請日": leave_date.strftime("%Y-%m-%d"),
        "理由": reason,
        "ステータス": "申請中"
    }

    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(CSV_FILE, index=False)

# アプリUI（スマホ対応）
st.set_page_config(page_title="有給申請", layout="centered")
st.title("📱 有給休暇申請フォーム")

with st.form("form"):
    name = st.text_input("氏名", placeholder="例：田中一郎")
    dept = st.selectbox("所属", ["総務課", "経理課", "医務課", "看護部", "その他"])
    leave_date = st.date_input("取得希望日", min_value=date.today())
    reason = st.text_area("理由", placeholder="例：私用のため")

    submitted = st.form_submit_button("✅ 申請する")

    if submitted:
        if name and reason:
            save_data(name, dept, leave_date, reason)
            st.success("申請が送信されました。")
        else:
            st.error("氏名と理由は必須です。")


import streamlit as st
import pandas as pd
import uuid
import os
from datetime import date, datetime

CSV_FILE = "yukyu_applications.csv"

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=[
            "申請ID", "氏名", "所属", "申請日", "理由",
            "ステータス", "申請日時", "上司承認日時", "人事承認日時"
        ])

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

def submit_application(name, dept, leave_date, reason):
    df = load_data()
    new_row = {
        "申請ID": str(uuid.uuid4())[:8],
        "氏名": name,
        "所属": dept,
        "申請日": leave_date.strftime("%Y-%m-%d"),
        "理由": reason,
        "ステータス": "申請中",
        "申請日時": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "上司承認日時": "",
        "人事承認日時": ""
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)

def process_approval(approver_type):
    df = load_data()
    st.subheader("承認対象一覧")
    if approver_type == "上司":
        target_df = df[df["ステータス"] == "申請中"]
    else:
        target_df = df[df["ステータス"] == "上司承認済"]

    if target_df.empty:
        st.info("現在、承認待ちの申請はありません。")
        return

    for i, row in target_df.iterrows():
        with st.expander(f"🔹 申請ID: {row['申請ID']} | {row['氏名']} | {row['申請日']}"):
            st.markdown(f"**所属：** {row['所属']}")
            st.markdown(f"**理由：** {row['理由']}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"✅ 承認 ({row['申請ID']})"):
                    df.at[i, "ステータス"] = ("上司承認済" if approver_type == "上司" else "人事承認済")
                    df.at[i, ("上司承認日時" if approver_type == "上司" else "人事承認日時")] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    save_data(df)
                    st.success("承認しました。ページを再読み込みしてください。")
            with col2:
                if st.button(f"❌ 否認 ({row['申請ID']})"):
                    df.at[i, "ステータス"] = "否認"
                    df.at[i, ("上司承認日時" if approver_type == "上司" else "人事承認日時")] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    save_data(df)
                    st.warning("否認しました。ページを再読み込みしてください。")

def main():
    st.set_page_config(page_title="有給休暇申請", layout="centered")
    menu = st.sidebar.radio("機能を選択してください", [
        "📱 申請フォーム（スマホ）",
        "🧑‍💼 承認画面（上司）",
        "🏢 承認画面（人事課）"
    ])

    if menu == "📱 申請フォーム（スマホ）":
        st.title("📱 有給休暇申請フォーム")
        with st.form("form"):
            name = st.text_input("氏名", placeholder="例：田中一郎")
            dept = st.selectbox("所属", ["総務課", "経理課", "医務課", "看護部", "その他"])
            leave_date = st.date_input("取得希望日", min_value=date.today())
            reason = st.text_area("理由", placeholder="例：私用のため")
            submitted = st.form_submit_button("✅ 申請する")
            if submitted:
                if name and reason:
                    submit_application(name, dept, leave_date, reason)
                    st.success("申請が送信されました。")
                else:
                    st.error("氏名と理由は必須です。")

    elif menu == "🧑‍💼 承認画面（上司）":
        st.title("🧑‍💼 承認画面（上司）")
        process_approval("上司")

    else:
        st.title("🏢 承認画面（人事課）")
        process_approval("人事課")

if __name__ == "__main__":
    main()

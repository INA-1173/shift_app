import streamlit as st
from utils.shift_utils import load_requests, upsert_request, create_monthly_summary

st.title("スタッフ画面")
st.subheader("希望シフト提出")

# 名前一覧
name_list = ["長塚", "桝谷", "稲村", "矢澤"]

# 日付一覧
days = list(range(1, 32))

# 入力UI
selected_name = st.selectbox("名前を選んでください", name_list)
lunch_days = st.multiselect("昼間の出勤日を選んでください", days)
night_days = st.multiselect("夜間の出勤日を選んでください", days)

lunch_days.sort()
night_days.sort()

# 送信ボタン
if st.button("送信"):
    df = upsert_request(selected_name, lunch_days, night_days)
    st.success("希望シフトを保存しました")
else:
    df = load_requests()

# 提出状況表示
st.subheader("現在の提出状況")
st.dataframe(df, width="stretch")

# 月間シフト表表示
st.subheader("月間シフト表")
shift_df = create_monthly_summary(df)
st.dataframe(shift_df, width="stretch")
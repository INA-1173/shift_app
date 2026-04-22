import streamlit as st
import pandas as pd
from utils.shift_utils import (
    load_requests,
    text_to_days,
    build_output_table,
    to_excel_bytes
)

st.title("管理者編集画面")

if "admin_logged_in" not in st.session_state or not st.session_state["admin_logged_in"]:
    st.error("この画面は管理者専用です。先にログインしてください")
    st.stop()

st.success("管理者としてログイン中")

df = load_requests()

st.subheader("スタッフ希望一覧")
st.dataframe(df, width="stretch")

st.subheader("シフト表の生成")

category = []
days = list(range(1, 32))

for day in days:
    for _, row in df.iterrows():
        name = row["名前"]

        if pd.notna(row["昼"]):
            if day in text_to_days(row["昼"]):
                category.append({
                    "日": day,
                    "名前": name,
                    "区分": "昼",
                    "開始時間": "11:00",
                    "厨房担当": False
                })

        if pd.notna(row["夜"]):
            if day in text_to_days(row["夜"]):
                category.append({
                    "日": day,
                    "名前": name,
                    "区分": "夜",
                    "開始時間": "17:00",
                    "厨房担当": False
                })

shift_long = pd.DataFrame(category)

st.subheader("シフト編集")

if "edit_df" not in st.session_state:
    st.session_state.edit_df = pd.DataFrame(
        columns=["日", "名前", "区分", "開始時間", "厨房担当"]
    )

if st.button("シフト表を作成"):
    st.session_state.edit_df = shift_long.copy()
    st.success("シフト表を作成しました")
    st.rerun()

edited_df = st.data_editor(
    st.session_state.edit_df,
    width="stretch",
    num_rows="dynamic",
    key="editor_table",
    column_config={
        "厨房担当": st.column_config.CheckboxColumn("厨房担当")
    }
)

st.session_state.edit_df = edited_df

# 厨房が複数いないかチェック
for day in range(1, 32):
    for kubun in ["昼", "夜"]:
        kitchen = edited_df[
            (edited_df["日"] == day) &
            (edited_df["区分"] == kubun) &
            (edited_df["厨房担当"] == True)
        ]

        if len(kitchen) > 1:
            st.error(f"{day}日 {kubun} に厨房担当が複数います")


if st.button("保存"):
    edited_df.to_csv("data/shift_long.csv", index=False, encoding="utf-8-sig")
    st.success("保存しました！")
    st.rerun()

st.markdown("---")
st.subheader("出力")

output_df = build_output_table(edited_df)

st.subheader("プレビュー")
st.dataframe(output_df, width="stretch")

csv_data = output_df.to_csv(index=False, encoding="utf-8-sig")

st.download_button(
    "CSVダウンロード",
    csv_data,
    "shift_output.csv",
    "text/csv"
)

excel_data = to_excel_bytes(output_df, edited_df)

st.download_button(
    "Excelダウンロード",
    excel_data,
    "shift_output.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
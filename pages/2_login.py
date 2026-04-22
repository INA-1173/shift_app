import streamlit as st

st.title("管理者ログイン")

# 初期化（これないとバグる）
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

password = st.text_input("パスワードを入力してください", type="password")

if st.button("ログイン"):
    if password == st.secrets["ADMIN_PASSWORD"]:
        st.session_state["admin_logged_in"] = True
        st.success("ログイン成功！編集画面へ進んでください")
    else:
        st.error("パスワードが違います")

if st.session_state["admin_logged_in"]:
    st.info("現在ログイン中です")

if st.button("ログアウト"):
    st.session_state["admin_logged_in"] = False
    st.success("ログアウトしました")
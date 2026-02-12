import streamlit as st
import hashlib

def check_password(auth_level="editor"):
    def password_entered():
        password_hash = hashlib.sha256(
            st.session_state["password"].encode()
        ).hexdigest()

        admin_hash = hashlib.sha256("admin2024".encode()).hexdigest()
        editor_hash = hashlib.sha256("tsukuba1872".encode()).hexdigest()

        if auth_level == "admin":
            if password_hash == admin_hash:
                st.session_state["admin_authenticated"] = True
                del st.session_state["password"]
                return

        if password_hash == editor_hash:
            st.session_state["editor_authenticated"] = True
            del st.session_state["password"]
            return

        st.session_state["auth_failed"] = True

    if auth_level == "admin":
        if st.session_state.get("admin_authenticated", False):
            return True
    else:
        if (
            st.session_state.get("editor_authenticated", False)
            or st.session_state.get("admin_authenticated", False)
        ):
            return True

    st.text_input(
        "パスワードを入力",
        type="password",
        on_change=password_entered,
        key="password",
    )

    return False

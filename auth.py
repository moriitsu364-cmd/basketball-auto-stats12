import streamlit as st
import hashlib

# ========================================
# 認証機能
# ========================================
def check_password():
    """編集者権限の確認"""
    def password_entered():
        """パスワードが入力されたかチェック"""
        if hashlib.sha256(st.session_state["password"].encode()).hexdigest() == st.secrets.get("ADMIN_PASSWORD_HASH", hashlib.sha256("tsukuba1872".encode()).hexdigest()):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.markdown("""
    <div style="max-width: 500px; margin: 100px auto; padding: 40px; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <h2 style="color: #1d428a; text-align: center; margin-bottom: 30px;">EDITOR ACCESS</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input(
            "Enter Password",
            type="password",
            on_change=password_entered,
            key="password",
        )
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("❌ Incorrect password")
        
        st.info("💡 Default password: tsukuba1872")
        st.caption("Set ADMIN_PASSWORD_HASH in secrets.toml for custom password")
    
    return False

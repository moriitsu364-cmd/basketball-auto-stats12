"""認証機能"""
import streamlit as st
import hashlib


def check_password(password: str = None) -> bool:
    """編集者権限の確認
    
    Args:
        password: 確認するパスワード（Noneの場合はセッション状態から取得）
    
    Returns:
        認証が成功した場合True
    """
    # 引数でパスワードが渡された場合は直接チェック
    if password is not None:
        hashed = hashlib.sha256(password.encode()).hexdigest()
        expected_hash = hashlib.sha256("tsukuba1872".encode()).hexdigest()
        
        # secrets.tomlからカスタムハッシュを取得（存在する場合）
        try:
            if hasattr(st, 'secrets') and "ADMIN_PASSWORD_HASH" in st.secrets:
                expected_hash = st.secrets["ADMIN_PASSWORD_HASH"]
        except Exception:
            pass
        
        return hashed == expected_hash
    
    # 以下は元の実装（セッション状態ベース）
    def password_entered():
        """パスワードが入力されたかチェック"""
        entered_password = st.session_state["password"]
        hashed = hashlib.sha256(entered_password.encode()).hexdigest()
        expected_hash = st.secrets.get(
            "ADMIN_PASSWORD_HASH", 
            hashlib.sha256("tsukuba1872".encode()).hexdigest()
        )
        
        if hashed == expected_hash:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    # すでに認証済みの場合
    if st.session_state.get("password_correct", False):
        return True

    # 認証画面を表示
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

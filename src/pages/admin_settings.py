"""管理者設定ページ - セキュリティ強化版"""
import streamlit as st
import hashlib
import time
from datetime import datetime
from pathlib import Path
from config import ADMIN_SETTINGS, PLAYER_IMAGES_DIR, STAFF_IMAGES_DIR


def check_admin_auth():
    """管理者認証（強化版）"""
    # ログイン試行回数の制限
    if 'login_attempts' not in st.session_state:
        st.session_state['login_attempts'] = 0
        st.session_state['lockout_until'] = None
    
    # ロックアウト中かチェック
    if st.session_state['lockout_until']:
        if time.time() < st.session_state['lockout_until']:
            remaining = int(st.session_state['lockout_until'] - time.time())
            st.error(f"🔒 ログインがロックされています。残り {remaining} 秒")
            return False
        else:
            st.session_state['lockout_until'] = None
            st.session_state['login_attempts'] = 0
    
    def password_entered():
        entered_password = st.session_state["admin_password"]
        hashed = hashlib.sha256(entered_password.encode()).hexdigest()
        expected_hash = st.secrets.get(
            "ADMIN_PASSWORD_HASH",
            hashlib.sha256("tsukuba1872".encode()).hexdigest()
        )
        
        if hashed == expected_hash:
            st.session_state["admin_authenticated"] = True
            st.session_state["admin_login_time"] = time.time()
            st.session_state['login_attempts'] = 0
            del st.session_state["admin_password"]
        else:
            st.session_state["admin_authenticated"] = False
            st.session_state['login_attempts'] += 1
            
            # 最大試行回数を超えたらロックアウト
            if st.session_state['login_attempts'] >= ADMIN_SETTINGS['max_login_attempts']:
                st.session_state['lockout_until'] = time.time() + ADMIN_SETTINGS['lockout_duration']
                st.error(f"❌ ログイン試行回数が上限に達しました。{ADMIN_SETTINGS['lockout_duration']}秒間ロックされます。")
            else:
                remaining = ADMIN_SETTINGS['max_login_attempts'] - st.session_state['login_attempts']
                st.error(f"❌ パスワードが正しくありません（残り試行回数: {remaining}）")

    # セッションタイムアウトチェック
    if st.session_state.get("admin_authenticated", False):
        if time.time() - st.session_state.get("admin_login_time", 0) > ADMIN_SETTINGS['session_timeout']:
            st.session_state["admin_authenticated"] = False
            st.warning("⏰ セッションがタイムアウトしました。再度ログインしてください。")
    
    if st.session_state.get("admin_authenticated", False):
        return True
    
    # ログインフォーム
    st.markdown("""
    <div style="max-width: 600px; margin: 100px auto; padding: 3rem; background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); 
                border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.5); border: 2px solid #333;">
        <h2 style="color: #ffffff; text-align: center; margin-bottom: 2rem; font-size: 2rem; text-transform: uppercase; letter-spacing: 2px;">
            🔐 管理者ログイン<br>
            <span style="font-size: 1rem; color: #888; letter-spacing: 1px;">ADMIN ACCESS</span>
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input(
            "パスワード / Password",
            type="password",
            on_change=password_entered,
            key="admin_password",
        )
        
        st.info("💡 デフォルトパスワード: tsukuba1872")
        st.caption("secrets.tomlでADMIN_PASSWORD_HASHを設定してカスタムパスワードを使用できます")
    
    return False


def render():
    """管理者設定ページを表示"""
    if not check_admin_auth():
        return
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1d428a 0%, #c8102e 100%); padding: 2rem; margin: -1rem -2rem 2rem -2rem; border-radius: 0 0 12px 12px;">
        <h1 style="color: white; font-size: 2.5rem; font-weight: 900; margin: 0; text-transform: uppercase; letter-spacing: 2px;">
            ⚙️ 管理者設定
        </h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 1.1rem; margin-top: 0.5rem;">
            ADMIN SETTINGS / システム統括管理
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ログアウトボタン
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        if st.button("🚪 ログアウト", use_container_width=True):
            st.session_state["admin_authenticated"] = False
            st.rerun()
    
    # タブ
    tabs = st.tabs([
        "📊 システム概要",
        "🖼️ 画像管理",
        "👥 チーム情報",
        "🔒 セキュリティ",
        "⚙️ その他設定"
    ])
    
    # タブ1: システム概要
    with tabs[0]:
        st.markdown("### システム情報 / System Information")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("セッション時間", f"{int((time.time() - st.session_state.get('admin_login_time', time.time())) / 60)}分")
        
        with col2:
            st.metric("データファイル", "basketball_stats.csv")
        
        with col3:
            st.metric("ログイン試行", f"{st.session_state.get('login_attempts', 0)}回")
        
        st.markdown("---")
        
        st.markdown("### 最近のアクティビティ")
        st.info("この機能は今後実装予定です。")
    
    # タブ2: 画像管理
    with tabs[1]:
        st.markdown("### 選手・スタッフ画像管理 / Image Management")
        
        # ディレクトリ作成
        Path(PLAYER_IMAGES_DIR).mkdir(parents=True, exist_ok=True)
        Path(STAFF_IMAGES_DIR).mkdir(parents=True, exist_ok=True)
        
        img_tabs = st.tabs(["選手画像", "スタッフ画像"])
        
        with img_tabs[0]:
            st.markdown("#### 選手画像アップロード")
            player_name = st.text_input("選手名", key="player_name_img")
            player_image = st.file_uploader(
                "選手の画像をアップロード（背景透過推奨）",
                type=['png', 'jpg', 'jpeg', 'webp'],
                key="player_image"
            )
            
            if player_image and player_name:
                if st.button("選手画像を保存", key="save_player_img"):
                    # 画像を保存
                    img_path = Path(PLAYER_IMAGES_DIR) / f"{player_name}.png"
                    with open(img_path, "wb") as f:
                        f.write(player_image.getbuffer())
                    st.success(f"✅ {player_name}の画像を保存しました")
            
            # 既存画像一覧
            st.markdown("#### 登録済み選手画像")
            player_images = list(Path(PLAYER_IMAGES_DIR).glob("*"))
            if player_images:
                cols = st.columns(4)
                for i, img_path in enumerate(player_images):
                    with cols[i % 4]:
                        st.image(str(img_path), caption=img_path.stem, use_container_width=True)
            else:
                st.info("画像がまだ登録されていません")
        
        with img_tabs[1]:
            st.markdown("#### スタッフ画像アップロード")
            staff_name = st.text_input("スタッフ名", key="staff_name_img")
            staff_role = st.selectbox("役職", ["ヘッドコーチ", "アシスタントコーチ", "マネージャー"], key="staff_role")
            staff_image = st.file_uploader(
                "スタッフの画像をアップロード",
                type=['png', 'jpg', 'jpeg', 'webp'],
                key="staff_image"
            )
            
            if staff_image and staff_name:
                if st.button("スタッフ画像を保存", key="save_staff_img"):
                    img_path = Path(STAFF_IMAGES_DIR) / f"{staff_name}_{staff_role}.png"
                    with open(img_path, "wb") as f:
                        f.write(staff_image.getbuffer())
                    st.success(f"✅ {staff_name}（{staff_role}）の画像を保存しました")
            
            # 既存画像一覧
            st.markdown("#### 登録済みスタッフ画像")
            staff_images = list(Path(STAFF_IMAGES_DIR).glob("*"))
            if staff_images:
                cols = st.columns(3)
                for i, img_path in enumerate(staff_images):
                    with cols[i % 3]:
                        st.image(str(img_path), caption=img_path.stem, use_container_width=True)
            else:
                st.info("画像がまだ登録されていません")
    
    # タブ3: チーム情報
    with tabs[2]:
        st.markdown("### チーム情報設定 / Team Information")
        st.info("この機能は team_info ページで実装されます")
    
    # タブ4: セキュリティ
    with tabs[3]:
        st.markdown("### セキュリティ設定 / Security Settings")
        
        st.markdown("#### パスワード変更")
        st.markdown("""
        新しいパスワードハッシュを生成するには、以下のコマンドを実行してください：
        
        ```bash
        python -c "import hashlib; print(hashlib.sha256('新しいパスワード'.encode()).hexdigest())"
        ```
        
        生成されたハッシュを `.streamlit/secrets.toml` の `ADMIN_PASSWORD_HASH` に設定してください。
        """)
        
        st.markdown("#### セッション設定")
        st.info(f"セッションタイムアウト: {ADMIN_SETTINGS['session_timeout'] / 60}分")
        st.info(f"最大ログイン試行回数: {ADMIN_SETTINGS['max_login_attempts']}回")
        st.info(f"ロックアウト時間: {ADMIN_SETTINGS['lockout_duration'] / 60}分")
    
    # タブ5: その他設定
    with tabs[4]:
        st.markdown("### その他の設定 / Other Settings")
        
        st.markdown("#### データバックアップ")
        if st.button("📥 全データをバックアップ"):
            st.success("バックアップ機能は今後実装予定です")
        
        st.markdown("#### データベースメンテナンス")
        if st.button("🔧 データベースを最適化"):
            st.success("最適化機能は今後実装予定です")

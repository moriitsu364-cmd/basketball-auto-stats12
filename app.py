import streamlit as st
import pandas as pd

# 簡易データベース
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["試合日", "選手名", "得点", "3P", "AST", "REB"])

st.title("🏀 BasketStats AI 管理システム")

# メニュー切り替え
menu = st.sidebar.selectbox("メニュー", ["画像から登録", "シーズン統計"])

if menu == "画像から登録":
    st.header("スコアシート読み込み")
    uploaded_file = st.file_uploader("スコアシートをアップロード", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="解析対象", width=300)
        # 本来はここでAI解析を呼び出します
        st.info("AI解析シミュレーション実行中...")
        
        # 解析結果のプレビュー（手入力で修正可能）
        st.subheader("解析結果の確認・修正")
        data = {
            "試合日": ["2026-02-12", "2026-02-12"],
            "選手名": ["Player 1", "Player 2"],
            "得点": [12, 8],
            "3P": [2, 0],
            "AST": [4, 1],
            "REB": [3, 10]
        }
        df_edit = pd.data_editor(pd.DataFrame(data))

        if st.button("シーズンデータへ保存"):
            st.session_state.db = pd.concat([st.session_state.db, df_edit], ignore_index=True)
            st.success("保存しました！")

else:
    st.header("シーズンスタッツ集計")
    if not st.session_state.db.empty:
        summary = st.session_state.db.groupby("選手名")[["得点", "3P", "AST", "REB"]].sum()
        st.table(summary)
        st.bar_chart(summary["得点"])
    else:
        st.write("データがまだありません。")

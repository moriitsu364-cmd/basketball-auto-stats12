import streamlit as st
import pandas as pd

# データの保存先（セッション状態）の初期化
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
        st.info("AI解析結果を表示します。数値を修正して保存してください。")
        
        # 修正：data_editorが使えない場合でも動くように、シンプルな入力方式にバックアップを用意
        data = {
            "試合日": ["2026-02-12", "2026-02-12"],
            "選手名": ["Player 1", "Player 2"],
            "得点": [12, 8],
            "3P": [2, 0],
            "AST": [4, 1],
            "REB": [3, 10]
        }
        df_sample = pd.DataFrame(data)

        # data_editorがエラーになる場合は、通常のテーブル表示にする
        try:
            df_edit = st.data_editor(df_sample, num_rows="dynamic")
        except AttributeError:
            st.warning("お使いの環境では直接編集ができません。以下の内容で保存します。")
            st.table(df_sample)
            df_edit = df_sample

        if st.button("シーズンデータへ保存"):
            st.session_state.db = pd.concat([st.session_state.db, df_edit], ignore_index=True)
            st.success("保存しました！「シーズン統計」メニューから確認できます。")

else:
    st.header("シーズンスタッツ集計")
    if not st.session_state.db.empty:
        # 数字の列を数値型に変換（計算エラー防止）
        cols = ["得点", "3P", "AST", "REB"]
        st.session_state.db[cols] = st.session_state.db[cols].apply(pd.to_numeric)
        
        # 選手ごとに集計
        summary = st.session_state.db.groupby("選手名")[cols].sum()
        
        st.subheader("通算成績")
        st.dataframe(summary)
        
        st.subheader("得点グラフ")
        st.bar_chart(summary["得点"])
    else:
        st.info("まだデータがありません。「画像から登録」でデータを追加してください。")

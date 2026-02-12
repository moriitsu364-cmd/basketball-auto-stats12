import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import io
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ========================================
# ページ設定
# ========================================
st.set_page_config(
    page_title="TSUKUBA Stats Dashboard",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================================
# 筑波カラー & プロフェッショナル・カスタムCSS
# ========================================
st.markdown("""
<style>
    /* 全体の背景 - 深みのあるダークブルーグレー */
    .stApp {
        background-color: #0f172a;
        background-image: radial-gradient(circle at top right, #1e293b, #0f172a);
    }
    
    /* メインコンテナ */
    .main {
        background: transparent;
    }
    
    /* ヘッダー部分 - 筑波ブルーのアクセント */
    .tsukuba-header {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(10px);
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 4px solid #00A1E9;
        box-shadow: 0 10px 30px rgba(0, 161, 233, 0.15);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .tsukuba-header h1 {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 900;
        margin: 0;
        letter-spacing: 2px;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    .tsukuba-header .subtitle {
        color: #00A1E9;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    
    /* ナビゲーションタブ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
        padding: 0 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1e293b;
        color: #94a3b8;
        border-radius: 8px 8px 0 0;
        padding: 1rem 2rem;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: #00A1E9 !important;
        color: #ffffff !important;
        font-weight: bold;
    }
    
    /* 統計カード - ガラスデザイン */
    .stat-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        border-color: #00A1E9;
        background: rgba(30, 41, 59, 0.

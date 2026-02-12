"""Gemini AI機能"""
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
from config import GEMINI_PROMPT


@st.cache_resource
def setup_gemini():
    """Gemini APIのセットアップ
    
    Returns:
        (model, model_name): モデルインスタンスとモデル名のタプル
    """
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return None, None
    
    try:
        genai.configure(api_key=api_key)
        
        # 利用可能なモデルを取得
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # 優先順位付きモデルリスト
        priority_models = [
            'models/gemini-1.5-pro-latest',
            'models/gemini-1.5-pro',
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.5-flash'
        ]
        
        # 優先モデルから選択
        model_name = None
        for preferred in priority_models:
            if preferred in available_models:
                model_name = preferred
                break
        
        # 優先モデルがない場合は最初の利用可能なモデルを使用
        if not model_name and available_models:
            model_name = available_models[0]
        
        if model_name:
            model = genai.GenerativeModel(model_name)
            return model, model_name
        
        return None, None
        
    except Exception as e:
        st.error(f"Gemini API setup error: {e}")
        return None, None


def analyze_scoresheet(model, image: Image.Image) -> str:
    """スコアシート画像を分析してCSVデータを取得
    
    Args:
        model: Geminiモデルインスタンス
        image: スコアシート画像
    
    Returns:
        CSV形式のテキスト
    
    Raises:
        Exception: 分析に失敗した場合
    """
    try:
        response = model.generate_content([GEMINI_PROMPT, image])
        csv_text = response.text.replace('```csv', '').replace('```', '').strip()
        return csv_text
    except Exception as e:
        raise Exception(f"スコアシート分析エラー: {str(e)}")

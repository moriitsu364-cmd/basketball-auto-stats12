import google.generativeai as genai
import streamlit as st
# ========================================
# Gemini API設定
# ========================================
@st.cache_resource
def setup_gemini():
    """Gemini APIのセットアップ"""
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        return None, None
    
    try:
        genai.configure(api_key=api_key)
        
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        priority_models = [
            'models/gemini-1.5-pro-latest',
            'models/gemini-1.5-pro',
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.5-flash'
        ]
        
        model_name = None
        for preferred in priority_models:
            if preferred in available_models:
                model_name = preferred
                break
        
        if not model_name and available_models:
            model_name = available_models[0]
        
        if model_name:
            model = genai.GenerativeModel(model_name)
            return model, model_name
        
        return None, None
        
    except Exception as e:
        st.error(f"Gemini API setup error: {e}")
        return None, None

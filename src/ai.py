"""Gemini AI機能 - 修正版"""
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import re
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
            'models/gemini-1.5-flash',
            'models/gemini-2.0-flash-exp'
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
        st.error(f"❌ Gemini API setup error: {e}")
        return None, None


def clean_csv_response(text: str) -> str:
    """AIレスポンスからCSVテキストを抽出・クリーニング
    
    Args:
        text: AIからのレスポンステキスト
    
    Returns:
        クリーニングされたCSVテキスト
    """
    # マークダウンのコードブロックを除去
    text = re.sub(r'```csv\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    # 前後の空白を除去
    text = text.strip()
    
    # 空行を除去
    lines = [line for line in text.split('\n') if line.strip()]
    
    # ヘッダー行の検証
    if lines and not lines[0].startswith('No,'):
        # ヘッダーがない場合は追加
        header = 'No,PlayerName,GS,PTS,3PM,3PA,3P%,2PM,2PA,2P%,DK,FTM,FTA,FT%,OR,DR,TOT,AST,STL,BLK,TO,PF,TF,OF,FO,DQ,MIN'
        lines.insert(0, header)
    
    return '\n'.join(lines)


def validate_csv_data(csv_text: str) -> tuple[bool, str]:
    """CSVデータの妥当性を検証
    
    Args:
        csv_text: CSVテキスト
    
    Returns:
        (is_valid, error_message): 検証結果とエラーメッセージ
    """
    try:
        lines = csv_text.strip().split('\n')
        
        # 最低限の行数チェック
        if len(lines) < 2:
            return False, "データが不足しています（ヘッダーとデータ行が必要）"
        
        # ヘッダーのチェック
        header = lines[0].split(',')
        required_columns = ['No', 'PlayerName', 'PTS']
        
        for col in required_columns:
            if col not in header:
                return False, f"必須カラムが不足しています: {col}"
        
        # データ行のカラム数チェック
        header_count = len(header)
        for i, line in enumerate(lines[1:], start=2):
            columns = line.split(',')
            if len(columns) != header_count:
                return False, f"{i}行目のカラム数が不一致です（期待: {header_count}, 実際: {len(columns)}）"
        
        return True, ""
        
    except Exception as e:
        return False, f"検証エラー: {str(e)}"


def analyze_scoresheet(model, image: Image.Image, max_retries: int = 2) -> str:
    """スコアシート画像を分析してCSVデータを取得
    
    Args:
        model: Geminiモデルインスタンス
        image: スコアシート画像
        max_retries: 最大リトライ回数
    
    Returns:
        CSV形式のテキスト
    
    Raises:
        Exception: 分析に失敗した場合
    """
    for attempt in range(max_retries):
        try:
            # 画像のリサイズ（大きすぎる場合）
            max_size = (2000, 2000)
            if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # AIに分析依頼
            response = model.generate_content([GEMINI_PROMPT, image])
            
            if not response or not response.text:
                raise Exception("AIからのレスポンスが空です")
            
            # レスポンスのクリーニング
            csv_text = clean_csv_response(response.text)
            
            # データの検証
            is_valid, error_msg = validate_csv_data(csv_text)
            
            if not is_valid:
                if attempt < max_retries - 1:
                    st.warning(f"⚠️ データ検証失敗（試行 {attempt + 1}/{max_retries}）: {error_msg}")
                    st.info("再試行中...")
                    continue
                else:
                    raise Exception(f"データ検証失敗: {error_msg}")
            
            # 成功
            return csv_text
            
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"⚠️ 分析エラー（試行 {attempt + 1}/{max_retries}）: {str(e)}")
                st.info("再試行中...")
                continue
            else:
                raise Exception(f"スコアシート分析エラー（{max_retries}回試行後）: {str(e)}")
    
    raise Exception("分析に失敗しました")


def analyze_with_custom_prompt(model, image: Image.Image, custom_prompt: str) -> str:
    """カスタムプロンプトで画像を分析
    
    Args:
        model: Geminiモデルインスタンス
        image: 分析する画像
        custom_prompt: カスタムプロンプト
    
    Returns:
        AIのレスポンステキスト
    """
    try:
        response = model.generate_content([custom_prompt, image])
        
        if not response or not response.text:
            raise Exception("AIからのレスポンスが空です")
        
        return response.text.strip()
        
    except Exception as e:
        raise Exception(f"画像分析エラー: {str(e)}")

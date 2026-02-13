"""ユーティリティ関数 - 共通の問題を修正"""
import pandas as pd
import streamlit as st
from typing import Optional, List, Dict, Any
from pathlib import Path
import os
import hashlib
from datetime import datetime, timedelta


class DataValidator:
    """データバリデーション用クラス"""
    
    @staticmethod
    def validate_player_stats(df: pd.DataFrame) -> tuple[bool, str]:
        """選手統計データのバリデーション"""
        required_cols = ['PlayerName', 'PTS', 'TOT', 'AST']
        
        if df.empty:
            return False, "データが空です"
        
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return False, f"必須カラムが不足しています: {', '.join(missing_cols)}"
        
        return True, "OK"
    
    @staticmethod
    def validate_game_data(df: pd.DataFrame) -> tuple[bool, str]:
        """試合データのバリデーション"""
        required_cols = ['GameDate', 'Opponent', 'TeamScore', 'OpponentScore']
        
        if df.empty:
            return False, "データが空です"
        
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return False, f"必須カラムが不足しています: {', '.join(missing_cols)}"
        
        return True, "OK"
    
    @staticmethod
    def clean_percentage(value: Any) -> float:
        """パーセンテージデータのクリーニング"""
        if pd.isna(value):
            return 0.0
        
        if isinstance(value, str):
            # '%'を削除
            value = value.replace('%', '').strip()
            try:
                val = float(value)
                # 100より大きい場合は100で割る
                if val > 1:
                    val = val / 100
                return round(val, 3)
            except ValueError:
                return 0.0
        
        try:
            val = float(value)
            if val > 1:
                val = val / 100
            return round(val, 3)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def clean_time(value: Any) -> str:
        """時間データのクリーニング"""
        if pd.isna(value):
            return "00:00"
        
        if isinstance(value, str):
            # すでに正しい形式の場合
            if ':' in value:
                return value
            # 数字のみの場合は分に変換
            try:
                minutes = int(value)
                return f"{minutes:02d}:00"
            except ValueError:
                return "00:00"
        
        try:
            minutes = int(value)
            return f"{minutes:02d}:00"
        except (ValueError, TypeError):
            return "00:00"


class ImageHandler:
    """画像処理用クラス"""
    
    @staticmethod
    def get_image_path(image_type: str, name: str, base_dir: Optional[Path] = None) -> Optional[Path]:
        """画像パスを取得"""
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        
        if image_type == 'player':
            image_dir = base_dir / "data" / "images" / "players"
        elif image_type == 'staff':
            image_dir = base_dir / "data" / "images" / "staff"
        else:
            return None
        
        # 対応する拡張子を探す
        extensions = ['.png', '.jpg', '.jpeg', '.webp']
        for ext in extensions:
            image_path = image_dir / f"{name}{ext}"
            if image_path.exists():
                return image_path
        
        return None
    
    @staticmethod
    def save_image(uploaded_file, save_path: Path) -> bool:
        """画像を保存"""
        try:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            return True
        except Exception as e:
            st.error(f"画像の保存に失敗しました: {e}")
            return False
    
    @staticmethod
    def validate_image(uploaded_file, max_size_mb: int = 5) -> tuple[bool, str]:
        """画像のバリデーション"""
        if uploaded_file is None:
            return False, "ファイルが選択されていません"
        
        # ファイルサイズのチェック
        file_size = uploaded_file.size / (1024 * 1024)  # MB
        if file_size > max_size_mb:
            return False, f"ファイルサイズが大きすぎます（最大{max_size_mb}MB）"
        
        # ファイル形式のチェック
        allowed_types = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp']
        if uploaded_file.type not in allowed_types:
            return False, "対応していないファイル形式です（PNG, JPG, WEBP のみ）"
        
        return True, "OK"


class SecurityHelper:
    """セキュリティヘルパークラス"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """パスワードをハッシュ化"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """パスワードを検証"""
        return SecurityHelper.hash_password(password) == password_hash
    
    @staticmethod
    def check_session_timeout(timeout_seconds: int = 3600) -> bool:
        """セッションタイムアウトをチェック"""
        if 'last_activity' not in st.session_state:
            st.session_state.last_activity = datetime.now()
            return False
        
        last_activity = st.session_state.last_activity
        if isinstance(last_activity, str):
            try:
                last_activity = datetime.fromisoformat(last_activity)
            except ValueError:
                st.session_state.last_activity = datetime.now()
                return False
        
        elapsed = (datetime.now() - last_activity).total_seconds()
        
        if elapsed > timeout_seconds:
            return True
        
        st.session_state.last_activity = datetime.now()
        return False
    
    @staticmethod
    def check_lockout(max_attempts: int = 5, lockout_duration: int = 900) -> tuple[bool, Optional[int]]:
        """ロックアウト状態をチェック"""
        if 'login_attempts' not in st.session_state:
            st.session_state.login_attempts = 0
            st.session_state.lockout_until = None
        
        # ロックアウト中かチェック
        if st.session_state.lockout_until:
            lockout_until = st.session_state.lockout_until
            if isinstance(lockout_until, str):
                try:
                    lockout_until = datetime.fromisoformat(lockout_until)
                except ValueError:
                    st.session_state.lockout_until = None
                    return False, None
            
            if datetime.now() < lockout_until:
                remaining = int((lockout_until - datetime.now()).total_seconds())
                return True, remaining
            else:
                # ロックアウト期間終了
                st.session_state.login_attempts = 0
                st.session_state.lockout_until = None
        
        # 試行回数をチェック
        if st.session_state.login_attempts >= max_attempts:
            st.session_state.lockout_until = datetime.now() + timedelta(seconds=lockout_duration)
            return True, lockout_duration
        
        return False, None


class StatsCalculator:
    """統計計算用クラス"""
    
    @staticmethod
    def calculate_averages(df: pd.DataFrame, numeric_cols: List[str]) -> Dict[str, float]:
        """平均値を計算"""
        averages = {}
        for col in numeric_cols:
            if col in df.columns:
                try:
                    avg = df[col].mean()
                    averages[col] = round(avg, 2) if not pd.isna(avg) else 0.0
                except Exception:
                    averages[col] = 0.0
        return averages
    
    @staticmethod
    def calculate_totals(df: pd.DataFrame, numeric_cols: List[str]) -> Dict[str, float]:
        """合計値を計算"""
        totals = {}
        for col in numeric_cols:
            if col in df.columns:
                try:
                    total = df[col].sum()
                    totals[col] = round(total, 2) if not pd.isna(total) else 0.0
                except Exception:
                    totals[col] = 0.0
        return totals
    
    @staticmethod
    def calculate_fg_percentage(df: pd.DataFrame) -> float:
        """FG成功率を計算"""
        try:
            if '2PM' in df.columns and '3PM' in df.columns and '2PA' in df.columns and '3PA' in df.columns:
                fgm = df['2PM'].sum() + df['3PM'].sum()
                fga = df['2PA'].sum() + df['3PA'].sum()
                if fga > 0:
                    return round(fgm / fga * 100, 1)
        except Exception:
            pass
        return 0.0
    
    @staticmethod
    def calculate_win_rate(wins: int, losses: int) -> float:
        """勝率を計算"""
        total = wins + losses
        if total == 0:
            return 0.0
        return round(wins / total * 100, 1)


class ErrorHandler:
    """エラーハンドリング用クラス"""
    
    @staticmethod
    def handle_file_error(e: Exception, operation: str = "ファイル操作"):
        """ファイル操作エラーのハンドリング"""
        error_msg = str(e)
        if "Permission denied" in error_msg:
            st.error(f"{operation}に失敗しました: 権限がありません")
        elif "No such file" in error_msg:
            st.error(f"{operation}に失敗しました: ファイルが見つかりません")
        elif "Read-only" in error_msg:
            st.error(f"{operation}に失敗しました: 読み取り専用です")
        else:
            st.error(f"{operation}に失敗しました: {error_msg}")
    
    @staticmethod
    def handle_data_error(e: Exception, operation: str = "データ操作"):
        """データ操作エラーのハンドリング"""
        error_msg = str(e)
        if "KeyError" in error_msg:
            st.error(f"{operation}に失敗しました: 必要なカラムが見つかりません")
        elif "ValueError" in error_msg:
            st.error(f"{operation}に失敗しました: データ形式が正しくありません")
        else:
            st.error(f"{operation}に失敗しました: {error_msg}")


# グローバルインスタンス
validator = DataValidator()
image_handler = ImageHandler()
security = SecurityHelper()
stats_calc = StatsCalculator()
error_handler = ErrorHandler()

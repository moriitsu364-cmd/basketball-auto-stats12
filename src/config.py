"""アプリケーション設定 - 改善版（エラーハンドリング強化）"""
from pathlib import Path
import os
import sys
import hashlib

# デバッグモード（環境変数から取得）
DEBUG_MODE = os.getenv('DEBUG', 'False').lower() == 'true'

def safe_mkdir(path: Path, description: str = ""):
    """安全にディレクトリを作成"""
    try:
        path.mkdir(parents=True, exist_ok=True)
        if DEBUG_MODE:
            print(f"✅ ディレクトリ作成: {path}")
        return True
    except (PermissionError, OSError, FileExistsError) as e:
        if DEBUG_MODE:
            print(f"⚠️ ディレクトリ作成スキップ ({description}): {e}")
        return False

# ベースディレクトリの設定
try:
    BASE_DIR = Path(__file__).parent.parent
except Exception:
    BASE_DIR = Path.cwd()

DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = DATA_DIR / "images"

# ディレクトリを確実に作成（エラーを無視）
safe_mkdir(DATA_DIR, "データディレクトリ")
safe_mkdir(IMAGES_DIR, "画像ディレクトリ")
safe_mkdir(IMAGES_DIR / "players", "選手画像ディレクトリ")
safe_mkdir(IMAGES_DIR / "staff", "スタッフ画像ディレクトリ")

# データベースファイル（文字列パス）
DATA_FILE = str(DATA_DIR / "basketball_stats.csv")
TEAM_INFO_FILE = str(DATA_DIR / "team_info.csv")
OPPONENT_STATS_FILE = str(DATA_DIR / "opponent_stats.csv")
PLAYER_IMAGES_DIR = str(IMAGES_DIR / "players")
STAFF_IMAGES_DIR = str(IMAGES_DIR / "staff")

# カラム定義
STAT_COLUMNS = [
    'No', 'PlayerName', 'GS', 'PTS', '3PM', '3PA', '3P%', 
    '2PM', '2PA', '2P%', 'DK', 'FTM', 'FTA', 'FT%',
    'OR', 'DR', 'TOT', 'AST', 'STL', 'BLK', 'TO', 
    'PF', 'TF', 'OF', 'FO', 'DQ', 'MIN',
    'GameDate', 'Season', 'Opponent', 'TeamScore', 'OpponentScore',
    'GameFormat'
]

# チーム情報カラム
TEAM_INFO_COLUMNS = [
    'Season', 'TeamName', 'HeadCoach', 'AssistantCoaches', 
    'Managers', 'HomeVenue', 'TeamMotto', 'SeasonGoals'
]

# 対戦相手統計カラム
OPPONENT_STATS_COLUMNS = [
    'Season', 'Opponent', 'GamesPlayed', 'Wins', 'Losses',
    'AvgPtsFor', 'AvgPtsAgainst', 'AvgRebFor', 'AvgRebAgainst',
    'AvgAstFor', 'AvgAstAgainst'
]

# シーズンリスト
SEASONS = ["2023-24", "2024-25", "2025-26", "2026-27"]

# 試合形式
GAME_FORMATS = {
    '4Q': '4クォーター制',
    '2Q': '2クォーター制',
    'Other': 'その他'
}

# カラー設定
NBA_COLORS = {
    'primary': '#1d428a',
    'secondary': '#c8102e',
    'background': '#ffffff',
    'card_bg': '#f8f9fa',
    'gold': '#ffd700',
    'silver': '#c0c0c0',
    'bronze': '#cd7f32',
    'dark': '#212529',
    'light': '#f8f9fa',
    'gray': '#6c757d',
    'success': '#28a745',
    'danger': '#dc3545',
    'warning': '#ffc107',
    'info': '#17a2b8'
}

# 統計カテゴリ
STAT_CATEGORIES = {
    'PTS': {'label': 'ポイント', 'short': 'PPG', 'icon': '🏀', 'description': '得点'},
    'TOT': {'label': 'リバウンド', 'short': 'RPG', 'icon': '💪', 'description': '総リバウンド'},
    'AST': {'label': 'アシスト', 'short': 'APG', 'icon': '🎯', 'description': 'アシスト'},
    'STL': {'label': 'スティール', 'short': 'SPG', 'icon': '🛡️', 'description': 'スティール'},
    'BLK': {'label': 'ブロック', 'short': 'BPG', 'icon': '🚫', 'description': 'ブロック'},
    '3PM': {'label': '3ポイント', 'short': '3PM', 'icon': '🎯', 'description': '3ポイント成功数'},
    '3P%': {'label': '3P成功率', 'short': '3P%', 'icon': '📊', 'description': '3ポイント成功率'},
    'FG%': {'label': 'FG成功率', 'short': 'FG%', 'icon': '📊', 'description': 'フィールドゴール成功率'},
    'FT%': {'label': 'FT成功率', 'short': 'FT%', 'icon': '🎯', 'description': 'フリースロー成功率'},
    'MIN': {'label': '出場時間', 'short': 'MIN', 'icon': '⏱️', 'description': '出場時間'}
}

# Gemini AIプロンプト
GEMINI_PROMPT = """
Extract basketball scoresheet data from this image in CSV format with headers:

No,PlayerName,GS,PTS,3PM,3PA,3P%,2PM,2PA,2P%,DK,FTM,FTA,FT%,OR,DR,TOT,AST,STL,BLK,TO,PF,TF,OF,FO,DQ,MIN

Rules:
- GS: 1 if starter (●), 0 otherwise
- Percentages: numbers only (no % symbol), use decimal format (e.g., 0.5 for 50%)
- MIN: format like "32:38" (minutes:seconds)
- Use 0 for missing values
- Exclude Team/Coaches rows
- Exclude TOTALS row
- Extract player names accurately in Japanese
- PlayerName should be in format: "姓 名" (e.g., "山田 太郎")
- No should be jersey number

Output CSV only, no explanations, no markdown formatting.
"""

# 画像設定
IMAGE_SETTINGS = {
    'max_size_mb': 5,
    'allowed_formats': ['png', 'jpg', 'jpeg', 'webp'],
    'thumbnail_size': (300, 300),
    'profile_size': (500, 500),
    'max_width': 2000,
    'max_height': 2000
}

# 管理者設定
ADMIN_SETTINGS = {
    'session_timeout': 3600,
    'max_login_attempts': 5,
    'lockout_duration': 900,
    'default_password': 'tsukuba1872'
}

# デフォルトパスワードのハッシュ（SHA-256）
DEFAULT_PASSWORD_HASH = hashlib.sha256('tsukuba1872'.encode()).hexdigest()

# ロギング設定
LOGGING_CONFIG = {
    'enabled': DEBUG_MODE,
    'level': 'DEBUG' if DEBUG_MODE else 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# パフォーマンス設定
PERFORMANCE_SETTINGS = {
    'cache_ttl': 300,
    'max_dataframe_size': 10000,
    'chunk_size': 1000
}

# UI設定
UI_SETTINGS = {
    'items_per_page': 10,
    'chart_height': 400,
    'chart_width': 600,
    'animation_duration': 500
}

# 環境情報をデバッグ出力
if DEBUG_MODE:
    print(f"🔍 デバッグモード: 有効")
    print(f"📁 BASE_DIR: {BASE_DIR}")
    print(f"📁 DATA_DIR: {DATA_DIR}")
    print(f"📁 IMAGES_DIR: {IMAGES_DIR}")
    print(f"🐍 Python: {sys.version}")
    print(f"📂 作業ディレクトリ: {os.getcwd()}")

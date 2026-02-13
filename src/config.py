"""アプリケーション設定 - 改善版"""
from pathlib import Path
import os

# ベースディレクトリの設定
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = DATA_DIR / "images"

# ディレクトリを確実に作成（エラーを無視）
try:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    (IMAGES_DIR / "players").mkdir(parents=True, exist_ok=True)
    (IMAGES_DIR / "staff").mkdir(parents=True, exist_ok=True)
except (PermissionError, OSError, FileExistsError):
    # 読み取り専用ファイルシステムの場合はスキップ
    pass

# データベースファイル
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
    'GameFormat'  # 新規: '4Q', '2Q', 'Other'
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

# NBAカラー
NBA_COLORS = {
    'primary': '#1d428a',
    'secondary': '#c8102e',
    'background': '#ffffff',  # 白背景
    'card_bg': '#f8f9fa',     # カード背景
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
    'session_timeout': 3600,  # 1時間
    'max_login_attempts': 5,
    'lockout_duration': 900,   # 15分
    'default_password': 'tsukuba1872'  # デフォルトパスワード（本番では変更すること）
}

# デフォルトパスワードのハッシュ（SHA-256）
import hashlib
DEFAULT_PASSWORD_HASH = hashlib.sha256('tsukuba1872'.encode()).hexdigest()

# デバッグモード
DEBUG_MODE = os.getenv('DEBUG', 'False').lower() == 'true'

# ロギング設定
LOGGING_CONFIG = {
    'enabled': True,
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# パフォーマンス設定
PERFORMANCE_SETTINGS = {
    'cache_ttl': 300,  # キャッシュの有効期限（秒）
    'max_dataframe_size': 10000,  # データフレームの最大行数
    'chunk_size': 1000  # チャンク処理のサイズ
}

# UI設定
UI_SETTINGS = {
    'items_per_page': 10,
    'chart_height': 400,
    'chart_width': 600,
    'animation_duration': 500
}

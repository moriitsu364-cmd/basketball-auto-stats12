"""アプリケーション設定"""

# データベース
DATA_FILE = "data/basketball_stats.csv"
TEAM_INFO_FILE = "data/team_info.csv"
OPPONENT_STATS_FILE = "data/opponent_stats.csv"
PLAYER_IMAGES_DIR = "data/images/players"
STAFF_IMAGES_DIR = "data/images/staff"

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
    'background': '#f5f5f5',
    'gold': '#ffd700',
    'silver': '#c0c0c0',
    'bronze': '#cd7f32',
    'dark': '#000000',
    'light': '#ffffff',
    'gray': '#6c757d',
    'success': '#28a745',
    'danger': '#dc3545',
    'warning': '#ffc107'
}

# 統計カテゴリ
STAT_CATEGORIES = {
    'PTS': {'label': 'ポイント', 'short': 'PPG', 'icon': '🏀'},
    'TOT': {'label': 'リバウンド', 'short': 'RPG', 'icon': '💪'},
    'AST': {'label': 'アシスト', 'short': 'APG', 'icon': '🎯'},
    'STL': {'label': 'スティール', 'short': 'SPG', 'icon': '🛡️'},
    'BLK': {'label': 'ブロック', 'short': 'BPG', 'icon': '🚫'},
    '3PM': {'label': '3ポイント', 'short': '3PM', 'icon': '🎯'},
    'FG%': {'label': 'FG成功率', 'short': 'FG%', 'icon': '📊'},
    'MIN': {'label': '出場時間', 'short': 'MIN', 'icon': '⏱️'}
}

# Gemini AIプロンプト
GEMINI_PROMPT = """
Extract basketball scoresheet data from this image in CSV format with headers:

No,PlayerName,GS,PTS,3PM,3PA,3P%,2PM,2PA,2P%,DK,FTM,FTA,FT%,OR,DR,TOT,AST,STL,BLK,TO,PF,TF,OF,FO,DQ,MIN

Rules:
- GS: 1 if starter (●), 0 otherwise
- Percentages: numbers only (no % symbol)
- MIN: format like "32:38"
- Use 0 for missing values
- Exclude Team/Coaches rows
- Exclude TOTALS row
- Extract player names accurately

Output CSV only, no explanations.
"""

# 画像設定
IMAGE_SETTINGS = {
    'max_size_mb': 5,
    'allowed_formats': ['png', 'jpg', 'jpeg', 'webp'],
    'thumbnail_size': (300, 300),
    'profile_size': (500, 500)
}

# 管理者設定
ADMIN_SETTINGS = {
    'session_timeout': 3600,  # 1時間
    'max_login_attempts': 5,
    'lockout_duration': 900   # 15分
}

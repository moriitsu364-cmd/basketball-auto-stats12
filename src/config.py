"""アプリケーション設定"""

# データベース
DATA_FILE = "data/basketball_stats.csv"

# カラム定義
STAT_COLUMNS = [
    'No', 'PlayerName', 'GS', 'PTS', '3PM', '3PA', '3P%', 
    '2PM', '2PA', '2P%', 'DK', 'FTM', 'FTA', 'FT%',
    'OR', 'DR', 'TOT', 'AST', 'STL', 'BLK', 'TO', 
    'PF', 'TF', 'OF', 'FO', 'DQ', 'MIN',
    'GameDate', 'Season', 'Opponent', 'TeamScore', 'OpponentScore'
]

# シーズンリスト
SEASONS = ["2023-24", "2024-25", "2025-26", "2026-27"]

# NBAカラー
NBA_COLORS = {
    'primary': '#1d428a',
    'secondary': '#c8102e',
    'background': '#f5f5f5',
    'gold': '#ffd700',
    'silver': '#c0c0c0',
    'bronze': '#cd7f32'
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

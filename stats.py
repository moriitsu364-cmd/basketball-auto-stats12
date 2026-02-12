import pandas as pd
# ========================================
# 統計計算
# ========================================
def calculate_stats(df, player_name=None):
    """統計を計算"""
    if player_name:
        df = df[df['PlayerName'] == player_name]
    
    if len(df) == 0:
        return {
            'GP': 0, 'PTS': 0, 'REB': 0, 'AST': 0, 'STL': 0, 'BLK': 0,
            'FG%': 0, '3P%': 0, 'FT%': 0, 'TO': 0, 'PF': 0
        }
    
    stats = {
        'GP': len(df),
        'PTS': df['PTS'].mean(),
        'REB': df['TOT'].mean(),
        'AST': df['AST'].mean(),
        'STL': df['STL'].mean(),
        'BLK': df['BLK'].mean(),
        'TO': df['TO'].mean(),
        'PF': df['PF'].mean(),
        'FG%': (df['3PM'].sum() + df['2PM'].sum()) / (df['3PA'].sum() + df['2PA'].sum()) * 100 if (df['3PA'].sum() + df['2PA'].sum()) > 0 else 0,
        '3P%': df['3PM'].sum() / df['3PA'].sum() * 100 if df['3PA'].sum() > 0 else 0,
        'FT%': df['FTM'].sum() / df['FTA'].sum() * 100 if df['FTA'].sum() > 0 else 0,
    }
    return stats

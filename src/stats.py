"""統計計算 - パーセンテージ修正版（堅牢性向上）"""
import pandas as pd
import numpy as np


def safe_numeric(value):
    """値を安全に数値に変換"""
    try:
        if pd.isna(value):
            return 0
        if isinstance(value, str):
            # 文字列から数値を抽出
            value = value.replace('%', '').replace(',', '').strip()
            return float(value) if value else 0
        return float(value)
    except:
        return 0


def safe_percentage(made, attempted):
    """安全なパーセンテージ計算（0-100の範囲で返す）"""
    try:
        made = safe_numeric(made)
        attempted = safe_numeric(attempted)
        
        if attempted == 0:
            return 0
        
        pct = made / attempted
        
        # 既に0-1形式なら100倍、0-100形式ならそのまま
        if pct <= 1:
            return pct * 100
        # 異常に大きい値（100より大きい）はそのまま返す
        return pct
    except:
        return 0


def calculate_stats(df: pd.DataFrame, player_name: str = None) -> dict:
    """選手またはチームの統計を計算
    
    Args:
        df: データフレーム
        player_name: 選手名（Noneの場合はチーム全体）
    
    Returns:
        統計情報の辞書
    """
    if player_name:
        df = df[df['PlayerName'] == player_name]
    
    if len(df) == 0:
        return {
            'GP': 0, 'PTS': 0, 'REB': 0, 'AST': 0, 'STL': 0, 'BLK': 0,
            'FG%': 0, '3P%': 0, 'FT%': 0, 'TO': 0, 'PF': 0
        }
    
    # 安全な数値変換を使用
    total_3pm = df['3PM'].apply(safe_numeric).sum()
    total_3pa = df['3PA'].apply(safe_numeric).sum()
    total_2pm = df['2PM'].apply(safe_numeric).sum()
    total_2pa = df['2PA'].apply(safe_numeric).sum()
    total_ftm = df['FTM'].apply(safe_numeric).sum()
    total_fta = df['FTA'].apply(safe_numeric).sum()
    
    total_fgm = total_3pm + total_2pm
    total_fga = total_3pa + total_2pa
    
    stats = {
        'GP': len(df),
        'PTS': df['PTS'].apply(safe_numeric).mean(),
        'REB': df['TOT'].apply(safe_numeric).mean(),
        'AST': df['AST'].apply(safe_numeric).mean(),
        'STL': df['STL'].apply(safe_numeric).mean(),
        'BLK': df['BLK'].apply(safe_numeric).mean(),
        'TO': df['TO'].apply(safe_numeric).mean(),
        'PF': df['PF'].apply(safe_numeric).mean(),
        'FG%': safe_percentage(total_fgm, total_fga),
        '3P%': safe_percentage(total_3pm, total_3pa),
        'FT%': safe_percentage(total_ftm, total_fta),
    }
    
    return stats


def get_leaders(df: pd.DataFrame, stat: str, n: int = 10) -> pd.DataFrame:
    """リーダーボードを取得
    
    Args:
        df: データフレーム
        stat: 統計カテゴリ（'PTS', 'TOT', 'AST'）
        n: 上位何人まで取得するか
    
    Returns:
        リーダーボードのデータフレーム
    """
    # 数値変換してから集計
    df_clean = df.copy()
    df_clean[stat] = df_clean[stat].apply(safe_numeric)
    
    leaders = df_clean.groupby('PlayerName').agg({
        stat: ['sum', 'mean', 'count']
    }).round(1)
    
    stat_labels = {
        'PTS': ['Total', 'PPG', 'GP'],
        'TOT': ['Total', 'RPG', 'GP'],
        'AST': ['Total', 'APG', 'GP'],
        'STL': ['Total', 'SPG', 'GP'],
        'BLK': ['Total', 'BPG', 'GP']
    }
    
    leaders.columns = stat_labels.get(stat, ['Total', 'AVG', 'GP'])
    leaders = leaders.sort_values(leaders.columns[1], ascending=False).head(n)
    
    return leaders


def calculate_team_stats(game_data: pd.DataFrame) -> dict:
    """試合のチーム統計を計算
    
    Args:
        game_data: 試合のデータフレーム
    
    Returns:
        チーム統計の辞書
    """
    # 安全な数値変換を使用
    total_3pm = game_data['3PM'].apply(safe_numeric).sum()
    total_3pa = game_data['3PA'].apply(safe_numeric).sum()
    total_2pm = game_data['2PM'].apply(safe_numeric).sum()
    total_2pa = game_data['2PA'].apply(safe_numeric).sum()
    total_ftm = game_data['FTM'].apply(safe_numeric).sum()
    total_fta = game_data['FTA'].apply(safe_numeric).sum()
    
    total_fgm = total_3pm + total_2pm
    total_fga = total_3pa + total_2pa
    
    return {
        'total_pts': game_data['PTS'].apply(safe_numeric).sum(),
        'total_reb': game_data['TOT'].apply(safe_numeric).sum(),
        'total_ast': game_data['AST'].apply(safe_numeric).sum(),
        'fg_pct': safe_percentage(total_fgm, total_fga),
        '3p_pct': safe_percentage(total_3pm, total_3pa),
        'ft_pct': safe_percentage(total_ftm, total_fta),
    }


def calculate_season_overview(season_data: pd.DataFrame) -> dict:
    """シーズン概要を計算
    
    Args:
        season_data: シーズンのデータフレーム
    
    Returns:
        シーズン概要の辞書
    """
    games = len(season_data['GameDate'].unique())
    players = season_data['PlayerName'].nunique()
    
    # 安全な数値変換
    season_data_clean = season_data.copy()
    season_data_clean['PTS'] = season_data_clean['PTS'].apply(safe_numeric)
    season_data_clean['TeamScore'] = season_data_clean['TeamScore'].apply(safe_numeric)
    season_data_clean['OpponentScore'] = season_data_clean['OpponentScore'].apply(safe_numeric)
    
    avg_pts = season_data_clean.groupby('GameDate')['PTS'].sum().mean()
    wins = len(season_data_clean[season_data_clean['TeamScore'] > season_data_clean['OpponentScore']]['GameDate'].unique())
    losses = len(season_data_clean[season_data_clean['TeamScore'] < season_data_clean['OpponentScore']]['GameDate'].unique())
    
    return {
        'games': games,
        'players': players,
        'avg_pts': avg_pts,
        'wins': wins,
        'losses': losses,
        'win_pct': (wins / games * 100) if games > 0 else 0
    }

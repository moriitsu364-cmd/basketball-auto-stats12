"""統計計算 - パーセンテージ修正版"""
import pandas as pd


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
    
    total_fgm = df['3PM'].sum() + df['2PM'].sum()
    total_fga = df['3PA'].sum() + df['2PA'].sum()
    
    # パーセンテージは0-1形式で保存されているので、100倍して表示用にする
    def safe_percentage(made, attempted):
        """安全なパーセンテージ計算（0-100の範囲で返す）"""
        if attempted == 0:
            return 0
        pct = (made / attempted)
        # 既に0-1形式なら100倍、0-100形式ならそのまま
        if pct <= 1:
            return pct * 100
        return pct
    
    stats = {
        'GP': len(df),
        'PTS': df['PTS'].mean(),
        'REB': df['TOT'].mean(),
        'AST': df['AST'].mean(),
        'STL': df['STL'].mean(),
        'BLK': df['BLK'].mean(),
        'TO': df['TO'].mean(),
        'PF': df['PF'].mean(),
        'FG%': safe_percentage(total_fgm, total_fga),
        '3P%': safe_percentage(df['3PM'].sum(), df['3PA'].sum()),
        'FT%': safe_percentage(df['FTM'].sum(), df['FTA'].sum()),
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
    leaders = df.groupby('PlayerName').agg({
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
    total_fgm = game_data['3PM'].sum() + game_data['2PM'].sum()
    total_fga = game_data['3PA'].sum() + game_data['2PA'].sum()
    
    # パーセンテージは0-1形式で保存されているので、100倍して表示用にする
    def safe_percentage(made, attempted):
        """安全なパーセンテージ計算（0-100の範囲で返す）"""
        if attempted == 0:
            return 0
        pct = (made / attempted)
        # 既に0-1形式なら100倍、0-100形式ならそのまま
        if pct <= 1:
            return pct * 100
        return pct
    
    return {
        'total_pts': game_data['PTS'].sum(),
        'total_reb': game_data['TOT'].sum(),
        'total_ast': game_data['AST'].sum(),
        'fg_pct': safe_percentage(total_fgm, total_fga),
        '3p_pct': safe_percentage(game_data['3PM'].sum(), game_data['3PA'].sum()),
        'ft_pct': safe_percentage(game_data['FTM'].sum(), game_data['FTA'].sum()),
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
    avg_pts = season_data.groupby('GameDate')['PTS'].sum().mean()
    wins = len(season_data[season_data['TeamScore'] > season_data['OpponentScore']]['GameDate'].unique())
    losses = len(season_data[season_data['TeamScore'] < season_data['OpponentScore']]['GameDate'].unique())
    
    return {
        'games': games,
        'players': players,
        'avg_pts': avg_pts,
        'wins': wins,
        'losses': losses,
        'win_pct': (wins / games * 100) if games > 0 else 0
    }

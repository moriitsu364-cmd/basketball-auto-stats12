"""データベース操作"""
import pandas as pd
import streamlit as st
from pathlib import Path
from config import DATA_FILE, STAT_COLUMNS


class StatsDatabase:
    """バスケットボール統計データベース"""
    
    def __init__(self):
        self.data_file = Path(DATA_FILE)
        self.data_file.parent.mkdir(exist_ok=True)
    
    @property
    def df(self) -> pd.DataFrame:
        """データフレームを取得"""
        if 'database' not in st.session_state:
            self.load()
        return st.session_state['database']
    
    def load(self):
        """データベースを読み込み"""
        if self.data_file.exists():
            try:
                st.session_state['database'] = pd.read_csv(self.data_file)
            except Exception as e:
                st.error(f"データ読み込みエラー: {e}")
                st.session_state['database'] = self._create_empty()
        else:
            st.session_state['database'] = self._create_empty()
    
    def save(self) -> bool:
        """データベースを保存"""
        try:
            self.df.to_csv(self.data_file, index=False)
            return True
        except Exception as e:
            st.error(f"保存エラー: {e}")
            return False
    
    def add_game(self, game_df: pd.DataFrame):
        """試合データを追加"""
        st.session_state['database'] = pd.concat(
            [self.df, game_df], 
            ignore_index=True
        )
    
    def delete_game(self, game_date: str, opponent: str):
        """試合データを削除"""
        st.session_state['database'] = self.df[
            ~((self.df['GameDate'] == game_date) & 
              (self.df['Opponent'] == opponent))
        ]
    
    def get_season_data(self, season: str) -> pd.DataFrame:
        """シーズンデータを取得"""
        return self.df[self.df['Season'] == season]
    
    def get_player_data(self, player_name: str) -> pd.DataFrame:
        """選手データを取得"""
        return self.df[self.df['PlayerName'] == player_name].sort_values('GameDate')
    
    def get_game_data(self, game_date: str) -> pd.DataFrame:
        """試合データを取得"""
        return self.df[self.df['GameDate'] == game_date]
    
    def get_all_seasons(self) -> list:
        """全シーズンのリストを取得"""
        return sorted(self.df['Season'].unique(), reverse=True)
    
    def get_all_players(self) -> list:
        """全選手のリストを取得"""
        return sorted(self.df['PlayerName'].unique())
    
    def get_all_games(self) -> list:
        """全試合のリストを取得"""
        return sorted(self.df['GameDate'].unique(), reverse=True)
    
    @staticmethod
    def _create_empty() -> pd.DataFrame:
        """空のデータフレームを作成"""
        return pd.DataFrame(columns=STAT_COLUMNS)

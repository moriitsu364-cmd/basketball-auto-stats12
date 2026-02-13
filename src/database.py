"""データベース操作 - 改善版"""
import pandas as pd
import streamlit as st
from pathlib import Path
from typing import Optional, List
import os


class StatsDatabase:
    """バスケットボール統計データベース"""
    
    def __init__(self, data_file: str = "data/basketball_stats.csv"):
        # スクリプトの場所を基準にパスを設定
        base_dir = Path(__file__).parent.parent
        self.data_file = base_dir / data_file
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 必要なカラム定義
        self.stat_columns = [
            'No', 'PlayerName', 'GS', 'PTS', '3PM', '3PA', '3P%', 
            '2PM', '2PA', '2P%', 'DK', 'FTM', 'FTA', 'FT%',
            'OR', 'DR', 'TOT', 'AST', 'STL', 'BLK', 'TO', 
            'PF', 'TF', 'OF', 'FO', 'DQ', 'MIN',
            'GameDate', 'Season', 'Opponent', 'TeamScore', 'OpponentScore',
            'GameFormat'
        ]
    
    @property
    def df(self) -> pd.DataFrame:
        """データフレームを取得"""
        if 'database' not in st.session_state:
            self.load()
        return st.session_state.get('database', self._create_empty())
    
    def load(self) -> bool:
        """データベースを読み込み"""
        try:
            if self.data_file.exists():
                df = pd.read_csv(self.data_file)
                # カラムの検証
                missing_cols = set(self.stat_columns) - set(df.columns)
                if missing_cols:
                    st.warning(f"不足しているカラムを追加します: {missing_cols}")
                    for col in missing_cols:
                        df[col] = None if col == 'GameFormat' else 0
                
                st.session_state['database'] = df
                return True
            else:
                st.session_state['database'] = self._create_empty()
                st.info("新しいデータベースを作成しました")
                return True
        except Exception as e:
            st.error(f"データ読み込みエラー: {e}")
            st.session_state['database'] = self._create_empty()
            return False
    
    def save(self) -> bool:
        """データベースを保存"""
        try:
            df = self.df
            if df.empty:
                st.warning("保存するデータがありません")
                return False
            
            # ディレクトリが存在することを確認
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            
            # CSVに保存
            df.to_csv(self.data_file, index=False)
            st.success(f"データを保存しました: {self.data_file}")
            return True
        except Exception as e:
            st.error(f"保存エラー: {e}")
            return False
    
    def add_game(self, game_df: pd.DataFrame) -> bool:
        """試合データを追加"""
        try:
            if game_df.empty:
                st.warning("追加するデータがありません")
                return False
            
            # カラムの検証
            missing_cols = set(self.stat_columns) - set(game_df.columns)
            if missing_cols:
                for col in missing_cols:
                    game_df[col] = None if col == 'GameFormat' else 0
            
            # データを追加
            current_df = self.df
            st.session_state['database'] = pd.concat(
                [current_df, game_df], 
                ignore_index=True
            )
            return True
        except Exception as e:
            st.error(f"データ追加エラー: {e}")
            return False
    
    def delete_game(self, game_date: str, opponent: str) -> bool:
        """試合データを削除"""
        try:
            df = self.df
            before_count = len(df)
            
            st.session_state['database'] = df[
                ~((df['GameDate'] == game_date) & 
                  (df['Opponent'] == opponent))
            ]
            
            after_count = len(st.session_state['database'])
            deleted = before_count - after_count
            
            if deleted > 0:
                st.success(f"{deleted}件のレコードを削除しました")
                return True
            else:
                st.warning("削除するデータが見つかりませんでした")
                return False
        except Exception as e:
            st.error(f"削除エラー: {e}")
            return False
    
    def get_season_data(self, season: str) -> pd.DataFrame:
        """シーズンデータを取得"""
        try:
            df = self.df
            if 'Season' not in df.columns:
                return self._create_empty()
            return df[df['Season'] == season].copy()
        except Exception as e:
            st.error(f"シーズンデータ取得エラー: {e}")
            return self._create_empty()
    
    def get_player_data(self, player_name: str) -> pd.DataFrame:
        """選手データを取得"""
        try:
            df = self.df
            if 'PlayerName' not in df.columns:
                return self._create_empty()
            return df[df['PlayerName'] == player_name].sort_values('GameDate').copy()
        except Exception as e:
            st.error(f"選手データ取得エラー: {e}")
            return self._create_empty()
    
    def get_game_data(self, game_date: str) -> pd.DataFrame:
        """試合データを取得"""
        try:
            df = self.df
            if 'GameDate' not in df.columns:
                return self._create_empty()
            return df[df['GameDate'] == game_date].copy()
        except Exception as e:
            st.error(f"試合データ取得エラー: {e}")
            return self._create_empty()
    
    def get_all_seasons(self) -> List[str]:
        """全シーズンのリストを取得"""
        try:
            df = self.df
            if df.empty or 'Season' not in df.columns:
                return []
            return sorted(df['Season'].dropna().unique().tolist(), reverse=True)
        except Exception as e:
            st.error(f"シーズン一覧取得エラー: {e}")
            return []
    
    def get_all_players(self) -> List[str]:
        """全選手のリストを取得"""
        try:
            df = self.df
            if df.empty or 'PlayerName' not in df.columns:
                return []
            return sorted(df['PlayerName'].dropna().unique().tolist())
        except Exception as e:
            st.error(f"選手一覧取得エラー: {e}")
            return []
    
    def get_all_games(self) -> List[str]:
        """全試合のリストを取得"""
        try:
            df = self.df
            if df.empty or 'GameDate' not in df.columns:
                return []
            return sorted(df['GameDate'].dropna().unique().tolist(), reverse=True)
        except Exception as e:
            st.error(f"試合一覧取得エラー: {e}")
            return []
    
    def _create_empty(self) -> pd.DataFrame:
        """空のデータフレームを作成"""
        return pd.DataFrame(columns=self.stat_columns)
    
    def get_stats_summary(self) -> dict:
        """統計サマリーを取得"""
        try:
            df = self.df
            return {
                'total_games': len(df['GameDate'].unique()) if not df.empty else 0,
                'total_players': len(df['PlayerName'].unique()) if not df.empty else 0,
                'total_seasons': len(df['Season'].unique()) if not df.empty else 0,
                'total_records': len(df)
            }
        except Exception as e:
            st.error(f"統計サマリー取得エラー: {e}")
            return {
                'total_games': 0,
                'total_players': 0,
                'total_seasons': 0,
                'total_records': 0
            }

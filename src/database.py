"""データベース操作 - 修正版"""
import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path
from typing import Optional, List, Dict
import os


class StatsDatabase:
    """バスケットボール統計データベース - 修正版"""
    
    def __init__(self, data_file: str = "data/basketball_stats.csv"):
        # スクリプトの場所を基準にパスを設定
        base_dir = Path(__file__).parent.parent
        self.data_file = base_dir / data_file
        
        # ディレクトリを作成（エラーを無視）
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError, FileExistsError):
            # 読み取り専用ファイルシステムの場合はスキップ
            pass
        
        # 必要なカラム定義
        self.stat_columns = [
            'No', 'PlayerName', 'GS', 'PTS', '3PM', '3PA', '3P%', 
            '2PM', '2PA', '2P%', 'DK', 'FTM', 'FTA', 'FT%',
            'OR', 'DR', 'TOT', 'AST', 'STL', 'BLK', 'TO', 
            'PF', 'TF', 'OF', 'FO', 'DQ', 'MIN',
            'GameDate', 'Season', 'Opponent', 'TeamScore', 'OpponentScore',
            'GameFormat'
        ]
        
        # 数値カラムの定義
        self.numeric_columns = [
            'No', 'GS', 'PTS', '3PM', '3PA', '2PM', '2PA', 'DK',
            'FTM', 'FTA', 'OR', 'DR', 'TOT', 'AST', 'STL', 'BLK',
            'TO', 'PF', 'TF', 'OF', 'FO', 'DQ', 'TeamScore', 'OpponentScore'
        ]
        
        # パーセンテージカラムの定義
        self.percentage_columns = ['3P%', '2P%', 'FT%']
        
        # データフレームの初期化
        self._df = None
        self.load()
    
    @property
    def df(self) -> pd.DataFrame:
        """データフレームを取得"""
        if self._df is None:
            self.load()
        return self._df if self._df is not None else self._create_empty()
    
    def load(self) -> bool:
        """データベースを読み込み"""
        try:
            if self.data_file.exists():
                # CSVを読み込み
                df = pd.read_csv(self.data_file)
                
                # カラムの検証と追加
                missing_cols = set(self.stat_columns) - set(df.columns)
                if missing_cols:
                    st.warning(f"不足しているカラムを追加します: {missing_cols}")
                    for col in missing_cols:
                        if col == 'GameFormat':
                            df[col] = '4Q'  # デフォルト値
                        elif col == 'MIN':
                            df[col] = '00:00'
                        else:
                            df[col] = 0
                
                # データ型の変換と検証
                df = self._validate_and_convert_types(df)
                
                # パーセンテージの再計算
                df = self._recalculate_percentages(df)
                
                self._df = df
                
                # セッション状態にも保存（互換性のため）
                st.session_state['database'] = df
                
                return True
            else:
                self._df = self._create_empty()
                st.session_state['database'] = self._df
                st.info("新しいデータベースを作成しました")
                return True
                
        except Exception as e:
            st.error(f"データ読み込みエラー: {e}")
            self._df = self._create_empty()
            st.session_state['database'] = self._df
            return False
    
    def _validate_and_convert_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """データ型の検証と変換"""
        try:
            # 数値カラムを数値型に変換
            for col in self.numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
            # パーセンテージカラムを数値型に変換
            for col in self.percentage_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
            
            # 文字列カラムの処理
            string_columns = ['PlayerName', 'GameDate', 'Season', 'Opponent', 'GameFormat', 'MIN']
            for col in string_columns:
                if col in df.columns:
                    df[col] = df[col].fillna('').astype(str)
            
            return df
            
        except Exception as e:
            st.warning(f"データ型変換中にエラーが発生しました: {e}")
            return df
    
    def _recalculate_percentages(self, df: pd.DataFrame) -> pd.DataFrame:
        """パーセンテージを再計算"""
        try:
            # 3P%を計算
            if '3PA' in df.columns and '3PM' in df.columns:
                df['3P%'] = df.apply(
                    lambda row: round(row['3PM'] / row['3PA'], 3) if row['3PA'] > 0 else 0.0,
                    axis=1
                )
            
            # 2P%を計算
            if '2PA' in df.columns and '2PM' in df.columns:
                df['2P%'] = df.apply(
                    lambda row: round(row['2PM'] / row['2PA'], 3) if row['2PA'] > 0 else 0.0,
                    axis=1
                )
            
            # FT%を計算
            if 'FTA' in df.columns and 'FTM' in df.columns:
                df['FT%'] = df.apply(
                    lambda row: round(row['FTM'] / row['FTA'], 3) if row['FTA'] > 0 else 0.0,
                    axis=1
                )
            
            return df
            
        except Exception as e:
            st.warning(f"パーセンテージ計算中にエラーが発生しました: {e}")
            return df
    
    def save(self) -> bool:
        """データベースを保存"""
        try:
            df = self.df
            if df.empty:
                st.warning("保存するデータがありません")
                return False
            
            # ディレクトリが存在することを確認（エラーを無視）
            try:
                self.data_file.parent.mkdir(parents=True, exist_ok=True)
            except (PermissionError, OSError, FileExistsError):
                pass
            
            # データの最終検証
            df = self._validate_and_convert_types(df)
            df = self._recalculate_percentages(df)
            
            # CSVに保存
            try:
                df.to_csv(self.data_file, index=False)
            except (PermissionError, OSError) as e:
                st.error(f"❌ ファイルへの書き込み権限がありません: {e}")
                st.info("💡 Streamlit Cloudを使用している場合、データは一時的にセッション内にのみ保存されます")
                # セッション状態には保存
                self._df = df
                st.session_state['database'] = df
                return False
            
            # メモリ上のデータも更新
            self._df = df
            st.session_state['database'] = df
            
            st.success(f"✅ データを保存しました（{len(df)}件）")
            return True
            
        except Exception as e:
            st.error(f"❌ 保存エラー: {e}")
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
                    if col == 'GameFormat':
                        game_df[col] = '4Q'
                    elif col == 'MIN':
                        game_df[col] = '00:00'
                    else:
                        game_df[col] = 0
            
            # データ型の変換
            game_df = self._validate_and_convert_types(game_df)
            game_df = self._recalculate_percentages(game_df)
            
            # 重複チェック
            if self._check_duplicate(game_df):
                st.warning("⚠️ 同じ試合データが既に存在します")
                if not st.checkbox("それでも追加しますか？"):
                    return False
            
            # データを追加
            current_df = self.df
            self._df = pd.concat([current_df, game_df], ignore_index=True)
            st.session_state['database'] = self._df
            
            st.success(f"✅ {len(game_df)}件のレコードを追加しました")
            return True
            
        except Exception as e:
            st.error(f"❌ データ追加エラー: {e}")
            return False
    
    def _check_duplicate(self, game_df: pd.DataFrame) -> bool:
        """重複データのチェック"""
        try:
            if 'GameDate' not in game_df.columns or 'Opponent' not in game_df.columns:
                return False
            
            game_date = game_df['GameDate'].iloc[0]
            opponent = game_df['Opponent'].iloc[0]
            
            existing = self.df[
                (self.df['GameDate'] == game_date) & 
                (self.df['Opponent'] == opponent)
            ]
            
            return len(existing) > 0
            
        except Exception:
            return False
    
    def delete_game(self, game_date: str, opponent: str) -> bool:
        """試合データを削除"""
        try:
            df = self.df
            before_count = len(df)
            
            self._df = df[
                ~((df['GameDate'] == game_date) & 
                  (df['Opponent'] == opponent))
            ].copy()
            
            st.session_state['database'] = self._df
            
            after_count = len(self._df)
            deleted = before_count - after_count
            
            if deleted > 0:
                st.success(f"✅ {deleted}件のレコードを削除しました")
                return True
            else:
                st.warning("削除するデータが見つかりませんでした")
                return False
                
        except Exception as e:
            st.error(f"❌ 削除エラー: {e}")
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
    
    def get_player_data(self, player_name: str, season: Optional[str] = None) -> pd.DataFrame:
        """選手データを取得"""
        try:
            df = self.df
            if 'PlayerName' not in df.columns:
                return self._create_empty()
            
            player_df = df[df['PlayerName'] == player_name].copy()
            
            if season:
                player_df = player_df[player_df['Season'] == season]
            
            return player_df.sort_values('GameDate')
            
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
    
    def get_all_players(self, season: Optional[str] = None) -> List[str]:
        """全選手のリストを取得"""
        try:
            df = self.df
            if df.empty or 'PlayerName' not in df.columns:
                return []
            
            if season:
                df = df[df['Season'] == season]
            
            return sorted(df['PlayerName'].dropna().unique().tolist())
        except Exception as e:
            st.error(f"選手一覧取得エラー: {e}")
            return []
    
    def get_all_games(self, season: Optional[str] = None) -> List[str]:
        """全試合のリストを取得"""
        try:
            df = self.df
            if df.empty or 'GameDate' not in df.columns:
                return []
            
            if season:
                df = df[df['Season'] == season]
            
            return sorted(df['GameDate'].dropna().unique().tolist(), reverse=True)
        except Exception as e:
            st.error(f"試合一覧取得エラー: {e}")
            return []
    
    def _create_empty(self) -> pd.DataFrame:
        """空のデータフレームを作成"""
        df = pd.DataFrame(columns=self.stat_columns)
        
        # データ型を設定
        for col in self.numeric_columns:
            if col in df.columns:
                df[col] = df[col].astype(int)
        
        for col in self.percentage_columns:
            if col in df.columns:
                df[col] = df[col].astype(float)
        
        return df
    
    def get_stats_summary(self) -> Dict[str, int]:
        """統計サマリーを取得"""
        try:
            df = self.df
            if df.empty:
                return {
                    'total_games': 0,
                    'total_players': 0,
                    'total_seasons': 0,
                    'total_records': 0
                }
            
            return {
                'total_games': len(df['GameDate'].unique()) if 'GameDate' in df.columns else 0,
                'total_players': len(df['PlayerName'].unique()) if 'PlayerName' in df.columns else 0,
                'total_seasons': len(df['Season'].unique()) if 'Season' in df.columns else 0,
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

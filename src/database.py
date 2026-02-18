"""データベース操作 - 改善版（エラーハンドリング強化）"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import os
import sys

# Streamlitのインポート（オプショナル）
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False
    # Streamlitがない場合のダミー関数
    class DummySt:
        @staticmethod
        def error(msg): print(f"ERROR: {msg}")
        @staticmethod
        def warning(msg): print(f"WARNING: {msg}")
        @staticmethod
        def info(msg): print(f"INFO: {msg}")
        @staticmethod
        def success(msg): print(f"SUCCESS: {msg}")
    st = DummySt()

# デバッグモード
DEBUG_MODE = os.getenv('DEBUG', 'False').lower() == 'true'

class StatsDatabase:
    """バスケットボール統計データベース - 改善版"""
    
    def __init__(self, data_file: str = "data/basketball_stats.csv"):
        """初期化"""
        # パスの設定
        try:
            base_dir = Path(__file__).parent.parent
        except Exception:
            base_dir = Path.cwd()
        
        self.data_file = base_dir / data_file
        
        if DEBUG_MODE:
            print(f"🔍 データファイルパス: {self.data_file}")
        
        # ディレクトリを作成（エラーを無視）
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            if DEBUG_MODE:
                print(f"⚠️ ディレクトリ作成スキップ: {e}")
        
        # カラム定義
        self.stat_columns = [
            'No', 'PlayerName', 'GS', 'PTS', '3PM', '3PA', '3P%', 
            '2PM', '2PA', '2P%', 'DK', 'FTM', 'FTA', 'FT%',
            'OR', 'DR', 'TOT', 'AST', 'STL', 'BLK', 'TO', 
            'PF', 'TF', 'OF', 'FO', 'DQ', 'MIN',
            'GameDate', 'Season', 'Opponent', 'TeamScore', 'OpponentScore',
            'GameFormat'
        ]
        
        # 数値カラム
        self.numeric_columns = [
            'No', 'GS', 'PTS', '3PM', '3PA', '2PM', '2PA', 'DK',
            'FTM', 'FTA', 'OR', 'DR', 'TOT', 'AST', 'STL', 'BLK',
            'TO', 'PF', 'TF', 'OF', 'FO', 'DQ', 'TeamScore', 'OpponentScore'
        ]
        
        # パーセンテージカラム
        self.percentage_columns = ['3P%', '2P%', 'FT%']
        
        # データフレームの初期化
        self._df = None
        self.load()
    
    @property
    def df(self) -> pd.DataFrame:
        """データフレームを安全に取得"""
        if self._df is None:
            self.load()
        return self._df if self._df is not None else self._create_empty()
    
    def _create_empty(self) -> pd.DataFrame:
        """空のデータフレームを作成"""
        df = pd.DataFrame(columns=self.stat_columns)
        
        # データ型を設定
        for col in self.numeric_columns:
            df[col] = pd.Series(dtype='int64')
        
        for col in self.percentage_columns:
            df[col] = pd.Series(dtype='float64')
        
        df['PlayerName'] = pd.Series(dtype='str')
        df['GameDate'] = pd.Series(dtype='str')
        df['Season'] = pd.Series(dtype='str')
        df['Opponent'] = pd.Series(dtype='str')
        df['MIN'] = pd.Series(dtype='str')
        df['GameFormat'] = pd.Series(dtype='str')
        
        if DEBUG_MODE:
            print("✅ 空のデータフレームを作成しました")
        
        return df
    
    def load(self) -> bool:
        """データを読み込み"""
        try:
            if self.data_file.exists():
                if DEBUG_MODE:
                    print(f"📂 ファイル読み込み: {self.data_file}")
                
                # CSVを読み込み
                df = pd.read_csv(self.data_file)
                
                if DEBUG_MODE:
                    print(f"📊 読み込んだ行数: {len(df)}")
                    print(f"📋 カラム: {list(df.columns)}")
                
                # カラムの検証
                missing_cols = set(self.stat_columns) - set(df.columns)
                if missing_cols:
                    st.warning(f"⚠️ 不足カラムを追加: {missing_cols}")
                    for col in missing_cols:
                        if col == 'GameFormat':
                            df[col] = '4Q'
                        elif col == 'MIN':
                            df[col] = '00:00'
                        elif col in self.numeric_columns:
                            df[col] = 0
                        elif col in self.percentage_columns:
                            df[col] = 0.0
                        else:
                            df[col] = ''
                
                # データ型変換
                df = self._validate_and_convert_types(df)
                
                # パーセンテージ再計算
                df = self._recalculate_percentages(df)
                
                self._df = df
                
                # セッション状態にも保存（Streamlitがある場合）
                if HAS_STREAMLIT and hasattr(st, 'session_state'):
                    st.session_state['database'] = df
                
                if DEBUG_MODE:
                    print("✅ データ読み込み成功")
                
                return True
            else:
                if DEBUG_MODE:
                    print(f"ℹ️ ファイルが存在しません: {self.data_file}")
                    print("✅ 新しいデータベースを作成")
                
                self._df = self._create_empty()
                
                if HAS_STREAMLIT and hasattr(st, 'session_state'):
                    st.session_state['database'] = self._df
                    st.info("新しいデータベースを作成しました")
                
                return True
                
        except Exception as e:
            st.error(f"❌ データ読み込みエラー: {e}")
            if DEBUG_MODE:
                import traceback
                print(traceback.format_exc())
            
            self._df = self._create_empty()
            if HAS_STREAMLIT and hasattr(st, 'session_state'):
                st.session_state['database'] = self._df
            return False
    
    def _validate_and_convert_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """データ型の検証と変換"""
        try:
            # 数値カラムの変換
            for col in self.numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            
            # パーセンテージカラムの変換
            for col in self.percentage_columns:
                if col in df.columns:
                    df[col] = self._clean_percentage(df[col])
            
            # 文字列カラムの変換
            string_cols = ['PlayerName', 'GameDate', 'Season', 'Opponent', 'MIN', 'GameFormat']
            for col in string_cols:
                if col in df.columns:
                    df[col] = df[col].fillna('').astype(str)
            
            if DEBUG_MODE:
                print("✅ データ型変換完了")
            
            return df
            
        except Exception as e:
            st.warning(f"⚠️ データ型変換エラー: {e}")
            if DEBUG_MODE:
                import traceback
                print(traceback.format_exc())
            return df
    
    def _clean_percentage(self, series: pd.Series) -> pd.Series:
        """パーセンテージデータのクリーニング"""
        def clean_value(val):
            if pd.isna(val):
                return 0.0
            
            if isinstance(val, str):
                val = val.replace('%', '').strip()
                try:
                    val = float(val)
                except ValueError:
                    return 0.0
            
            try:
                val = float(val)
                if val > 1:
                    val = val / 100
                return round(val, 3)
            except (ValueError, TypeError):
                return 0.0
        
        return series.apply(clean_value)
    
    def _recalculate_percentages(self, df: pd.DataFrame) -> pd.DataFrame:
        """パーセンテージの再計算"""
        try:
            # 3P%の再計算
            if '3PA' in df.columns and '3PM' in df.columns:
                mask = df['3PA'] > 0
                df.loc[mask, '3P%'] = (df.loc[mask, '3PM'] / df.loc[mask, '3PA']).round(3)
            
            # 2P%の再計算
            if '2PA' in df.columns and '2PM' in df.columns:
                mask = df['2PA'] > 0
                df.loc[mask, '2P%'] = (df.loc[mask, '2PM'] / df.loc[mask, '2PA']).round(3)
            
            # FT%の再計算
            if 'FTA' in df.columns and 'FTM' in df.columns:
                mask = df['FTA'] > 0
                df.loc[mask, 'FT%'] = (df.loc[mask, 'FTM'] / df.loc[mask, 'FTA']).round(3)
            
            return df
            
        except Exception as e:
            if DEBUG_MODE:
                print(f"⚠️ パーセンテージ再計算エラー: {e}")
            return df
    
    def save(self) -> bool:
        """データを保存"""
        try:
            if self._df is not None:
                self._df.to_csv(self.data_file, index=False, encoding='utf-8-sig')
                if DEBUG_MODE:
                    print(f"✅ データ保存成功: {self.data_file}")
                return True
            else:
                st.warning("⚠️ 保存するデータがありません")
                return False
                
        except Exception as e:
            st.error(f"❌ データ保存エラー: {e}")
            if DEBUG_MODE:
                import traceback
                print(traceback.format_exc())
            return False
    
    def add_game_stats(self, stats_df: pd.DataFrame) -> bool:
        """試合統計を追加"""
        try:
            if stats_df.empty:
                st.warning("⚠️ 追加するデータが空です")
                return False
            
            # カラムを検証
            missing_cols = set(self.stat_columns) - set(stats_df.columns)
            if missing_cols:
                for col in missing_cols:
                    if col == 'GameFormat':
                        stats_df[col] = '4Q'
                    elif col == 'MIN':
                        stats_df[col] = '00:00'
                    elif col in self.numeric_columns:
                        stats_df[col] = 0
                    elif col in self.percentage_columns:
                        stats_df[col] = 0.0
                    else:
                        stats_df[col] = ''
            
            # データ型変換
            stats_df = self._validate_and_convert_types(stats_df)
            
            # データを追加
            if self._df is None or self._df.empty:
                self._df = stats_df
            else:
                self._df = pd.concat([self._df, stats_df], ignore_index=True)
            
            # 保存
            return self.save()
            
        except Exception as e:
            st.error(f"❌ データ追加エラー: {e}")
            if DEBUG_MODE:
                import traceback
                print(traceback.format_exc())
            return False
    
    def get_player_stats(self, player_name: str = None, season: str = None) -> pd.DataFrame:
        """選手統計を取得"""
        try:
            df = self.df.copy()
            
            if df.empty:
                return self._create_empty()
            
            if player_name:
                df = df[df['PlayerName'] == player_name]
            
            if season:
                df = df[df['Season'] == season]
            
            return df
            
        except Exception as e:
            st.error(f"❌ 統計取得エラー: {e}")
            if DEBUG_MODE:
                import traceback
                print(traceback.format_exc())
            return self._create_empty()
    
    def get_season_stats(self, season: str) -> pd.DataFrame:
        """シーズン統計を取得"""
        return self.get_player_stats(season=season)
    
    def get_game_stats(self, game_date: str) -> pd.DataFrame:
        """試合統計を取得"""
        try:
            df = self.df.copy()
            
            if df.empty:
                return self._create_empty()
            
            df = df[df['GameDate'] == game_date]
            return df
            
        except Exception as e:
            st.error(f"❌ 試合統計取得エラー: {e}")
            if DEBUG_MODE:
                import traceback
                print(traceback.format_exc())
            return self._create_empty()
    
    def get_all_players(self, season: str = None) -> List[str]:
        """全選手リストを取得"""
        try:
            df = self.df.copy()
            
            if df.empty:
                return []
            
            if season:
                df = df[df['Season'] == season]
            
            if 'PlayerName' in df.columns:
                return sorted(df['PlayerName'].unique().tolist())
            else:
                return []
                
        except Exception as e:
            if DEBUG_MODE:
                print(f"⚠️ 選手リスト取得エラー: {e}")
            return []
    
    def get_all_seasons(self) -> List[str]:
        """全シーズンリストを取得"""
        try:
            df = self.df.copy()
            
            if df.empty:
                return []
            
            if 'Season' in df.columns:
                return sorted(df['Season'].unique().tolist(), reverse=True)
            else:
                return []
                
        except Exception as e:
            if DEBUG_MODE:
                print(f"⚠️ シーズンリスト取得エラー: {e}")
            return []
    
    def get_all_games(self, season: str = None) -> List[str]:
        """全試合リストを取得"""
        try:
            df = self.df.copy()
            
            if df.empty:
                return []
            
            if season:
                df = df[df['Season'] == season]
            
            if 'GameDate' in df.columns:
                return sorted(df['GameDate'].unique().tolist(), reverse=True)
            else:
                return []
                
        except Exception as e:
            if DEBUG_MODE:
                print(f"⚠️ 試合リスト取得エラー: {e}")
            return []
    
    def get_stats_summary(self) -> dict:
        """データベースの統計サマリーを取得"""
        try:
            df = self.df.copy()
            
            if df.empty:
                return {
                    'total_games': 0,
                    'total_players': 0,
                    'total_seasons': 0,
                    'total_records': 0
                }
            
            total_games = len(df['GameDate'].unique()) if 'GameDate' in df.columns else 0
            total_players = len(df['PlayerName'].unique()) if 'PlayerName' in df.columns else 0
            total_seasons = len(df['Season'].unique()) if 'Season' in df.columns else 0
            total_records = len(df)
            
            return {
                'total_games': total_games,
                'total_players': total_players,
                'total_seasons': total_seasons,
                'total_records': total_records
            }
        except Exception as e:
            if DEBUG_MODE:
                print(f"⚠️ 統計サマリー取得エラー: {e}")
            return {
                'total_games': 0,
                'total_players': 0,
                'total_seasons': 0,
                'total_records': 0
            }

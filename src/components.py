"""再利用可能なUIコンポーネント - 完全改良版（ランキング修正、日英対応）"""
import streamlit as st
import os
from pathlib import Path
from config import PLAYER_IMAGES_DIR, STAFF_IMAGES_DIR


def stat_card(label: str, value, subtitle: str = "", card_type: str = "", label_jp: str = ""):
    """統計カードを表示
    
    Args:
        label: カードのラベル（日本語）
        value: 表示する値
        subtitle: サブタイトル（オプション）
        card_type: カードタイプ（"primary", "secondary"）
        label_jp: 英語ラベル（オプション）
    """
    type_class = f" {card_type}" if card_type else ""
    subtitle_html = f'<div class="stat-subtitle">{subtitle}</div>' if subtitle else ''
    jp_label = f'<div style="font-size: 0.7rem; color: #888; margin-top: 0.3rem;">{label_jp}</div>' if label_jp else ''
    
    st.markdown(f"""
    <div class="stat-card{type_class}">
        <div class="stat-label">{label}{jp_label}</div>
        <div class="stat-value">{value}</div>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


def ranking_row(rank: int, player: str, stat_value, stat_label: str, 
                color: str = "#1d428a", image_path: str = None, player_number: str = ""):
    """ランキング行を表示（完全改良版: 画像、背番号、名前を正しく表示）
    
    Args:
        rank: 順位
        player: 選手名
        stat_value: 統計値
        stat_label: 統計ラベル（例: "PPG"）
        color: 表示色
        image_path: 選手画像のパス（オプション）
        player_number: 背番号（オプション）
    """
    # stat_valueを安全にfloatへ変換
    try:
        stat_value_f = float(stat_value)
        stat_value_str = f"{stat_value_f:.1f}"
    except (ValueError, TypeError):
        stat_value_str = str(stat_value)

    rank_class = f"rank-{rank}" if rank <= 3 else ""
    
    # 画像があれば表示、なければデフォルトアバター
    avatar_html = ''
    if image_path and os.path.exists(image_path):
        # Base64エンコードして埋め込み
        import base64
        try:
            with open(image_path, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode()
            avatar_html = f'''
            <div style="width: 60px; height: 60px; border-radius: 50%; overflow: hidden; margin-right: 1rem; border: 3px solid {color}; flex-shrink: 0;">
                <img src="data:image/png;base64,{img_data}" style="width: 100%; height: 100%; object-fit: cover;" />
            </div>
            '''
        except Exception as e:
            # 画像読み込みエラー時はデフォルトアバター
            avatar_html = f'''
            <div style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, {color} 0%, rgba(255,255,255,0.2) 100%); margin-right: 1rem; border: 3px solid {color}; flex-shrink: 0; display: flex; align-items: center; justify-content: center;">
                <span style="color: #fff; font-size: 1.5rem; font-weight: 900;">{player[0] if player else "?"}</span>
            </div>
            '''
    else:
        # デフォルトアバター（選手名の頭文字）
        avatar_html = f'''
        <div style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, {color} 0%, rgba(255,255,255,0.2) 100%); margin-right: 1rem; border: 3px solid {color}; flex-shrink: 0; display: flex; align-items: center; justify-content: center;">
            <span style="color: #fff; font-size: 1.5rem; font-weight: 900;">{player[0] if player else "?"}</span>
        </div>
        '''
    
    # 背番号表示
    number_html = ""
    if player_number:
        number_html = f'<span style="color: {color}; font-size: 1.1rem; font-weight: 800; margin-right: 1rem; background: rgba(255,255,255,0.1); padding: 0.2rem 0.5rem; border-radius: 4px;">#{player_number}</span>'
    
    # メダル表示（トップ3）
    medal_html = ""
    if rank == 1:
        medal_html = '<span style="font-size: 1.5rem; margin-right: 0.5rem;">🥇</span>'
    elif rank == 2:
        medal_html = '<span style="font-size: 1.5rem; margin-right: 0.5rem;">🥈</span>'
    elif rank == 3:
        medal_html = '<span style="font-size: 1.5rem; margin-right: 0.5rem;">🥉</span>'
    
    st.markdown(f"""
    <div class="ranking-row {rank_class}" style="background: linear-gradient(90deg, rgba(29, 66, 138, 0.1) 0%, rgba(200, 16, 46, 0.05) 100%); padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 5px solid {color}; display: flex; justify-content: space-between; align-items: center;">
        <div style="display: flex; align-items: center; flex: 1;">
            {medal_html}
            {avatar_html}
            <div style="display: flex; flex-direction: column;">
                <div style="display: flex; align-items: center; margin-bottom: 0.3rem;">
                    <span style="color: {color}; font-size: 1.8rem; font-weight: 900; margin-right: 1rem;">#{rank}</span>
                    {number_html}
                </div>
                <span style="color: #ffffff; font-size: 1.5rem; font-weight: 700;">{player}</span>
            </div>
        </div>
        <div style="text-align: right;">
            <div style="color: {color}; font-size: 2.5rem; font-weight: 900; line-height: 1;">{stat_value_str}</div>
            <div style="color: #888; font-size: 1rem; margin-top: 0.3rem; font-weight: 600;">{stat_label}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def game_card(date: str, opponent: str, team_score: int, opp_score: int, game_format: str = "4Q"):
    """試合カードを表示
    
    Args:
        date: 試合日
        opponent: 対戦相手
        team_score: 自チームスコア
        opp_score: 相手チームスコア
        game_format: 試合形式（4Q, 2Q, Other）
    """
    result = "勝利" if team_score > opp_score else "敗北"
    result_en = "WIN" if team_score > opp_score else "LOSS"
    result_class = "win" if result == "勝利" else "loss"
    
    st.markdown(f"""
    <div class="game-card">
        <div class="game-date">{date} <span style="color: #555;">({game_format})</span></div>
        <div class="teams">筑波 / TSUKUBA <span style="color: #888;">vs</span> {opponent}</div>
        <div class="score">{team_score} - {opp_score}</div>
        <div class="result {result_class}">{result} / {result_en}</div>
    </div>
    """, unsafe_allow_html=True)


def player_card(player_name: str, player_number: str, image_path: str = None, position: str = ""):
    """選手カードを表示（背景画像付き）
    
    Args:
        player_name: 選手名
        player_number: 背番号
        image_path: 選手画像のパス（オプション）
        position: ポジション（オプション）
    """
    # 背景画像のHTML
    bg_image_html = ''
    if image_path and os.path.exists(image_path):
        import base64
        with open(image_path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode()
        bg_image_html = f'<img src="data:image/png;base64,{img_data}" class="player-card-image" />'
    
    position_html = f'<div style="color: #888; font-size: 1.2rem; margin-top: 0.5rem;">{position}</div>' if position else ''
    
    st.markdown(f"""
    <div class="player-card">
        {bg_image_html}
        <div class="player-card-content">
            <div class="player-number">#{player_number}</div>
            <div class="player-name">{player_name}</div>
            {position_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str, title_jp: str = ""):
    """セクションヘッダーを表示（日英対応）
    
    Args:
        title: セクションタイトル（日本語）
        title_jp: セクションタイトル（英語、オプション）
    """
    jp_html = f'<span style="font-size: 0.8rem; color: #888; margin-left: 1rem; font-weight: 600;">{title_jp}</span>' if title_jp else ''
    st.markdown(f"""
    <div class="section-header" style="border-left: 5px solid #c8102e; padding-left: 1.5rem; margin: 2rem 0 1.5rem 0;">
        <span style="font-size: 1.8rem; font-weight: 900; color: #ffffff; text-transform: uppercase; letter-spacing: 0.05rem;">{title}</span>
        {jp_html}
    </div>
    """, unsafe_allow_html=True)


def staff_card(name: str, role: str, image_path: str = None):
    """スタッフカードを表示
    
    Args:
        name: 氏名
        role: 役職
        image_path: 写真のパス
    """
    image_html = ''
    if image_path and os.path.exists(image_path):
        import base64
        with open(image_path, 'rb') as f:
            img_data = base64.b64encode(f.read()).decode()
        image_html = f'''
        <div style="width: 100%; height: 250px; border-radius: 8px; overflow: hidden; margin-bottom: 1rem;">
            <img src="data:image/png;base64,{img_data}" style="width: 100%; height: 100%; object-fit: cover; filter: grayscale(20%);" />
        </div>
        '''
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); padding: 1.5rem; border-radius: 8px; border: 2px solid #333; margin-bottom: 1rem;">
        {image_html}
        <div style="color: #ffffff; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.5rem;">{name}</div>
        <div style="color: #888; font-size: 1rem;">{role}</div>
    </div>
    """, unsafe_allow_html=True)


def comparison_table(data_dict: dict, highlight_max: bool = True):
    """比較テーブルを表示
    
    Args:
        data_dict: 比較データ
        highlight_max: 最大値をハイライトするか
    """
    # HTMLテーブル生成
    headers = list(data_dict.keys())
    rows = len(data_dict[headers[0]])
    
    html = '<table style="width: 100%; background: #1a1a1a; border: 2px solid #333; border-radius: 8px; overflow: hidden;">'
    html += '<thead><tr style="background: linear-gradient(180deg, #2d2d2d 0%, #1a1a1a 100%);">'
    
    for header in headers:
        html += f'<th style="color: #fff; padding: 1rem; border-bottom: 2px solid #c8102e; font-weight: 700; text-transform: uppercase;">{header}</th>'
    html += '</tr></thead><tbody>'
    
    for i in range(rows):
        html += '<tr style="border-bottom: 1px solid #333;">'
        row_values = [data_dict[h][i] for h in headers[1:]]
        
        for j, header in enumerate(headers):
            value = data_dict[header][i]
            cell_style = 'color: #fff; padding: 1rem;'
            
            # 最大値をハイライト
            if j > 0 and highlight_max and i > 0:  # 最初の行はヘッダーなのでスキップ
                try:
                    numeric_values = [float(str(v).replace('%', '')) for v in row_values if str(v).replace('.', '').replace('%', '').replace('-', '').isdigit()]
                    if numeric_values and float(str(value).replace('%', '')) == max(numeric_values):
                        cell_style += ' background: rgba(200, 16, 46, 0.2); font-weight: 700;'
                except:
                    pass
            
            html += f'<td style="{cell_style}">{value}</td>'
        html += '</tr>'
    
    html += '</tbody></table>'
    st.markdown(html, unsafe_allow_html=True)

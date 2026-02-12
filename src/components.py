"""再利用可能なUIコンポーネント"""
import streamlit as st


def stat_card(label: str, value, subtitle: str = "", card_type: str = ""):
    """統計カードを表示
    
    Args:
        label: カードのラベル
        value: 表示する値
        subtitle: サブタイトル（オプション）
        card_type: カードタイプ（"primary", "secondary"）
    """
    type_class = f" {card_type}" if card_type else ""
    subtitle_html = f'<div class="stat-subtitle">{subtitle}</div>' if subtitle else ''
    
    st.markdown(f"""
    <div class="stat-card{type_class}">
        <div class="stat-label">{label}</div>
        <div class="stat-value">{value}</div>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


def ranking_row(rank: int, player: str, stat_value: float, stat_label: str, color: str = "#1d428a"):
    """ランキング行を表示
    
    Args:
        rank: 順位
        player: 選手名
        stat_value: 統計値
        stat_label: 統計ラベル（例: "PPG"）
        color: 表示色
    """
    rank_class = f"rank-{rank}" if rank <= 3 else ""
    st.markdown(f"""
    <div class="ranking-row {rank_class}">
        <div>
            <span style="color: {color}; font-size: 1.25rem; font-weight: 700; margin-right: 1rem;">#{rank}</span>
            <span style="color: #212529; font-size: 1.1rem; font-weight: 600;">{player}</span>
        </div>
        <div style="text-align: right;">
            <span style="color: {color}; font-size: 1.5rem; font-weight: 700;">{stat_value:.1f}</span>
            <span style="color: #6c757d; font-size: 0.9rem; margin-left: 0.5rem;">{stat_label}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def game_card(date: str, opponent: str, team_score: int, opp_score: int):
    """試合カードを表示
    
    Args:
        date: 試合日
        opponent: 対戦相手
        team_score: 自チームスコア
        opp_score: 相手チームスコア
    """
    result = "WIN" if team_score > opp_score else "LOSS"
    result_class = "win" if result == "WIN" else "loss"
    
    st.markdown(f"""
    <div class="game-card">
        <div class="game-date">{date}</div>
        <div class="teams">TSUKUBA vs {opponent}</div>
        <div class="score">{team_score} - {opp_score}</div>
        <div class="result {result_class}">{result}</div>
    </div>
    """, unsafe_allow_html=True)


def player_card(player_name: str, player_number: str):
    """選手カードを表示
    
    Args:
        player_name: 選手名
        player_number: 背番号
    """
    st.markdown(f"""
    <div class="player-card">
        <div class="player-number">#{player_number}</div>
        <div class="player-name">{player_name}</div>
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str):
    """セクションヘッダーを表示
    
    Args:
        title: セクションタイトル
    """
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

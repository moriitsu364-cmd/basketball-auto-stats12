"""グラフ作成"""
import plotly.graph_objects as go
from config import NBA_COLORS


def create_nba_chart(data, title: str, x_col: str, y_col: str, color: str = None):
    """NBAスタイルのチャートを作成
    
    Args:
        data: データフレーム
        title: グラフタイトル
        x_col: X軸のカラム名
        y_col: Y軸のカラム名
        color: 線の色（デフォルトはNBAプライマリカラー）
    
    Returns:
        Plotlyのfigureオブジェクト
    """
    if color is None:
        color = NBA_COLORS['primary']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data[x_col],
        y=data[y_col],
        mode='lines+markers',
        line=dict(color=color, width=3),
        marker=dict(size=8, color=color),
        fill='tozeroy',
        fillcolor=f'rgba(29, 66, 138, 0.1)'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color='#212529', family='Arial')),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#212529'),
        xaxis=dict(
            gridcolor='#f0f0f0',
            showgrid=True,
            zeroline=False,
            tickangle=-45,
            title=None
        ),
        yaxis=dict(
            gridcolor='#f0f0f0',
            showgrid=True,
            zeroline=False,
            title=None
        ),
        hovermode='x unified',
        margin=dict(l=40, r=20, t=40, b=60),
        height=350
    )
    
    return fig


def create_comparison_chart(data1, data2, name1: str, name2: str, x_col: str, y_col: str):
    """比較チャートを作成
    
    Args:
        data1: 選手1のデータフレーム
        data2: 選手2のデータフレーム
        name1: 選手1の名前
        name2: 選手2の名前
        x_col: X軸のカラム名
        y_col: Y軸のカラム名
    
    Returns:
        Plotlyのfigureオブジェクト
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data1[x_col],
        y=data1[y_col],
        mode='lines+markers',
        name=name1,
        line=dict(color=NBA_COLORS['primary'], width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=data2[x_col],
        y=data2[y_col],
        mode='lines+markers',
        name=name2,
        line=dict(color=NBA_COLORS['secondary'], width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='POINTS PER GAME COMPARISON',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#212529'),
        xaxis=dict(gridcolor='#f0f0f0', showgrid=True),
        yaxis=dict(gridcolor='#f0f0f0', showgrid=True),
        hovermode='x unified',
        height=400
    )
    
    return fig

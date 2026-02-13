"""改良されたグラフ作成 - 棒グラフ、円グラフ対応"""
import plotly.graph_objects as go
import plotly.express as px
from config import NBA_COLORS


def create_line_chart(data, title: str, x_col: str, y_col: str, color: str = None, title_jp: str = ""):
    """折れ線グラフを作成
    
    Args:
        data: データフレーム
        title: グラフタイトル（英語）
        x_col: X軸のカラム名
        y_col: Y軸のカラム名
        color: 線の色
        title_jp: グラフタイトル（日本語）
    
    Returns:
        Plotlyのfigureオブジェクト
    """
    if color is None:
        color = NBA_COLORS['primary']
    
    full_title = f"{title}<br><sub>{title_jp}</sub>" if title_jp else title
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data[x_col],
        y=data[y_col],
        mode='lines+markers',
        line=dict(color=color, width=4),
        marker=dict(size=10, color=color, line=dict(width=2, color='#ffffff')),
        fill='tozeroy',
        fillcolor=f'rgba{tuple(list(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + [0.1])}'
    ))
    
    fig.update_layout(
        title=dict(
            text=full_title,
            font=dict(size=20, color='#ffffff', family='Arial'),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#1a1a1a',
        paper_bgcolor='#1a1a1a',
        font=dict(color='#ffffff'),
        xaxis=dict(
            gridcolor='#333',
            showgrid=True,
            zeroline=False,
            tickangle=-45,
            title=None,
            color='#ffffff'
        ),
        yaxis=dict(
            gridcolor='#333',
            showgrid=True,
            zeroline=False,
            title=None,
            color='#ffffff'
        ),
        hovermode='x unified',
        margin=dict(l=40, r=20, t=80, b=80),
        height=400
    )
    
    return fig


def create_bar_chart(data, title: str, x_col: str, y_col: str, color: str = None, 
                     title_jp: str = "", orientation='v'):
    """棒グラフを作成
    
    Args:
        data: データフレーム
        title: グラフタイトル（英語）
        x_col: X軸のカラム名
        y_col: Y軸のカラム名
        color: 棒の色
        title_jp: グラフタイトル（日本語）
        orientation: 'v'（縦）または 'h'（横）
    
    Returns:
        Plotlyのfigureオブジェクト
    """
    if color is None:
        color = NBA_COLORS['secondary']
    
    full_title = f"{title}<br><sub>{title_jp}</sub>" if title_jp else title
    
    if orientation == 'v':
        fig = go.Figure(go.Bar(
            x=data[x_col],
            y=data[y_col],
            marker=dict(
                color=data[y_col],
                colorscale=[[0, '#1d428a'], [1, '#c8102e']],
                line=dict(width=2, color='#ffffff')
            ),
            text=data[y_col],
            textposition='outside',
            textfont=dict(color='#ffffff', size=12)
        ))
    else:
        fig = go.Figure(go.Bar(
            x=data[y_col],
            y=data[x_col],
            orientation='h',
            marker=dict(
                color=data[y_col],
                colorscale=[[0, '#1d428a'], [1, '#c8102e']],
                line=dict(width=2, color='#ffffff')
            ),
            text=data[y_col],
            textposition='outside',
            textfont=dict(color='#ffffff', size=12)
        ))
    
    fig.update_layout(
        title=dict(
            text=full_title,
            font=dict(size=20, color='#ffffff'),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#1a1a1a',
        paper_bgcolor='#1a1a1a',
        font=dict(color='#ffffff'),
        xaxis=dict(
            gridcolor='#333',
            showgrid=True,
            color='#ffffff'
        ),
        yaxis=dict(
            gridcolor='#333',
            showgrid=True,
            color='#ffffff'
        ),
        margin=dict(l=60, r=20, t=80, b=80),
        height=400
    )
    
    return fig


def create_pie_chart(labels, values, title: str, title_jp: str = ""):
    """円グラフを作成
    
    Args:
        labels: ラベルリスト
        values: 値リスト
        title: グラフタイトル（英語）
        title_jp: グラフタイトル（日本語）
    
    Returns:
        Plotlyのfigureオブジェクト
    """
    full_title = f"{title}<br><sub>{title_jp}</sub>" if title_jp else title
    
    colors = ['#1d428a', '#c8102e', '#ffd700', '#4169e1', '#ff4757', 
              '#20c997', '#6c757d', '#f8d7da', '#5cb85c']
    
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.4,  # ドーナツチャート
        marker=dict(
            colors=colors[:len(labels)],
            line=dict(color='#ffffff', width=3)
        ),
        textfont=dict(size=14, color='#ffffff'),
        textposition='outside',
        textinfo='label+percent'
    ))
    
    fig.update_layout(
        title=dict(
            text=full_title,
            font=dict(size=20, color='#ffffff'),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#1a1a1a',
        paper_bgcolor='#1a1a1a',
        font=dict(color='#ffffff'),
        showlegend=True,
        legend=dict(
            font=dict(color='#ffffff'),
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=20, r=20, t=80, b=20),
        height=400
    )
    
    return fig


def create_comparison_chart(data_list, names: list, x_col: str, y_col: str, 
                            title: str = "Player Comparison", title_jp: str = "選手比較"):
    """複数選手比較チャートを作成
    
    Args:
        data_list: データフレームのリスト
        names: 選手名のリスト
        x_col: X軸のカラム名
        y_col: Y軸のカラム名
        title: グラフタイトル
        title_jp: 日本語タイトル
    
    Returns:
        Plotlyのfigureオブジェクト
    """
    full_title = f"{title}<br><sub>{title_jp}</sub>"
    
    colors = ['#1d428a', '#c8102e', '#ffd700', '#4169e1', '#ff4757', 
              '#20c997', '#6c757d', '#f8d7da']
    
    fig = go.Figure()
    
    for i, (data, name) in enumerate(zip(data_list, names)):
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[y_col],
            mode='lines+markers',
            name=name,
            line=dict(color=colors[i % len(colors)], width=3),
            marker=dict(size=8, line=dict(width=2, color='#ffffff'))
        ))
    
    fig.update_layout(
        title=dict(
            text=full_title,
            font=dict(size=20, color='#ffffff'),
            x=0.5,
            xanchor='center'
        ),
        plot_bgcolor='#1a1a1a',
        paper_bgcolor='#1a1a1a',
        font=dict(color='#ffffff'),
        xaxis=dict(
            gridcolor='#333',
            showgrid=True,
            color='#ffffff'
        ),
        yaxis=dict(
            gridcolor='#333',
            showgrid=True,
            color='#ffffff'
        ),
        hovermode='x unified',
        legend=dict(
            font=dict(color='#ffffff', size=12),
            bgcolor='rgba(0,0,0,0.5)',
            bordercolor='#555',
            borderwidth=2
        ),
        margin=dict(l=60, r=20, t=80, b=80),
        height=450
    )
    
    return fig


def create_radar_chart(categories, values_list, names: list, title: str = "Stats Radar", title_jp: str = "スタッツレーダー"):
    """レーダーチャートを作成
    
    Args:
        categories: カテゴリリスト
        values_list: 値のリスト（選手ごと）
        names: 選手名リスト
        title: グラフタイトル
        title_jp: 日本語タイトル
    
    Returns:
        Plotlyのfigureオブジェクト
    """
    full_title = f"{title}<br><sub>{title_jp}</sub>"
    
    colors = ['#1d428a', '#c8102e', '#ffd700', '#4169e1']
    
    fig = go.Figure()
    
    for i, (values, name) in enumerate(zip(values_list, names)):
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=name,
            line=dict(color=colors[i % len(colors)], width=3),
            fillcolor=f'rgba{tuple(list(int(colors[i % len(colors)].lstrip("#")[j:j+2], 16) for j in (0, 2, 4)) + [0.2])}'
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                color='#ffffff',
                gridcolor='#333'
            ),
            angularaxis=dict(
                color='#ffffff',
                gridcolor='#333'
            ),
            bgcolor='#1a1a1a'
        ),
        showlegend=True,
        legend=dict(
            font=dict(color='#ffffff'),
            bgcolor='rgba(0,0,0,0)'
        ),
        title=dict(
            text=full_title,
            font=dict(size=20, color='#ffffff'),
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor='#1a1a1a',
        font=dict(color='#ffffff'),
        height=500
    )
    
    return fig

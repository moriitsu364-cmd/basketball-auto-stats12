"""改良されたグラフ作成 - 完全版（正しいグラフタイプと軸、日英対応）"""
import plotly.graph_objects as go
import plotly.express as px
from config import NBA_COLORS
import pandas as pd


def create_nba_chart(data, title: str, x_col: str, y_col: str, chart_type: str = 'line', 
                     color: str = None, title_jp: str = ""):
    """NBA風チャートを作成（汎用関数）
    
    Args:
        data: データフレーム
        title: グラフタイトル（日本語）
        x_col: X軸のカラム名
        y_col: Y軸のカラム名
        chart_type: チャートタイプ ('line', 'bar', 'scatter')
        color: 色
        title_jp: グラフタイトル（英語）
    
    Returns:
        Plotlyのfigureオブジェクト
    """
    if chart_type == 'line':
        return create_line_chart(data, title, x_col, y_col, color, title_jp)
    elif chart_type == 'bar':
        return create_bar_chart(data, title, x_col, y_col, color, title_jp)
    else:
        return create_line_chart(data, title, x_col, y_col, color, title_jp)


def create_line_chart(data, title: str, x_col: str, y_col: str, color: str = None, title_jp: str = ""):
    """折れ線グラフを作成（改良版）
    
    Args:
        data: データフレーム
        title: グラフタイトル（日本語）
        x_col: X軸のカラム名
        y_col: Y軸のカラム名
        color: 線の色
        title_jp: グラフタイトル（英語）
    
    Returns:
        Plotlyのfigureオブジェクト
    """
    if color is None:
        color = NBA_COLORS['primary']
    
    # タイトルを日英併記
    full_title = f"{title}<br><sub style='color: #888;'>{title_jp}</sub>" if title_jp else title
    
    fig = go.Figure()
    
    # データをソート（x軸が数値または日付の場合）
    try:
        data_sorted = data.sort_values(by=x_col)
    except:
        data_sorted = data
    
    fig.add_trace(go.Scatter(
        x=data_sorted[x_col],
        y=data_sorted[y_col],
        mode='lines+markers',
        line=dict(color=color, width=5),
        marker=dict(size=12, color=color, line=dict(width=3, color='#ffffff')),
        fill='tozeroy',
        fillcolor=f'rgba{tuple(list(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + [0.15])}'
    ))
    
    # X軸のラベル（試合番号の場合）
    x_axis_title = None
    if x_col == 'GameNumber':
        x_axis_title = '試合番号 / Game Number'
    elif x_col == 'GameDate':
        x_axis_title = '試合日 / Date'
    
    fig.update_layout(
        title=dict(
            text=full_title,
            font=dict(size=24, color='#212529', family='Arial, sans-serif'),
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        plot_bgcolor='#fafbfc',
        paper_bgcolor='#ffffff',
        font=dict(color='#212529', size=12),
        xaxis=dict(
            gridcolor='#e8eaed',
            showgrid=True,
            zeroline=False,
            tickangle=0,
            title=x_axis_title,
            title_font=dict(size=14, color='#495057', family='Arial, sans-serif'),
            color='#212529',
            dtick=1 if x_col == 'GameNumber' else None,  # 試合番号は1刻み
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            gridcolor='#e8eaed',
            showgrid=True,
            zeroline=False,
            title=None,
            color='#212529',
            tickfont=dict(size=11)
        ),
        hovermode='x unified',
        margin=dict(l=60, r=40, t=100, b=80),
        height=450,
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Arial, sans-serif'
        )
    )
    
    return fig


def create_bar_chart(data, title: str, x_col: str, y_col: str, color: str = None, 
                     title_jp: str = "", orientation='v'):
    """棒グラフを作成（改良版）
    
    Args:
        data: データフレーム
        title: グラフタイトル（日本語）
        x_col: X軸のカラム名
        y_col: Y軸のカラム名
        color: 棒の色
        title_jp: グラフタイトル（英語）
        orientation: 'v'（縦）または 'h'（横）
    
    Returns:
        Plotlyのfigureオブジェクト
    """
    if color is None:
        color = NBA_COLORS['secondary']
    
    full_title = f"{title}<br><sub style='color: #888;'>{title_jp}</sub>" if title_jp else title
    
    # データをソート（値の大きい順）
    data_sorted = data.sort_values(by=y_col, ascending=False)
    
    if orientation == 'v':
        fig = go.Figure(go.Bar(
            x=data_sorted[x_col],
            y=data_sorted[y_col],
            marker=dict(
                color=data_sorted[y_col],
                colorscale=[[0, '#1d428a'], [1, '#c8102e']],
                line=dict(width=2, color='#ffffff')
            ),
            text=[f'{val:.1f}' for val in data_sorted[y_col]],
            textposition='outside',
            textfont=dict(color='#212529', size=12, weight='bold')
        ))
    else:
        fig = go.Figure(go.Bar(
            x=data_sorted[y_col],
            y=data_sorted[x_col],
            orientation='h',
            marker=dict(
                color=data_sorted[y_col],
                colorscale=[[0, '#1d428a'], [1, '#c8102e']],
                line=dict(width=2, color='#ffffff')
            ),
            text=[f'{val:.1f}' for val in data_sorted[y_col]],
            textposition='outside',
            textfont=dict(color='#212529', size=12, weight='bold')
        ))
    
    fig.update_layout(
        title=dict(
            text=full_title,
            font=dict(size=24, color='#212529', family='Arial, sans-serif'),
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        plot_bgcolor='#fafbfc',
        paper_bgcolor='#ffffff',
        font=dict(color='#212529', size=12),
        xaxis=dict(
            gridcolor='#e8eaed',
            showgrid=True,
            color='#212529',
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            gridcolor='#e8eaed',
            showgrid=True,
            color='#212529',
            tickfont=dict(size=11)
        ),
        margin=dict(l=60, r=40, t=100, b=80),
        height=450,
        showlegend=False,
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Arial, sans-serif'
        )
    )
    
    return fig


def create_pie_chart(labels, values, title: str, title_jp: str = ""):
    """円グラフを作成（改良版）
    
    Args:
        labels: ラベルリスト
        values: 値リスト
        title: グラフタイトル（日本語）
        title_jp: グラフタイトル（英語）
    
    Returns:
        Plotlyのfigureオブジェクト
    """
    full_title = f"{title}<br><sub style='color: #888;'>{title_jp}</sub>" if title_jp else title
    
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
        textfont=dict(size=14, color='#212529', weight='bold'),
        textposition='outside',
        textinfo='label+percent'
    ))
    
    fig.update_layout(
        title=dict(
            text=full_title,
            font=dict(size=24, color='#212529', family='Arial, sans-serif'),
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        plot_bgcolor='#fafbfc',
        paper_bgcolor='#ffffff',
        font=dict(color='#212529', size=12),
        showlegend=True,
        legend=dict(
            font=dict(color='#212529', size=12),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#e8eaed',
            borderwidth=1
        ),
        margin=dict(l=40, r=40, t=100, b=40),
        height=450,
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Arial, sans-serif'
        )
    )
    
    return fig


def create_comparison_chart(data_list, names: list, x_col: str, y_col: str, 
                            title: str = "選手比較", title_jp: str = "Player Comparison"):
    """複数選手比較チャートを作成
    
    Args:
        data_list: データフレームのリスト
        names: 選手名のリスト
        x_col: X軸のカラム名
        y_col: Y軸のカラム名
        title: グラフタイトル（日本語）
        title_jp: 英語タイトル
    
    Returns:
        Plotlyのfigureオブジェクト
    """
    full_title = f"{title}<br><sub style='color: #888;'>{title_jp}</sub>"
    
    colors = ['#1d428a', '#c8102e', '#ffd700', '#4169e1', '#ff4757', 
              '#20c997', '#6c757d', '#f8d7da']
    
    fig = go.Figure()
    
    for i, (data, name) in enumerate(zip(data_list, names)):
        # データをソート
        try:
            data_sorted = data.sort_values(by=x_col)
        except:
            data_sorted = data
        
        fig.add_trace(go.Scatter(
            x=data_sorted[x_col],
            y=data_sorted[y_col],
            mode='lines+markers',
            name=name,
            line=dict(color=colors[i % len(colors)], width=4),
            marker=dict(size=10, line=dict(width=2, color='#ffffff'))
        ))
    
    # X軸のラベル
    x_axis_title = None
    if x_col == 'GameNumber':
        x_axis_title = '試合番号 / Game Number'
    elif x_col == 'GameDate':
        x_axis_title = '試合日 / Date'
    
    fig.update_layout(
        title=dict(
            text=full_title,
            font=dict(size=24, color='#212529', family='Arial, sans-serif'),
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        plot_bgcolor='#fafbfc',
        paper_bgcolor='#ffffff',
        font=dict(color='#212529', size=12),
        xaxis=dict(
            gridcolor='#e8eaed',
            showgrid=True,
            color='#212529',
            title=x_axis_title,
            title_font=dict(size=14, color='#495057', family='Arial, sans-serif'),
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            gridcolor='#e8eaed',
            showgrid=True,
            color='#212529',
            tickfont=dict(size=11)
        ),
        hovermode='x unified',
        legend=dict(
            font=dict(color='#212529', size=12),
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='#e8eaed',
            borderwidth=1,
            x=1,
            y=1,
            xanchor='right',
            yanchor='top'
        ),
        margin=dict(l=60, r=40, t=100, b=80),
        height=500,
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Arial, sans-serif'
        )
    )
    
    return fig


def create_radar_chart(categories, values_list, names: list, 
                       title: str = "スタッツレーダー", title_jp: str = "Stats Radar"):
    """レーダーチャートを作成
    
    Args:
        categories: カテゴリリスト
        values_list: 値のリスト（選手ごと）
        names: 選手名リスト
        title: グラフタイトル（日本語）
        title_jp: 英語タイトル
    
    Returns:
        Plotlyのfigureオブジェクト
    """
    full_title = f"{title}<br><sub style='color: #888;'>{title_jp}</sub>"
    
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
                color='#212529',
                gridcolor='#e8eaed',
                tickfont=dict(size=11)
            ),
            angularaxis=dict(
                color='#212529',
                gridcolor='#e8eaed',
                tickfont=dict(size=12)
            ),
            bgcolor='#fafbfc'
        ),
        showlegend=True,
        legend=dict(
            font=dict(color='#212529', size=12),
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='#e8eaed',
            borderwidth=1
        ),
        title=dict(
            text=full_title,
            font=dict(size=24, color='#212529', family='Arial, sans-serif'),
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        paper_bgcolor='#ffffff',
        font=dict(color='#212529', size=12),
        height=550,
        margin=dict(l=80, r=80, t=100, b=80),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Arial, sans-serif'
        )
    )
    
    return fig

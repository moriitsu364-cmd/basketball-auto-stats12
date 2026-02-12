import plotly.express as px
import plotly.graph_objects as go 

def create_nba_chart(data, title, x_col, y_col, color='#1d428a'):
    """NBAスタイルのチャート"""
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

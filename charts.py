import plotly.express as px

def create_bar_chart(df, x, y):
    fig = px.bar(df, x=x, y=y)
    return fig

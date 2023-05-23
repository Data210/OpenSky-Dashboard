from connection_string import create_connection_string
from sqlalchemy import create_engine, text
import pandas as pd
import plotly.graph_objects as go

connect_string = create_connection_string()
engine = create_engine(connect_string)
try:
    engine = create_engine(connect_string)
except:
    print('Error: Connection String Failed')

def get_df_from_query(query):
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    return df

def get_velocity_by_date():
    query = 'SELECT * FROM velocity_by_date_view'
    df = get_df_from_query(query)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['the_time'], y=df['avg_velocity'], mode='lines',
                             line=dict(width=3)))

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showline=True,
            showgrid=True,
            gridwidth=1,
            gridcolor='rgb(225, 225, 225)',
            zeroline=False,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.show()

def get_altitudes_by_date():
    query = 'SELECT * FROM altitudes_by_date_view'
    df = get_df_from_query(query)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['the_time'], y=df['avg_baro'], mode='lines',
                             line=dict(width=3)))
    fig.add_trace(go.Scatter(x=df['the_time'], y=df['avg_geo'], mode='lines',
                             line=dict(width=3)))

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ),
        ),
        yaxis=dict(
            showline=True,
            showgrid=True,
            gridwidth=1,
            gridcolor='rgb(225, 225, 225)',
            zeroline=False,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_yaxes(title_text="<b>Baro Altitude</b>", title_font=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ), secondary_y=False)
    fig.update_yaxes(title_text="<b>Geo Altitude</b>",title_font=dict(
                family='Arial',
                size=12,
                color='rgb(82, 82, 82)',
            ), secondary_y=True)
    fig.show()

def get_vertical_rate_by_date():
    query = 'SELECT * FROM vertical_rate_by_date_view'
    df = get_df_from_query(query)

def get_unique_plane_by_date():
    query = 'SELECT * FROM unique_plane_by_date_view'
    df = get_df_from_query(query)

def get_unique_plane_by_country():
    query = 'SELECT * FROM unique_plane_by_country_view'
    df = get_df_from_query(query)

def main():
    get_altitudes_by_date()

if __name__ == '__main__':
    main()
import plotly.graph_objects as go
from flask import Flask, render_template, jsonify, request
import requests
import json
import pandas as pd
import plotly
import plotly.express as px
import time
import os
from utils.connection_string import create_postgres_conn

app = Flask(__name__)

state_columns = [
    "icao24",
    "callsign",
    "origin_country",
    "time_position",
    "last_contact",
    "longitude",
    "latitude",
    "baro_altitude",
    "on_ground",
    "velocity",
    "true_track",
    "vertical_rate",
    "sensors",
    "geo_altitude",
    "squawk",
    "spi",
    "position_source",
]

cached_states = None
cached_states_trace = None
cached_airports = None
cached_scattermapbox = None
query_data = dict()

mode = os.getenv("MODE")

if mode is None:
    raise Exception("MODE not set in environment file.")


def cache_scattermapbox():
    token = open(".mapbox_token").read()
    fig = go.Figure()
    #Airports
    fig.add_trace(get_airport_trace())
    #Track line
    fig.add_trace(go.Scattermapbox(mode="lines", lon=[0], lat=[0], hoverinfo="skip"))
    #Track endpoint
    fig.add_trace(go.Scattermapbox(mode="markers", lon=[0], lat=[0], marker={"size": 1}, hoverinfo="skip"))
    #Aircrafts
    fig.add_trace(go.Scattermapbox(
        mode="markers",
        lon=[1],
        lat=[1],
        hoverinfo="none",
        marker={
            "size": 0,
            "symbol": "airport",
            "angle": [],
            "allowoverlap": True,
        },
        customdata=[],
    ))
    fig.update_layout(
        mapbox={"accesstoken": token, "style": "dark", "zoom": 0}, showlegend=False
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        uirevision=True,
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def get_current_states_dev(count: int = 0):
    url = f"https://opensky-network.org/api/states/all"
    payload = {}
    headers = {"Cookie": "XSRF-TOKEN=1f3d9767-c581-485b-bb02-f83712c5efe2"}
    response = requests.request("GET", url, headers=headers, data=payload,auth=('ethanjolly3','ethanjolly3'))
    if (
        response.text == None
        or response.status_code == 404
        or response.status_code == 503
    ):
        print(response.text)
    decoded = json.loads(response.text)
    document = decoded
    df = pd.DataFrame(
        document["states"],
        columns=[
            "icao24",
            "callsign",
            "origin_country",
            "time_position",
            "last_contact",
            "longitude",
            "latitude",
            "baro_altitude",
            "on_ground",
            "velocity",
            "true_track",
            "vertical_rate",
            "sensors",
            "geo_altitude",
            "squawk",
            "spi",
            "position_source",
        ],
    )

    if count > 0:
        df = df.sample(count)

    return df


def get_airport_trace():
    global cached_airports
    df = cached_airports
    trace = go.Scattermapbox(
        hoverinfo="skip",
        mode="markers",
        lon=df["longitude"],
        lat=df["latitude"],
        marker={"size": 2, "color":"rgba(150, 159, 237)"},
        customdata=df[["airport", "type", "iso", "latitude", "longitude"]],
    )
    return trace


def get_states_trace(df):
    rotation_angles = df.true_track.fillna(0)
    trace = go.Scattermapbox(
        mode="markers",
        lon=df["longitude"],
        lat=df["latitude"],
        hoverinfo="none",
        marker={
            "size": 10,
            "symbol": "airport",
            "angle": rotation_angles,
            "allowoverlap": True,
        },
        customdata= df[
            [
                "icao24",
                "callsign",
                "origin_country",
                "latitude",
                "longitude",
                "baro_altitude",
                "velocity",
            ]
        ],
    )
    fig = go.Figure()
    fig.add_trace(trace)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json


def get_flights_data(view_name, limit=0, type="json"):
    with create_postgres_conn() as conn:
        if limit > 0:
            sql = f"select * from {view_name} limit {limit};"
        else:
            sql = f"select * from {view_name};"

        df = pd.read_sql_query(sql, conn)
        if type == "json":
            df = df.to_json(orient="values")
    return df


def get_updated_graph_data():
    global cached_states
    global cached_states_trace
    print("Getting data")
    if mode == 'DEV':
        cached_states = get_current_states_dev()
        cached_states_trace = get_states_trace(cached_states)
    print("Returning graph")
    return cached_states_trace


def plot_altitude(df):
    # fig = px.line(df, x='time', y='baro_altitude')
    layout = go.Layout(
        titlefont={"color": "#FFFFFF"},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",  # Sets background color to transparent
        xaxis=dict(
            linecolor="#FFFFFF",
            color="#FFFFFF",  # Sets color of X-axis line
            showgrid=False,
            showticklabels=False,  # Removes X-axis grid lines
        ),
        yaxis=dict(
            linecolor="#FFFFFF",
            color="#FFFFFF",  # Sets color of Y-axis line
            showgrid=False,  # Removes Y-axis grid lines
        ),
        margin=go.layout.Margin(
            l=20,  # left margin
            r=20,  # right margin
            b=20,  # bottom margin
            t=20,  # top margin
        ),
        autosize=True,
    )

    fig = go.Figure(
        data=go.Scatter(x=df["time"], y=df["baro_altitude"], line_color="#ff675f"),
        layout=layout,
    )

    return fig


def update_flights_cache(query_data):
    query_data["last_update"] = time.time()
    query_data["flights_by_country"] = get_flights_data("flights_by_country")
    query_data["flights_by_operator"] = get_flights_data("flights_by_operator", 10)
    query_data["flights_arriving_airport"] = get_flights_data(
        "total_flights_arriving_by_airport", 10
    )
    query_data["flights_departing_airport"] = get_flights_data(
        "total_flights_departing_by_airport", 10
    )
    query_data["flights_by_weekday"] = get_flights_data("total_flights_per_day", 10)
    query_data["aircraft_flight_metrics"] = get_flights_data(
        "total_flight_time_num_flights_distance_per_aircraft"
    )
    query_data["most_popular_operator_by_country"] = get_flights_data(
        "most_popular_operator_by_country"
    )
    query_data["grouped_stats"] = get_flights_data("grouped_stats")
    query_data["domestic_vs_international_flights"] = get_flights_data(
        "domestic_vs_international_flights"
    )
    # query_data["popular_routes"] = get_flights_data("popular_routes")
    query_data["most_popular_route_by_country"] = get_flights_data(
        "most_popular_route_by_country_ordered"
    )
    query_data["popular_routes"] = get_flights_data("all_routes")


def update_state_cache(data):
    global cached_states
    temp_data_df = pd.DataFrame(data, columns=state_columns)
    cached_states = temp_data_df


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/live")
def live():
    return render_template("live.html")


@app.route("/stats")
def stats():
    return render_template("stats.html", query_data=query_data)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/initialise-livemap", methods=["GET"])
def initialise_map():
    global cached_scattermapbox
    return cached_scattermapbox

@app.route("/graph-data", methods=["GET"])
def graph_data():
    data = get_updated_graph_data()
    return data


@app.route("/states", methods=["PUT"])
def put_state():
    data = request.json
    update_state_cache(data)
    global cached_states
    global cached_states_trace
    cached_states_trace = get_states_trace(cached_states)
    return "OK"


@app.route("/flights", methods=["PUT"])
def put_flights():
    global last_flight_query
    last_flight_query = time.time()
    update_flights_cache(query_data)
    return "OK"


if __name__ == "__main__":
    update_flights_cache(query_data)
    cached_airports = get_flights_data('all_airports',type='df')
    cached_scattermapbox = cache_scattermapbox()
    app.run(debug=True)

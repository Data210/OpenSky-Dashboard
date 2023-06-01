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

api_username = os.getenv("OPENSKY_USERNAME")
api_password = os.getenv("OPENSKY_PASSWORD")

app = Flask(__name__)

icaos = ["ab1644", "aa9321", "a77ec5"]

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

mode = os.getenv("MODE")
if mode is None:
    raise Exception("MODE not set in environment file.")


def get_current_states_v3(count: int = 0):
    url = f"https://opensky-network.org/api/states/all"
    payload = {}
    headers = {"Cookie": "XSRF-TOKEN=1f3d9767-c581-485b-bb02-f83712c5efe2"}
    response = requests.request("GET", url, headers=headers, data=payload)
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

def get_current_states(number: int = 0):
    url = f"https://opensky-network.org/api/states/all"
    payload = {}
    headers = {"Cookie": "XSRF-TOKEN=1f3d9767-c581-485b-bb02-f83712c5efe2"}
    response = requests.request("GET", url, headers=headers, data=payload)
    decoded = json.loads(response.text)
    states = decoded["states"]
    if number > 0:
        icaos = [state[0] for state in states[-number:]]
    else:
        icaos = [state[0] for state in states]
    return icaos


def get_flights(icao24: str):
    end_time = int(time.time())
    begin_time = end_time - 3600 * 24 * 2
    url = f"https://opensky-network.org/api/flights/aircraft?icao24={icao24}&begin={begin_time}&end={end_time}"
    payload = {}
    headers = {"Cookie": "XSRF-TOKEN=1f3d9767-c581-485b-bb02-f83712c5efe2"}
    response = requests.request("GET", url, headers=headers, data=payload)
    if (
        response.text == None
        or response.status_code == 404
        or response.status_code == 503
    ):
        return df

    decoded = json.loads(response.text)
    df = pd.DataFrame(
        decoded,
        columns=[
            "icao24",
            "firstSeen",
            "estDepartureAirport",
            "lastSeen",
            "estArrivalAirport",
            "callsign",
            "estDepartureAirportHorizDistance",
            "estDepartureAirportVertDistance",
            "estArrivalAirportHorizDistance" "estArrivalAirportVertDistance",
            "departureAirportCandidatesCount",
            "arrivalAirportCandidatesCount",
        ],
    )
    return df


def get_tracks(icao24_list: list):
    df = pd.DataFrame(
        columns=[
            "time",
            "latitude",
            "longitude",
            "baro_altitude",
            "true_track",
            "on_ground",
            "icao24",
            "startTime",
            "endTime",
        ]
    )
    for icao24 in icao24_list:
        url = f"https://opensky-network.org/api/tracks/all?icao24={icao24}&time=0"
        payload = {}
        headers = {"Cookie": "XSRF-TOKEN=1f3d9767-c581-485b-bb02-f83712c5efe2"}
        response = requests.request("GET", url, headers=headers, data=payload)
        if (
            response.text == None
            or response.status_code == 404
            or response.status_code == 503
        ):
            continue

        decoded = json.loads(response.text)
        df_temp = pd.DataFrame(decoded["path"])
        df_temp.columns = [
            "time",
            "latitude",
            "longitude",
            "baro_altitude",
            "true_track",
            "on_ground",
        ]
        df_temp["icao24"] = decoded["icao24"]
        df_temp["startTime"] = decoded["startTime"]
        df_temp["endTime"] = decoded["endTime"]
        df = pd.concat([df, df_temp])
    return df


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


def get_states_trace(df):
    # trace_dict = {
    #     "mode": "markers",
    #     "lon": df["longitude"],
    #     "lat": df["latitude"],
    #     "hoverinfo": "none",
    #     "marker": {
    #         "size": 10,
    #         "symbol": "airport",
    #         "angle": rotation_angles,
    #         "allowoverlap": True,
    #     },
    #     "customdata": df[
    #         [
    #             "icao24",
    #             "callsign",
    #             "origin_country",
    #             "latitude",
    #             "longitude",
    #             "baro_altitude",
    #             "velocity",
    #         ]
    #     ],
    # }
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
    
    #     hovertemplate="<br>".join(
    #         [
    #             "ICAO24: %{customdata[0]}",
    #             "Callsign: %{customdata[1]}",
    #             "Origin_Country: %{customdata[2]}",
    #             "Latitude: %{customdata[3]}",
    #             "Longitude: %{customdata[4]}",
    #             "Altitude: %{customdata[5]}",
    #             "Velocity: %{customdata[6]}",
    #         ]
    #     ),
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json


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
        # hovertemplate="<br>".join(
        #     [
        #         "Airport: %{customdata[0]}",
        #         "Type: %{customdata[1]}",
        #         "ISO: %{customdata[2]}",
        #         "Latitude: %{customdata[3]}",
        #         "Longitude: %{customdata[4]}",
        #     ]
        # ),
    )
    return trace


def plot_states(df):
    global cached_airports
    token = open(".mapbox_token").read()  # you need your own token
    trace = get_states_trace(df)
    airports_trace = get_airport_trace()

    fig = go.Figure()
    fig.add_trace(airports_trace)
    fig.add_trace(go.Scattermapbox(mode="lines", lon=[0], lat=[0], hoverinfo="skip"))
    fig.add_trace(
        go.Scattermapbox(
            mode="markers", lon=[0], lat=[0], marker={"size": 1}, hoverinfo="skip"
        )
    )
    fig.add_trace(trace)
    fig.update_layout(
        mapbox={"accesstoken": token, "style": "dark", "zoom": 0}, showlegend=False
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        uirevision=True,
    )
    fig.update_geos(oceancolor="#ff0000")
    # fig = px.scatter_geo(df,
    #               lat="latitude",
    #               lon="longitude",
    #               #color="icao24",
    #               projection="natural earth",
    #               )
    return fig


def plot_tracks(df):
    df_markers = df.query("time == endTime")

    fig = px.line_geo(
        df, lat="latitude", lon="longitude", color="icao24", projection="orthographic"
    )
    fig_markers = px.scatter_geo(
        df_markers,
        lat="latitude",
        lon="longitude",
        color="icao24",
        projection="orthographic",
    )
    fig_markers2 = px.scatter_geo(
        df_markers,
        lat="latitude",
        lon="longitude",
        color="icao24",
        projection="orthographic",
    )
    fig_markers.update_traces(
        marker={"symbol": ["star-triangle-up"], "size": 15, "angle": 45}
    )
    fig_markers2.update_traces(
        marker={"symbol": ["diamond-tall"], "size": 15, "angle": 45}
    )
    for trace in fig_markers.data:
        fig.add_trace(trace)
    for trace in fig_markers2.data:
        fig.add_trace(trace)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        # coastlinecolor = '#ffaaaa'
    )
    fig.update_geos(
        # countrycolor='#aaaaaa',
        # coastlinecolor='#aaaaaa',
        bgcolor="rgba(0,0,0,0)",
        landcolor="#66aa66",
        showocean=True,
        oceancolor="LightBlue",
        lakecolor="LightBlue",
    )
    return fig


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
            "size": 10,
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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/live")
def live():
    return render_template("live.html")


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


@app.route("/track-data/<icao24>", methods=["POST"])
def track_data(icao24):
    # Retrieve or generate the updated graph data
    df = get_tracks([icao24])
    fig = plot_altitude(df)
    div = fig.to_html(full_html=False, include_plotlyjs=False)
    lineJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return lineJSON
    # Return the graph data as JSON

    return data


@app.route("/flight-data/<icao24>", methods=["POST"])
def flight_data(icao24):
    # Retrieve or generate the updated graph data
    df = get_flights(icao24)
    data = df.to_json(orient="records")
    # Return the graph data as JSON
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



def get_updated_graph_data():
    global cached_states
    global cached_states_trace
    print("Getting data")
    if mode == 'DEV':
        cached_states = get_current_states_v3()
        cached_states_trace = get_states_trace(cached_states)
    print("Returning graph")
    return cached_states_trace

query_data = dict()
update_flights_cache(query_data)
cached_airports = get_flights_data('all_airports',type='df')
cached_scattermapbox = cache_scattermapbox()

if __name__ == "__main__":
    app.run(debug=True)

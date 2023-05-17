import plotly.graph_objects as go
from flask import Flask, render_template, jsonify
import requests
import json
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pymongo
import time
import os

MONGODB_URI = "mongodb+srv://admin:iloveplanes@ethan-cluster.cr8xduf.mongodb.net/"
client = pymongo.MongoClient(MONGODB_URI)

api_username = os.getenv("OPENSKY_USERNAME")
api_password = os.getenv("OPENSKY_PASSWORD")

app = Flask(__name__)

icaos = ["ab1644","aa9321","a77ec5"]
db = client.get_database('aircraft')
collection = db.get_collection('states')
def get_current_states_v3(count: int = 0):
    url = f"https://opensky-network.org/api/states/all"
    payload = {}
    headers = {'Cookie': 'XSRF-TOKEN=1f3d9767-c581-485b-bb02-f83712c5efe2'}
    response = requests.request("GET", url, headers=headers, data=payload,auth=(api_username, api_password))
    if response.text == None or response.status_code == 404 or response.status_code == 503:
        print(response.text)
    decoded = json.loads(response.text)
    document = decoded
    df = pd.DataFrame(document['states'],columns = ["icao24", "callsign","origin_country",
            "time_position","last_contact","longitude",
            "latitude","baro_altitude","on_ground",
            "velocity","true_track","vertical_rate",
            "sensors","geo_altitude","squawk",
            "spi","position_source"])
    
    if count > 0:
        df = df.sample(count)

    return df

def get_current_states_v2(count: int = 0):
    cursor = collection.find().sort('_id',-1).limit(1)
    document = cursor.next()
    df = pd.DataFrame(document['states'],columns = ["icao24", "callsign","origin_country",
            "time_position","last_contact","longitude",
            "latitude","baro_altitude","on_ground",
            "velocity","true_track","vertical_rate",
            "sensors","geo_altitude","squawk",
            "spi","position_source"])
    
    if count > 0:
        df = df.sample(count)

    return df

def get_current_states(number: int = 0):
        url = f"https://opensky-network.org/api/states/all"
        payload = {}
        headers = {'Cookie': 'XSRF-TOKEN=1f3d9767-c581-485b-bb02-f83712c5efe2'}
        response = requests.request("GET", url, headers=headers, data=payload)
        decoded = json.loads(response.text)
        states = decoded['states']
        if number > 0:
            icaos = [state[0] for state in states[-number:]]
        else:
            icaos = [state[0] for state in states]
        return icaos

def get_flights(icao24: str):
    end_time = int(time.time())
    begin_time = end_time - 3600 * 24
    url = f"https://opensky-network.org/api/flights/aircraft?icao24={icao24}&begin={begin_time}&end={end_time}"
    payload = {}
    headers = {'Cookie': 'XSRF-TOKEN=1f3d9767-c581-485b-bb02-f83712c5efe2'}
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.text == None or response.status_code == 404 or response.status_code == 503:
        print(response.text)
        return df
    
    decoded = json.loads(response.text)
    print(decoded)
    df = pd.DataFrame(decoded, columns = ["icao24","firstSeen","estDepartureAirport",
                       "lastSeen","estArrivalAirport","callsign",
                       "estDepartureAirportHorizDistance","estDepartureAirportVertDistance","estArrivalAirportHorizDistance"
                       "estArrivalAirportVertDistance","departureAirportCandidatesCount","arrivalAirportCandidatesCount"])
    return df

def get_tracks(icao24_list: list):
    df = pd.DataFrame(columns = ["time","latitude","longitude","baro_altitude","true_track","on_ground","icao24","startTime","endTime"])
    for icao24 in icao24_list:
        url = f"https://opensky-network.org/api/tracks/all?icao24={icao24}&time=0"
        payload = {}
        headers = {'Cookie': 'XSRF-TOKEN=1f3d9767-c581-485b-bb02-f83712c5efe2'}
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.text == None or response.status_code == 404 or response.status_code == 503:
            print(response.text)
            continue
        
        decoded = json.loads(response.text)
        df_temp = pd.DataFrame(decoded['path'])
        df_temp.columns = ["time","latitude","longitude","baro_altitude","true_track","on_ground"]
        df_temp["icao24"] = decoded['icao24']
        df_temp["startTime"] = decoded['startTime']
        df_temp["endTime"] = decoded['endTime']
        df = pd.concat([df,df_temp])
    return df

def plot_altitude(df):
    # fig = px.line(df, x='time', y='baro_altitude')
    layout = go.Layout(
    title="Altitude",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',  # Sets background color to transparent
    xaxis=dict(
        linecolor="#FFFFFF",
        color="#FFFFFF",  # Sets color of X-axis line
        showgrid=False,
        showticklabels=False  # Removes X-axis grid lines
    ),
    yaxis=dict( 
        linecolor="#FFFFFF",
        color="#FFFFFF",  # Sets color of Y-axis line
        showgrid=False,  # Removes Y-axis grid lines    
    ),
     margin=go.layout.Margin(
        l=0, #left margin
        r=0, #right margin
        b=0, #bottom margin
        t=0  #top margin
    )
)

    fig = go.Figure(
        data=go.Scatter(x=df['time'], y=df['baro_altitude'],line_color='#ff675f'),
        layout=layout
    )   

    return fig

def plot_states(df):
    rotation_angles = df.true_track.fillna(0)
    token = open(".mapbox_token").read() # you need your own token
    fig = go.Figure()
    fig = go.Figure(go.Scattermapbox( mode = "markers", lon = df['longitude'], lat = df['latitude'], marker = {'size': 10, 'symbol': "airport",'angle':rotation_angles,'allowoverlap':True}, customdata=df[['icao24','callsign','origin_country','latitude','longitude','baro_altitude']], hovertemplate='<br>'.join([ 'ICAO24: %{customdata[0]}', 'Callsign: %{customdata[1]}', 'Origin_Country: %{customdata[2]}', 'Latitude: %{customdata[3]}', 'Longitude: %{customdata[4]}', 'Altitude: %{customdata[5]}' ]) ))
    fig.update_layout( mapbox = { 'accesstoken': token, 'style': "dark", 'zoom': 0}, showlegend = False)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin={"r": 0, "t": 0, "l": 0, "b": 0},

        #coastlinecolor = '#ffaaaa'
    )
    fig.update_geos(
        oceancolor = '#ff0000'
    )
    # fig = px.scatter_geo(df,
    #               lat="latitude",
    #               lon="longitude",
    #               #color="icao24",
    #               projection="natural earth",
    #               )
    return fig

def plot_tracks(df):
    df_markers = df.query("time == endTime")

    fig = px.line_geo(df,
                    lat="latitude",
                    lon="longitude",
                    color="icao24",
                    projection="orthographic"
                    )
    fig_markers = px.scatter_geo(df_markers,
                    lat="latitude",
                    lon="longitude",
                    color="icao24",
                    projection="orthographic",
    )
    fig_markers2 = px.scatter_geo(df_markers,
                    lat="latitude",
                    lon="longitude",
                    color="icao24",
                    projection="orthographic",
    )
    fig_markers.update_traces(
        marker={'symbol':['star-triangle-up'],'size':15, 'angle':45}
    )
    fig_markers2.update_traces(
        marker={'symbol':['diamond-tall'],'size':15, 'angle':45}
    )
    for trace in fig_markers.data:
        fig.add_trace(trace)
    for trace in fig_markers2.data:
        fig.add_trace(trace)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        #coastlinecolor = '#ffaaaa'
    )
    fig.update_geos(
                    # countrycolor='#aaaaaa',
                    # coastlinecolor='#aaaaaa',
                    bgcolor='rgba(0,0,0,0)',
                    landcolor='#66aa66',
                    showocean=True,
                    oceancolor='LightBlue',
                    lakecolor='LightBlue')
    return fig

@app.route('/')
def index():
    # Create a Plotly figure
    # Convert the figure to HTML div
    #fig = plot_tracks(get_tracks(get_current_states(20)))
    fig = plot_states(get_current_states_v2())
    div = fig.to_html(full_html=False,include_plotlyjs=False,)
    graphJSON = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', plot_div=div, graphJSON=graphJSON)

@app.route('/graph-data', methods=['POST'])
def graph_data():
    # Retrieve or generate the updated graph data
    data = get_updated_graph_data()

    # Return the graph data as JSON
    return data

@app.route('/track-data/<icao24>', methods=['POST'])
def track_data(icao24):
    # Retrieve or generate the updated graph data
    df = get_tracks([icao24])
    fig = plot_altitude(df)
    div = fig.to_html(full_html=False,include_plotlyjs=False)
    lineJSON = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    return lineJSON
    # Return the graph data as JSON


    return data

@app.route('/flight-data/<icao24>', methods=['POST'])
def flight_data(icao24):
    # Retrieve or generate the updated graph data
    df = get_flights(icao24)
    data = df.to_json(orient="records")
    # Return the graph data as JSON
    return data

def get_updated_graph_data():
    # Your logic to retrieve or generate updated graph data
    print("Getting data")
    #fig = plot_tracks(get_tracks(get_current_states(20)))
    #data = get_current_states_v2(1000)
    data = get_current_states_v2()
    fig = plot_states(data)
    div = fig.to_html(full_html=False,include_plotlyjs=False)
    print("Returning graph")
    return plotly.io.to_json(fig)

if __name__ == '__main__':
    app.run(debug=True)
$(document).ready(function () {
    line_chart('graph1', "Flights by weekday")
})

function line_chart(target_id, title) {
    var trace1 = {
        x: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        y: [10, 12, 15, 20, 21, 18, 14],
        type: 'scatter',
        mode: 'lines',
        fill: 'tozeroy',
        fillcolor: "rgba(150, 159, 237,0.2)",
        line: {
            color: "rgba(150, 159, 237,0.7)",
            width: 5,
            shape: 'spline',
            smoothing: 1
        }
    };

    layout = {
        title: {
            text: '<b>'+title+'</b>',
            font: {
                color: '#FFFFFF',
                family: 'Helvetica',
                size: 40
            },
            yref: 'paper',
            // automargin: true,
        },
        showlegend: false,
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        xaxis: {
            linecolor: "#FFFFFF",
            color: "#FFFFFF",
            tickfont:{
                size:20
            },
            showgrid: false,
            ticklen: 15,
            title_standoff:15,
            showticklabels: true,
            tickwidth: 0,
            automargin: true,
        },
        yaxis: {
            linecolor: "#FFFFFF",
            color: "#FFFFFF",
            gridcolor: "rgba(0,0,0,0.5)",
            tickfont:{
                size:20
            },
            showgrid: true,
            automargin: true,
            
        },
        margin: {
            // pad:20,
            l: 10,
            r: 10,
            b: 10,
            t: 80,
        },
        autosize: true,
        uirevision: true
    }

    var data = [trace1];

    Plotly.newPlot(target_id, data, layout, { displayModeBar: false });
}

function bar_chart(target_id, data, title) {

    var data = [{
        type: 'bar',
        x: data.map(subArray => subArray[1]),
        y: data.map(subArray => subArray[0]),
        orientation: 'h',
        marker: {
            color: '#dbbb06'
        }
    }];

    layout = {
        title: {
            text: title,
            font: {
                color: '#FFFFFF',
                family: 'Helvetica'
            }
        },
        xaxis: {
            showline: true,
            showgrid: false,
            ticks: 'outside',
            linecolor: 'rgb(255, 255, 255)',
            linewidth: 2,
            zeroline: false,
            tickcolor: 'rgb(225, 225, 225)',
            tickfont: {
                family: 'Arial',
                size: 12,
                color: 'rgb(255, 255, 255)',
            },
        },
        yaxis: {
            showline: true,
            showgrid: true,
            gridwidth: 1,
            gridcolor: 'rgb(225, 225, 225)',
            zeroline: false,
            linecolor: 'rgb(255, 255, 255)',
            linewidth: 2,
            tickcolor: 'rgb(225, 225, 225)',
            ticks: 'outside',
            tickfont: {
                family: 'Arial',
                size: 12,
                color: 'rgb(255, 255, 255)',
            }
        },
        margin: {
            l: 200,
            r: 15,
            b: 30,
            t: 40
        },
        paper_bgcolor: 'rgba(0,0,0,0.5)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        autosize: true
    }
    config = {
        displayModeBar: false
    }

    Plotly.newPlot(target_id, data, layout, config);
}
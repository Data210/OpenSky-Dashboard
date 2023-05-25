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
        fillcolor: "rgba(219, 187, 6,0.4)",
        line: {
            color: "rgba(219, 187, 6,0.5)",
            width: 5,
            shape: 'spline',
            smoothing: 1.3
        }
    };

    layout = {
        title: {
            text: title,
            font: {
                color: '#FFFFFF',
                family: 'Helvetica'
            }
        },
        showlegend: false,
        paper_bgcolor: 'rgba(0,0,0,0.2)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        xaxis: {
            linecolor: "#FFFFFF",
            color: "#FFFFFF",
            showgrid: false,
            showticklabels: true
        },
        yaxis: {
            linecolor: "#FFFFFF",
            color: "#FFFFFF",
            showgrid: false,
        },
        margin: {
            l: 30,
            r: 15,
            b: 30,
            t: 40
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
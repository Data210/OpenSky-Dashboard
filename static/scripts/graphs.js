$(document).ready(function () {

})

function line_chart(target_id, data, title) {
    var trace1 = {
        x: data.map(subArray => subArray[0]),
        y: data.map(subArray => subArray[1]),
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
            text: '<b>' + title + '</b>',
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
            tickfont: {
                size: 20
            },
            showgrid: false,
            ticklen: 15,
            title_standoff: 15,
            showticklabels: true,
            tickwidth: 0,
            automargin: true,
        },
        yaxis: {
            linecolor: "#FFFFFF",
            color: "#FFFFFF",
            gridcolor: "rgba(0,0,0,0.5)",
            tickfont: {
                size: 20
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
            color: 'rgba(150, 159, 237,0.7)'
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
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        autosize: true
    }
    config = {
        displayModeBar: false
    }

    Plotly.newPlot(target_id, data, layout, config);
}

function choropleth_map(target_id, data, title) {
    // console.log(data)
    var colorScale = [
        [0, 'rgb(240,240,240)'],  // No data color (light gray)
        [0.1, 'rgb(220,220,220)'], // Lowest value color (dark gray)
        [1.0, 'rgb(120, 129, 200)']      // Highest value color (blue)
    ];

    var data = [{
        type: 'choropleth',
        locations: data.map(subArray => subArray[0]),
        z: data.map(subArray => subArray[1]),
        locationmode: 'ISO-3',
        colorscale: colorScale,
        zmax: 900,
        zmin: 0,
        autocolorscale: false,
        // reversescale: true,
        // text: data.map(subArray => subArray[0]),
        colorbar: {
            bordercolor: '#FFFFFF',
            orientation: 'v',
            thickness: 20,
            tickfont: { family: 'Arial', size: 12, color: '#FFFFFF' },
            x: 1
            // title: { font: { color: '#FFFFFF', family: 'Arial', size: 12 }, side: 'top', text: 'Number Of Flights' },
        },
    }];

    layout = {
        colorbar: {
            orientation: "h",

        },
        // title: {
        //     text: title,
        //     font: {
        //         color: '#FFFFFF',
        //         family: 'Helvetica'
        //     }
        // },
        geo: {
            showframe: false,
            // showcoastlines:false,
            bgcolor: 'rgba(0,0,0,0)',
            showland: true,
            landcolor: '#d3d3d3'
        },
        margin: { "r": 50, "t": 0, "l": 0, "b": 0 },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',

    }
    config = {
        displayModeBar: false
    }

    Plotly.newPlot(target_id, data, layout, config);
}

function generate_table(element, columnNames, data) {
    $(`#${element}`).html("")
    for (const row of data) {
        row_html = '';
        for (const cell of row) {
            row_html = row_html + `
                    <td class="px-4 py-4 text-sm">
                    ${cell ?? "N/A"}
                    </td>`
        }
        $(`#${element}`).append(
            `<tr class="bg-background border-b dark:bg-background dark:border-secondary hover:bg-slate-50 dark:hover:bg-slate-600">
                ${row_html}
            </tr>`
        )
    }
}
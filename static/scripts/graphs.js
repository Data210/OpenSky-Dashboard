$(document).ready(function () {

})

function brightness_gradient(steps,r,g,b,a){
    if (steps <= 1) {
        return [`rgba(${r}, ${g}, ${b},${a})`]
    }
    colors = []
    for (let index = 0; index < steps; index++) {
        d_r = Math.floor((255 - r)*(index/(steps-1)))
        d_g = Math.floor((255 - g)*(index/(steps-1)))
        d_b = Math.floor((255 - b)*(index/(steps-1)))

        colors.push(`rgba(${r+d_r},${g+d_g},${b+d_b},${a})`)
    }
    return colors
}

function interpolate(a,b,t){
    return a + (b - a) * t
}

function line_chart(target_id, data, title) {
    x = data.map(subArray => subArray[0]);
    y = data.map(subArray => subArray[1]);
    let trace1 = {
        x: data.map(subArray => subArray[0]),
        y: data.map(subArray => subArray[1]),
        type: 'scatter',
        mode: 'lines',
        // fill: 'tozeroy',
        // fillcolor: "rgba(150, 159, 237,0.2)",
        line: {
            color: "rgba(240, 240, 240,1)",
            width: 5,
            shape: 'spline',
            // smoothing: 1
        }
    };
    let traces = []
    traces.push(trace1)
    n = 50
    for (let index = 0; index < n; index++) {
        let trace = {
            x: x,
            y: y.map(ele => interpolate(0,ele,index/(n-1))),
            type: 'scatter',
            mode: 'lines',
            fill: 'tonexty',
            fillcolor: `rgba(150, 159, 237,${Math.pow(index/(n-1),2)})`,
            hoverinfo: 'skip',
            line: {
                color: `rgba(150, 159, 237,${index/(n-1)}}`, //${1-(index/(n-1))}
                width: 0,
                shape: 'spline',
                smoothing: 1
            }
        };
        traces.push(trace)    
    }

    layout = {
        title: {
            text: '<b>' + title + '</b>',
            font: {
                color: '#FFFFFF',
                family: 'Helvetica',
                size: 32
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
            tickangle: 90,
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
    console.log(traces)
    Plotly.newPlot(target_id, traces, layout, { displayModeBar: false });
}

function bar_chart(target_id, data, title) {

    var data = [{
        type: 'bar',
        x: data.map(subArray => subArray[1]),
        y: data.map(subArray => subArray[0]),
        orientation: 'h',
        marker: {
            color:  brightness_gradient(10,150, 159, 237,.8)
        }
    }];

    layout = {
        // title: {
        //     text: title,
        //     font: {
        //         color: '#FFFFFF',
        //         family: 'Helvetica'
        //     }
        // },
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
            l: 220,
            r: 10,
            b: 30,
            t: 10
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
        [0, 'rgba(240,240,240,1)'],  // No data color (light gray)
        [0.015, 'rgba(160, 160, 220,1)'], // Lowest value color (dark gray)
        [0.2, 'rgba(56, 65, 136,1)']  ,
        [1, 'rgba(28, 32, 68,1)']      // Highest value color (blue)
    ];

    var data = [{
        type: 'choropleth',
        locations: data.map(subArray => subArray[0]),
        z: data.map(subArray => subArray[1]),
        locationmode: 'ISO-3',
        colorscale: colorScale,
        // zmax: 900,
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
            landcolor: 'rgba(255,255,255,0)'
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

function getMaxOfArray(numArray) {
    return Math.max.apply(null, numArray);
}

function route_map(target_id, data, title){
    var data_list = [];
    var count = data.map(subArray => subArray[7])
    var startLongitude = data.map(subArray => subArray[2])
    var endLongitude = data.map(subArray => subArray[4])
    var startLat = data.map(subArray => subArray[3])
    var endLat = data.map(subArray => subArray[5])
    var dep = data.map(subArray => subArray[0])
    var arr = data.map(subArray => subArray[1])

    for ( var i = 0 ; i < count.length; i++ ) {
        var opacityValue = count[i]/getMaxOfArray(count);

        var result = {
            type: 'scattergeo',
            lon: [ startLongitude[i] , endLongitude[i] ],
            lat: [ startLat[i] , endLat[i] ],
            mode: 'lines',
            line: {
                width: 2.5,
                color: 'rgb(150, 159, 237)'
            },
            opacity: opacityValue,
            hoverinfo:'text',
            text:`Departed: ${dep[i]}<br>Arrived: ${arr[i]}<br>No. Flights: ${count[i]}`
        };

        data_list.push(result);
    };

    var layout = {
        showlegend: false,
        geo:{
            projection: {
                type: 'equirectangular'
            },
            showland:false,
            showframe:false,
            showcoastlines:true,
            showlake:false,
            showcountries:true,
            bgcolor:'rgba(0,0,0,0)',
            landcolor:'rgb(243, 243, 243)',
            countrycolor:'rgb(128,128,128)',
            coastlinecolor:'rgb(105,105,105)'
        },
        margin:{"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor:'rgba(0,0,0,0)',
        plot_bgcolor:'rgba(0,0,0,0)'
    };
    config = {
        displayModeBar: false,
        staticPlot: true
    };

    Plotly.newPlot(target_id, data_list, layout,config,{showLink: false});
}

function generate_table(element, columnNames, data, limit=0) {
    $(`#${element}`).html("")
    if (limit > 0){
        data = data.slice(0,limit)
    }
    for (const row of data) {
        sliced_row = row.slice(0,columnNames.length)
        row_html = '';
        for (const cell of sliced_row) {
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

function donut_chart(target_id, data, title){

    var graph_data = [{
        values: data[0],
        labels: ['Domestic','International' ],
        name: 'Flight type',
        marker: {
            colors: ['rgb(120, 129, 200)','rgb(230, 230, 230)']
        },
        textfont:{
            family: 'Arial Black',
            size: 17.5,

        },
        textinfo: "label+percent",
        hole: .6,
        type: 'pie'
    }];
    
    var layout = {
        annotations: [
        {
            font: {
                size: 34,
                color: " rgb(255,255,255)",
                family: 'Arial Black',
            },
            showarrow: false,
            text: 'Flight Type',
            x: 0.5,
            y: 0.5,
            xanchor: 'center'
        }],
        showlegend: false,
        margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        autosize: true
    };
    config = {
        displayModeBar: false
    }
    
    Plotly.newPlot(target_id, graph_data, layout,config);
}
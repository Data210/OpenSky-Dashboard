$(document).ready(function () {
    line_chart('graph1', "Flights by weekday")
})

function line_chart(target_id,title){
    var trace1 = {
        x: ["Mon", "Tue","Wed","Thu","Fri","Sat","Sun"],
        y: [10, 12, 15, 20, 21, 18, 14],
        type: 'scatter',
        mode: 'lines',
        fill: 'tozeroy',
        fillcolor:"rgba(219, 187, 6,0.4)",
        line: {
            color: "rgba(219, 187, 6,0.5)",
            width:5,
            shape:'spline',
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
      
      Plotly.newPlot(target_id, data, layout, {displayModeBar: false});
}
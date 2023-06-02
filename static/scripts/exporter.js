
function getChartState (id) {
const el = document.getElementById(id)
return {
    data: el.data, // current data
    layout: el.layout // current layout
}
}

async function getHtml(id) {
    const state = getChartState(id)

    return `
        <head>
            <meta charset="utf-8" />
            <script src="https://cdn.plot.ly/plotly-2.20.0.min.js"></script>
        </head>
        <div id="${id}"></div>
        
        <script type="text/javascript">
            Plotly.newPlot(
            '${id}', 
            ${JSON.stringify(state.data)},
            ${JSON.stringify(state.layout)}
            )
        <\/script>
`
}

async function exportToHtml (id) {
    // Create URL
    const blob = new Blob([await getHtml(id)], { type: 'text/html' })
    const url = URL.createObjectURL(blob)
  
    // Create downloader
    const downloader = document.createElement('a')
    downloader.href = url
    downloader.download = 'export.html'
  
    // Trigger click
    downloader.click()
  
    // Clean up
    URL.revokeObjectURL(url)
  }
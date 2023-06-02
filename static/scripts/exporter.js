function getChartState (id) {
const el = document.getElementById(id)
return {
    data: el.data,
    layout: el.layout,
    config: el._context
}
}
async function getHtml(id) {

    return $(document.getElementById(id)).html()
}

async function downloadHtml (id) {
    // Create URL
    const blob = new Blob([await getHtml(id)], { type: 'text/html' })
    const url = URL.createObjectURL(blob)
  
    // Create downloader
    const downloader = document.createElement('a')
    downloader.href = url
    downloader.download = `${id}.html`
  
    // Trigger click
    downloader.click()
  
    // Clean up
    URL.revokeObjectURL(url)
  }

async function getGraphHtml(id) {
    const state = getChartState(id)

    return `
        <script type="text/javascript">
            Plotly.newPlot(
            '${id}', 
            ${JSON.stringify(state.data)},
            ${JSON.stringify(state.layout)},
            ${JSON.stringify(state.config)}
            )
        <\/script>
`
}

async function exportToHtml (id) {
    // Create URL
    const blob = new Blob([await getGraphHtml(id)], { type: 'text/html' })
    const url = URL.createObjectURL(blob)
  
    // Create downloader
    const downloader = document.createElement('a')
    downloader.href = url
    downloader.download = `${id}.html`
  
    // Trigger click
    downloader.click()
  
    // Clean up
    URL.revokeObjectURL(url)
  }
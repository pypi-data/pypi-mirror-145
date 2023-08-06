function wordfreqChart(canvasID, labels, data) {
    var ctx = document.getElementById(canvasID).getContext('2d');
    var chart_object = new Chart(ctx, {
        type: 'line', options: {},
        data: {
            labels: labels, datasets: [{label: 'Natural Log Word Frequency', data: data, borderWidth: 1}]
        },
    });
    return chart_object;
}

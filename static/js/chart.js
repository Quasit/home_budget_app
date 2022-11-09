function buildChart(canvas, labels, dataset, colors) {
    new Chart(
        document.getElementById(canvas),
        config = {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Podział wydatków na kategorie',
                    data: dataset,
                    backgroundColor: colors,
                    hoverOffset: 20
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        }
    )
};
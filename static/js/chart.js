const data = {
    labels: [
        'Kategoria 1',
        'Kategoria 2',
        'Kategoria 3',
        'Kategoria 4',
        'Kategoria 5',
        'Kategoria 6',
        'Kategoria 7',
        'Kategoria 8',
        'Kategoria 9',
        'Kategoria 10',
        'Kategoria 11',
        'Kategoria 12',
        'Kategoria 13',
        'Kategoria 14',
        'Kategoria 15'
    ],
    datasets: [{
        label: 'Podział wydatków na kategorie',
        data: [1000, 200, 600, 500, 1100, 200, 400, 800, 200, 600, 500, 900, 300, 600, 700],
        backgroundColor: [
            'rgb(72, 131, 33)',
            'rgb(230, 58, 0)',
            'rgb(242, 178, 2)',
            'rgb(150, 73, 203)',
            'rgb(24, 143, 167)',
            'rgb(92, 39, 81)',
            'rgb(71, 70, 71)',
            'rgb(151, 204, 4)',
            'rgb(4, 150, 255)',
            'rgb(57, 47, 90)',
            'rgb(165, 36, 61)',
            'rgb(255, 201, 113)',
            'rgb(109, 211, 206)',
            'rgb(42, 127, 98)',
            'rgb(105, 220, 158)'
            
        ],
        hoverOffset: 20
    }]
};

const config = {
    type: 'pie',
    data: data,
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
};

function buildChart(canvas) {
    new Chart(
        document.getElementById(canvas),
        config
    )
};
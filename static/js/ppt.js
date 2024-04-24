CKEDITOR.inline( '.editor' );

  function cloneDiv(wrapperId) {
    // Clone the wrapper
    var originalWrapper = document.getElementById(wrapperId);
    var clonedWrapper = originalWrapper.cloneNode(true);



    // Append the cloned wrapper after the original wrapper
    originalWrapper.parentNode.insertBefore(clonedWrapper, originalWrapper.nextSibling);
  }
        const ctx = document.getElementById('myChart').getContext('2d');
        let myChart;

        const dataPoints = [{
                label: "Brand7",
                y: 2
            },
            {
                label: "Brand6",
                y: 9
            },
            {
                label: "Brand5",
                y: 12
            },
            {
                label: "Brand4",
                y: 16
            },
            {
                label: "Brand3",
                y: 18
            },
            {
                label: "Brand2",
                y: 21
            },
            {
                label: "Brand1",
                y: 24
            }
        ];

        const chartData = {
            labels: dataPoints.map(point => point.label),
            datasets: [{
                label: 'Data Points',
                data: dataPoints.map(point => point.y),
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        };

        myChart = new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: {
                indexAxis: 'y',
                scales: {
                    x: {
                        beginAtZero: true
                    }
                }
            }
        });

        const handleClick = (evt) => {
            const activePoint = myChart.getElementsAtEventForMode(evt, 'nearest', { intersect: true }, true)[0];
            if (activePoint) {
                const index = activePoint.index;
                const newValue = prompt('Enter new value:', dataPoints[index].y);
                if (newValue !== null) {
                    dataPoints[index].y = parseInt(newValue, 10);
                    myChart.data.datasets[0].data[index] = parseInt(newValue, 10);
                    myChart.update();
                }
            }
        };

        myChart.options.onClick = handleClick;

        const ctx2 = document.getElementById('myChart2').getContext('2d');
        let myChart2;

        const primaryData = [{
            label: "FY 22-23",
            y: 20
        }, {
            label: "YTD 22-23",
            y: 30
        }, {
            label: "OB/RF",
            y: 40
        }, {
            label: "Prev QTR",
            y: 40
        }, {
            label: "Sales Plan",
            y: 50
        }, {
            label: "Achievement",
            y: 50
        }, {
            label: "YTD 23-24",
            y: 50
        }];

        const secondaryData = [{
            label: "FY 22-23",
            y: 22
        }, {
            label: "YTD 22-23",
            y: 35
        }, {
            label: "OB/RF",
            y: 45
        }, {
            label: "Prev QTR",
            y: 47
        }, {
            label: "Sales Plan",
            y: 60
        }, {
            label: "Achievement",
            y: 60
        }, {
            label: "YTD 23-24",
            y: 60
        }];

        const chartData2 = {
            labels: primaryData.map(point => point.label),
            datasets: [{
                label: 'Primary Data',
                data: primaryData.map(point => point.y),
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1,
                yAxisID: 'primary-y-axis'
            }, {
                label: 'Secondary Data',
                data: secondaryData.map(point => point.y),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                yAxisID: 'secondary-y-axis'
            }]
        };

        myChart2 = new Chart(ctx2, {
            type: 'bar',
            data: chartData2,
            options: {
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        id: 'primary-y-axis',
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(255, 99, 132, 0.2)'
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        id: 'secondary-y-axis',
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(75, 192, 192, 0.2)'
                        }
                    }
                }
            }
        });

        const handleClick2 = (evt) => {
            const activePoint = myChart2.getElementsAtEventForMode(evt, 'nearest', { intersect: true }, true)[0];
            if (activePoint) {
                const index = activePoint.index;
                const datasetIndex = activePoint.datasetIndex;
                const newValue = prompt('Enter new value:', datasetIndex === 0 ? primaryData[index].y : secondaryData[index].y);
                if (newValue !== null) {
                    if (datasetIndex === 0) {
                        primaryData[index].y = parseInt(newValue, 10);
                        myChart2.data.datasets[0].data[index] = parseInt(newValue, 10);
                    } else {
                        secondaryData[index].y = parseInt(newValue, 10);
                        myChart2.data.datasets[1].data[index] = parseInt(newValue, 10);
                    }
                    myChart2.update();
                }
            }
        };

        myChart2.options.onClick = handleClick2;

                // Third Chart
        const ctx3 = document.getElementById('myChart3').getContext('2d');
        let myChart3;

        const dataPoints3 = [{
            y: 25
        }, {
            y: 26
        }, {
            y: 20
        }, {
            y: 30
        }];

        const chartData3 = {
            labels: dataPoints3.map((point, index) => `WEEK ${index + 1}`),
            datasets: [{
                label: 'Data Points',
                data: dataPoints3.map(point => point.y),
                backgroundColor: 'rgba(255, 206, 86, 0.2)',
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 1
            }]
        };

        myChart3 = new Chart(ctx3, {
            type: 'bar',
            data: chartData3,
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        const handleClick3 = (evt) => {
            const activePoint = myChart3.getElementsAtEventForMode(evt, 'nearest', { intersect: true }, true)[0];
            if (activePoint) {
                const index = activePoint.index;
                const newValue = prompt('Enter new value:', dataPoints3[index].y);
                if (newValue !== null) {
                    dataPoints3[index].y = parseInt(newValue, 10);
                    myChart3.data.datasets[0].data[index] = parseInt(newValue, 10);
                    myChart3.update();
                }
            }
        };

        myChart3.options.onClick = handleClick3;
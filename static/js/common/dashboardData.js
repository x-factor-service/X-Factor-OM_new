var randomNo = function () {
    return Math.floor(Math.random() * 60) + 30
};

var handleRenderChartNCOMG = function () {
    // global apexchart settings
    Apex = {
        title: {
          style: {
            fontSize: "12px",
            fontWeight: "bold",
            fontFamily: app.font.family,
            color: app.color.white,
          },
        },
        legend: {
          fontFamily: app.font.family,
          labels: {
            colors: "#fff",
            show: true,
          },
        },
        tooltip: {
          style: {
            fontSize: "10px",
            fontFamily: app.font.family,
          },
        },
        grid: {
          borderColor: "rgba(" + app.color.whiteRgb + ", .25)",
        },
        dataLabels: {
          style: {
            fontSize: "12px",
            fontFamily: app.font.family,
            fontWeight: "bold",
            colors: undefined,
          },
        },
        xaxis: {
          axisBorder: {
            show: false,
            color: "rgba(" + app.color.whiteRgb + ", .25)",
            height: 1,
            width: "100%",
            offsetX: 0,
            offsetY: -1,
          },
          axisTicks: {
            show: false,
            borderType: "solid",
            color: "rgba(" + app.color.whiteRgb + ", .25)",
            height: 6,
            offsetX: 0,
            offsetY: 0,
          },
          labels: {
            style: {
              colors: "#fff",
              fontSize: "9px",
              fontFamily: app.font.family,
              fontWeight: 400,
              cssClass: "apexcharts-xaxis-label",
            },
          },
        },
        yaxis: {
          labels: {
            style: {
              colors: "#fff",
              fontSize: "9px",
              fontFamily: app.font.family,
              fontWeight: 400,
              cssClass: "apexcharts-xaxis-label",
            },
          },
        },
    };

    //--------------------------------------------------------------------------
    // 자산 관리 현황 미니도넛, 프로그레스 바 - DISK 사용률 초과 서버, MEMORY 사용률 초과 서버
    //--------------------------------------------------------------------------

    var disk_widthPercentage = (dataList.disk_donutData / dataList.allOnline_donutData) * 100;
    document.querySelector("#disk-bar").style.width = disk_widthPercentage + "%";
    var mem_widthPercentage = (dataList.memory_donutData / dataList.allOnline_donutData) * 100;
    document.querySelector("#mem-bar").style.width = mem_widthPercentage + "%";
    var cpu_widthPercentage = (dataList.cpu_donutData / dataList.allOnline_donutData) * 100;
    document.querySelector("#cpu-bar").style.width = cpu_widthPercentage + "%";
    var om_disk_chartOptions = {
        series: [20, 20, 20, 20, 20],
        chart: {
          width: 100,
          height: 100,
          type: 'donut',
          toolbar: {
            show: false
          }
        },
        colors: ['rgba(223, 224, 223, .2)', 'rgba(223, 224, 223, .4)', 'rgba(223, 224, 223, .5)', 'rgba(223, 224, 223, .8)', 'rgba(223, 224, 223, 1)'],
        plotOptions: {
          pie: {
            donut: {
              labels: {
                show: false
              }
            }
          }
        },
        dataLabels: {
          enabled: false
        },
        legend: {
          show: false
        },
        stroke: {
          show: false
        },
        tooltip: {
          enabled: false
        }
    };
    var chartContainers = document.querySelectorAll('.om_disk_chart');
    chartContainers.forEach(function(container) {
        var chart = new ApexCharts(container, om_disk_chartOptions);
        chart.render();
    });
    //--------------------------------------------------------------------------
    // os 설치 현황, 유/무선 연결 현황, 물리/가상 자산 현황
    //--------------------------------------------------------------------------
    var os_pieDataItem = []
    var os_pieDataCount = []
    for (var i = 0; i < dataList.os_pieData.length; i++) {
        os_pieDataItem.push(dataList.os_pieData[i]['item']);
        os_pieDataCount.push(dataList.os_pieData[i]['count']);
    };

    var wire_pieDataItem = []
    var wire_pieDataCount = []
    for (var i = 0; i < dataList.wire_pieData.length; i++) {
        wire_pieDataItem.push(dataList.wire_pieData[i]['item']);
        wire_pieDataCount.push(dataList.wire_pieData[i]['count']);
    };

    var virtual_pieDataItem = []
    var virtual_pieDataCount = []
    for (var i = 0; i < dataList.virtual_pieData.length; i++) {
        virtual_pieDataItem.push(dataList.virtual_pieData[i]['item']);
        virtual_pieDataCount.push(dataList.virtual_pieData[i]['count']);
    };

    function createDonutChart(divId, seriesData, labelsData) {
        var donutOptions = {
            series: seriesData,
            chart: {
                type: 'donut',
                width: '100%',
                height: 220
            },
            colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', '#46537B', '#2F4858'],
            labels: labelsData,
            dataLabels: {
                enabled: true,
                style: {
                    colors: ["rgba(" + app.color.whiteRgb + ", 1)"],
                    fontWeight: '300'
                },
                formatter(val, opts) {
                    const name = opts.w.globals.labels[opts.seriesIndex];
                    return [name + ' ' + val.toFixed(1) + '%'];
                }
            },
            stroke: {
                width: 0
            },
            fill: {
                type: 'gradient'
            },
            legend: {
                position: 'bottom',
                formatter: function(val, opts) {
                    const seriesValue = opts.w.globals.series[opts.seriesIndex];
                    return val + ": " + seriesValue + "대";
                }
            }
        };
        var donut_chart = new ApexCharts(document.querySelector("#" + divId), donutOptions);
        donut_chart.render();
    }

    createDonutChart("os_donut", os_pieDataCount, os_pieDataItem);
    createDonutChart("wire_donut", wire_pieDataCount, wire_pieDataItem);
    createDonutChart("vp_donut", virtual_pieDataCount, virtual_pieDataItem);

    //--------------------------------------------------------------------------
    // 자산 관리 현황 관리 자산, 미관리 자산, 예상 유휴 자산 라인차트
    //--------------------------------------------------------------------------
    var asset_counts = dataList.allAsset_lineData.map(function(item) {
        return {x: item.item, y: item.count};
    });
    var discover_counts = dataList.discover_lineData.map(function(item) {
        return {x: item.item, y: item.count};
    });
    var idle_counts = dataList.idle_lineData.map(function(item) {
        return {x: item.item, y: item.count};
    });

    var asset_overview_chart_options = {
      series: [
        {
          name: '관리 자산',
          data: asset_counts
        },
        {
          name: '미관리 자산',
          data: discover_counts
        },
        {
          name: '예상 유휴 자산',
          data: idle_counts
        }
      ],
      chart: {
        type: 'line',
        background: 'transparent',
        foreColor: 'rgba(255, 255, 255, 0.75)',
        height: 200,
        width: '100%',
        toolbar: {
            show: true,
            tools: {
                zoom: false,
                pan: false
            }
        }
      },
      stroke: {
        width: 3
      },
      grid: {
        borderColor: 'rgba(144, 164, 174, 0.5)'
      },
      colors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', ],
      dataLabels: {
        enabled: true,
        background: {
            enabled: true,
            foreColor: 'rgba(29, 40, 53, 0.95)'
        },
        dropShadow: {
            enabled: false,
        },
        style: {
            fontSize: '9px',
        }
      },
      xaxis: {
        type: 'category',
        categories: dataList.allAsset_lineData.map(function(item) {
            return item.item;
        })
      },
      yaxis: {
        title: {
          text: 'Count'
        }
      },
      legend: {
        markers: {
          fillColors: ['#009D83', 'rgba(' + app.color.themeRgb + ', 1)', '#B8A89A', ]
        },
        itemMargin: {
          horizontal: 20
        },
        labels: {
          colors: 'rgba(255, 255, 255, 0.75)',
        },
        position: 'top'
      }
    };

    var asset_overview_chart = new ApexCharts(document.querySelector('#asset_overview_chart'), asset_overview_chart_options);
    asset_overview_chart.render();
};

$(document).ready(function () {
    handleRenderChartNCOMG();
});






//SBOM 페이지
var sbom_all = '../sbom_detail/?cpe='
var colors = ['#0079BF', '#0088A8', '#00867A', '#5BC160', '#DAD056'];
//CVE가 탐지된 SBOM 테이블
var cveInSbomTable = function () {
    var dashboardpopupTable = $('#cveInSbom_dataTable').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center mb-6 d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
        pageLength: 20,
        responsive: true,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [[6, "desc"]],
        ajax: {
            url: 'paging_cis/',
            type: "POST",
            dataSrc: function (res) {
                var data = res.data.item;
                return data;
            }
        },
        createdRow: function (row, data, dataIndex) {
            if (data.score) {
                if (data.score.includes('Critical')) {
                    $('td:eq(4)', row).css({
                        'background-color': 'rgba(255, 0, 0, 0.5)',
                    });
                } else if (data.score.includes('High')) {
                    $('td:eq(4)', row).css({
                        'background-color': 'rgba(255, 165, 0, 0.5)',
                    });
                } else if (data.score.includes('Medium')) {
                    $('td:eq(4)', row).css({
                        'background-color': 'rgba(255, 255, 0, 0.5)',
                    });
                } else if (data.score.includes('Low')) {
                    $('td:eq(4)', row).css({
                        'background-color': 'rgba(0, 128, 0, 0.5)',
                    });
                }
            }
        },
        columns: [
            {data: 'index'},
            {data: 'comp_name'},
            {data: 'comp_ver'},
            {data: 'cve_id'},
            {data: 'score'},
            {data: 'detect_time'},
            {data: 'detect_count'}
        ],
        columnDefs: [
            {targets: 0, width: '5%', className: 'text-center', orderable: false},
            {targets: 1, width: '31%', render: function (data, type, row) {
                return '<div class="text-center text-truncate text-teal sbom-cursor fs-12px fw-bold" title="' + row.comp_name + '" data-toggle="tooltip">' + data + '</div>'
            }},
            {targets: 2, width: '16%', render: function (data, type, row) {
                if (data === null) {
                    data = '';
                }
                return '<div class="text-center text-truncate text-teal sbom-cursor fs-12px fw-bold" title="' + row.comp_ver + '" data-toggle="tooltip">' + data + '</div>'
            }},
            {targets: 3, width: '21%', render: function (data, type, row) {
                return '<div class="text-center text-truncate sbom-cursor fs-12px" title="' + row.cve_id + '" data-toggle="tooltip">' + data + '</div>'
            }},
            {targets: 4, width: '11%', render: function (data, type, row) {
                return '<div class="text-center text-truncate sbom-cursor fs-12px" title="' + row.score + '" data-toggle="tooltip">' + data + '</div>'
            }},
            {targets: 5, width: '10%', render: function (data, type, row) {
                return '<div class="text-center text-truncate sbom-cursor fs-12px" title="' + row.detect_time + '" data-toggle="tooltip">' + data + '</div>'
            }},
            {targets: 6, width: '6%', render: function (data, type, row) {
                return '<div class="text-center text-truncate sbom-cursor fs-12px" title="' + row.detect_count + '" data-toggle="tooltip">' + data + '</div>'
            }}
        ],
        language: {
            "decimal": "",
            "info": "전체 _TOTAL_건",
            "infoEmpty": "데이터가 없습니다.",
            "emptyTable": "데이터가 없습니다.",
            "thousands": ",",
            "lengthMenu": "페이지당 _MENU_ 개씩 보기",
            "loadingRecords": "로딩 중입니다.",
            "processing": "",
            "zeroRecords": "검색 결과 없음",
            "paginate": {
                "first": "처음",
                "last": "끝",
                "next": "다음",
                "previous": "이전"
            },
            "search": "검색:",
            "infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
            "infoPostFix": "",
        },
        pagingType: 'numbers',
        rowCallback: function(row, data) {
            $(row).on('click', function() {
                window.location.href = 'cve_detail?cve_id=' + data.cve_id + '&comp_name=' + data.comp_name + '&comp_ver=' + data.comp_ver;
            });
        },
        drawCallback: function () {
            var current_page = dashboardpopupTable.page;
            var total_pages = dashboardpopupTable.page.info().pages;
            $('#cve_nexts').remove();
            $('#cve_after').remove();

            if (total_pages > 10) {
                $('<button type="button" class="btn" id="cveInSbom_nexts">≫</button>')
                    .insertAfter('#cveInSbom_dataTable_paginate .paginate_button:last');
                $('<button type="button" class="btn" id="cveInSbom_after">≪</button>')
                    .insertBefore('#cveInSbom_dataTable_paginate .paginate_button:first');
            };
        }
    });

    $(document).on('click', '#cveInSbom_nexts, #cveInSbom_after', function() {
        var current_page = dashboardpopupTable.page();
        var total_pages = dashboardpopupTable.page.info().pages;
        if ($(this).attr('id') == 'cveInSbom_nexts') {
                if (current_page + 10 < total_pages) {
                    dashboardpopupTable.page(current_page + 10).draw('page');
                } else {
                    dashboardpopupTable.page(total_pages - 1).draw('page');
                }
                } else {
                    dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
                }
    });
    $(document).ready(function() {
    var customStyle = '<style>#cveInSbom_nexts, #cveInSbom_after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
    });
};

//sbom detail table : 자산 목록 테이블
var urlParams = new URLSearchParams(window.location.search);

var cve_id = urlParams.get('cve_id');
var comp_name = urlParams.get('comp_name');
var comp_ver = urlParams.get('comp_ver');

var sbomDetail_datatable = function () {
	var dashboardpopupTable = $('#sbom_detail_dataTable').DataTable({
		dom: "<'row mb-3'<'col-md-4 mb-3 mb-md-0'l><'col-md-8 text-right'<'d-flex justify-content-end'fB>>>t<'row align-items-center'<'mr-auto col-md-6 mb-3 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
		lengthMenu: [15, 20, 30, 40, 50],
		responsive: true,
		searching: true,
		ordering: true,
		serverSide: true,
		displayLength: false,
		autoWidth: false,
		order: [
		    [1, "asc"]
		],
		ajax: {
            url: window.location.pathname,
            type: "POST",
            data: {
                cve_id: cve_id,
                comp_name: comp_name,
                comp_ver: comp_ver
            },
            dataSrc: function (res) {
                var data = res.data.assetItem;
                return data;
            }
        },
        columns: [
            {data: 'index'},
            {data: 'computer_name'},
            {data: 'ipv4_address'},
            {data: 'name'},
            {data: 'version'},
            {data: 'path'},
            {data: 'type'}
        ],
		columnDefs: [
		    {targets: 0, width: '5%', className: 'text-center'},
		    {targets: 1, width: '10%', className: 'text-center', render: function (data, type, row) {
                return '<div class="text-center text-truncate text-teal fs-12px fw-bold" title="' + row.computer_name + '" data-toggle="tooltip">' + data + '</div>'}},
		    {targets: 2, width: '7%', className: 'text-center', render: function (data, type, row) {
                return '<div class="text-center text-truncate text-teal fs-12px fw-bold" title="' + row.ipv4_address + '" data-toggle="tooltip">' + data + '</div>'}},
		    {targets: 3, width: '9%', className: 'text-center', render: function (data, type, row) {
                return '<div class="text-center text-truncate text-teal fs-12px fw-bold" title="' + row.name + '" data-toggle="tooltip">' + data + '</div>'}},
		    {targets: 4, width: '9%', className: 'text-center', render: function (data, type, row) {
                return '<div class="text-center text-truncate text-teal fs-12px fw-bold" title="' + row.version + '" data-toggle="tooltip">' + data + '</div>'}},
		    {targets: 5, width: '52%', className: 'text-center', render: function (data, type, row) {
                return '<div class="text-center text-truncate text-teal fs-12px fw-bold" title="' + row.path + '" data-toggle="tooltip">' + data + '</div>'}},
		    {targets: 6, width: '8%', className: 'text-center', render: function (data, type, row) {
                return '<div class="text-center text-truncate text-teal fs-12px fw-bold" title="' + row.type + '" data-toggle="tooltip">' + data + '</div>'}}
		],
		language: {
			"decimal": "",
			"info": "전체 _TOTAL_건",
			"infoEmpty": "데이터가 없습니다.",
			"emptyTable": "데이터가 없습니다.",
			"thousands": ",",
			"lengthMenu": "페이지당 _MENU_ 개씩 보기",
			"loadingRecords": "로딩 중입니다.",
			"processing": "",
			"zeroRecords": "검색 결과 없음",
			"paginate": {
				"first": "처음",
				"last": "끝",
				"next": "다음",
				"previous": "이전"
			},
			"search": "검색:",
			"infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
			"infoPostFix": "",
		},
	});
};

//SBOM 목록 전체 테이블
var sbom_dataTable = function () {
    var dashboardpopupTable = $('#sbom_dataTable').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
        pageLength: 20,
        responsive: true,
        searching: true,
        ordering: true,
        serverSide: true,
        autoWidth: false,
        displayLength: false,
        order: [
            [ 5, "desc"],
            [ 1, "desc"]
        ],
        ajax: {
            url: 'paging/',
            type: "POST",
            dataSrc: function (res) {
                var data = res.data.item;
                return data;
            }
        },
        columns: [
            {data: 'index'},
            {data: 'name'},
            {data: 'version'},
            {data: 'path'},
            {data: 'type'},
            {data: 'count'}
        ],
        columnDefs: [
            {targets: 0, width: '5%', className: 'text-center', orderable: false},
            {targets: 1, width: '15%', className: '', render: function (data, type, row) {
                return '<div class="text-start text-truncate text-teal fs-12px fw-bold" title="' + row.name + '" data-toggle="tooltip" onclick="openPopupWindow(\''+sbom_all+row.cpe+'\', 1500, 600)">' + data + '<input type="hidden" name="cpe" value=row.cpe></a></span>'
            }},
            {targets: 2, width: '10%', className: '', render: function (data, type, row) {
                return '<div class="text-center text-truncate fs-12px" title="' + row.version + '" data-toggle="tooltip">' + data + '</span>'
            }},
            {targets: 3, width: '55%', className: '', render: function (data, type, row) {
                return '<div class="text-start text-truncate fs-12px" title="' + row.path + '" data-toggle="tooltip">' + data + '</span>'
            }},
            {targets: 4, width: '10%', className: '', render: function (data, type, row) {
                return '<div class="text-center text-truncate fs-12px" title="' + row.type + '" data-toggle="tooltip">' + data + '</span>'
            }},
            {targets: 5, width: '5%', className: 'text-center text-truncate fs-12px'},
        ],
        language: {
            "decimal": "",
            "info": "전체 _TOTAL_건",
            "infoEmpty": "데이터가 없습니다.",
            "emptyTable": "데이터가 없습니다.",
            "thousands": ",",
            "lengthMenu": "페이지당 _MENU_ 개씩 보기",
            "loadingRecords": "로딩 중입니다.",
            "processing": "",
            "zeroRecords": "검색 결과 없음",
            "paginate": {
                "first": "처음",
                "last": "끝",
                "next": "다음",
                "previous": "이전"
            },
            "search": "검색:",
            "infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
            "infoPostFix": "",
        },
        pagingType: 'numbers',

        drawCallback: function () {
            var current_page = dashboardpopupTable.page;
            var total_pages = dashboardpopupTable.page.info().pages;
            $('#sbom_nexts').remove();
            $('#sbom_after').remove();

            if (total_pages > 10) {
                $('<button type="button" class="btn" id="sbom_nexts">≫</button>')
                    .insertAfter('#sbom_dataTable_paginate .paginate_button:last');
                $('<button type="button" class="btn" id="sbom_after">≪</button>')
                    .insertBefore('#sbom_dataTable_paginate .paginate_button:first');
            }
        }
    });

    $(document).on('click', '#sbom_nexts, #sbom_after', function() {
        var current_page = dashboardpopupTable.page();
        var total_pages = dashboardpopupTable.page.info().pages;
        if ($(this).attr('id') == 'sbom_nexts') {
                if (current_page + 10 < total_pages) {
                    dashboardpopupTable.page(current_page + 10).draw('page');
                } else {
                    dashboardpopupTable.page(total_pages - 1).draw('page');
                }
                } else {
                    dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
                }
    });
    $(document).ready(function() {
    var customStyle = '<style>#sbom_nexts, #sbom_after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
    });
};

//SBOM 페이지 차트
var handleRenderChartSBOM = function () {
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

    // 가장 많이 탐지된 취약 오픈소스 (상위 5개)
        // 데이터가 비어 있는 경우 기본값 설정
    if (Array.isArray(sbomDataList.sbom_pieData) && sbomDataList.sbom_pieData.length === 0) {
        sbomDataList.sbom_pieData = [{ count: 0, comp_name: '-', comp_ver: '-' }];
    }

    var sbom_pieDataCount = sbomDataList.sbom_pieData.map(item => parseInt(item.count));
    var sbom_pieDataLabels = sbomDataList.sbom_pieData.map(item => `${item.comp_name} ${item.comp_ver}`);

    var createPieChart = {
        series: sbom_pieDataCount,
        chart: {
            type: 'pie',
            height: 180,
            events: {
                mounted: (chart) => {
                    chart.windowResizeHandler();
                },
            },
        },
        stroke: {
            width: 0
        },
        labels: sbom_pieDataLabels,
        tooltip: {
            y: {
                title: {
                    formatter: function() {
                        return ''; // 이 부분을 추가하여 기본 라벨명 표시를 비활성화합니다.
                    }
                },
                formatter: function(val, opts) {
                    const dataPoint = sbomDataList.sbom_pieData[opts.dataPointIndex];

                    return [
                        `name : ${dataPoint.comp_name}`,
                        `ver: ${dataPoint.comp_ver}`,
                        `count: ${val}`
                    ].join('<br/>');
                }
            }
        },
        dataLabels: {
            enabled: true,
            style: {
                colors: ["rgba(" + app.color.whiteRgb + ", 1)"],
                fontWeight: '300'
            },
            formatter(val) {
                return val.toFixed(1) + '%';
            }
        },
        colors: colors,
        fill: {
            type: 'gradient'
        },
        legend: {
            formatter: function(val, opts) {
                if (val.length > 20) {
                val = val.substring(0, 17) + "...";
                }
                return val + " : " + opts.w.globals.series[opts.seriesIndex] + "개";
            }
        }
    };

    var sbom_pie_chart = new ApexCharts(document.querySelector("#sbom_pie"), createPieChart);
    sbom_pie_chart.render();

    setTimeout(function() {
        var legends = document.querySelectorAll('#sbom_pie .apexcharts-legend-text');
        legends.forEach((legend, index) => {
            var originalLabel = sbom_pie_chart.w.globals.labels[index];
            legend.setAttribute('title', originalLabel);
        });
    }, 1000);


// sbom line chart
    var categories_date = sbomDataList.sbom_lineData.map(item => item.date);
    var linecount = sbomDataList.sbom_lineData.map(item => parseInt(item.count, 10));
    var sbomLineChart = {
      chart: {
        type: 'line',
        height: 200,
        events: {
            mounted: (chart) => {
            chart.windowResizeHandler();
            },
        },
        zoom: {
          enabled: false
        },
        toolbar: {
          show: false
        },
        animations: {
          enabled: true,
          easing: 'easeinout',
          speed: 800,
          animateGradually: {
            enabled: true,
            delay: 150
          },
          dynamicAnimation: {
            enabled: true,
            speed: 350
          }
        }
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        curve: 'smooth',
        width: 2.5
      },
      series: [{
        name: '자산 수',
        data: linecount  // 여기에 실제 데이터를 넣으세요!
      }],
      xaxis: {
        categories: categories_date,  // 여기에 실제 날짜를 넣으세요!
        labels: {
          style: {
            colors: "rgba(" + app.color.whiteRgb + ", 1)",
            fontWeight: '300'
          }
        },
        axisBorder: {
          show: false
        },
        axisTicks: {
          show: false
        }
      },
      yaxis: {
        labels: {
          style: {
            colors: '#8e8da4'
          }
        }
      },
      colors: ['#ADFF2F'],
      fill: {
        type: 'gradient',
        gradient: {
          opacityFrom: 0.7,
          opacityTo: 0.9,
          stops: [0, 100]
        }
      },
      markers: {
        size: 4,
        colors: ['#FFA41B'],
        strokeColors: '#fff',
        strokeWidth: 2,
        hover: {
          size: 7,
        }
      },
      tooltip: {
        theme: 'dark',
        marker: {
          show: true,
        },
        x: {
          show: true
        },
        y: {
          title: {
            formatter: function(val) {
              return val
            }
          }
        }
      },
      grid: {
        borderColor: 'rgba(144, 164, 174, 0.5)'
      }
    }

    var sbom_line_chart = new ApexCharts(
      document.querySelector("#sbom_line"),
      sbomLineChart
    );

    sbom_line_chart.render();

// bar chart
    var categories_ip = sbomDataList.sbom_barData.map(item => item.ip);
    var countData = sbomDataList.sbom_barData.map(item => parseInt(item.count, 10));
    var sbomBarChart = {
              series: [{
              data: countData
            }],
              chart: {
              type: 'bar',
              height: 210
            },
            plotOptions: {
              bar: {
                borderRadius: 4,
                horizontal: true,
                distributed: true
              }
            },
            dataLabels: {
              enabled: false
            },
            xaxis: {
              categories: categories_ip,
              labels: {
                formatter: function(value) {
                    return Math.round(value); // 소수점을 반올림하여 제거
                }
              }
            },
            colors: colors,
            fill: {
                type: 'gradient'
            },
            tooltip: {
                custom: function({ series, seriesIndex, dataPointIndex, w }) {
                    var bgColor = colors[dataPointIndex];
                    return '<div style="padding: 7px 15px; background-color: ' + bgColor + '; color: #000; font-weight: bold; font-size: 11px;">' +
                           '취약 오픈소스 개수: ' + series[seriesIndex][dataPointIndex] +
                           '</div>';
                }
            },
            legend: {
                show: false
            }
        };

    var sbomBarChart = new ApexCharts(document.querySelector("#sbomBarChart"), sbomBarChart);
    sbomBarChart.render();
    setTimeout(function() {
        sbomBarChart.update();
    }, 200);
};

function adjustWidth() {
    const cveNavItem = document.querySelector('.cveList');
    const sbomNavItem = document.querySelector('.sbomList');
    const chartContainer = document.querySelector('.col-xl-3');
    const tableContainer = document.querySelector('.col-xl-9');

    sbomNavItem.addEventListener('click', function() {
        chartContainer.style.display = 'none';
        tableContainer.classList.remove('col-xl-9');
        tableContainer.classList.add('col-xl-12');
    });

    cveNavItem.addEventListener('click', function() {
        chartContainer.style.display = 'block';
        tableContainer.classList.remove('col-xl-12');
        tableContainer.classList.add('col-xl-9');
    });
}


$(document).ready(function () {
    cveInSbomTable();
    sbom_dataTable();
    sbomDetail_datatable();
    handleRenderChartSBOM();
    adjustWidth();

});

document.getElementById("backButton").addEventListener("click", function() {
  history.back();
});




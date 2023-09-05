//SBOM 페이지
var aa = '../sbom_detail/?cpe='
var sbom_dataTable = function () {
    var dashboardpopupTable = $('#sbom_dataTable').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
        lengthMenu: [[20, 50, 100, 200], [20, 50, 100, 200]],
        responsive: true,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [
            [ 5, "desc"],
            [ 1, "asc"]
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
            {data: 'index', width: "5%"},
            {data: 'name', width: "20%"},
            {data: 'version', width: "10%"},
            {data: 'cpe', width: "45%"},
            {data: 'type', width: "10%"},
            {data: 'count', width: "10%"}
        ],
        columnDefs: [
            {targets: 0, width: "5%", className: 'text-center', orderable: false},
            {
                targets: 1, width: "20%", className: '', render: function (data, type, row) {
                    return '<div style="cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: #b6effb"; title="' + row.name + '" data-toggle="tooltip" onclick="openPopupWindow(\''+aa+row.cpe+'\', 1500, 600)">' + data + '<input type="hidden" name="cpe" value=row.cpe></a></span>'
                }
            },
            {
                targets: 2, width: "10%", className: '', render: function (data, type, row) {
                    return '<div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap"; title="' + row.version + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {targets: 3, width: "45%", style: 'text-center text-truncate', render: function (data, type, row) {
                    return '<div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap"; title="' + row.cpe + '" data-toggle="tooltip">' + data + '</span>'
                }},
            {targets: 4, width: "10%", style: 'text-center text-truncate', render: function (data, type, row) {
                    return '<div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap"; title="' + row.type + '" data-toggle="tooltip">' + data + '</span>'
                }},
            {targets: 5, width: "10%", className: 'text-center'},
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

function openPopupWindow(url, width, height){
    var left = (screen.width - width) /2;
    var top = (screen.height - height) /2;
    var windowFeatures = 'width=' + width + ',height=' + height + ', left=' + left + ', top'
    window.open(url, '_blank',windowFeatures)
    return false;
}

var sbom_cveTable = function () {
    var dashboardpopupTable = $('#sbom_cveTable').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
        lengthMenu: [[20, 50, 100, 200], [20, 50, 100, 200]],
        responsive: true,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [[ 6, "desc" ]],
        ajax: {
            url: 'paging_cve/',
            type: "POST",
            dataSrc: function (res) {
                var data = res.data.item;
                return data;
            }
        },
        columns: [
            {data: 'index', width: "6%"},
            {data: 'comp_name', width: "29%"},
            {data: 'comp_ver', width: "15%"},
            {data: 'cve_id', width: "20%"},
            {data: 'score', width: "15%"},
            {data: 'vuln_last_reported', width: "15%"},
            {data: 'number', visible: false}
        ],
        columnDefs: [
            {targets: 0, width: "6%", className: 'text-center', orderable: false},
            {
                targets: 1,
                width: "29%",
                render: function (data, type, row) {
                    return '<div class="click_search" style="cursor: pointer; color: #D3FFBF; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + row.comp_name + '" data-toggle="tooltip">' + data + '</div>'
                }
            },
            {
                targets: 2,
                width: "15%",
                render: function (data, type, row) {
                    if (data === null) {
                        data = '';
                    }
                    return '<div class="click_search" style="cursor: pointer; color: #D3FFBF; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + row.comp_ver + '" data-toggle="tooltip">' + data + '</div>'
                }
            },
            {
                targets: 3,
                width: "20%",
                render: function (data, type, row) {
                    return '<div style="cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + row.cve_id + '" data-toggle="tooltip">' + data + '</div>'
                }
            },
            {
                targets: 4,
                width: "15%",
                render: function (data, type, row) {
                    return '<div style="cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + row.score + '" data-toggle="tooltip">' + data + '</div>'
                }
            },
            {
                targets: 5,
                width: "15%",
                render: function (data, type, row) {
                    return '<div style="cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + row.vuln_last_reported + '" data-toggle="tooltip">' + data + '</div>'
                }
            },
            {
                targets: 6,
                render: function (data, type, row) {
                    return '<div style="cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + row.number + '" data-toggle="tooltip">' + data + '</div>'
                }
            }
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
            $('#cve_nexts').remove();
            $('#cve_after').remove();

            if (total_pages > 10) {
                $('<button type="button" class="btn" id="cve_nexts">≫</button>')
                    .insertAfter('#sbom_dataTable_paginate .paginate_button:last');
                $('<button type="button" class="btn" id="cve_after">≪</button>')
                    .insertBefore('#sbom_dataTable_paginate .paginate_button:first');
            };

            $('#sbom_cveTable tbody').off('click', 'tr').on('click', 'tr', function () {
                var data = dashboardpopupTable.row(this).data();
                var cveId = data.solution;
                var accordionExists = $(this).next('.accordion-row').length > 0;
                if (accordionExists) {
                    $(this).next('.accordion-row').remove();
                    return;
                }
                var accordionHTML = `
                <tr class="accordion-row">
                    <td colspan="${dashboardpopupTable.columns().nodes().length}">
                        <div class="accordion" id="accordionExample">
                            <div class="card">
                                <div class="card-body">
                                    <strong>취약점 설명 :</strong> ${data.note}
                                    <hr>
                                    <strong>대응 방안 :</strong> ${data.solution}
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
                `;
                $(this).after(accordionHTML);
            });
        }
    });

    $(document).on('click', '#cve_nexts, #cve_after', function() {
        var current_page = dashboardpopupTable.page();
        var total_pages = dashboardpopupTable.page.info().pages;
        if ($(this).attr('id') == 'cve_nexts') {
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
    var customStyle = '<style>#cve_nexts, #cve_after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
    $('head').append(customStyle);
    });

};

var cveInSbomTable = function () {
    var dashboardpopupTable = $('#cveInSbom_dataTable').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center mb-6 d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
        lengthMenu: [[20, 50, 100, 200], [20, 50, 100, 200]],
        responsive: true,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [[ 6, "desc" ]],
        ajax: {
            url: 'paging_cis/',
            type: "POST",
            dataSrc: function (res) {
                $('#loadingSpinner').hide();
                var data = res.data.item;
                return data;
            },
            beforeSend: function() {
                $('#loadingSpinner').show();
                var loadingTextBase = "Loading";
                var count = 1;
                loadingInterval = setInterval(function() {
                    var dots = new Array(count % 4+1).join(".");
                    $('#loadingText').text(loadingTextBase + dots);
                    count++;
                }, 250);
            },
            error: function() {
                $('#loadingSpinner').hide();
            }
        },
        columns: [
            {data: 'index', width: "6%"},
            {data: 'comp_name', width: "29%"},
            {data: 'comp_ver', width: "15%"},
            {data: 'cve_id', width: "20%"},
            {data: 'score', width: "15%"},
            {data: 'vuln_last_reported', width: "15%"},
            {data: 'number', visible: false}
        ],
        columnDefs: [
            {targets: 0, width: "5%", className: 'text-center', orderable: false},
            {
                targets: 1,
                width: "29%",
                render: function (data, type, row) {
                    return '<div class="click_search text-center" style="cursor: pointer; color: #D3FFBF; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + row.comp_name + '" data-toggle="tooltip">' + data + '</div>'
                }
            },
            {
                targets: 2,
                width: "15%",
                render: function (data, type, row) {
                    if (data === null) {
                        data = '';
                    }
                    return '<div class="click_search text-center" style="cursor: pointer; color: #D3FFBF; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + row.comp_ver + '" data-toggle="tooltip">' + data + '</div>'
                }
            },
            {
                targets: 3,
                width: "20%",
                render: function (data, type, row) {
                    return '<div class="text-center" style="cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + row.cve_id + '" data-toggle="tooltip">' + data + '</div>'
                }
            },
            {
                targets: 4,
                width: "15%",
                render: function (data, type, row) {
                    return '<div class="text-center" style="cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + row.score + '" data-toggle="tooltip">' + data + '</div>'
                }
            },
            {
                targets: 5,
                width: "15%",
                render: function (data, type, row) {
                    return '<div class="text-center" style="cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + row.vuln_last_reported + '" data-toggle="tooltip">' + data + '</div>'
                }
            },
            {
                targets: 6,
                render: function (data, type, row) {
                    return '<div style="cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + row.number + '" data-toggle="tooltip">' + data + '</div>'
                }
            }
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
            $('#cve_nexts').remove();
            $('#cve_after').remove();

            if (total_pages > 10) {
                $('<button type="button" class="btn" id="cveInSbom_nexts">≫</button>')
                    .insertAfter('#cveInSbom_dataTable_paginate .paginate_button:last');
                $('<button type="button" class="btn" id="cveInSbom_after">≪</button>')
                    .insertBefore('#cveInSbom_dataTable_paginate .paginate_button:first');
            };

            $('#cveInSbom_dataTable tbody').off('click', 'tr').on('click', 'tr', function () {
                var data = dashboardpopupTable.row(this).data();
                var cveId = data.solution; // 4번째 컬럼의 데이터
                var accordionExists = $(this).next('.accordion-row').length > 0;
                if (accordionExists) {
                    $(this).next('.accordion-row').remove();
                    return;
                }
                var accordionHTML = `
                <tr class="accordion-row">
                    <td colspan="${dashboardpopupTable.columns().nodes().length}">
                        <div class="accordion" id="accordionExample">
                            <dl class="row m-1 bg-white bg-opacity-25 line-height-2 pt-1">
                                <dt class="col-sm-2 text-danger">취약점 설명</dt>
                                <dd class="col-sm-10">${data.note}</dd>
                                <dt class="col-sm-2 text-danger">대응 방안</dt>
                                <dd class="col-sm-10">${data.solution}</dd>
                            </dl>
                        </div>
                    </td>
                </tr>
                `;
                $(this).after(accordionHTML);
            });
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


var sbomInCveTable = function () {
    var dashboardpopupTable = $('#sbomInCve_dataTable').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
        lengthMenu: [[20, 50, 100, 200], [20, 50, 100, 200]],
        responsive: true,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        order: [
            [ 5, "desc"],
            [ 1, "asc"]
        ],
        ajax: {
            url: 'paging_sic/',
            type: "POST",
            dataSrc: function (res) {
                var data = res.data.item;
                return data;
            }
        },
        columns: [
            {data: 'index', width: "5%"},
            {data: 'name', width: "20%"},
            {data: 'version', width: "10%"},
            {data: 'cpe', width: "45%"},
            {data: 'type', width: "10%"},
            {data: 'count', width: "10%"}
        ],
        columnDefs: [
            {targets: 0, width: "5%", className: 'text-center', orderable: false},
            {
                targets: 1, width: "20%", className: '', render: function (data, type, row) {
                    return '<div style="cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: #b6effb"; title="' + row.name + '" data-toggle="tooltip" onclick="openPopupWindow(\''+aa+row.cpe+'\', 1500, 600)">' + data + '<input type="hidden" name="cpe" value=row.cpe></a></span>'
                }
            },
            {
                targets: 2, width: "10%", className: '', render: function (data, type, row) {
                    return '<div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap"; title="' + row.version + '" data-toggle="tooltip">' + data + '</span>'
                }
            },
            {targets: 3, width: "45%", style: 'text-center text-truncate', render: function (data, type, row) {
                    return '<div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap"; title="' + row.cpe + '" data-toggle="tooltip">' + data + '</span>'
                }},
            {targets: 4, width: "10%", style: 'text-center text-truncate', render: function (data, type, row) {
                    return '<div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap"; title="' + row.type + '" data-toggle="tooltip">' + data + '</span>'
                }},
            {targets: 5, width: "10%", className: 'text-center'},
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

// SBOM 페이지 차트
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

    // 탐지된 취약 오픈소스 Top 5
    if (Array.isArray(sbomDataList.sbom_pieData) && sbomDataList.sbom_pieData.length === 0) {
    sbomDataList.sbom_pieData = [{ count: 0, comp_name: '-', comp_ver: '-' }];}
    var sbom_pieDataCount = sbomDataList.sbom_pieData.map(item => parseInt(item.count));
    var sbom_pieDataItem = sbomDataList.sbom_pieData.map(item => `${item.comp_name} ${item.comp_ver}`);
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
      labels: sbom_pieDataItem,
      dataLabels: {
                enabled: true,
                style: {
                    colors: ["rgba(" + app.color.whiteRgb + ", 1)"],
                    fontWeight: '300'
                },
                formatter(val, opts) {
                    const name = opts.w.globals.labels[opts.seriesIndex];
                    return [val.toFixed(1) + '%'];
                }
            },
      colors: ['#0079BF', '#0088A8', '#00867A', '#5BC160', '#DAD056'],
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
    }, 100);





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
        data: [5000, 5200, 5500, 5300, 5600, 5700, 5900]  // 여기에 실제 데이터를 넣으세요!
      }],
      xaxis: {
        categories: ['07-20', '07-21', '07-22', '07-23', '07-24', '07-25', '07-26'],  // 여기에 실제 날짜를 넣으세요!
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
      colors: ['#546E7A'],
      fill: {
        type: 'gradient',
        gradient: {
          shadeIntensity: 1,
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























};





$(document).ready(function () {
//    $('a[data-target="#detect"]').click(function(event) {
//        event.preventDefault();
//        $('a[data-target="#all"]').removeClass('active');
//        $('a[data-target="#detect"]').addClass('active');
//        $('#all').hide();
//        $('#detect').show();
//    });
//    $('a[data-target="#all"]').click(function(event) {
//        event.preventDefault();
//        $('a[data-target="#detect"]').removeClass('active');
//        $('a[data-target="#all"]').addClass('active');
//        $('#detect').hide();
//        $('#all').show();
//    });


    handleRenderChartSBOM();
    sbom_dataTable();
    sbom_cveTable();
    cveInSbomTable();
    sbomInCveTable();

});




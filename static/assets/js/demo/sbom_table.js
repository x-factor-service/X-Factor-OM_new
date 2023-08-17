
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

// var sbom_detail_dataTable = function () {
//     var dashboardpopupTable = $('#sbom_detail_dataTable').DataTable({
//         dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
//         lengthMenu: [[20, 50, 100, 200], [20, 50, 100, 200]],
//         responsive: true,
//         searching: true,
//         ordering: false,
//         serverSide: true,
//         displayLength: false,
//         ajax: {
//             url: 'paging/',
//             type: "GET",
//             dataSrc: function (res) {
//                 var data = res.data.item;
//                 return data;
//             }
//         },
//         columns: [
//             {data: 'index', width: "5%"},
//             {data: 'name', width: "15%"},
//             {data: 'version', width: "10%"},
//             {data: 'cpe', width: "50%"},
//             {data: 'type', width: "10%"},
//             {data: 'count', width: "10%"}
//         ],
//         columnDefs: [
//             {targets: 0, width: "5%", className: 'text-center'},
//             {
//                 targets: 1, width: "15%", className: '', render: function (data, type, row) {
//                     return '<span title="' + row.name + '" data-toggle="tooltip">' + data + '</span>'
//                 }
//             },
//             {
//                 targets: 2, width: "10%", className: '', render: function (data, type, row) {
//                     return '<span title="' + row.version + '" data-toggle="tooltip">' + data + '</span>'
//                 }
//             },
//             {targets: 3, width: "50%", style: 'text-center text-truncate', render: function (data, type, row) {
//                     return '<span title="' + row.cpe + '" data-toggle="tooltip">' + data + '</span>'
//                 }},
//             {targets: 4, width: "10%", className: 'text-center'},
//             {targets: 5, width: "10%", className: 'text-center'},
//         ],
//         language: {
//             "decimal": "",
//             "info": "전체 _TOTAL_건",
//             "infoEmpty": "데이터가 없습니다.",
//             "emptyTable": "데이터가 없습니다.",
//             "thousands": ",",
//             "lengthMenu": "페이지당 _MENU_ 개씩 보기",
//             "loadingRecords": "로딩 중입니다.",
//             "processing": "",
//             "zeroRecords": "검색 결과 없음",
//             "paginate": {
//                 "first": "처음",
//                 "last": "끝",
//                 "next": "다음",
//                 "previous": "이전"
//             },
//             "search": "검색:",
//             "infoFiltered": "(전체 _MAX_ 건 중 검색결과)",
//             "infoPostFix": "",
//         },
//         pagingType: 'numbers',
//
//         drawCallback: function () {
//             var current_page = dashboardpopupTable.page;
//             var total_pages = dashboardpopupTable.page.info().pages;
//             $('#nexts').remove();
//             $('#after').remove();
//
//             if (total_pages > 10) {
//                 $('<button type="button" class="btn" id="nexts">≫</button>')
//                     .insertAfter('#sbom_dataTable_paginate .paginate_button:last');
//                 $('<button type="button" class="btn" id="after">≪</button>')
//                     .insertBefore('#sbom_dataTable_paginate .paginate_button:first');
//             }
//         }
//     });
//
//     $(document).on('click', '#nexts, #after', function() {
//         var current_page = dashboardpopupTable.page();
//         var total_pages = dashboardpopupTable.page.info().pages;
//         if ($(this).attr('id') == 'nexts') {
//                 if (current_page + 10 < total_pages) {
//                     dashboardpopupTable.page(current_page + 10).draw('page');
//                 } else {
//                     dashboardpopupTable.page(total_pages - 1).draw('page');
//                 }
//                 } else {
//                     dashboardpopupTable.page(Math.max(current_page - 10, 0)).draw('page');
//                 }
//     });
//     $(document).ready(function() {
//     var customStyle = '<style>#nexts, #after {color: #FFFFFF; background-color: #FFFFFF26; margin-left: 5px; height: 33px; padding: 6px 12px; font-size: 15px; padding: 6px 12px; margin-right: 5px;}</style>';
//     $('head').append(customStyle);
//     });
//
// };

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
            {targets: 0, width: "5%", className: 'text-center', orderable: false},
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
            }
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
        dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>",
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



            // 테이블의 행을 클릭했을 때의 이벤트 리스너 추가
    $('#cveInSbom_dataTable tbody').off('click', 'tr').on('click', 'tr', function () {
        var data = dashboardpopupTable.row(this).data();
        var cveId = data.cve_id; // 4번째 컬럼의 데이터

        // 현재 행의 아래에 아코디언이 이미 열려있는지 확인
        var accordionExists = $(this).next('.accordion').length > 0;

        // 아코디언이 이미 있으면 제거
        if (accordionExists) {
            $(this).next('.accordion').remove();
            return;
        }

        // 아코디언 형식으로 cveId 값을 표시
        var accordionHTML = `
        <div class="accordion" id="accordionExample">
            <div class="card">
                <div class="card-header" id="headingOne">
                    <h2 class="mb-0">
                        <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                            CVE ID: ${cveId}
                        </button>
                    </h2>
                </div>

                <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordionExample">
                    <div class="card-body">
                        ${cveId}에 대한 상세 정보나 내용을 여기에 추가합니다.
                    </div>
                </div>
            </div>
        </div>
        `;

        // 테이블의 해당 행 뒤에 아코디언 HTML 삽입
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








$(document).ready(function () {
    $('#sbom_cveTable').on('click', 'tr', function() {

        if ($(this).closest('thead').length === 0) {
            $('#sbom_cveTable tbody tr').css('background-color', '');
            $(this).css('background-color', '#FF9F0C');
        }

        var searchTerm = '';
        var displayTerm = '';

        $(this).find('.click_search').each(function() {
            var value = $(this).text();
            searchTerm += value + '||';
            displayTerm += value + ' ';
        });

        var sbom_dataTable = $('#sbom_dataTable').DataTable();

        sbom_dataTable.search(searchTerm.trim()).draw();

        $('#sbom_dataTable_wrapper div.dataTables_filter input').val(displayTerm.trim());
    });

    sbom_dataTable();
    sbom_cveTable();
    cveInSbomTable();
    sbomInCveTable();
});




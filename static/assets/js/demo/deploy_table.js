
//deploy 페이지
var deploy_package = function () {
    var dashboardpopupTable = $('#packageDataTable').DataTable({
        dom: "<'d-flex justify-content-between'<'col-md-4 mb-md-0'><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>t",
        lengthMenu: [[20, 50, 100, 200], [20, 50, 100, 200]],
        responsive: true,
        searching: true,
        ordering: false,
        serverSide: true,
        displayLength: false,
        paging: false,
        destroy: true,
        order: [
            [ 2, "desc"],
            [ 0, "asc"]
        ],
        ajax: {
            url: 'package/',
            type: "POST",
            data: function (data) {
                return {'search': data.search.value}
            },
            dataSrc: function (res) {
                var data = res.item;
                return data;
            }
        },
        columns: [
            {data: 'Name', width: "15%"},
            {data: 'Content_set', width: "10%"},
            {data: 'Command', width: "35%"},
        ],
        columnDefs: [
            {targets: 0, className: 'text-center', render: function (data, type, row) {
                    return '<span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; max-width: 200px;" title="' + row.Name + '" data-toggle="tooltip">' + data + '</span>'
                }},
            {targets: 1, className: 'text-center', render: function (data, type, row) {
                    return '<span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; max-width: 100px;" title="' + row.Content_set + '" data-toggle="tooltip">' + data + '</span>'
                }},
            {targets: 2, className: 'text-center', render: function (data, type, row) {
                    return '<span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; max-width: 300px;" title="' + row.Command + '" data-toggle="tooltip">' + data + '</span>'
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
    });
};

var deploy_computerGroup = function () {
    var dashboardpopupTable = $('#computerGroupDataTable').DataTable({
        dom: "<'d-flex justify-content-between'<'col-md-4 mb-md-0'l><'text-right'fB>><'align-items-center d-flex justify-content-between'<'mr-auto col-md-6 mb-md-0 mt-n2'i><'mb-0 col-md-6'p>>t",
        lengthMenu: [[20, 50, 100, 200], [20, 50, 100, 200]],
        responsive: true,
        searching: true,
        ordering: false,
        serverSide: true,
        displayLength: false,
        paging: false,
        ajax: {
            url: 'computerGroup/',
            type: "POST",
            data: function (data) {
                return {'search': data.search.value}
            },
            dataSrc: function (res) {
                var data = res.item;
                return data;
            }
        },
        columns: [
            {data: 'Name', width: "15%"},
            {data: 'Content_set', width: "10%"},
            {data: 'Expression', width: "35%"},
        ],
        columnDefs: [
            {targets: 0, className: 'text-center', render: function (data, type, row) {
                    return '<div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; max-width: 200px;" title="' + row.Name + '" data-toggle="tooltip">' + data + '</div>'
                }},
            // , render: funct'<div style="cursor: pointer; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="' + row.Name + '" data-toggle="tooltip">'+data+'</div>'}
            {targets: 1, className: 'text-center', render: function (data, type, row) {
                    return '<div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; max-width: 100px;" title="' + row.Content_set + '" data-toggle="tooltip">' + data + '</div>'
                }},
            {targets: 2, className: 'text-center', render: function (data, type, row) {
                    return '<div style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; max-width: 300px;" title="' + row.Expression + '" data-toggle="tooltip">' + data + '</div>'
                }}
        ],
        language: {
            "decimal": "",
            "info": "전체 _TOTAL_건",
            "infoEmpty": "데이터가 없습니다.",
            "emptyTable": "데이터가 없습니다.",
            "thousands": ",",
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

    });
};


$(document).ready(function () {

    deploy_package();
    deploy_computerGroup();

});


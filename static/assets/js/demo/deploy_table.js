
//deploy 페이지
var deploy_package = function () {
    var dashboardpopupTable = $('#packageDataTable').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>t",
        lengthMenu: [[20, 50, 100, 200], [20, 50, 100, 200]],
        responsive: true,
        searching: true,
        ordering: true,
        serverSide: true,
        displayLength: false,
        paging: false,
        ajax: {
            url: 'package/',
            type: "POST",

            dataSrc: function (res) {
                var data = res.item;
                return data;
            }
        },
        columns: [
            {data: 'Display_name', width: "5%"},
            {data: 'Content_set', width: "5%"},
            {data: 'Command', width: "15%"},
        ],
        columnDefs: [
            {targets: 0, width: "1%", className: 'text-center'},
            {targets: 1, width: "10%", className: 'text-center'},
            {targets: 2, width: "15%", className: 'text-center'}
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

// rowCallback: function (row, data) {
//     var outputPValue = $('#outputP').text();
//     var outputCValue = $('#outputC').text();
//     $('#outputPValue').val(outputPValue);
//     $('#outputCValue').val(outputCValue);
//
//     $('#action_btn').on('click', function (event) {
//         var outputPValue = $('#outputP').text();
//         var outputCValue = $('#outputC').text();
//
//         $('#outputPValue').val(outputPValue);
//         $('#outputCValue').val(outputCValue);
//     });
//
//     var stateP = {};
//     var resultP = $('#outputP');
//
//     $(row).on('click', function () {
//         var index = Array.from(row).indexOf(this);
//
//         if (!stateP.hasOwnProperty(index)) {
//             stateP[index] = false;
//         }
//
//         if (stateP[index]) {
//             // 이미 선택된 상태인 경우 원래대로 되돌립니다.
//             Array.from(row).forEach(function (item) {
//                 $(item).on('click', rowCallback);
//             });
//             resultP.html(resultP.html().replace(data.Display_name.trim() + '<br>', ''));
//             $(row).css('background-color', '');
//
//             var rows = $(row).siblings();
//             rows.on('click', function () {
//             });
//         } else {
//             // 선택되지 않은 상태인 경우 주황색으로 변경합니다.
//             $(row).css('background-color', 'orange');
//             resultP.append(data.Display_name.trim() + '<br>');
//             Array.from(row).forEach(function (item) {
//                 if (item !== this) {
//                     item.off('click', rowCallback);
//                 }
//             }, this);
//             var rows = $(row).siblings();
//             rows.off('click');
//         }
//
//         stateP[index] = !stateP[index];
//     });
//     Array.from(row).forEach(function (item) {
//         console.log(item)
//         item.on('click', rowCallback);
//     });
// }

    });
};

var deploy_computerGroup = function () {
    var dashboardpopupTable = $('#computerGroupDataTable').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'l><'text-right'fB>><'align-items-center d-flex justify-content-between'<'mr-auto col-md-6 mb-md-0 mt-n2'i><'mb-0 col-md-6'p>>t",
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

            dataSrc: function (res) {
                var data = res.item;
                return data;
            }
        },
        columns: [
            {data: 'Name', width: "1%"},
            {data: 'Content_set', width: "5%"},
            {data: 'Expression', width: "15%"},
        ],
        columnDefs: [
            {targets: 0, width: "1%", className: 'text-center'},
            {targets: 0, width: "10%", className: 'text-center'},
            {targets: 0, width: "15%", className: 'text-center'}
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


    // rowCallback: function (row, data) {
    //         // 토글 상태를 추적하기 위한 객체를 생성합니다.
    //         var stateC = {};
    //         $(row).on('click', function () {
    //             var index = Array.from(row).indexOf(this);
    //             // 초기 토글 상태를 false로 설정합니다.
    //             if (!stateC.hasOwnProperty(index)) {
    //                 stateC[index] = false;
    //             }
    //             var resultC = document.getElementById('outputC');
    //             if (stateC[index]) {
    //             // 이미 선택된 상태인 경우 원래대로 되돌립니다.
    //                 Array.from(row).forEach(function (item) {
    //                 item.addEventListener('click', rowCallback);
    //                 });
    //             resultC.innerHTML = resultC.innerHTML.replace(data.Name.trim() + '<br>', '');
    //             row.style.backgroundColor = '';
    //             } else {
    //                 // 선택되지 않은 상태인 경우 주황색으로 변경합니다.
    //                 row.style.backgroundColor = 'orange';
    //                 resultC.innerHTML += data.Name.trim() + '<br>';
    //                 Array.from(row).forEach(function (item) {
    //                     if (item !== this) {
    //                         item.removeEventListener('click', rowCallback);
    //                     }
    //                 }, this);
    //             }
    //             stateC[index] = !stateC[index]
    //
    //         });
    //         Array.from(row).forEach(function (item) {
    //             console.log(item)
    //             item.addEventListener('click', rowCallback);
    //         });
    //     }

    });

};


$(document).ready(function () {

    var $clickedRow = ''
    var resultP = document.getElementById('outputP');
    var resultC = document.getElementById('outputC');
    $("#packageDataTable").on('click', 'tbody tr', function () {
        $clickedRow = $(this);
        var isClicked = $clickedRow.hasClass('clicked');
        $clickedRow.addClass('clicked');
        var tdValue = $clickedRow.find('td:eq(0)').text();
         // 클릭한 행의 상태에 따라 동작을 처리합니다.
        if (isClicked) {
            // 클릭한 행이 이미 선택된 상태인 경우 선택 해제
            $clickedRow.removeClass('clicked');
            $clickedRow.css('background-color', '');
            resultP.innerHTML = resultP.innerHTML.replace(tdValue + '<br>', '');
            // $('tbody tr').removeClass('disabled');
            $('#packageDataTable tbody tr').css('pointer-events', 'auto');
        } else {
            // 클릭한 행을 선택 상태로 하이라이트하고 다른 행의 클릭을 비활성화
            $('#packageDataTable tbody tr').not($clickedRow).css('pointer-events', 'none');
            // $('tbody tr').not($clickedRow).addClass('disabled');
            $clickedRow.addClass('clicked');
            resultP.innerHTML = tdValue + '<br>';
            $clickedRow.css('background-color', 'orange');
        }
    });

    $("#computerGroupDataTable").on('click', 'tbody tr', function () {
        var $clickedRow = $(this);
        var isClicked = $clickedRow.hasClass('clicked');
        var tdValue = $clickedRow.find('td:eq(0)').text();
  // 클릭한 행의 상태에 따라 동작을 처리합니다.
    if (isClicked) {

    // 클릭한 행이 이미 선택된 상태인 경우 선택 해제
    $clickedRow.removeClass('clicked');
    $clickedRow.css('background-color', '');
    resultC.innerHTML = resultC.innerHTML.replace(tdValue + '<br>', '');
    $('tbody tr').removeClass('disabled');
    // $('tbody tr').css('pointer-events', 'auto');
    } else {
    // 클릭한 행을 선택 상태로 하이라이트하고 다른 행의 클릭을 비활성화
    // $('tbody tr').not($clickedRow).css('pointer-events', 'none');
    $('tbody tr').not($clickedRow).addClass('disabled');
    $clickedRow.addClass('clicked');
    resultC.innerHTML += tdValue + '<br>';
    $clickedRow.css('background-color', 'orange');
    }
});


    // if ($("#sbom_dataTable").length > 0) {
    var outputCValue = document.getElementById('outputC').textContent;
    document.getElementById('outputCValue').value = outputCValue;
    var errorMsgDiv = document.getElementById('errorMsg');
    var outputP = document.getElementById('cb1');
    var outputC = document.getElementById('cb2');
    var inputs = document.querySelectorAll('.outputP, .outputC');

    inputs.forEach(function (input) {
        input.addEventListener('input', function () {
            errorMsgDiv.textContent = '';
        });
    });

    document.getElementById('action_btn').addEventListener('click', function (event) {
        var outputPValue = document.getElementById('outputP').textContent;
        var outputCValue = document.getElementById('outputP').textContent;

        inputs.forEach(function (input) {
            if (input.value === '') {
                input.classList.add('error-border');
                event.preventDefault();
            }
        });

        // 에러 메시지 출력
        if (outputPValue === '' || outputCValue === '') {
            event.preventDefault();
            errorMsgDiv.textContent = 'package 또는 computer group을 선택해주세요.';
        }else {
            // 두 개의 값이 모두 있는 경우 에러 메시지 제거
            errorMsgDiv.textContent = ' <br><br>';
            document.getElementById('outputPValue').value = outputPValue;
            document.getElementById('outputCValue').value = outputCValue;
        }
    });
        deploy_package();
        deploy_computerGroup();
        // sbom_detail_dataTable();
    // }
});


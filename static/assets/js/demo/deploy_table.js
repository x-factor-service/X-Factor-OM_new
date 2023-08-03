
//deploy 페이지
var deploy_package = function () {
    var dashboardpopupTable = $('#packageDataTable').DataTable({
        dom: "<'d-flex justify-content-between mb-3'<'col-md-4 mb-md-0'><'text-right'<'d-flex justify-content-end'fB>>>t<'align-items-center d-flex justify-content-between'<' mr-auto col-md-6 mb-md-0 mt-n2 'i><'mb-0 col-md-6'p>>t",
        lengthMenu: [[20, 50, 100, 200], [20, 50, 100, 200]],
        responsive: true,
        searching: true,
        ordering: false,
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
            {data: 'Name', width: "5%"},
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
            document.getElementById("registry").disabled = false;
            var divElement1 = document.getElementById("colVal1");
            var divElement2 = document.getElementById("colVal3");
            var parentElement = document.getElementById("colval3");
            divElement1.classList.remove("col-3"); // 기존 클래스 제거
            divElement1.classList.add("col-5"); // 새로운 클래스 추가
            divElement2.style.display = "none";
            divElement1.style.paddingRight = colVal2OriginalPaddingRight;// 새로운 클래스 추가
            while (parentElement.firstChild) {
                parentElement.removeChild(parentElement.firstChild);
            }
            // 클릭한 행이 이미 선택된 상태인 경우 선택 해제
            $clickedRow.removeClass('clicked');
            $clickedRow.css('background-color', '');
            resultP.innerHTML = resultP.innerHTML.replace(tdValue + '<br>', '');
            // $('tbody tr').removeClass('disabled');
            $('#packageDataTable tbody tr').css('pointer-events', 'auto');
        } else {
            document.getElementById("registry").disabled = true;
            // 클릭한 행을 선택 상태로 하이라이트하고 다른 행의 클릭을 비활성화
            $('#packageDataTable tbody tr').not($clickedRow).css('pointer-events', 'none');
            // $('tbody tr').not($clickedRow).addClass('disabled');
            $clickedRow.addClass('clicked');
            resultP.innerHTML = tdValue + '<br>';
            $clickedRow.css('background-color', 'orange');
            var id = tdValue;

          // Ajax 요청을 보냅니다.
            $.ajax({
                type: 'POST', // HTTP 요청 방식을 선택합니다.
                url: 'packCheck/', // 데이터를 처리할 서버 엔드포인트 URL을 입력합니다.
                data: { 'id': id }, // 서버로 보낼 데이터를 설정합니다.
                success: function(response) {
                  // 성공적인 응답을 받았을 때 수행할 동작을 정의합니다.
                    console.log('성공:', response);
                    if (typeof response.a === 'number' && response.a > 0) {
                        var divElement1 = document.getElementById("colVal1");
                        var divElement2 = document.getElementById("colVal3");
                        divElement1.classList.remove("col-5"); // 기존 클래스 제거
                        divElement1.classList.add("col-3"); // 새로운 클래스 추가
                        divElement2.style.display = "none";
                        divElement1.style.paddingRight = "0";// 새로운 클래스 추가
                        divElement2.removeAttribute("style");
                        var parentElement = document.getElementById("colval3"); // input 박스를 추가할 부모 요소를 가져옴
                        for (var i = 1; i <= 10; i++) {
                          // div 태그 생성
                            var divElement = document.createElement("div");
                            divElement.textContent = "parameter " + i;
                          // input 요소 생성
                            var inputElement = document.createElement("input");
                            var inputhidden = document.createElement("input");
                            inputElement.type = "text";
                            inputhidden.type = "hidden";
                            inputElement.name = "param" + i;
                            inputElement.classList.add("form-control", "inBox");
                          // div 태그에 input 요소 추가
                            divElement.appendChild(inputElement);
                          // div 태그를 부모 요소에 추가
                            parentElement.appendChild(divElement);
                          // 줄 바꿈
                            var brElement = document.createElement("br");
                            parentElement.appendChild(brElement);
                        }
                    } else {
                        return
                    }
                },
                error: function(xhr, status, error) {
                  // 오류가 발생했을 때 수행할 동작을 정의합니다.
                    console.error('오류:', status, error);
                }
            });
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
        var outputCValue = document.getElementById('outputC').textContent;
        alert('')
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
            errorMsgDiv.textContent = ' ';
            document.getElementById('outputPValue').value = outputPValue;
            document.getElementById('outputCValue').value = outputCValue;
        }
    });
        deploy_package();
        deploy_computerGroup();
        // sbom_detail_dataTable();
    // }
});


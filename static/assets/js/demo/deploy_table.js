
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

    var $clickedRow = ''
    var resultP = document.getElementById('outputP'); // 왼쪽 package 목록에서 선택된 값이 deploy action에 package 박스에 들어감.
    var resultC = document.getElementById('outputC'); // 왼쪽 computer group 목록에서 선택된 값이 deploy action에 computer group 박스에 들어감.

    // packageDataTable 테이블의 tbody tr 클릭 이벤트시 호출되는 초기화 함수
    function resetDivClasses() {
        var divElement4 = document.getElementById("colVal4");
        var divElement3 = document.getElementById("colVal3");

        // Set divElement4 to its original state
        divElement4.classList.remove("col-xl-4");
        divElement4.classList.add("col-xl-8");

        // Set divElement3 to its original state (hidden)
        divElement3.style.display = "none";
    };

    // packageDataTable 테이블의 tbody tr 클릭 이벤트시 호출되는 클래스 부여 함수
    function toggleDivClasses() {
        var divElement4 = document.getElementById("colVal4");
        var divElement3 = document.getElementById("colVal3");

        if (divElement4.classList.contains("col-xl-8")) {
            divElement4.classList.remove("col-xl-8");
            divElement4.classList.add("col-xl-4");
            divElement3.style.display = "block";
        } else {
            divElement4.classList.remove("col-xl-4");
            divElement4.classList.add("col-xl-8");
            divElement3.style.display = "none";
        };
    };

    // packageDataTable 테이블의 tbody tr 이벤트 리스너
    $("#packageDataTable").on('click', 'tbody tr', function () {
        $clickedRow = $(this);
        var isClicked = $clickedRow.hasClass('clicked');

        // 원래 클릭했던 곳의 색을 없애기 위해 다른 행들의 클래스를 제거합니다.
        $('#packageDataTable tbody tr').not($clickedRow).removeClass('clicked').css('background-color', '');
        $clickedRow.addClass('clicked');

        var tdValue = $clickedRow.find('td:eq(0)').text(); // 클릭한 행의 첫 번째 셀(td)에서 텍스트를 가져옵니다.

        var parentElement = document.getElementById("colVal3_param");
        var parentElement1 = document.getElementById("pack"); // deploy action 에 있는 pack

        if (isClicked) {
            // colVal3_param 안에 있는 div 태그 모두 삭제
            while (parentElement.firstChild) {
                parentElement.removeChild(parentElement.firstChild);
                resetDivClasses();
            }
            // pack 안에 있는 div 태그 모두 삭제
            while (parentElement1.firstChild) {
                parentElement1.removeChild(parentElement1.firstChild);
                resetDivClasses();
            }
            // 클릭한 행이 이미 선택된 상태인 경우 선택 해제
            $clickedRow.removeClass('clicked');
            $clickedRow.css('background-color', '');
            resultP.innerHTML = resultP.innerHTML.replace(tdValue + '<br>', '');
            $('#packageDataTable tbody tr').css('pointer-events', 'auto');
            resetDivClasses();
        } else {
            // colVal3_param 안에 있는 div 태그 모두 삭제
            while (parentElement.firstChild) {
                parentElement.removeChild(parentElement.firstChild);
                resetDivClasses();
            }
            // pack 안에 있는 div 태그 모두 삭제
            while (parentElement1.firstChild) {
                parentElement1.removeChild(parentElement1.firstChild);
                resetDivClasses();
            }

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
                    // console.log('성공:', response);
                    if (typeof response.a === 'number' && response.a > 0) {
                        param(response.a);
                        toggleDivClasses();
                    } else {
                        // colVal3_param 안에 있는 div 태그 모두 삭제
                        while (parentElement.firstChild) {
                            resetDivClasses()
//                            parentElement.removeChild(parentElement.firstChild);
                        }
                        // pack 안에 있는 div 태그 모두 삭제
                        while (parentElement1.firstChild) {
                            resetDivClasses()
//                            parentElement1.removeChild(parentElement1.firstChild);
                        }
                        return
                    }
                },
                cache: true, // AJAX 호출 결과를 캐시하도록 브라우저에 지시
                error: function(xhr, status, error) {
                  // 오류가 발생했을 때 수행할 동작을 정의합니다.
                    // console.error('오류:', status, error);
                },
            });
        }
    });

    // package에 필요한 파라미터 div 생성
    function param(count){
        var parentElement = document.getElementById("colVal3_param"); // input 박스를 추가할 부모 요소를 가져옴
        var parentElement1 = document.getElementById("pack"); // input 박스를 추가할 부모 요소를 가져옴

        for (var i = 1; i <= count; i++) {
            // div 태그 생성
            var divElement = document.createElement("div");
            divElement.textContent = "parameter " + i;
            // input 요소 생성
            var inputElement = document.createElement("input");
            var inputHidden = document.createElement("input");
            inputElement.type = "text";
            inputHidden.type = "hidden";
            inputElement.name = "param" + i;
            inputHidden.name = "hidden" + i;
            inputElement.classList.add("form-control");
            // div 태그에 input 요소 추가
            divElement.appendChild(inputElement);
            // div 태그를 부모 요소에 추가
            parentElement.appendChild(divElement);
            parentElement1.appendChild(inputHidden);
            // 줄 바꿈
            var brElement = document.createElement("br");
            parentElement.appendChild(brElement);
        }
    };

    // computerGroupDataTable 테이블의 tbody tr 이벤트 리스너
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
        } else {
            $('tbody tr').not($clickedRow).addClass('disabled');
            $clickedRow.addClass('clicked');
            resultC.innerHTML += tdValue + '<br>';
            $clickedRow.css('background-color', 'orange');
        }
    });

    //outputP 내부 콘텐츠를 재설정하는 기능
    $("#deployPCK_resetBtn").click(function() {
        $("#outputP").empty();
         $("#packageDataTable tbody tr").removeClass('clicked').css('background-color', '');
         resetDivClasses()
    });

    //outputC 내부 콘텐츠를 재설정하는 기능
    $("#deployGRP_resetBtn").click(function() {
    $("#outputC").empty();
    $("#computerGroupDataTable tbody tr").removeClass('clicked').css('background-color', '');
    });


    // deploy action 버튼 이벤트 리스너
    var outputCValue = document.getElementById('outputC').textContent;
    document.getElementById('outputCValue').value = outputCValue;

    var errorMsgDiv = document.getElementById('errorMsg');
    var outputP = document.getElementById('cb1');
    var outputC = document.getElementById('cb2');
    var inputs = document.querySelectorAll('.outputP, .outputC');
    var parentElement1 = document.getElementById("pack");

    inputs.forEach(function (input) {
        input.addEventListener('input', function () {
            errorMsgDiv.textContent = '';
        });
    });
    var index = 0;
    // deploy action 버튼 이벤트 리스너
    document.getElementById('action_btn').addEventListener('click', function (event) {
        var outputPValue = document.getElementById('outputP').textContent;
        var outputCValue = document.getElementById('outputC').textContent;
        var inputElements = document.querySelectorAll("#colVal3_param input");
        var parentElement = document.getElementById("colVal3_param");
        var now = new Date();
        var year = now.getFullYear();
        var month = (now.getMonth() + 1).toString().padStart(2, '0');
        var day = now.getDate().toString().padStart(2, '0');

        var hours = now.getHours().toString().padStart(2, '0');
        var minutes = now.getMinutes().toString().padStart(2, '0');
        var seconds = now.getSeconds().toString().padStart(2, '0');

        var ad = (year + "-" + month + "-" + day + " " + hours + ":" + minutes + ":" +seconds);


        // console.log(parentElement + '1');
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
            errorMsgDiv.innerHTML = '<br/><br/>';
            document.getElementById('outputPValue').value = outputPValue;
            document.getElementById('outputCValue').value = outputCValue;
        }

        inputElements.forEach(function(inputElement, index) {
            var hiddenInput = document.querySelector('input[name="hidden' +(index+1)+'"]');
            var paramInput = document.querySelector('input[name="param' +(index+1)+'"]');
            if (hiddenInput.length > 1) {
                hiddenInput.value = inputElement.value;
                paramInput.classList.remove("error")
                alert(inputElement.value)
            }else {
                event.preventDefault();
                paramInput.classList.add("error")
                errorMsgDiv.textContent = '파라미터 값을 입력해 주세요.';
            }

        });
            if (confirm("배포하시겠습니까?") == true){

            var intervalMap = {};

            function increaseProgressBar(id) {
                var progressBarValue = 0;

                var increaseInterval = setInterval(function() {

                    var randomIncrease = Math.floor(Math.random() * 4) + 2;

                    progressBarValue += randomIncrease;

                    if (progressBarValue > 99) {
                        clearInterval(increaseInterval);
                        progressBarValue = 99;
                    }

                    var progressBarElement = document.querySelector('#' + id);
                    if (progressBarElement !== null) {
                      progressBarElement.style.width = progressBarValue + '%';
                      progressBarElement.textContent = progressBarValue + '%';
                    }
                        if (progressBarValue === 99 && progressBarElement !== null) {
                          clearInterval(intervalMap[id]);
                          delete intervalMap[id];

                        }
                },800);
                intervalMap[id] = increaseInterval;
            }

            var ulElement = document.getElementById('as');

            var liElement = document.createElement('li');
            liElement.className = "status-item d-flex align-items-center w-100 h-100";

            var innerHTMLString =
                `<div class="status-sequence fs-12px fw-bold w-10 text-center">01</div>
                <div class="status-info w-90 d-flex p-1">
                    <p class="m-0 fs-12px"><strong class="fw-bold">Package Name:</strong> ${outputPValue}</p>
                    <p class="m-0 fs-12px"><strong class="fw-bold">Action Date:</strong> ${ad}</p>
                    <div class="progress fs-10px">
                        <div id="progress-bar-${index}"class="progress-bar progress-bar-striped progress-bar-animated bg-warning" style="width: 0%">0%</div>
                    </div>`;



            liElement.innerHTML = innerHTMLString;

            ulElement.insertBefore(liElement, ulElement.firstChild);

                if (ulElement.children.length > 5) {
                   ulElement.removeChild(ulElement.lastChild);
                }
                increaseProgressBar(`progress-bar-${index}`);

                Array.from(ulElement.children).forEach(function(child, index) {
                   child.querySelector('.status-sequence').textContent = '0' + (index + 1);
                });
                index++;
                $.ajax({
                    url: '/deploy_action_val/',
                    type: 'POST',
                    data: {
                        outputPValue: outputPValue,
                        outputCValue: outputCValue,
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    },
                    success: function(response) {

                        console.log(response);
                        var progressBarId = `progress-bar-${index - 1}`;

                        if (intervalMap[progressBarId]) {
                            clearInterval(intervalMap[progressBarId]);
                            delete intervalMap[progressBarId];
                        }

                        var progressBarElement = document.getElementById(progressBarId);

                        if (progressBarElement) {

                            progressBarElement.classList.remove('bg-warning', 'progress-bar-striped', 'progress-bar-animated');
                            var parentDiv = progressBarElement.parentNode;

                            parentDiv.removeChild(progressBarElement);

                            var a = response.per[0];
                            var b = response.per[1];

                            var newProgressBarA = document.createElement('div');
                            newProgressBarA.className = "progress-bar";
                            newProgressBarA.style.width = a;
                            newProgressBarA.textContent = a;

                            var newProgressBarB = document.createElement('div');
                            newProgressBarB.className = "progress-bar bg-danger";
                            newProgressBarB.style.width = b;
                            newProgressBarB.textContent = b;

                            parentDiv.appendChild(newProgressBarA);
                            parentDiv.appendChild(newProgressBarB);

                            location.reload();

                        }
                    },
                    error: function(xhr, status, error) {
                        console.error('Error:', error);
                    }
                });
            } else {
                event.preventDefault();
                return;
            }
        });
    deploy_package();
    deploy_computerGroup();
});


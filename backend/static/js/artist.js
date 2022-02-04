// 사용 변수들
var clicked_platform = "";

const isEmpty = 
    function(value){ 
        if( value == "" || value == null || value == undefined || ( value != null && typeof value == "object" && !Object.keys(value).length ) ){ 
            return true 
        }else{ 
                return false 
        } 
    };


//artist create function
$('#add-submit').click(function(e){
    var trs_value = $('input[type=text]');  //artist info
    var urls_tr = $('.add-table').find('#artist-urls').find('tr')
    var datas = [];

    for(var r=0;r<urls_tr.length;r++){
        var cells = urls_tr[r].getElementsByTagName("td");
        //console.log(cells.length);
        if(cells.length < 3){
            datas.push({
                "platform_name": cells[0].innerHTML,
                "url1": cells[1].firstElementChild.value,
                "url2": "",
            });
        } else{
            datas.push({
                "platform_name": cells[0].innerHTML,
                "url1": cells[1].firstElementChild.value,
                "url2": cells[2].firstElementChild.value,
            });
        }
    }

    console.log(datas);

    var charRe = /^[a-z]|[A-Z]$/;

    if(trs_value[0].value==""){
        alert("아티스트의 이름을 입력해주세요.");
        e.preventDefault();
        return;
    }else if(trs_value[1].value=="" || !charRe.test(trs_value[1].value)){
        alert("구분을 S/A/B형태로 입력해주세요.");
        e.preventDefault();
        return;
    }else if(trs_value[2].value=="" ||( trs_value[2].value!="M" && trs_value[2].value!="F")){
        alert("성별을 M/F형태로 입력해주세요.");
        e.preventDefault();
        return;
    }else if(trs_value[3].value==""){
        alert("멤버 수를 입력해주세요.");
        e.preventDefault();
        return;
    }
    var data = {
        "name": trs_value[0].value,
        "level": trs_value[1].value,
        "gender": trs_value[2].value,
        "member_num": trs_value[3].value,
        "member_nationality": trs_value[4].value,
        "agency":trs_value[5].value,
        // "debut_date": trs_value[6].value,
        "urls": datas,
    };
    if(trs_value[6].value!=""){
        data["debut_date"] = trs_value[6].value;
    }

    //console.log(JSON.stringify(data));

    $.ajax({
        url: "/dataprocess/api/artist/",
        type: 'POST',
        datatype:'json',
        data: JSON.stringify(data),
        success: res => {
            alert("저장되었습니다.");
            location.href = "/dataprocess/artist/";
        },
        error: e => {
            console.log(e);
            alert(e.responseText);
        },
    });
    
})

//artist update
$('#save-artists').click(function(){
    var datas=[];
    var artist_tr = $('#artist-body').find('tr');

    for(var r=0;r<artist_tr.length;r++){
        var cells = artist_tr[r].getElementsByTagName("td");
        var tmp_json = {
            "id": cells[0].firstElementChild.value,
            "name": cells[1].firstElementChild.value,
            "level": cells[2].firstElementChild.value,
            "gender": cells[3].firstElementChild.value,
            "member_num": parseInt(cells[4].firstElementChild.value),
            "member_nationality": cells[5].firstElementChild.value,
            "agency":cells[6].firstElementChild.value,
            "active": cells[8].firstElementChild.checked
        };
        if (cells[7].firstElementChild.value!="")
            tmp_json["debut_date"] = cells[7].firstElementChild.value;
        datas.push(tmp_json);
    }
    $.ajax({
        url: '/dataprocess/api/artist/',
        type: 'PUT',
        datatype:'json',
        data: JSON.stringify(datas),
        success: res => {
            alert('저장되었습니다.');
        },
        error: e => {
            console.log(e);
            alert(e.responseText);
        },
    })
})

//show platforms per artist
//아티스트 클릭시
$('input[name=artist-name]').click(function(){
    $('input[name=artist-name]').removeClass("clicked-input-btn");
    var artist = $(this).val();
    // $(this).removeClass("input-btn");
    $(this).addClass("clicked-input-btn");

    // console.log(artist);

    $.ajax({
        url: '/dataprocess/api/platform_of_artist/',
        type: 'GET',
        datatype:'json',
        data : {'artist':artist},
        contentType: 'application/json; charset=utf-8',
        success: res => {
            //아티스트 표 작게 처리
            make_artist_hidden();
            document.getElementById("artist-subtitle").style.color = "#000000";
            document.getElementById("artist-subtitle").innerHTML = artist+" 플랫폼";
            const data_list = res.data;
            $('#artist-body-platform').empty();
            data_list.forEach(data => {//data를 화면에 표시
                const tableRow = $('<tr></tr>')
                // 해당 row에 대한 column 데이터들 넣기
                for(key in data){
                    let dataCol;
                    if(key==='active'){
                        if(data[key]==true){
                            dataCol = $('<td class="platform_hidden"><input checked type="checkbox"></input></td>'); 
                        }else{
                            dataCol = $('<td class="platform_hidden"><input type="checkbox"></input></td>'); 
                        }
                    } else if(key === 'name'){
                        dataCol = document.createElement('td');
                        dataCol.innerHTML = `
                        <td>
                            <span class="platform-names input-btn">${data[key]}</span>
                        </td>
                        `;
                    } 
                    else{
                        dataCol = document.createElement('td');
                        if(key === 'artist_id' || key==='id' || key==='platform_id')
                            dataCol.setAttribute('class', 'hidden');
                        dataCol.classList.add("platform_hidden");
                        dataCol.innerHTML = `
                        <td>
                            <input title=${data[key]} type="text" value="${data[key]}" style="width:100%"></input>
                        </td>
                        `;
                    }
                    tableRow.append(dataCol);
                }
                $('#artist-body-platform').append(tableRow);
            });
        },
        error: e => {
            alert(e.responseText);
        },
    })
})

//update artist's platform info
//artist update
$('#save-artists-platform').click(function(){
    var datas=[];
    var artist_tr = $('#artist-body-platform').find('tr');

    for(var r=0;r<artist_tr.length;r++){
        var cells = artist_tr[r].getElementsByTagName("td");

       
        datas.push({
            "type": "artist-platform-update",
            "id": cells[2].firstElementChild.value,
            "platform": cells[3].firstElementChild.innerHTML,
            "target_url": cells[4].firstElementChild.value,
            "target_url_2" : cells[5].firstElementChild.value,
        });

    }

    console.log(datas);

    $.ajax({
        url: '/dataprocess/api/platform_of_artist/',
        type: 'PUT',
        datatype:'json',
        data: JSON.stringify(datas),
        success: res => {
            alert('저장되었습니다.');
        },
        error: e => {
            console.log(e);
            alert(e.responseText);
        },
    })
    
})

function add_new_collect_target_item(item_num){
    //새로운 collect_target_item을 row상에 추가하는 함수4
    const tableRow = $('<tr></tr>');
    for(var i=0;i<6;i++){
        let dataCol = document.createElement('td');
        if(i===0){//id -> 아직 없으므로 0으로 두기
            dataCol.setAttribute('class', 'hidden');
            dataCol.innerHTML = `
            <td>
                <input type="text" value="0"></input>
            </td>
            `;
        }else if(i==1){//collect_Target_id -> 아직 없으므로 0으로 두기
            dataCol.setAttribute('class', 'hidden');
            dataCol.innerHTML = `
            <td>
                <input type="text" value="0"></input>
            </td>
            `;
        }else if(i==2){//항목
            dataCol.innerHTML = `
                <td>
                    <span style="width:100%">항목${item_num}</span>
                </td>`;
        }else if(i==3){//target name
            dataCol.innerHTML = `
                <td>
                    <input type="text" value="" style="width:100%"></input>
                </td>
                `;
        }else if(i==4){//xpath
            dataCol.setAttribute('class', 'item_hidden');
            dataCol.innerHTML = `
            <td>
                <textarea style="width:100%"></textarea>
            </td>
            `;
        }else if(i==5){//delete button
            dataCol.setAttribute('class', 'item_hidden');
            dataCol.innerHTML = `
                <td>
                    <button class="btn btn-danger"
                    onclick=delete_collect_target_item_notindb(${item_num-1})>삭제</button>
                </td>
            `;
        }
        tableRow.append(dataCol);
    }
    $('#artist-body-list').append(tableRow);
}

//show collect target of platform
//플랫폼 클릭시
$(document).on('click','.platform-names',function(){
    $('.platform-names').removeClass("clicked-input-btn");
    var artist_name = document.getElementById("artist-subtitle").innerHTML.replace(" 플랫폼","");
    var platform = $(this).text();
    clicked_platform = platform;
    $(this).addClass("clicked-input-btn");

    $.ajax({
        url: '/dataprocess/api/collect_target_item/',
        type: 'GET',
        datatype:'json',
        data : {'platform': platform, 'artist': artist_name},
        contentType: 'application/json; charset=utf-8',
        success: res => {
            //플랫폼창 작게 만들기
            make_platform_hidden();
            item_open = true;
            document.getElementById("item_open").classList.remove("fa-chevron-right");
            document.getElementById("item_open").classList.add("fa-chevron-left");
            document.getElementById("platform-subtitle").style.color = "#000000";
            document.getElementById("platform-subtitle").innerHTML = artist_name+" "+ platform+ " 조사항목";
            const data_list = res.data["items"];
            console.log(data_list);
            $('#artist-body-list').empty();
            let len = 0;
            if(data_list.length>0){
                data_list.forEach(data=>{//data를 화면에 표시
                    len += 1;
                    const tableRow = $('<tr></tr>');
                    // 해당 row에 대한 column 데이터들 넣기
                    // (id, collect_target_id), target_name, xpath
                    for(key in data){
                        let dataCol;
                        if(key==='id' || key==='collect_target_id'){
                            dataCol = document.createElement('td');
                            dataCol.setAttribute('class', 'hidden');
                            dataCol.innerHTML = `
                            <td>
                                <input type="text" title="${data[key]}" value="${data[key]}" style="width:100%"></input>
                            </td>
                            `;
                            tableRow.append(dataCol);
                            if(key=='collect_target_id'){
                                //조사항목 td 붙이기
                                //TODO: 순서대로 나열
                                let len2 = len;
                                let dataCol_name = dataCol = document.createElement('td');
                                dataCol_name.innerHTML = `
                                <td>
                                    <span style="width:100%">항목${len2}</span>
                                </td>
                                `;
                                tableRow.append(dataCol_name);
                            }
                        }else if(key==='target_name'){
                            dataCol = document.createElement('td');
                            dataCol.innerHTML = `
                            <td>
                                <input type="text" title="${data[key]}" value="${data[key]}" style="width:100%"></input>
                            </td>
                            `;
                            tableRow.append(dataCol);
                        }else if(key==='xpath'){
                            let len2 = len-1;
                            dataCol = document.createElement('td');
                            dataCol.classList.add("item_hidden");
                            dataCol.innerHTML = `
                            <t>
                                <textarea style="width:100%">${data[key]}</textarea>
                            </td>
                            `;
                            tableRow.append(dataCol);
                            //삭제 버튼 붙이기
                            let dataCol2 = document.createElement('td');
                            dataCol2.classList.add("item_hidden");
                            let dataCol2Btn = document.createElement('button');
                            dataCol2Btn.onclick = function(){
                                delete_collect_target_item(data["id"], len2);
                            };
                            dataCol2Btn.setAttribute('class', 'btn-danger');
                            dataCol2Btn.classList.add("btn");
                            dataCol2Btn.innerHTML = "삭제";
                            dataCol2.append(dataCol2Btn);
                            tableRow.append(dataCol2);
                        }
                    }
                    $('#artist-body-list').append(tableRow);
                });
            }
            else{
                //수집항목이 하나도 없을 때 editing 화면
                //항목 #번 인자 넘겨주기
                add_new_collect_target_item(len+1);
            }
            //맨 뒤에 스케줄 관련 row 붙이기
            append_schedule_row();
            var schedule_type = res.data["schedule_type"];
            if(schedule_type=="hour"){
                schedule_type = "시간별";
            }else if(schedule_type=="daily"){
                schedule_type = "일별";
            }
            document.getElementById("dropTitle").innerHTML = schedule_type;
        },
        error: e => {
            alert(e.responseText);
        },
    });
})

function check_schedule(schedule_type){
    document.getElementById("dropTitle").innerHTML = schedule_type;
}

function append_schedule_row(){
    const tableRow = $('<tr></tr>');
    for(var i=0;i<4;i++){
        let dataCol = document.createElement('td');
        if(i==0){
            dataCol.innerHTML = `
            <td>
                <span style="color: rgb(247, 78, 78);">
                스케줄
                </span>
            </td>`;
        }else if(i==1){
            dataCol.innerHTML = `
            <td>
                <div class="dropdown">
                    <button class="dropbtn" id="dropTitle"> 
                        선택
                    </button>
                    <div class="dropdown-content">
                        <div onclick="check_schedule('일별')">일별</div>
                        <div onclick="check_schedule('시간별')">시간별</div>
                    </div>
                </div>
            </td>`;
        }
        tableRow.append(dataCol);
    }
    $('#artist-body-list').append(tableRow);
}

// collect_target_delete
// $()

//update platform collect target
$(document).on('click','#save-list',function(){
    var bodydatas = [];
    var item_tr = $('#artist-body-list').find('tr');
    //마지막 열은 스케줄과 관련되었기 때문에 제외
    for(var r=0;r<item_tr.length-1;r++){
        console.log(item_tr[r].classList);
        if(item_tr[r].classList == 'hidden'){
            //숨겨져 있다면 삭제된 것이므로 제외
            continue;
        }
        var cells = item_tr[r].getElementsByTagName("td");
        var cells2 = item_tr[r].getElementsByTagName("textarea");
        if(cells[3].firstElementChild.value != "")
            bodydatas.push({
                "id": cells[0].firstElementChild.value,
                "collect_target": cells[1].firstElementChild.value,
                "target_name": cells[3].firstElementChild.value,
                "xpath": cells2[0].value,
            });
        else{
            alert("조사항목을 입력하세요.");
            return;
        }
    }
    var schedule_type = "daily";
    if(document.getElementById("dropTitle").innerHTML=="시간별"){
        schedule_type = "hour";
    }
    $.ajax({
        url: '/dataprocess/api/collect_target_item/',
        type: 'PUT',
        datatype:'json',
        data :JSON.stringify({
            "artist": document.getElementById("artist-subtitle").innerHTML.replace(" 플랫폼",""),
            "platform": clicked_platform,
            "items": bodydatas,
            "schedule_type": schedule_type
        }),
        contentType: 'application/json; charset=utf-8',
        success: res => {
            alert('저장되었습니다.');

        },
        error: e => {
            alert(e.responseText);
        },
    })
})

//항목 칸 추가
$(document).on('click','#url_add_button',function(){
    tr = $(this).closest('tr');
    var attri_col = $('<td style="display: flex;"><input class="add-target-input-2"  type="text" placeholder="URL 2" /></td>')
    //tr.find('td').find('.add-target-input-2').val()
    console.log(tr.find('td').find('input').length);
    if(tr.find('td').find('input').length <= 1){
        tr.append(attri_col)
    }else{
        alert("URL 은 최대 2개까지 입력 가능합니다.")
    }
})


$(document).on('click','#url_delete_button',function(){
    tr = $(this).closest('tr');
    //tr.find('td').find('.add-target-input-2').val()
    if(tr.find('td').find('input').length > 1){
        tr.find("td:last").remove();
    } else{
        alert("URL 을 한 개 이상 입력해주세요.")
    }
})

//delete collect_target_item (api상)
function delete_collect_target_item(id, index){
    if (confirm("삭제하시겠습니까?")) {
        var data = {"id": id};
        $.ajax({
            url: "/dataprocess/api/collect_target_item/",
            type: 'DELETE',
            datatype:'json',
            data: JSON.stringify(data),
            success: res => {
                alert('삭제되었습니다.');
                delete_screen_collect_target_item(index);
            },
            error: e => {
                alert(e.responseText);
            },
        });
    } 
};

function delete_collect_target_item_notindb(index){
    if (confirm("삭제하시겠습니까?")) {
        delete_screen_collect_target_item(index);
    } 
}

//delete collect_target_item (화면상)
function delete_screen_collect_target_item(index){
    //삭제하기: hidden 처리해서 숨기기
    var item_tr = $('#artist-body-list').find('tr');
    item_tr[index].setAttribute('class','hidden');
};

//수집항목 +버튼
$(document).on('click','#artist_attr_add_button',function(){
    var item_tr = $('#artist-body-list').find('tr');
    let len = item_tr.length;
    //스케줄 삭제
    item_tr[len-1].remove();
    //끝에 append
    add_new_collect_target_item(len);
    //스케줄 추가
    append_schedule_row();
})

var artist_open = true;
var platform_open = true;
var item_open = true;

function make_artist_hidden(){
    //아티스트 표 작게 처리
    artist_open = false;
    var artist_hiddens = document.getElementsByClassName("artist_hidden");
    for(var i=0;i<artist_hiddens.length;i++){
        let ii = i;
        artist_hiddens[ii].classList.add("tmp-hidden");
    }
    document.getElementById("artist_open").classList.add("fa-chevron-right");
    document.getElementById("artist_open").classList.remove("fa-chevron-left");;
}

function make_artist_visible(){
    //아티스트 표 다보이게 처리
    artist_open = true;
    var artist_hiddens = document.getElementsByClassName("artist_hidden");
    for(var i=0;i<artist_hiddens.length;i++){
        let ii = i;
        artist_hiddens[ii].classList.remove("tmp-hidden");
    }
    document.getElementById("artist_open").classList.remove("fa-chevron-right");
    document.getElementById("artist_open").classList.add("fa-chevron-left")
}

$("#artist_open_btn").click(function (){
    if(artist_open==true){
        make_artist_hidden();
    }else{
        make_artist_visible();
    }
});

function make_platform_hidden(){
    //플랫폼 표 작게 처리
    platform_open = false;
    var platform_hiddens = document.getElementsByClassName("platform_hidden");
    for(var i=0;i<platform_hiddens.length;i++){
        let ii = i;
        platform_hiddens[ii].classList.add("tmp-hidden");
    }
    document.getElementById("platform_open").classList.add("fa-chevron-right");
    document.getElementById("platform_open").classList.remove("fa-chevron-left");;
}

function make_platform_visible(){
    //플랫폼 표 다보이게 처리
    platform_open = true;
    var platform_hiddens = document.getElementsByClassName("platform_hidden");
    for(var i=0;i<platform_hiddens.length;i++){
        let ii = i;
        platform_hiddens[ii].classList.remove("tmp-hidden");
    }
    document.getElementById("platform_open").classList.remove("fa-chevron-right");
    document.getElementById("platform_open").classList.add("fa-chevron-left")
}

$("#platform_open_btn").click(function (){
    if(platform_open==true){
        make_platform_hidden();
    }else{
        make_platform_visible();
    }
});


function make_item_hidden(){
    //조사항목 표 작게 처리
    item_open = false;
    var item_hiddens = document.getElementsByClassName("item_hidden");
    for(var i=0;i<item_hiddens.length;i++){
        let ii = i;
        item_hiddens[ii].classList.add("tmp-hidden");
    }
    document.getElementById("item_open").classList.add("fa-chevron-right");
    document.getElementById("item_open").classList.remove("fa-chevron-left");
}

function make_item_visible(){
    //조사항목 표 다보이게 처리
    item_open = true;
    var item_hiddens = document.getElementsByClassName("item_hidden");
    for(var i=0;i<item_hiddens.length;i++){
        let ii = i;
        item_hiddens[ii].classList.remove("tmp-hidden");
    }
    document.getElementById("item_open").classList.remove("fa-chevron-right");
    document.getElementById("item_open").classList.add("fa-chevron-left");
}

$("#item_open_btn").click(function (){
    if(item_open==true){
        make_item_hidden();
    }else{
        make_item_visible();
    }
});
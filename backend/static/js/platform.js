function render_platform_table(data){//parsing한 데이터 화면에 render
    const tableRow = $('<tr></tr>')
    console.log(data);
    // 해당 row에 대한 column 데이터들 넣기
    for(key in data){
        let dataCol;
        if(key==='active'){
            if(data[key]==true){
                dataCol = $('<td><input checked type="checkbox"></input></td>'); 
            }else{
                dataCol = $('<td><input type="checkbox"></input></td>'); 
            }
        }else if(key=='name'){
            dataCol = document.createElement('td');
            dataCol.innerHTML = `
            <td>
                <input type="text" value="${data[key]}" style="width:100%; font-weight:bold;"></input>
            </td>
            `;
        }
        else{
            dataCol = document.createElement('td');
            if(key==='id')
                dataCol.setAttribute('class', 'hidden');
            dataCol.innerHTML = `
            <td>
                <input type="text" value="${data[key]}" style="width:100%"></input>
            </td>
            `;
        }
       
        tableRow.append(dataCol);
    }
    $('#platform-body').append(tableRow);
}

var platform_info = [];

function platform_read_function(){
    $.ajax({
        url: '/dataprocess/api/platform/',
        type: 'GET',
        datatype:'json',
        contentType: 'application/json; charset=utf-8',
        success: res => {
            const data_list = res.data;
            platform_info = data_list;
            $('#platform-body').empty();
            data_list.forEach(data => {//data를 화면에 표시
                render_platform_table(data);
            });
        },
        error: e => {
            alert(e.responseText);
        },
    })
};

function platform_update_function(){
    // document.getElementById("loading_form").style.display = "flex";
    var datas=[];
    var platform_tr = document.getElementById("platform-body").getElementsByTagName("tr");
    for(var r=0;r<platform_tr.length;r++){
        var cells = platform_tr[r].getElementsByTagName("td");
        if(cells[1].firstElementChild.value=="" || cells[2].firstElementChild.value==""){
            alert("플랫폼 이름과 URL을 입력해주세요");
            return;
        }
        // 달라진 것만 서버에 보내기
        if(platform_info[r]['name'] != cells[1].firstElementChild.value || platform_info[r]['url'] != cells[2].firstElementChild.value
        || platform_info[r]['description'] != cells[3].firstElementChild.value || platform_info[r]['active'] != cells[4].firstElementChild.checked){
            datas.push({
                "id": cells[0].firstElementChild.value,
                "name": cells[1].firstElementChild.value,
                "url": cells[2].firstElementChild.value,
                "description": cells[3].firstElementChild.value,
                "active": cells[4].firstElementChild.checked
            });
            // list에 update
            platform_info[r]['name'] = cells[1].firstElementChild.value;
            platform_info[r]['url'] = cells[2].firstElementChild.value;
            platform_info[r]['description'] = cells[3].firstElementChild.value;
            platform_info[r]['active'] = cells[4].firstElementChild.checked;
        }
    }
    console.log("datas");
    console.log(datas);
    $.ajax({
        url: '/dataprocess/api/platform/',
        type: 'PUT',
        datatype:'json',
        data: JSON.stringify(datas),
        success: res => {
            alert("저장되었습니다.");
            document.getElementById("loading_form").style.display = "none";
        },
        error: e => {
            alert(e.responseText);
            document.getElementById("loading_form").style.display = "none";
        },
    })
};

function platform_create_function(){
    var created_platform_tr = document.getElementById("platform_attribute").getElementsByTagName("tr");
    var created_attribute_tr = document.getElementById("crawling_attribute").getElementsByTagName("tr");
    var collect_items_list = [];
    for(var i=0;i<created_attribute_tr.length;i++){
        var collect_item = created_attribute_tr[i].getElementsByTagName("td")[1].firstElementChild.value;
        var xpath = created_attribute_tr[i].getElementsByTagName("td")[2].firstElementChild.value;
        if(collect_item!=""){
            collect_items_list.push(
                {"target_name": collect_item,
                "xpath": xpath}
            );
        }
    }
    if(created_platform_tr[0].getElementsByTagName("td")[1].firstElementChild.value==""){
        alert("필수값을 모두 입력하세요.");
        return;
    }else if(created_platform_tr[1].getElementsByTagName("td")[1].firstElementChild.value==""){
        alert("필수값을 모두 입력하세요.");
        return;
    }else if(collect_items_list.length == 0){
        alert("필수값을 모두 입력하세요.");
        return;
    }
    document.getElementById("loading_form").style.display = "flex";
    var data = {
        "name":created_platform_tr[0].getElementsByTagName("td")[1].firstElementChild.value,
        "url":created_platform_tr[1].getElementsByTagName("td")[1].firstElementChild.value,
        "description":created_platform_tr[2].getElementsByTagName("td")[1].firstElementChild.value,
        "collect_items": collect_items_list
    };

    $.ajax({
        url: '/dataprocess/api/platform/',
        type: 'POST',
        datatype:'json',
        data: JSON.stringify(data),
        success: res => {
            console.log(res);
            alert("저장되었습니다.");
            document.getElementById("loading_form").style.display = "none";
            //reload-page
            location.reload();
        },
        error: e => {
            console.log(e);
            alert(e.responseText);
            document.getElementById("loading_form").style.display = "none";
        },
    });
    close_form_function();
};

//popup form opan, close
function open_form_function(e) {
    document.getElementById("create_form").style.display = "flex";
}
  
function close_form_function() {
    //입력된 내용 지우기
    var created_platform_tr = document.getElementById("platform_attribute").getElementsByTagName("tr");
    created_platform_tr[0].getElementsByTagName("td")[1].firstElementChild.value="";
    created_platform_tr[1].getElementsByTagName("td")[1].firstElementChild.value="";
    created_platform_tr[2].getElementsByTagName("td")[1].firstElementChild.value="";
    var created_attribute_tr = document.getElementById("crawling_attribute").getElementsByTagName("tr");
    const len = created_attribute_tr.length;
    for(var i=0;i<len;i++){
        if(i>0)
            document.getElementById("crawling_attribute").deleteRow(-1);
        else{
            created_attribute_tr[i].getElementsByTagName("td")[1].firstElementChild.value="";
            created_attribute_tr[i].getElementsByTagName("td")[2].firstElementChild.value="";
        }
    }
    document.getElementById("create_form").style.display = "none";
}

//항목 칸 추가
function add_attribute_function(){
    var attribute_num = document.getElementById("crawling_attribute").getElementsByTagName("tr");
    var attributeCol = document.createElement('tr');
    attributeCol.innerHTML = `
    <td>항목${attribute_num.length+1}</td>
    <td><input type="text" value="" style="width:100%"></input></td>
    <td><input type="text" value="" style="width:100%"></input></td>
    `;
    document.getElementById("crawling_attribute").append(attributeCol);
}

//마지막 항목 칸 삭제
function delete_attribute_function(){
    if(document.getElementById("crawling_attribute").getElementsByTagName("tr").length>1)
        document.getElementById("crawling_attribute").deleteRow(-1);
}

//first read platforms
//excel로부터 데이터 받은 게 있다면 그걸 보여주기
if(document.getElementById('import_data')){
    $('#platform-body').empty();
    var excel_objects = document.getElementById('import_data').innerHTML;
    excel_objects = eval('(' + excel_objects + ')');
    excel_objects.forEach(data => {//data를 화면에 표시
        render_platform_table(data);
    });
}
//excel로부터 받은 data를 보여주는 게 아니라면 DB 데이터 보여주기
else{
    platform_read_function();
}
document.getElementById('update_button').onclick = platform_update_function;
document.getElementById('openform_button').onclick = open_form_function;
document.getElementById('close_button').onclick = close_form_function;
document.getElementById('create_button').onclick = platform_create_function;
document.getElementById('attr_add_button').onclick = add_attribute_function;
document.getElementById('attr_delete_button').onclick = delete_attribute_function;
const isEmpty = 
    function(value){ 
        if( value == "" || value == null || value == undefined || ( value != null && typeof value == "object" && !Object.keys(value).length ) ){ 
            return true 
        }else{ 
                return false 
        } 
    };


//artist create function
$('.add-submit').click(function(e){
    var th = $('.add-table').find('th'); //platform names
    var trs_value = $('input[type=text]');  //artist info

    var platform_names = []
    for(var i = 2; i < th.length ; i++){
        platform_names.push(th[i].innerHTML);
    }

    var urls = [];
    for(var i=7;i<trs_value.length;i++){
        var collect_item = trs_value[i].value;
        if(collect_item !="" && !collect_item.startsWith("http") && !collect_item.startsWith("www") ){
            alert("데이터 수집 URL의 형식이 잘못되었습니다.");
            e.preventDefault();
            return;
        }
        urls.push(collect_item);
           
    }

    var charRe = /^[a-z]|[A-Z]$/;

    var target_urls = {};
    for( var i = 0; i<platform_names.length; i++){
        target_urls[platform_names[i]] = urls[i];
    }
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
        "urls": urls,
    };
    if(trs_value[6].value!=""){
        data["debut_date"] = trs_value[6].value;
    }

    console.log(JSON.stringify(data));

    $.ajax({
        url: "/dataprocess/api/artist/",
        type: 'POST',
        datatype:'json',
        data: JSON.stringify(data),
        success: res => {
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
            "member_num": cells[4].firstElementChild.value,
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
            console.log(res);
            alert("Successfully save!");
        },
        error: e => {
            console.log(e);
            alert(e.responseText);
        },
    })
})

//show platforms per artist
$('input[name=artist-name]').click(function(){
    var artist = $(this).val();

    console.log(artist);

    $.ajax({
        url: '/dataprocess/api/platform_of_artist/',
        type: 'GET',
        datatype:'json',
        data : {'artist':artist},
        contentType: 'application/json; charset=utf-8',
        success: res => {
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
                            dataCol = $('<td><input checked type="checkbox"></input></td>'); 
                        }else{
                            dataCol = $('<td><input type="checkbox"></input></td>'); 
                        }
                    } else if(key === 'name'){
                        dataCol = document.createElement('td');
                        dataCol.innerHTML = `
                        <td>
                            <span class="platform-names" style="width:100%; cursor:pointer;">${data[key]}</span>
                        </td>
                        `;
                    } 
                    else{
                        dataCol = document.createElement('td');
                        if(key === 'artist_id' || key==='id' || key==='platform_id')
                            dataCol.setAttribute('class', 'hidden');
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
            console.log(res);
            alert("Successfully save!");
        },
        error: e => {
            console.log(e);
            alert(e.responseText);
        },
    })
    
})

//show collect target of platform
$(document).on('click','.platform-names',function(){
    //console.log('clicked');

    var artist_name = document.getElementById("artist-subtitle").innerHTML.replace(" 플랫폼","");
    // var artist_id = $('.hidden').find('input').val();
    var platform = $(this).text();

    $.ajax({
        url: '/dataprocess/api/collect_target_item/',
        type: 'GET',
        datatype:'json',
        data : {'platform': platform, 'artist': artist_name},
        contentType: 'application/json; charset=utf-8',
        success: res => {
            document.getElementById("platform-subtitle").innerHTML = artist_name+" "+ platform+ " 조사항목";

            const data_list = res.data;
            console.log(data_list);
            $('#artist-body-list').empty();
            data_list.forEach(data=>{//data를 화면에 표시
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
                    }else if(key==='target_name'){
                        dataCol = document.createElement('td');
                        dataCol.innerHTML = `
                        <td>
                            <input type="text" title="${data[key]}" value="${data[key]}" style="width:100%"></input>
                        </td>
                        `;
                        tableRow.append(dataCol);
                    }else if(key==='xpath'){
                        dataCol = document.createElement('td');
                        dataCol.innerHTML = `
                        <td>
                            <textarea style="width:100%">${data[key]}</textarea>
                        </td>
                        `;
                        tableRow.append(dataCol);
                    }
                }
                $('#artist-body-list').append(tableRow);
            });
        },
        error: e => {
            alert(e.responseText);
        },
    })
})

//update platform collect target
$(document).on('click','#save-list',function(){
    var bodydatas = [];

    var item_tr = $('#artist-body-list').find('tr');
    for(var r=0;r<item_tr.length;r++){
        var cells = item_tr[r].getElementsByTagName("td");
        var cells2 = item_tr[r].getElementsByTagName("textarea");
        bodydatas.push({
            "id": cells[0].firstElementChild.value,
            "collect_target": cells[1].firstElementChild.value,
            "target_name": cells[2].firstElementChild.value,
            "xpath": cells2[0].value,
        });
    }
    $.ajax({
        url: '/dataprocess/api/collect_target_item/',
        type: 'PUT',
        datatype:'json',
        data :JSON.stringify(bodydatas),
        contentType: 'application/json; charset=utf-8',
        success: res => {
            alert('Successfully saved!');

        },
        error: e => {
            alert(e.responseText);
        },
    })
})
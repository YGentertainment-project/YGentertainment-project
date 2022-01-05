//artist create function
$('.add-submit').click(function(){
    var th = $('.add-table').find('th'); //platform names
    var trs_value = $('input[type=text]');  //artist info

    var platform_names = []
    for(var i = 2; i < th.length ; i++){
        platform_names.push(th[i].innerHTML);
    }

    var urls = [];
    for(var i=7;i<trs_value.length;i++){
        var collect_item = trs_value[i].value;
        if(collect_item!="")
           urls.push(collect_item)
    }

    var target_urls = {};
    for( var i = 0; i<platform_names.length; i++){
        target_urls[platform_names[i]] = urls[i];
    }

    var data = {
        "name": trs_value[0].value,
        "level": trs_value[1].value,
        "gender": trs_value[2].value,
        "member_num": trs_value[3].value,
        "member_nationality": trs_value[4].value,
        "agency":trs_value[5].value,
        "debut_date": trs_value[6].value,
        "urls": urls,
    };

    console.log(JSON.stringify(data));
    $.ajax({
        url: "/dataprocess/api/artist/",
        type: 'POST',
        datatype:'json',
        data: JSON.stringify(data),
        success: res => {
            console.log(res);
            console.log('success');
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

        datas.push({
            "id": cells[0].firstElementChild.value,
            "name": cells[1].firstElementChild.value,
            "level": cells[2].firstElementChild.value,
            "gender": cells[3].firstElementChild.value,
            "member_num": cells[4].firstElementChild.value,
            "member_nationality": cells[5].firstElementChild.value,
            "agency":cells[6].firstElementChild.value,
            "debut_date": cells[7].firstElementChild.value,
            "active": cells[8].firstElementChild.value
        });
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

    //console.log(artist);

    $.ajax({
        url: '/dataprocess/api/platform_of_artist/',
        type: 'GET',
        datatype:'json',
        data : {'artist':artist},
        contentType: 'application/json; charset=utf-8',
        success: res => {
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
                        if(key === 'artist_id' || key==='id')
                            dataCol.setAttribute('class', 'hidden');
                        dataCol.innerHTML = `
                        <td>
                            <input type="text" value="${data[key]}" style="width:100%"></input>
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
            "id": cells[1].firstElementChild.value,
            "platform": cells[2].firstElementChild.innerHTML,
            "target_url": cells[3].firstElementChild.value,
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

    var artist = $('.hidden').find('input').val();
    var platform = $(this).text();

    console.log(artist);
    console.log(platform);

    $.ajax({
        url: '/dataprocess/api/collect_target_item/',
        type: 'GET',
        datatype:'json',
        data : {'artist':artist, 'platform':platform},
        contentType: 'application/json; charset=utf-8',
        success: res => {
            const data_list = res.data;
            console.log(data_list);
            $('#artist-body-list').empty();
            const tableRow = $('<tr></tr>')
            let dataHTML = [];
            data_list.forEach(data => {//data를 화면에 표시
                for(key in data){
                    if(key !=='target_name'){
                        continue;
                    }
                    else{
                        dataHTML.push( `
                        <td>
                            <input type="text" value="${data[key]}" style="width:100%"></input>
                        </td>
                        `);
                    }
                }
            });
            for(let i = 0; i<dataHTML.length; i++){
                dataCol = document.createElement('td');
                dataCol.innerHTML = dataHTML[i];
                tableRow.append(dataCol);
            }
            $('#artist-body-list').append(tableRow);

        },
        error: e => {
            alert(e.responseText);
        },
    })
})
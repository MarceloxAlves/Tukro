var API_BASE = 'http://' + window.location.host + '/v1/';
var csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function DeletePostagem(id_postagem) {
    var url = API_BASE + 'postagens/' + id_postagem + '/delete';
    $.ajax({
        type: 'DELETE',
        url: url,
        headers: {'X-CSRFToken': csrftoken},
        data: {},
        success: function () {
            $('#postagem' + id_postagem).fadeOut(500);
        }
    });
}

function reaction(postagem_id, r) {
    alert(postagem_id)
    var url = API_BASE + 'postagens/' + postagem_id + '/reagir/'+r;
    $.ajax({
        type: 'GET',
        url: url,
        data: {},
        success: function (data) {
            $( "#postagem"+postagem_id+"reaction").text(data.total)
            $( "#container"+postagem_id+"reaction").html(
                '<i style="color:'+data.tipo.color+'" class="'+data.tipo.icon+'" aria-hidden="true"></i> '+ data.tipo.label
            )

        }
    });
}


function fileValidation(filePath){
    var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
    if(!allowedExtensions.exec(filePath)){
        return false;
    }
    return true
}
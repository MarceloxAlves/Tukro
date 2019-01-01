var API_BASE = 'http://'+window.location.host + '/v1/';
var csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
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
        headers: { 'X-CSRFToken': csrftoken},
        data: {},
        success: function () {
            $('#postagem' + id_postagem).fadeOut(500);
        }
    });
}
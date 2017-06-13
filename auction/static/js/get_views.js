$(function() {
    $('#get_views').on('click', function(event) {
        var lot_id = $(this).attr('data-ad-id');
        console.log('show_views');
        request_user_phone(lot_id);
    });

    function request_user_phone(lot_id) {
        console.log('request_user_phone');
        $.ajax({
            url : '/get_views/',
            type : 'POST',
            data : { lot_id: lot_id,
                     csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value },
            success : function (json) {
                $('#user_views').text('Просмотров: '+json['views']);
                console.log("success");
            },
            error : function(xhr, errmsg, err) {
                console.log(xhr.status + ' ' + xhr.responseText);
            }
        });
    };
});
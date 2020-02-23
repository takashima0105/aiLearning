function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

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


jQuery(function($) {
    $(document).ajaxSend(function() {
        $("#overlay").fadeIn(300);　
    });

    // 送信ボタンで呼ばれる
    $("form").submit(function(event) {
        // デフォルトのイベントをキャンセルし、ページ遷移しないように!
        event.preventDefault();

        var form = $(this);
        var formData = new FormData($(this).get(0));
        $.ajax({
                url: form.prop("action"),
                type: 'POST',
                processData: false,
                contentType: false,
                data: formData,
            })
            .done(function(data) {
                $("#chart_and_run").html(data);

                setTimeout(function() {
                    $("#overlay").fadeOut(300);
                }, 500);

            });
    });
});

window.onload = function() {

    function thisID(id) {
            return document.getElementById(id)
        }

    function showHide(id, id2='', type="block") {

        // toggles visibility

        var e = thisID(id);
        var e2 = thisID(id2);

        if (e.style.display === type) {
            e.style.display = "none";
        } else {
            e.style.display = type;
            e2.style.display = "none";
        }
    }

    thisID('delBtn').onclick =
        function() {showHide('areyousure', 'createGameForm', "inline")};

    thisID('sure-no').onclick =
            function() {showHide('areyousure', 'areyousure')};

    thisID('createBtn').onclick =
        function() {showHide('createGameForm', 'areyousure')};

    function scrollDivUp(id) {
            thisID(id).scrollTop = thisID(id).scrollHeight;
        }

    scrollDivUp('chat-msgs-container')


// #######################
// ###### AJAX FORM ######
// #######################

    $('#chat-form').on('submit', function(event){
        event.preventDefault();

        $.ajax({
            url: '/chat_post/',
            type: 'POST',
            data: { chat_msg: $('#chat-msg').val(),
                    chat_room: $('#chat-room').val()},

            success: function(json){

                $('#chat-msg').val('');
                $('#chat-ul-msgs').append(

                    '<li class="chat-li-msgs">' +
                        '<div class="form-container chat-1msg-container"' +
                             'id="chat-name-color">' +
                             '<span id="chat-username">' + 'YOU:' +
                            '</span>' + json.msg +
                        '</div>' +
                    '</li>'
                );

                scrollDivUp('chat-msgs-container');
            }
        });
    });

    function getMessages(){

        if (!scrolling) {
            $.get('/messages_ajax/' + $('#chat-room').val(), function(resp){

                if (resp === 'No new messages.') {
                    //console.log('No new messages.')
                    return;
                }

                $('#chat-ul-msgs').html(resp);
                //console.log('new messages rendered...');

                scrollDivUp('chat-msgs-container');
            });
        }
        scrolling = false;
    }

    var scrolling = false;
    $(function(){
        $('#chat-msgs-container').on('scroll', function(){
            scrolling = true;
        });

        refreshTimer = setInterval(getMessages, 1000);
    });


// -----------------------------------------------------------------------
// CSRF token (https://docs.djangoproject.com/en/2.2/ref/csrf/)
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
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
};

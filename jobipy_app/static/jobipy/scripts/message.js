$(document).ready(function () {
    $('#send-button').prop('disabled', true)
    retrieve_conversation($('#group-name').val())
})

function websockets(chat_mate_id, current_user, conversation_id) {
    let url_chat = `ws://${window.location.host}/ws/chat/${$('#group-name').val()}/`
    let url_notif = `ws://${window.location.host}/ws/notif/${chat_mate_id}/`
    const messageSocket = new WebSocket(url_chat)
    const notifSocket = new WebSocket(url_notif)

    messageSocket.onmessage = e => {
        let data = JSON.parse(e.data)
        const isCurrentUser = data['current_user'] === current_user;

        setTimeout(() => {
            if (!isCurrentUser) {
                read_message(conversation_id)
            }
        }, 500)

        const $message_div = $('<div>', {
            class: 'message-div',
            text: data['message'],
            css: isCurrentUser ? { marginLeft: 'auto' } : { marginRight: 'auto' }
        })

        $('#message-textarea').val('')
        $('#messages-div').append($message_div)
        $('#messages-div').scrollTop($('#messages-div')[0].scrollHeight);
    }

    $('#message-textarea').on('keydown', function (event) {
        if (event.key === 'Enter') {
            if (event.shiftKey) {
                return
            }
            else {
                event.preventDefault();
                if ($('#message-textarea').val()) {
                    send_message(conversation_id, $('#message-textarea').val());
                    messageSocket.send(JSON.stringify({
                        'message': $('#message-textarea').val(),
                        'current_user': current_user
                    }));
                    notifSocket.send(JSON.stringify({
                        'notif': true
                    }));
                }
            }
        }
    });

    $('#message-textarea').on('input', function () {
        if ($('#message-textarea').val().trim()) {
            $('#send-button').prop('disabled', false)
        } else {
            $('#send-button').prop('disabled', true)
        }
    });

    $('#send-button').on('click', function () {
        send_message(conversation_id, $('#message-textarea').val())
        messageSocket.send(JSON.stringify({
            'message': $('#message-textarea').val(),
            'current_user': current_user
        }))
        notifSocket.send(JSON.stringify({
            'notif': true
        }))
    })
}

function send_message(conversation_id, message) {
    $.ajax({
        type: "POST",
        url: "/api/message",
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(),
        },
        data: JSON.stringify({
            conversation_id: conversation_id,
            message: message
        })
    });
}

function read_message(conversation_id) {
    $.ajax({
        type: "PUT",
        url: `/api/message/read`,
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(),
        },
        data: JSON.stringify({
            id: conversation_id
        })
    })
}

function retrieve_conversation(group_name) {
    $.ajax({
        type: "GET",
        url: `/api/retrieve/conversation/group/${group_name}`,
        success: function (result) {
            if (result['message'] === 'Success') {
                websockets(result['chatmate']['id'], result['current_user']['name'], result['id'])
                setTimeout(() => {
                    read_message(result['id'])
                }, 500)
                $('#convo-container-div').show()
                $('#chat-mate-p').text(result['chatmate']['name'])
                result['messages'].forEach(message => {
                    const isCurrentUser = message['sender']['name'] === result['current_user']['name'];
                    const $message_div = $('<div>', {
                        class: 'message-div',
                        text: message['message'],
                        css: isCurrentUser ? { marginLeft: 'auto' } : { marginRight: 'auto' }
                    })
                    $('#messages-div').append($message_div)
                    $('#messages-div').scrollTop($('#messages-div')[0].scrollHeight);
                })
            }
            else {
                $('#no-messages-div').show()
            }
        }
    });
}
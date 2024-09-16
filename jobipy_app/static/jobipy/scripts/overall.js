let user_id = 0

$(document).ready(function () {
    fetch_user();
    get_notif()

    $('#logout-a').on('click', fetch_logout)
    $('#logout-a-big').on('click', fetch_logout)
    $('#notification-icon-div').on('click', function () {
        view_status(user_id)
    })
})

function fetch_logout() {
    $.ajax({
        url: '/api/logout',
        method: 'GET',
        success: function (result) {
            if (result['message'] === 'Logout Successfully') {
                window.location.href = '/';
            }
        },
        error: function (xhr, status, error) {
            console.error('Error logging out:', error);
        }
    });
}

function fetch_user() {
    $.ajax({
        url: '/api/user',
        method: 'GET',
        success: function (result) {
            if (result['message'] === 'Successful') {
                notifSocket(result['id'])
                user_id = result['id']
                $('#name-div').text(result['name']);

                if (window.location.pathname === '/profile') {
                    $('#name-p').text(result['name']);
                    $('#city-p').text(result['city']);
                    $('#email-p').html(`<strong>Email:</strong> ${result['email']}`);
                    $('#contact-no-p').html(`<strong>Contact No.:</strong> ${result['contact_number']}`);
                }
            } else {
                window.location.href = '/';
            }
        }
    });
}

function get_notif() {
    $.ajax({
        type: "GET",
        url: "/api/notification",
        success: function (result) {
            if (result['message'] === 'Success') {
                result['message_notification']['all_messages'].forEach(convo => {
                    const isCurrentUserSender = user_id === convo['sender']['id']
                    const msg_div = $('<div>', {
                        class: 'msg-div',
                        css: {
                            backgroundColor: isCurrentUserSender ? 'white' : (convo['is_read'] ? 'white' : '#c4c4c4'),
                        }
                    })
                    msg_div.hover(
                        function () {
                            $(this).css({
                                'background-color': '#0CB83C',
                            })
                        },
                        function () {
                            $(this).css({
                                'background-color': isCurrentUserSender ? 'white' : (convo['is_read'] ? 'white' : '#c4c4c4'),
                            })
                        }
                    );
                    const sender_span = $('<span>', {
                        text: convo['sender']['name']
                    })
                    const message_p = $('<p>', {
                        text: convo['message']
                    })
                    const message_time_p = $('<p>', {
                        class: 'time-p',
                        text: convo['time'],
                    })

                    msg_div.on('click', () => {
                        read_message(convo['id'])
                        window.location.href = `/message/${convo['group_name']}`
                    })
                    msg_div.append(sender_span, message_p, message_time_p)
                    $('#messages-div-header').append(msg_div)
                })

                result['status_notification']['notifications'].forEach(status => {
                    const msg_div = $('<div>', {
                        class: 'status-div',
                        css: {
                            backgroundColor: status['status_viewed'] ? 'white' : '#c4c4c4',
                        }
                    })
                    msg_div.hover(
                        function () {
                            $(this).css({
                                'background-color': '#0CB83C',
                            })
                        },
                        function () {
                            $(this).css({
                                'background-color': status['status_viewed'] ? 'white' : '#c4c4c4',
                            })
                        }
                    );
                    const sender_span = $('<span>', {
                        text: status['company']
                    })
                    const message_p = $('<p>', {
                        text: status['status']
                    })
                    msg_div.on('click', () => {
                        window.location.href = `/activities`
                    })
                    msg_div.append(sender_span, message_p)
                    $('#notifications-div-header').append(msg_div)
                })

                notif_count(result['message_notification']['notif_count'], 'message', 'message-icon-div')
                notif_count(result['status_notification']['notif_count'], 'status', 'notification-icon-div')
            }
        }
    });
}

function notif_count(count, notif_type, icon) {
    const notif = $('<div>', {
        id: `${notif_type}-notif-div`,
        text: count,
        css: {
            backgroundColor: '#4A90E2',
            width: 'fit-content',
            paddingLeft: '0.5em',
            paddingRight: '0.5em',
            color: 'white',
            textAlign: 'center',
            borderRadius: '10px',
            marginLeft: '1.5em',
            marginBottom: '1em'
        }
    })
    if (count > 0) {
        $('#nav-div').css({
            'column-gap': '2em',
        })
        $(`#${icon}`).append(notif)
    }
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

function view_status() {
    let url_notif = `ws://${window.location.host}/ws/notif/${user_id}/`
    const notifSocket = new WebSocket(url_notif)
    $.ajax({
        type: "PUT",
        url: `/api/application/status`,
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(),
        },
        success: function () {
            notifSocket.send(JSON.stringify({
                'notif': true
            }));
        }
    })
}

function notifSocket(id) {
    let url_notif = `ws://${window.location.host}/ws/notif/${id}/`
    const notifSocket = new WebSocket(url_notif)

    notifSocket.onmessage = e => {
        setTimeout(() => {
            $('#message-notif-div').remove()
            $('#status-notif-div').remove()
            $('.msg-div').remove()
            $('.status-div').remove()
            get_notif()
        }, 500)
    }
}
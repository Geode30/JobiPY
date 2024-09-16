$(document).ready(function () {
    $('#sign-in').on('click', function () {
        window.location.href = '/login';
    });

    $('#sign-up-form').on('submit', function (event) {
        event.preventDefault();
        $.ajax({
            url: '/api/register',
            type: 'POST',
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(),
            },
            data: JSON.stringify({
                firstname: $('#first-name-input').val(),
                lastname: $('#last-name-input').val(),
                email: $('#email-input').val(),
                password: $('#password-input').val(),
                confirmPass: $('#confirm-pass-input').val()
            }),
            contentType: 'application/json',
            success: function (result) {
                if (!result) {
                    message('There is something wrong on our end', 'danger');
                }

                if (result.message === 'User Created Successfully') {
                    message(result.message, 'success');

                    setTimeout(function () {
                        window.location.href = '/login';
                    }, 1200);
                } else {
                    message(result.message, 'danger');
                }
            }
        });
    });
});

function message(msg, color) {
    $('#message-div').remove();
    const messageDiv = $('<div>', {
        id: 'message-div',
        class: `alert alert-${color}`,
        text: msg,
        css: { marginTop: '1em' }
    });

    $('#content').append(messageDiv);
    $('html, body').scrollTop($(document).height());
}
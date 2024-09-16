$(document).ready(function () {
    $('#sign-up').on('click', function () {
        window.location.href = '/register';
    });

    $('#sign-in-form').on('submit', function (event) {
        event.preventDefault();
        $.ajax({
            url: `/api/login/${$('#email-input').val()}/${$('#password-input').val()}`,
            method: 'GET',
            success: function (result) {
                if (!result) {
                    message('There is something wrong on our end', 'danger');
                } else if (result.message === 'Login Successful') {
                    message(result.message, 'success');
                    if (result['preferences']) {
                        window.location.href = '/jobs';
                    } else {
                        window.location.href = '/setup';
                    }
                } else {
                    message(result.message, 'danger');
                }
            },
            error: function () {
                message('Invalid email', 'danger');
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
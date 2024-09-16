$(document).ready(function () {

    const fileInput = $('#myFileInput');
    const fileLabel = $('.custom-file-button');

    fileInput.on('change', function (event) {
        const fileName = event.target.files[0].name;
        fileLabel.text(fileName);
        $('#save-button').show();
    });

    $('#edit-button').on('click', function () {
        window.location.href = '/setup';
    })

    $('#save-button').on('click', () => {
        update_resume()
    })
})

function update_resume() {
    var formData = new FormData();
    formData.append('resume', $('#myFileInput')[0].files[0]);

    $('#loading-div').show();
    $('#content').hide();

    $.ajax({
        url: '/api/replace/resume',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(),
        },
        success: function (result) {
            if (result.message === 'Resume Replaced Successfully') {
                message(result.message, 'success');
            } else {
                message(result.message, 'danger');
            }
        },
        error: function () {
            message('An error occurred. Please try again.', 'danger');
        },
        complete: function () {
            window.location.href = '/profile';
        }
    });
}

function message(msg, color) {
    $('#message-div').remove();

    const messageDiv = $('<div>', {
        id: 'message-div',
        class: `alert alert-${color}`,
        text: msg,
        css: {
            marginTop: '1em'
        }
    })
    $('#info-div').append(messageDiv)
}
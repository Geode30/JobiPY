let preferences_available = false;

document.addEventListener('DOMContentLoaded', () => {
    fetch_user()

    $('#menu-div-big').hide()

    $.ajax({
        url: '/api/preferences',
        method: 'GET',
        success: function (result) {
            if (result['response'] === 'Successful') {
                preferences_available = true;
                $('#menu-div-big').show()

                $('#industry').val(result['industry']);
                $('#minimum-pay-input').val(result['minimum_base_pay']);
                $('#per').val(result['per']);
                $('#currency').val(result['currency']);
                $('#contact-input').val(result['contact_number']);
                $('#city-input').val(result['city']);
                $('#resume-div').css('display', 'none');

                let job_types = [];

                try {
                    job_types = result['job_type'].split(',');
                } catch (error) {
                    job_types = result['job_type'];
                }

                if (job_types.length > 0) {
                    job_types.forEach(function (job_type) {
                        $('input[type="checkbox"]').each(function () {
                            if ($(this).val() === job_type) {
                                $(this).prop('checked', true);
                            }
                        });
                    });
                }
            }

            if (!preferences_available) {
                $('#nav-div').hide()
            }
        },
        error: function (xhr, status, error) {
            console.error('Error fetching preferences:', error);
        }
    });

    const $fileInput = $('#myFileInput');
    const $fileLabel = $('.custom-file-button');

    $fileInput.on('change', function (event) {
        const fileName = event.target.files[0].name;
        $fileLabel.text(fileName);
    });

    $('#content').on('submit', function (event) {
        event.preventDefault();
        const formData = new FormData();
        let checkedCheckboxes = [];

        $('input[type="checkbox"]:checked').each(function () {
            checkedCheckboxes.push($(this).val());
        });

        formData.append('industry', $('#industry').val());
        formData.append('minimum_base_pay', $('#minimum-pay-input').val());
        formData.append('currency', $('#currency').val());
        formData.append('per', $('#per').val());
        formData.append('job_type', [checkedCheckboxes]);
        formData.append('email', $('#email-input').val());
        formData.append('name', $('#name-input').val());
        formData.append('contact_number', $('#contact-input').val());
        formData.append('city', $('#city-input').val());

        if (!preferences_available) {
            formData.append('resume', $fileInput[0].files[0]);
            fetch_preferences('POST', '/jobs', formData);
        } else {
            fetch_preferences('PUT', '/profile', JSON.stringify({
                'industry': $('#industry').val(),
                'minimum_base_pay': $('#minimum-pay-input').val(),
                'currency': $('#currency').val(),
                'per': $('#per').val(),
                'job_type': checkedCheckboxes,
                'email': $('#email-input').val(),
                'name': $('#name-input').val(),
                'contact_number': $('#contact-input').val(),
                'city': $('#city-input').val()
            }));
        }
    });
})

function disable_input(input, value) {
    const $input = $(`#${input}`);
    $input.val(value);
    $input.css({
        'background-color': '#e0e0e0',
        'pointer-events': 'none',
        'color': '#666'
    });
}

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

function fetch_user() {
    $.ajax({
        url: '/api/user',
        type: 'GET',
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(),
        },
        contentType: 'application/json',
        success: function (result) {
            if (result['message'] === 'Successful') {
                disable_input('name-input', result['name']);
                disable_input('email-input', result['email']);
            }
            else {
                window.location.href = '/';
            }
        }
    })
}

async function fetch_preferences(method, destination, formData) {
    document.querySelector('#loading-div').style.display = 'flex';
    document.querySelector('#content').style.display = 'none';
    await fetch('/api/setup', {
        method: method,
        headers: {
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
        },
        credentials: 'same-origin',
        body: formData
    }).then(response => response.json()).then(result => {
        document.querySelector('#loading-div').style.display = 'none';
        if (result.message === 'Preferences Created Successfully' || result.message === 'Preferences Updated Successfully') {
            document.querySelector('#content').style.display = 'flex';
            message(result.message, 'success');
            setTimeout(() => {
                window.location.href = destination;
            }, 2000)
        }
        else {
            message(result.message, 'danger');
        }
    })
}
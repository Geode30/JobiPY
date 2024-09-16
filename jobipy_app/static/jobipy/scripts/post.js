document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#post-form').addEventListener('submit', event => {
        event.preventDefault();
        var formData = new FormData();
        let checkedCheckboxes = [];

        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            if (checkbox.checked) {
                checkedCheckboxes.push(checkbox.value);
            }
        })

        formData.append('industry', document.querySelector('#industry').value);
        formData.append('minimum_base_pay', document.querySelector('#minimum-pay-input').value);
        formData.append('currency', document.querySelector('#currency').value);
        formData.append('per', document.querySelector('#per').value);
        formData.append('job_type', checkedCheckboxes);
        formData.append('company', document.querySelector('#company-name-input').value);
        formData.append('job_title', document.querySelector('#job-title-input').value);
        formData.append('city', document.querySelector('#city-input').value)
        formData.append('description', document.querySelector('#description-input').value)

        fetch('/api/post', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
            },
            credentials: 'same-origin',
            body: formData
        }).then(response => response.json()).then(result => {
            if (result['message'] === 'Job Post Successfully Created') {
                message(result['message'], 'success');
                window.location.href = '/jobs';
            }
            else {
                message(result['message'], 'danger');
            }
        })
    })
})

function message(msg, color) {
    $('#message-div').remove()

    const $messageDiv = $('<div>', {
        id: 'message-id',
        text: msg,
        class: `alert alert-${color}`,
        css: {
            marginTop: '1em'
        }
    })

    $('#post-form').append($messageDiv);
    $('html, body').scrollTop($(document).height());
}
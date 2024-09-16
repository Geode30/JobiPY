$(document).ready(function () {
    get_posted_jobs()
    $('#post-button').on('click', function () {
        window.location.href = '/post'
    })
})

function get_posted_jobs() {
    $.ajax({
        type: "GET",
        url: "/api/posted",
        success: function (result) {
            if (result['jobs'].length > 0) {
                $('#desc-title').text('Select a Job Post')
            }
            else {
                $('#desc-title').text('No Posted Jobs')
            }
            result['jobs'].forEach(job => {
                get_jobs(job)
            })
        }
    });
}

function get_resume(id, job_id) {
    $.ajax({
        type: "GET",
        url: `api/resume/${id}/${job_id}`,
        success: function (result) {
            view_status(id)
            $('#resume-div').show()
            $('#resume-img').attr('src', result['resume_path']);
            $('#status').val(result['application_status'])
        }
    });
}

function view_status(id) {
    let url_notif = `ws://${window.location.host}/ws/notif/${id}/`
    const notifSocket = new WebSocket(url_notif)
    setTimeout(() => {
        notifSocket.send(JSON.stringify({
            'notif': true
        }));
    }, 1000)
}

function generate_group_name(id, job_id) {
    $.ajax({
        type: "GET",
        url: "/api/group",
        success: function (result) {
            retrieve_conversation(id, job_id, result['group_name'])
        }
    });
}

function create_conversation(group_name, id, job_id) {
    $.ajax({
        type: "POST",
        url: '/api/conversation',
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(),
        },
        data: JSON.stringify({
            'group_name': group_name,
            'id': id,
            'job_id': job_id
        }),
        success: function (result) {
            if (result['message'] === 'Conversation Created Successfully') {
                window.location.href = `/message/${group_name}`
            }
        }
    });
}

function retrieve_conversation(id, job_id, group_name) {
    $.ajax({
        type: "GET",
        url: `/api/retrieve/conversation/id/${id}/${job_id}`,
        success: function (result) {
            if (result['message'] === 'Success') {
                window.location.href = `/message/${result['group_name']}`
            }
            else {
                create_conversation(group_name, id, job_id)
            }
        }
    });
}

function get_jobs(job) {
    const $div = $('<div>', { class: 'job-post-div' });

    const $jobTitle = $('<p>').text(job['job_title']).css({ fontSize: '2em', fontWeight: 'bold' });
    const $company = $('<p>').text(job['company']).css({ fontSize: '1.5em' });
    const $city = $('<p>').text(job['city']);
    const $pay = $('<p>').text(`${job["pay"]} per ${job["per"]}`);
    const $jobType = $('<p>').text(job['job_type'].replace(',', ', '));
    const $datePosted = $('<p>').text(`Posted: ${job['date_posted']}`);

    $div.on('click', function () {
        $('.job-post-div').css('border', '1px solid #757575');
        $('#job-desc-div').empty();
        $div.css('border', '1px solid #0CB83C');

        const $titleP = $('<p>', { id: 'title-p' }).text('Applicants');

        if (job['users_applied'].length === 0) {
            $titleP.text('No Applicant');
            $('#job-desc-div').append($titleP);
        } else {
            $('#job-desc-div').append($titleP);
            job['users_applied'].forEach(user => {
                const $userDiv = $('<div>', { class: 'user-div' }).text(user['name']);

                $userDiv.on('click', function () {
                    get_resume(user['id'], job['id']);
                    $('#content').hide();
                    $('#resume-div').show();

                    $('#message-button').off('click').on('click', function () {
                        generate_group_name(user['id'], job['id']);
                    });

                    $('#save-button').prop('disabled', true)
                    $('#status').on('change', function () {
                        $('#save-button').prop('disabled', false)
                    })
                    $('#save-button').on('click', function () {
                        set_status(user['id'], job['id'], $('#status').val())
                    })
                });

                $('#job-desc-div').append($userDiv);
            });
        }
    });

    $div.append($jobTitle, $company, $city, $pay, $jobType, $datePosted);

    $('#job-list-div').append($div);
}

function set_status(user_id, job_id, status) {
    $('#message-div').remove();
    $('#loading-div').show()
    $.ajax({
        type: "PUT",
        url: `/api/status/${user_id}/${job_id}/${status}`,
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(),
        },
        success: function (result) {
            if (result['message'] === 'Success') {
                let url_notif = `ws://${window.location.host}/ws/notif/${user_id}/`
                const notifSocket = new WebSocket(url_notif)

                setTimeout(() => {
                    notifSocket.send(JSON.stringify({
                        'notif': true
                    }));
                }, 500)

                $('#loading-div').hide()
                message('Status Saved Successfully', 'success')
            }
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
    $('#action-div').append(messageDiv)
}
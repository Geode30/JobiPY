$(document).ready(function () {
    get_applied_jobs()
})

function get_applied_jobs() {
    $.ajax({
        type: "GET",
        url: "/api/activities",
        success: function (result) {
            create_job_div(result)
            view_status(result['user_id'])
        }
    });
}

function create_job_div(result) {
    if (result['jobs_applied'].length > 0) {
        $('#desc-title').text('Select a Job Post')
    }
    else {
        $('#desc-title').text('No Applied Jobs')
    }

    result['jobs_applied'].forEach(job => {
        const jobs_div = $('<div>', {
            class: 'job-post-div'
        })
        const job_title = $('<p>', {
            class: 'job-title-p',
            text: job['job_title']
        })
        const company = $('<p>', {
            class: 'job-company-p',
            text: job['company']
        })
        const date_applied = $('<p>', {
            class: 'date-applied-p',
            text: `Applied on ${job['date_applied']}`
        })
        const statusTitle = $('<p>', {
            text: `Status:`,
            css: {
                fontWeight: 'bold'
            }
        })

        const status = $('<p>', {
            class: 'status-p',
            text: `${job['status']}`,
            css: {
                color: job['color'],
                fontWeight: 'bold'
            }
        })

        jobs_div.on('click', function () {
            create_job_details(job, jobs_div)
        })
        jobs_div.append(job_title, company, date_applied, statusTitle, status)
        $('#job-list-div').append(jobs_div)
    })
}

function view_status(user_id) {
    let url_notif = `ws://${window.location.host}/ws/notif/${user_id}/`
    const notifSocket = new WebSocket(url_notif)
    $.ajax({
        type: "PUT",
        url: `/api/application/status`,
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(),
        },
        success: function () {
            setTimeout(() => {
                notifSocket.send(JSON.stringify({
                    'notif': true
                }));
            }, 500)
        }
    })
}

function create_job_details(job, job_post) {
    $('.job-post-div').css('border', '1px solid #757575');
    job_post.css('border', '1px solid #0CB83C');
    const $jobDescDiv = $('#job-desc-div').empty();

    const $headDiv = $('<div>', { id: 'head-div' });
    const $detailsDiv = $('<div>', { id: 'details-div' });

    const $detailsTitle = $('<p>', { text: 'Job Details', css: { fontSize: '1.2em', fontWeight: 'bold' } });
    const $descriptionTitle = $('<p>', { text: 'Description', css: { fontSize: '1.2em', fontWeight: 'bold', marginTop: '1em', marginRight: 'auto', paddingLeft: '2em' } });

    const $jobTitleDetail = $('<p>', { text: job['job_title'], css: { fontSize: '1.5em', fontWeight: 'bold' } });
    const $companyDetail = $('<p>', { text: job['company'], class: 'head-class', css: { fontSize: '1em' } });
    const $cityDetail = $('<p>', { text: job['city'], class: 'head-class' });
    const $description = $('<div>', { text: job['description'], id: 'desc' });
    const $payDetail = $('<p>', { text: `${job["pay"]} per ${job["per"]}`, class: 'head-class' });
    const $jobTypeDetail = $('<p>', { text: job['job_type'].replace(',', ', '), class: 'head-class' });
    const $datePostedDetail = $('<p>', { text: `Posted: ${job['date_posted']}`, class: 'head-class' });

    $headDiv.append($jobTitleDetail, $companyDetail)
    $detailsDiv.append($detailsTitle, $jobTypeDetail, $payDetail, $cityDetail, $datePostedDetail);
    $jobDescDiv.append($headDiv, $detailsDiv, $descriptionTitle, $description);
}
document.addEventListener('DOMContentLoaded', () => {

    fetch_jobs();

    $('#search-button').on('click', function () {
        const job_title = $('#search-job').val();
        const city = $('#search-city').val();

        $('.job-post-div').remove();

        fetch_search(job_title, city);
    });
})

function fetch_search(job_title, city) {
    $.ajax({
        url: `/api/search/${job_title}/${city}`,
        method: 'GET',
        success: function (result) {
            $('.job-post-div').remove();
            result['jobs'].forEach(function (job) {
                get_jobs(job);
            });
        }
    });
}

function fetch_jobs() {
    $.ajax({
        url: '/api/jobs',
        method: 'GET',
        success: function (result) {
            if (result['jobs'].length > 0) {
                $('#desc-title').text('Select a Job Post')
            }
            else {
                $('#desc-title').text('No Available Jobs')
            }
            result['jobs'].forEach(function (job) {
                get_jobs(job);
            });
        }
    });
}

function fetch_job(id, div) {
    $('#loading-div').css('display', 'flex');
    $('#content').css('display', 'none');

    $.ajax({
        url: '/api/apply',
        type: 'PUT',
        headers: {
            'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(),
        },
        contentType: 'application/json',
        data: JSON.stringify({ 'id': id }),
        success: function (result) {
            $('#loading-div').css('display', 'none');
            $('#content').css('display', 'flex');
            $('#apply-button').css('display', 'none');
            message(result['message'], 'success');

            setTimeout(() => {
                div.slideUp()
                $('#job-desc-div').html('<div style="font-size: 3em; font-weight: bold; text-align: center; margin-top: 5em;">Select a Job Post</div>');
            }, 1000);
        },
        error: function (xhr, status, error) {
            console.error('Error fetching job:', error);
        }
    });
}

function message(msg, color) {
    $('#response-div').remove();
    const messageDiv = $('<div>', {
        id: 'response-div',
        class: `alert alert-${color}`,
        text: msg,
        css: { marginTop: '1em' }
    });

    $('#head-div').append(messageDiv);
}

function get_jobs(job) {
    const $div = $('<div>', { class: 'job-post-div' });

    const $jobTitle = $('<p>', { text: job['job_title'], css: { fontSize: '2em', fontWeight: 'bold' } });
    const $company = $('<p>', { text: job['company'], css: { fontSize: '1.5em' } });
    const $city = $('<p>', { text: job['city'] });
    const $pay = $('<p>', { text: `${job["pay"]} per ${job["per"]}` });
    const $jobType = $('<p>', { text: job['job_type'].replace(',', ', ') });
    const $datePosted = $('<p>', { text: `Posted: ${job['date_posted']}` });

    $div.append($jobTitle, $company, $city, $pay, $jobType, $datePosted)
        .on('click', function () {
            $('.job-post-div').css('border', '1px solid #757575');
            $div.css('border', '1px solid #0CB83C');

            const $jobDescDiv = $('#job-desc-div').empty();

            const $headDiv = $('<div>', { id: 'head-div' });
            const $detailsDiv = $('<div>', { id: 'details-div' });

            const $detailsTitle = $('<p>', { text: 'Job Details', css: { fontSize: '1.2em', fontWeight: 'bold' } });
            const $descriptionTitle = $('<p>', { text: 'Description', css: { fontSize: '1.2em', fontWeight: 'bold', marginTop: '1em', marginRight: 'auto', paddingLeft: '2em' } });

            const $jobTitleDetail = $('<p>', { text: job['job_title'], css: { fontSize: '1.5em', fontWeight: 'bold' } });
            const $companyDetail = $('<p>', { text: job['company'], class: 'head-class', css: { fontSize: '1em' } });
            const $cityDetail = $('<p>', { text: job['city'], class: 'head-class' });
            const $description = $('<div>', { text: job['description'], id: 'desc' });
            const $payDetail = $('<p>', {
                text: `${job['currency']} ${job["pay"]} per ${job["per"]}`, class: 'head-class', css: {
                    color: job['pay_color'],
                    fontWeight: 'bold'
                }
            });
            const $jobTypeDetail = $('<p>', {
                text: job['job_type'].replace(',', ', '), class: 'head-class', css: {
                    color: job['job_type_color'],
                    fontWeight: 'bold'
                }
            });
            const $datePostedDetail = $('<p>', { text: `Posted: ${job['date_posted']}`, class: 'head-class' });
            const $applyButton = $('<button>', {
                text: 'Apply',
                id: 'apply-button',
                class: 'btn btn-primary',
            }).on('click', function () {
                fetch_job(job['id'], $div);
            });

            $headDiv.append($jobTitleDetail, $companyDetail, $applyButton);
            $detailsDiv.append($detailsTitle, $jobTypeDetail, $payDetail, $cityDetail, $datePostedDetail);
            $jobDescDiv.append($headDiv, $detailsDiv, $descriptionTitle, $description);
        });

    $('#job-list-div').append($div);
}

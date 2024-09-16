$(document).ready(function () {

    $('#sign-in-div').click(function () {
        window.location.href = '/login';
    });

    $('#start-button').click(function () {
        window.location.href = '/register';
    });

    $('#industry').on('change', function () {
        hide_headliner()
        setTimeout(show_jobs, 500)
        $('#search-job').val('')
        $('#search-city').val('')
        get_jobs($('#industry').val())
    })

    $('#search-button').on('click', function () {
        if ($('#job-div').is(':visible')) {
            get_jobs($('#industry').val(), $('#search-job').val(), $('#search-city').val())
        }
    })
});

function hide_headliner() {
    $('#headliner').fadeOut(500)
}

function show_jobs() {
    $('#job-div').fadeIn(500)
}

function get_jobs(industry = null, job_title = null, city = null) {
    $('.job-post-div').remove()
    $('#loading-div').show()
    $.ajax({
        type: "GET",
        url: `/api/index/search/jobs`,
        data: {
            industry: industry,
            job_title: job_title,
            city: city
        },
        success: function (result) {
            if (result['message'] === 'Success') {
                $('#desc-title').text(result['jobs'].length === 0 ? 'No Available Jobs' : 'Select a Job Post')
                result['jobs'].forEach(job => {
                    create_job_list(job)
                })
            }

        },
        complete: function (jqXHR, textStatus) {
            $('#loading-div').hide()
        }
    });
}

function create_job_list(job) {
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
                text: `${job['currency']} ${job["pay"]} per ${job["per"]}`, class: 'head-class'
            });
            const $jobTypeDetail = $('<p>', {
                text: job['job_type'].replace(',', ', '), class: 'head-class'
            });
            const $datePostedDetail = $('<p>', { text: `Posted: ${job['date_posted']}`, class: 'head-class' });

            const sign_up_btn = $('<button>', {
                text: 'Register to apply',
                class: 'btn btn-primary'
            }).on('click', function () {
                window.location.href = '/register'
            })

            $headDiv.append($jobTitleDetail, $companyDetail, sign_up_btn);
            $detailsDiv.append($detailsTitle, $jobTypeDetail, $payDetail, $cityDetail, $datePostedDetail);
            $jobDescDiv.append($headDiv, $detailsDiv, $descriptionTitle, $description);
        });

    $('#job-list-div').append($div);
}

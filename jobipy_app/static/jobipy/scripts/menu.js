$(document).ready(function () {
    $('#logout-a-big, #jobs-a-big, #profile-a-big, #posted-a-big, #activities-a-big').css({
        'text-decoration': 'none',
        'color': 'white',
        'font-size': '1.2em',
        'height': '100%',
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center'
    });

    const url = window.location.pathname
    let path = url.slice(1)

    $(`#${path}-span-big`).css({
        'font-weight': 'bold',
        'padding-left': '0.1em',
        'padding-right': '0.1em',
        'border-bottom': '3px solid white',
    });

    $('#logout-a-big, #jobs-a-big, #profile-a-big, #posted-a-big, #activities-a-big').hover(
        function () {

            $(this).css({
                'cursor': 'pointer',
            });

            $('#logout-span-big, #jobs-span-big, #profile-span-big, #posted-span-big, #activities-span-big').css({
                'font-weight': '',
                'border-bottom': '',
                'transition': 'all 0.1s ease-in-out'
            });

            $(this).find('span').css({
                'font-weight': 'bold',
                'border-bottom': '3px solid white',
                'transition': 'all 0.1s ease-in-out'
            });
        },
        function () {
            $(this).find('span').css({
                'font-weight': '',
                'border-bottom': '',
                'transition': 'all 0.1s ease-in-out'
            });

            $(`#${path}-a-big`).find('span').css({
                'font-weight': 'bold',
                'border-bottom': '3px solid white',
            });
        }
    );
});

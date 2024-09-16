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


    $('#logout-a-big, #jobs-a-big, #profile-a-big, #posted-a-big, #activities-a-big').hover(
        function () {
            $(this).css({
                'cursor': 'pointer',
            })

            $(this).find('span').css({
                'cursor': 'pointer',
                'font-weight': 'bold',
                'border-bottom': '1px solid white',
                'transition': 'all 0.3s ease-in-out'
            });
        },
        function () {
            $(this).find('span').css({
                'cursor': '',
                'font-weight': '',
                'border-bottom': '',
                'transition': ''
            });
        }
    );
});

$(document).ready(function () {
    let isDivVisible = false;

    $('#menu-icon-div').click(function () {
        runAnimation('menu-div', 'appear');
        isDivVisible = true;
    });

    $('#message-icon-div').click(function () {
        runAnimation('message-div-header', 'appear');
        isDivVisible = true;
    });

    $('#notification-icon-div').click(function () {
        runAnimation('notification-div-header', 'appear');
        isDivVisible = true;
    });

    $('.close').on('click', function () {
        runAnimation('menu-div', 'disappear');
        runAnimation('message-div-header', 'disappear');
        runAnimation('notification-div-header', 'disappear');
        isDivVisible = false;
    });

    $('#content').click(function () {
        if (isDivVisible) {
            runAnimation('message-div-header', 'disappear');
            runAnimation('menu-div', 'disappear');
            runAnimation('notification-div-header', 'disappear');
            isDivVisible = false;
        }
    });

    $('#close-all-divs').click(function () {
        if (isDivVisible) {
            runAnimation('message-div-header', 'disappear');
            runAnimation('menu-div', 'disappear');
            runAnimation('notification-div-header', 'disappear');
            isDivVisible = false;
        }
    });
});

function runAnimation(div, animationName) {
    $(`#${div}`).css({
        'animation-name': animationName,
        'animation-duration': '0.5s',
        'animation-fill-mode': 'forwards',
        'animation-play-state': 'running'
    });
}
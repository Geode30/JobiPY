document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#app-name').addEventListener('click', () => {
        if (window.location.pathname === '/jobs') {
            window.location.href = '/jobs';
        }
        else if (window.location.pathname === '/setup') {

        }
        else {
            window.location.href = '/';
        }
    })
})
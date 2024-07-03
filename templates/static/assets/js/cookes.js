document.addEventListener('DOMContentLoaded', function () {
    var cookiePopup = document.getElementById('cookie-popup');
    var cookieAcceptButton = document.getElementById('cookie-accept');

    // Verifica se os cookies foram aceitos anteriormente
    if (!getCookie('cookiesAccepted')) {
        // Se não foram aceitos, exibe o popup
        cookiePopup.style.display = 'block';
    }

    // Adiciona um ouvinte de eventos ao botão de aceitação
    cookieAcceptButton.addEventListener('click', function () {
        // Define um cookie para registrar a aceitação
        setCookie('cookiesAccepted', 'true', 365);
        // Oculta o popup
        cookiePopup.style.display = 'none';
    });

    // Função para definir um cookie
    function setCookie(name, value, days) {
        var expires = '';
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = '; expires=' + date.toUTCString();
        }
        document.cookie = name + '=' + value + expires + '; path=/';
    }

    // Função para obter o valor de um cookie
    function getCookie(name) {
        var nameEQ = name + '=';
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) === ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }
});

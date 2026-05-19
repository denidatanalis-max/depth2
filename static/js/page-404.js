setTimeout(function () {
    var url = document.body.dataset.logoutUrl;
    if (url) window.location.href = url;
}, 3000);

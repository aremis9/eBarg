document.addEventListener("DOMContentLoaded", () => {
    var cardimg = document.getElementsByClassName("card-img-top")[0]

    var width = cardimg.getBoundingClientRect().width

    cardimg.style.height = cardimg.getBoundingClientRect().width



})
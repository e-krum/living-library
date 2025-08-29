window.onload = function() {
    const contents = document.getElementById('')
    const pageLinks = document.getElementsByClassName('page-link')
    for (let pageLink of pageLinks) {
        pageLink.onclick = function(event) {
            event.preventDefault();
            let href = this.attribute('href')
            fetch(href, {
                method: GET
            })
            .then(response => {
                response.text()
            })
            .then(html => {

            })
        }
    }
}
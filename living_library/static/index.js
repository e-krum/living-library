window.onload = function() {
    const pageLinks = document.getElementsByClassName('page-link')
    for (let pageLink of pageLinks) {
        pageLink.onclick = function(event) {
            // event.preventDefault();
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

    const cards = document.getElementsByClassName("book-card-display")
    for (let card of cards) {
        card.onclick = function(event) {
            let href = this.getAttribute('href')
            window.location.href = href
        }
    }
}
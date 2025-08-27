window.onload = function() {
    const randomBookForm = document.getElementById('random-book-form')
    const cardDisplay = document.getElementById('card')
    if (randomBookForm != null) {
        randomBookForm.onsubmit = function(event) {
            event.preventDefault();

            fetch('/card-display?state=0', {
                method: 'GET'
            })
            .then(response => {
                return response.text();
            })
            .then(html => {
                cardDisplay.innerHTML = html;
            })
        }
    }
}
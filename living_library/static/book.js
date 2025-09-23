window.onload = function() {
    const bookReviews = document.getElementById('book-reviews');
    const reviewBookForm = document.getElementById('book-review-form');
    const editButton = document.getElementById('edit-book');
    const bookDetails = document.getElementById('book-details');
    const editBookForm = document.getElementById('edit-book-form');

    reviewBookForm.onsubmit = function(event) {
        event.preventDefault();
        let href = this.getAttribute('action');
        fetch(href, {
            method: 'POST',
            body: new FormData(reviewBookForm)
        })
        .then(response => {
            return response.text();
        })
        .then(html => {
            bookReviews.innerHTML = html;
        })
    }

    editButton.onclick = function(event) {
        bookDetails.style.setProperty('display', 'none');
        editBookForm.style.setProperty('display', 'block');
    }
}
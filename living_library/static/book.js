window.onload = function() {
    const reviewBookForm = document.getElementById('book-review-form')

    reviewBookForm.onsubmit = function(event) {
        event.preventDefault();
    }
}
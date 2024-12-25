function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const question_cards = document.getElementsByClassName("question-card")

for (const question_card of question_cards) {
    const likeButton = question_card.querySelector(".like-button")
    const dislikeButton = question_card.querySelector(".dislike-button")
    const voteCount = question_card.querySelector(".vote-count")
    
    const questionId = question_card.dataset.questionId
    dislikeButton.addEventListener("click", () => {
        const request = new Request(`/${questionId}/vote_question`, {
            method: "POST",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            mode: 'same-origin',
            body: JSON.stringify({
                type: "Dislike",
            })
        })
    
        fetch(request).then((response) => {
            response.json().then((data) => {
                voteCount.innerText = data.vote_count
            })
        });
    })
    
    likeButton.addEventListener("click", () => {
        const request = new Request(`/${questionId}/vote_question`, {
            method: "POST",
            headers: {'X-CSRFToken': getCookie('csrftoken')},
            mode: 'same-origin',
            body: JSON.stringify({
                type: "Like",
            })
        })
    
        fetch(request).then((response) => {
            response.json().then((data) => {
                voteCount.innerText = data.vote_count
            })
        });
    })    
}

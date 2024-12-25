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

const cards = document.getElementsByClassName("answer-card-cls")

for (const card of cards) {
    const likeButton = card.querySelector(".like-button")
    const dislikeButton = card.querySelector(".dislike-button")
    const voteCount = card.querySelector(".vote-count")

    const answerId = card.dataset.answerId

    dislikeButton.addEventListener("click", () => {
        const request = new Request(`/${answerId}/vote_answer`, {
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
        const request = new Request(`/${answerId}/vote_answer`, {
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

const question_card = document.getElementsByClassName("question-block").item(0)
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

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const answer_cards = document.getElementsByClassName("answer-card-cls");
for (const answer_card of answer_cards) {
  const setCorrectButton = answer_card.querySelector(".is-accepted-button");

  const answerId = answer_card.dataset.answerId;
  setCorrectButton.addEventListener("click", () => {
    const request = new Request(`/${answerId}/set_correct`, {
      method: "POST",
      headers: { "X-CSRFToken": getCookie("csrftoken") },
      mode: "same-origin",
    });

    fetch(request).then((response) => {
        response.json().then((data) => {
            const current_status = setCorrectButton.classList.contains("circle-button-accepted");

            if (current_status === data.is_accepted) {
                return;
            }
            if (data.is_accepted === true) {
                setCorrectButton.classList.remove("circle-button-empty");
                setCorrectButton.classList.add("circle-button-accepted");

                const checkIcon = document.createElement("i");
                checkIcon.classList.add("fas", "fa-check");

                if (!setCorrectButton.contains(checkIcon)) {
                    setCorrectButton.appendChild(checkIcon);
                }
            } else {
                setCorrectButton.classList.remove("circle-button-accepted");
                setCorrectButton.classList.add("circle-button-empty");

                const checkIcon = setCorrectButton.querySelector("i.fas.fa-check");
                if (checkIcon) {
                    setCorrectButton.removeChild(checkIcon);
                }
            }
        });
    });
  });
}

document
  .getElementById("commentForm")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const body = document.getElementById("commentBody").value;
    const topic_id = document.getElementById("topicId").value;

    const response = await fetch("/api/comments", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic_id, body }),
    });

    const data = await response.json();
    const messageEl = document.getElementById("commentMessage");

    if (response.ok) {
      messageEl.style.color = "green";
      messageEl.textContent = "Comment added!";
      setTimeout(() => {
        location.reload();
      }, 1000);
    } else {
      messageEl.style.color = "red";
      messageEl.textContent = "Error posting comment.";
    }
  });

document
  .getElementById("newTopicForm")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const title = document.getElementById("title").value.trim();
    const body = document.getElementById("body").value.trim();
    const message = document.getElementById("message");

    if (!title || !body) {
      message.textContent = "Title and body are required.";
      return;
    }

    const response = await fetch("/api/topics", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title, body }),
    });

    if (response.status === 401) {
      // Session expired or not logged in
      window.location.href = "/login";
      return;
    }

    if (!response.ok) {
      message.textContent = "Failed to create topic.";
      return;
    }

    const data = await response.json();

    // Redirect to the new topic page
    window.location.href = `/topic/${data.id}`;
  });

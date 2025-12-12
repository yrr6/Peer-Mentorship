document
  .getElementById("registerForm")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    const messageEl = document.getElementById("message");

    if (response.ok) {
      messageEl.style.color = "green";
      messageEl.textContent = data.message + " Redirecting to login...";
      setTimeout(() => {
        window.location.href = "/"; // Redirect to login after success
      }, 2000);
    } else {
      messageEl.style.color = "red";
      messageEl.textContent = data.message || "Registration failed";
    }
  });

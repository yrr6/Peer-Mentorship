/* assets/js/app.js */

const API = "http://127.0.0.1:8000";

/* ------------------ REGISTER ------------------ */
function register() {
    const name = document.getElementById("reg_name").value;
    const email = document.getElementById("reg_email").value;
    const password = document.getElementById("reg_password").value;

    fetch(`${API}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
    })
    .then(res => res.json())
    .then(data => {
        alert("Account created successfully!");
        window.location.href = "login.html";
    })
    .catch(err => console.error(err));
}

/* ------------------ LOGIN ------------------ */
function login() {
    const email = document.getElementById("login_email").value;
    const password = document.getElementById("login_password").value;

    fetch(`${API}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
        if(data.access_token){
            localStorage.setItem("token", data.access_token);
            window.location.href = "dashboard.html";
        } else {
            alert("Login failed!");
        }
    })
    .catch(err => console.error(err));
}

/* ------------------ LOGOUT ------------------ */
function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

/* ------------------ CREATE POST ------------------ */
function createPost() {
    const text = document.getElementById("post_text").value;
    const token = localStorage.getItem("token");

    fetch(`${API}/posts/create`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ text })
    })
    .then(res => res.json())
    .then(data => {
        alert("Post created!");
        document.getElementById("post_text").value = "";
        loadPosts();
    })
    .catch(err => console.error(err));
}

/* ------------------ LOAD POSTS ------------------ */
function loadPosts() {
    const token = localStorage.getItem("token");
    fetch(`${API}/posts/all`, {
        headers: { "Authorization": `Bearer ${token}` }
    })
    .then(res => res.json())
    .then(posts => {
        const allPosts = document.getElementById("all_posts");
        allPosts.innerHTML = posts.map(p => `<p>${p.user}: ${p.text}</p>`).join('');
    })
    .catch(err => console.error(err));
}

/* ------------------ CHAT WEBSOCKET ------------------ */
let socket;
if(window.location.pathname.includes("chat")){
    socket = new WebSocket("ws://127.0.0.1:8000/chat/ws");

    socket.onmessage = (event) => {
        const msgBox = document.getElementById("messages");
        msgBox.innerHTML += `<p>${event.data}</p>`;
        msgBox.scrollTop = msgBox.scrollHeight;
    };
}

function sendMessage() {
    const msg = document.getElementById("msg_input").value;
    if(msg && socket){
        socket.send(msg);
        document.getElementById("msg_input").value = "";
    }
}

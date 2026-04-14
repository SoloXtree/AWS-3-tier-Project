document.getElementById("loginButton").addEventListener("click", function () {

    const username = document.querySelector("input[type='text']").value.trim();
    const password = document.querySelector("input[type='password']").value.trim();
    const responseEl = document.getElementById("response");

    // Basic validation
    if (username === "" || password === "") {
        responseEl.style.color = "#ff4444";
        responseEl.innerText = "⚠️ Please enter username and password";
        return;
    }

    // Show loading
    responseEl.style.color = "#00ff88";
    responseEl.innerText = "⏳ Logging in...";

    // Backend ALB URL
    const backendURL = "http://thegem.in/login";  // Replace with your actual ALB DNS

    fetch(backendURL, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok " + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        if (data.username && data.email) {
            responseEl.style.color = "#00ff88";
            responseEl.innerText = `✅ User: ${data.username} - Email: ${data.email}`;
        } else {
            responseEl.style.color = "#ff4444";
            responseEl.innerText = "⚠️ No user data found!";
        }
    })
    .catch(error => {
        console.error("Error fetching data:", error);
        responseEl.style.color = "#ff4444";
        responseEl.innerText = "❌ Failed to load data!";
    });
});

// Press Enter to login
document.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        document.getElementById("loginButton").click();
    }
});

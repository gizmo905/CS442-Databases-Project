const form = document.getElementById("loginForm");
const errorMsg = document.getElementById("errorMsg");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  // get form values
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();
  const role = document.getElementById("role").value; // temp, for testing

  // simple front-end validation
  if (!email || !password) {
    showError("Please enter email and password.");
    return;
  }

  // ====== FUTURE BACKEND INTEGRATION POINT ======
  // When your DB + API is ready, do something like:
  //
  // const res = await fetch("/api/login", {
  //   method: "POST",
  //   headers: { "Content-Type": "application/json" },
  //   body: JSON.stringify({ email, password })
  // });
  // const data = await res.json();
  // if (!res.ok) { showError(data.message); return; }
  //
  // const userRole = data.role; // "student" or "advisor"
  //
  // ====== TEMPORARY FRONT-END ONLY FLOW ======
  // For now we’ll just use the selected role to simulate.
  redirectToDashboard(role);
});

function redirectToDashboard(role) {
  // later you’ll actually go to /student/dashboard or /advisor/dashboard
  if (role === "student") {
    window.location.href = "StudentDashBoard.html";
  } else if (role === "advisor") {
    window.location.href = "advisor-dashboard.html";
  } else {
    showError("Unknown role.");
  }
}

function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.style.display = "block";
}

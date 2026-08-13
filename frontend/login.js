import { API } from './api.js';

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById("login-form");
  const emailInput = document.getElementById("email");
  const passwordInput = document.getElementById("password");
  const submitBtn = document.getElementById("submit-btn");
  const formStatus = document.getElementById("form-status");
  const togglePasswordBtn = document.getElementById("toggle-password");

  // Page load par inputs ko hamesha clean/empty karne ke liye
  function clearInputs() {
    if (form) form.reset();
    if (emailInput) emailInput.value = "";
    if (passwordInput) passwordInput.value = "";
  }

  clearInputs();

  // Browser back/forward button se aane par bhi clean rakhe
  window.addEventListener("pageshow", clearInputs);

  // Password Visibility Toggle
  if (togglePasswordBtn && passwordInput) {
    togglePasswordBtn.addEventListener("click", () => {
      const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
      passwordInput.setAttribute("type", type);

      const eyeIcon = togglePasswordBtn.querySelector(".icon-eye");
      const eyeOffIcon = togglePasswordBtn.querySelector(".icon-eye-off");

      if (type === "password") {
        if (eyeIcon) eyeIcon.style.display = "block";
        if (eyeOffIcon) eyeOffIcon.style.display = "none";
      } else {
        if (eyeIcon) eyeIcon.style.display = "none";
        if (eyeOffIcon) eyeOffIcon.style.display = "block";
      }
    });
  }

  // Handle Login Form Submit
  form?.addEventListener("submit", async (event) => {
    event.preventDefault();

    const emailVal = emailInput?.value.trim();
    const passwordVal = passwordInput?.value;

    if (!emailVal || !passwordVal) {
      if (formStatus) {
        formStatus.style.color = "#f87171";
        formStatus.textContent = "Please fill in all fields.";
      }
      return;
    }

    setLoading(true);

    try {
      const res = await API.login({ email: emailVal, password: passwordVal });
      const data = await res.json();

      if (!res.ok) {
        if (formStatus) {
          formStatus.style.color = "#f87171";
          formStatus.textContent = data?.detail || data?.message || "Incorrect email or password.";
        }
        setLoading(false);
        return;
      }

      const token = data.access_token || data.token;
      if (token) {
        localStorage.setItem("taskflow_token", token);
      }
      localStorage.setItem("isLoggedIn", "true");

      try {
        const userProfile = await API.getProfile();
        if (userProfile) {
          localStorage.setItem("taskflow_user", JSON.stringify(userProfile));
        }
      } catch (profileErr) {
        console.warn("Could not cache user profile upon login:", profileErr);
      }

      if (formStatus) {
        formStatus.style.color = "var(--accent-green, #4ade80)";
        formStatus.textContent = "Authenticated! Redirecting...";
      }

      setTimeout(() => {
        window.location.href = "dashboard.html";
      }, 500);

    } catch (err) {
      console.error("Login Error:", err);
      if (formStatus) {
        formStatus.style.color = "#f87171";
        formStatus.textContent = "Cannot connect to server. Check backend/Uvicorn connection.";
      }
      setLoading(false);
    }
  });

  function setLoading(isLoading) {
    if (submitBtn) {
      submitBtn.disabled = isLoading;
      submitBtn.classList.toggle("loading", isLoading);
    }
  }
});
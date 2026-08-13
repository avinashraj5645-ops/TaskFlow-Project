import { API } from './api.js';

const form = document.getElementById("signup-form");
const nameInput = document.getElementById("name") || document.getElementById("full-name");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const confirmInput = document.getElementById("confirm-password");

const nameError = document.getElementById("name-error");
const emailError = document.getElementById("email-error");
const passwordError = document.getElementById("password-error");
const confirmError = document.getElementById("confirm-password-error");

const submitBtn = document.getElementById("submit-btn");
const formStatus = document.getElementById("form-status");
const toggleBtn = document.getElementById("toggle-password");

if (toggleBtn) {
  toggleBtn.addEventListener("click", () => {
    const isPassword = passwordInput.type === "password";
    passwordInput.type = isPassword ? "text" : "password";
    toggleBtn.querySelector(".icon-eye")?.style.setProperty("display", isPassword ? "none" : "block");
    toggleBtn.querySelector(".icon-eye-off")?.style.setProperty("display", isPassword ? "block" : "none");
  });
}

function showError(inputEl, errorEl, message) {
  if (errorEl) {
    errorEl.textContent = message;
    errorEl.classList.add("show");
  }
  if (inputEl) inputEl.classList.add("invalid");
}

function clearError(inputEl, errorEl) {
  if (errorEl) {
    errorEl.textContent = "";
    errorEl.classList.remove("show");
  }
  if (inputEl) inputEl.classList.remove("invalid");
}

function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value.trim());
}

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  let valid = true;

  const nameVal = nameInput.value.trim();
  const emailVal = emailInput.value.trim();
  const passwordVal = passwordInput.value;
  const confirmVal = confirmInput ? confirmInput.value : passwordVal;

  if (nameVal.length === 0) {
    showError(nameInput, nameError, "Enter your name.");
    valid = false;
  } else clearError(nameInput, nameError);

  if (!isValidEmail(emailVal)) {
    showError(emailInput, emailError, "Enter a valid email address.");
    valid = false;
  } else clearError(emailInput, emailError);

  if (passwordVal.length < 8) {
    showError(passwordInput, passwordError, "Password must be at least 8 characters.");
    valid = false;
  } else clearError(passwordInput, passwordError);

  if (confirmInput && confirmVal !== passwordVal) {
    showError(confirmInput, confirmError, "Passwords do not match.");
    valid = false;
  } else clearError(confirmInput, confirmError);

  if (!valid) return;

  setLoading(true);

  try {
    const response = await API.signup({ name: nameVal, email: emailVal, password: passwordVal });

    if (!response.ok) {
      formStatus.style.color = "#f87171";
      formStatus.textContent = response.status === 422 ? "Invalid input details." : "Signup failed. Email may already exist.";
      return;
    }

    formStatus.style.color = "var(--accent-green)";
    formStatus.textContent = "Account created in Database — Redirecting to login...";
    setTimeout(() => { window.location.href = "login.html"; }, 1000);

  } catch (err) {
    formStatus.style.color = "#f87171";
    formStatus.textContent = "Server unreachable. Is the backend running?";
  } finally {
    setLoading(false);
  }
});

function setLoading(isLoading) {
  if (submitBtn) {
    submitBtn.classList.toggle("loading", isLoading);
    submitBtn.disabled = isLoading;
  }
}

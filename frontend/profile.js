import { API } from './api.js';

// Auth Guard Check - user logged in nahi hai toh login page par redirect karein
if (localStorage.getItem('isLoggedIn') !== 'true' && !localStorage.getItem('taskflow_token')) {
  window.location.href = 'login.html';
}

document.addEventListener('DOMContentLoaded', async () => {
  // DOM Elements
  const displayName = document.getElementById('display-name');
  const displayEmail = document.getElementById('display-email');
  const avatarIcon = document.getElementById('avatar-icon');
  const fullNameInput = document.getElementById('full-name');
  const userEmailInput = document.getElementById('user-email');
  const profileForm = document.getElementById('profile-details-form');
  const statusMsg = document.getElementById('profile-status');
  
  const passwordForm = document.getElementById('password-change-form');
  const currentPasswordInput = document.getElementById('current-password');
  const newPasswordInput = document.getElementById('new-password');
  const confirmPasswordInput = document.getElementById('confirm-password');
  const passwordError = document.getElementById('password-error');
  const passwordStatus = document.getElementById('password-status');
  
  const logoutBtn = document.getElementById('logout-btn');

  // 1. Database se User Profile load karne ka function
  async function loadUserProfile() {
    try {
      const user = await API.getProfile();
      if (!user) return;

      const name = user.name || '';
      const email = user.email || '';

      if (displayName) displayName.textContent = name || 'User';
      if (displayEmail) displayEmail.textContent = email;
      if (fullNameInput) fullNameInput.value = name;
      if (userEmailInput) userEmailInput.value = email;
      if (avatarIcon && name) {
        avatarIcon.textContent = name.charAt(0).toUpperCase();
      }
    } catch (err) {
      if (statusMsg) {
        statusMsg.style.color = '#f87171';
        statusMsg.textContent = 'Failed to load user profile from Database.';
      }
    }
  }

  // Profile initial load
  await loadUserProfile();

  // 2. "Save Changes" par Profile Update handle karna
  profileForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const newName = fullNameInput.value.trim();
    const newEmail = userEmailInput.value.trim();

    if (!newName || !newEmail) {
      if (statusMsg) {
        statusMsg.style.color = '#f87171';
        statusMsg.textContent = 'Name and Email cannot be empty!';
      }
      return;
    }

    try {
      if (statusMsg) {
        statusMsg.style.color = '#eab308';
        statusMsg.textContent = 'Saving to Database...';
      }

      const updatedUser = await API.updateProfile({ name: newName, email: newEmail });
      const nameToShow = updatedUser?.name || newName;
      const emailToShow = updatedUser?.email || newEmail;

      // Real-time UI update
      if (displayName) displayName.textContent = nameToShow;
      if (displayEmail) displayEmail.textContent = emailToShow;
      if (avatarIcon) avatarIcon.textContent = nameToShow.charAt(0).toUpperCase();

      if (statusMsg) {
        statusMsg.style.color = '#22c55e';
        statusMsg.textContent = 'Profile updated successfully!';
      }
    } catch (err) {
      if (statusMsg) {
        statusMsg.style.color = '#f87171';
        statusMsg.textContent = err.message || 'Failed to save changes to Database.';
      }
    }
  });

  // 3. Password Update Handler
  passwordForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (passwordError) passwordError.textContent = '';
    if (passwordStatus) passwordStatus.textContent = '';

    const currentPassword = currentPasswordInput.value;
    const newPassword = newPasswordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    if (!currentPassword || !newPassword || !confirmPassword) {
      if (passwordError) passwordError.textContent = 'Please fill in all password fields.';
      return;
    }

    if (newPassword.length < 8) {
      if (passwordError) passwordError.textContent = 'New password must be at least 8 characters long.';
      return;
    }

    if (newPassword !== confirmPassword) {
      if (passwordError) passwordError.textContent = 'New passwords do not match!';
      return;
    }

    try {
      if (passwordStatus) {
        passwordStatus.style.color = '#eab308';
        passwordStatus.textContent = 'Updating password...';
      }

      await API.updatePassword({ currentPassword, newPassword });

      if (passwordStatus) {
        passwordStatus.style.color = '#22c55e';
        passwordStatus.textContent = 'Password updated successfully!';
      }

      // Reset form input fields
      passwordForm.reset();
    } catch (err) {
      if (passwordStatus) passwordStatus.textContent = '';
      if (passwordError) {
        passwordError.textContent = err.message || 'Failed to update password.';
      }
    }
  });

  // 4. Logout Event Handler
  logoutBtn?.addEventListener('click', (e) => {
    e.preventDefault();
    localStorage.clear();
    sessionStorage.clear();
    window.location.href = 'login.html';
  });
});
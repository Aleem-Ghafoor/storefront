(function () {
  const passwordInput = document.querySelector('input[name="password"]');
  const toggleButton = document.getElementById("toggle-password");
  const form = document.getElementById("login-form");
  const submitBtn = document.getElementById("submit-btn");

  if (passwordInput && toggleButton) {
    toggleButton.addEventListener("click", function () {
      const isHidden = passwordInput.type === "password";
      passwordInput.type = isHidden ? "text" : "password";
      toggleButton.textContent = isHidden ? "Hide" : "Show";
    });
  }

  if (form && submitBtn) {
    form.addEventListener("submit", function () {
      submitBtn.disabled = true;
      submitBtn.textContent = "Signing in...";
    });
  }
})();

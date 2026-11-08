(function () {
  const logoutButton = document.getElementById("logout-btn");

  if (logoutButton) {
    logoutButton.addEventListener("click", function () {
      //logoutButton.disabled = true;
      logoutButton.textContent = "Logging out...";
    });
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("show");
          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.16,
      rootMargin: "0px 0px -30px 0px",
    }
  );

  document.querySelectorAll("[data-reveal]").forEach((node) => {
    observer.observe(node);
  });
})();

const menuBtn = document.getElementById("menuBtn");
const navLinks = document.getElementById("navLinks");
const themeBtn = document.getElementById("themeBtn");
const contactForm = document.getElementById("contactForm");
const formStatus = document.getElementById("formStatus");

menuBtn?.addEventListener("click", () => navLinks.classList.toggle("open"));

document.querySelectorAll("#navLinks a").forEach(link => {
  link.addEventListener("click", () => navLinks.classList.remove("open"));
});

const savedTheme = localStorage.getItem("portfolio-theme");
if (savedTheme === "dark") {
  document.body.classList.add("dark");
  themeBtn.textContent = "☀️";
}

themeBtn?.addEventListener("click", () => {
  document.body.classList.toggle("dark");
  const dark = document.body.classList.contains("dark");
  localStorage.setItem("portfolio-theme", dark ? "dark" : "light");
  themeBtn.textContent = dark ? "☀️" : "🌙";
});

contactForm?.addEventListener("submit", async (event) => {
  event.preventDefault();
  formStatus.textContent = "Sending...";
  const formData = new FormData(contactForm);
  const payload = Object.fromEntries(formData.entries());

  try {
    const response = await fetch("/api/contact", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Unable to send message.");
    formStatus.textContent = "Message sent successfully!";
    contactForm.reset();
  } catch (error) {
    formStatus.textContent = error.message;
  }
});

const sections = document.querySelectorAll("section[id]");
const links = document.querySelectorAll("#navLinks a[href^='#']");
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      links.forEach(link => link.classList.toggle("active", link.getAttribute("href") === "#" + entry.target.id));
    }
  });
}, {rootMargin: "-35% 0px -55% 0px"});
sections.forEach(section => observer.observe(section));

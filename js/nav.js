document.addEventListener("DOMContentLoaded", () => {
  const current = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("nav.site-nav a").forEach((link) => {
    const href = link.getAttribute("href");
    if (href === current || (current === "" && href === "index.html")) {
      link.classList.add("active");
    }
    if (current.startsWith("post.html") && href === "blog.html") {
      link.classList.add("active");
    }
  });
});

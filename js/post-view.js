document.addEventListener("DOMContentLoaded", async () => {
  const params = new URLSearchParams(location.search);
  const slug = params.get("slug");
  const titleEl = document.getElementById("post-title");
  const metaEl = document.getElementById("post-meta");
  const bodyEl = document.getElementById("post-body");

  if (!slug) {
    bodyEl.innerHTML = '<p class="empty-state">No post specified.</p>';
    return;
  }

  const file = POST_FILES.find((f) => f.replace(/\.md$/, "") === slug);
  if (!file) {
    bodyEl.innerHTML = '<p class="empty-state">Post not found.</p>';
    return;
  }

  const res = await fetch(`posts/${file}`);
  if (!res.ok) {
    bodyEl.innerHTML = '<p class="empty-state">Could not load post.</p>';
    return;
  }

  const raw = await res.text();
  const { meta, body } = parseFrontmatter(raw);

  document.title = `${meta.title || slug} — Blog`;
  titleEl.textContent = meta.title || slug;
  metaEl.textContent = formatDate(meta.date);
  bodyEl.innerHTML = markdownToHtml(body);
});

document.addEventListener("DOMContentLoaded", async () => {
  const container = document.getElementById("post-list");
  if (!container) return;

  const posts = await Promise.all(
    POST_FILES.map(async (file) => {
      const res = await fetch(`posts/${file}`);
      if (!res.ok) return null;
      const raw = await res.text();
      const { meta } = parseFrontmatter(raw);
      const slug = file.replace(/\.md$/, "");
      return { slug, file, ...meta };
    })
  );

  let valid = posts.filter(Boolean).sort((a, b) => new Date(b.date) - new Date(a.date));

  const limit = parseInt(container.dataset.limit, 10);
  if (limit) valid = valid.slice(0, limit);

  if (!valid.length) {
    container.innerHTML = '<p class="empty-state">No posts yet — add one in posts/ and list it in posts/manifest.js.</p>';
    return;
  }

  container.innerHTML = valid
    .map((p) => {
      const tags = (p.tags || "")
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean)
        .map((t) => `<span class="tag">${t}</span>`)
        .join("");
      return `
        <article class="card">
          <h3><a href="post.html?slug=${encodeURIComponent(p.slug)}">${p.title || p.slug}</a></h3>
          <div class="card-meta">${formatDate(p.date)}</div>
          <p class="excerpt">${p.excerpt || ""}</p>
          ${tags ? `<div style="margin-top:10px;">${tags}</div>` : ""}
        </article>`;
    })
    .join("\n");
});

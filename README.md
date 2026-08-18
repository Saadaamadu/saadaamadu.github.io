# Saada Amadu — Personal Website

A simple personal website: bio, CV, speaking/engagements, blog, and contact
info. No build tools, no frameworks — just HTML, CSS, and a little
JavaScript, so you can edit everything in a text editor and it just works.

Live at **[saadaamadu.com](https://saadaamadu.com)**.

## Preview it locally

From this folder, start a local server (needed so the blog's JavaScript can
load post files — opening index.html directly won't work for the blog):

```bash
python3 -m http.server 8000
```

Then open **http://localhost:8000** in your browser. Press Ctrl+C in the
terminal to stop the server when you're done.

## Editing content

### Bio (home page)
Open `index.html` and edit the text inside the `<div class="bio-header">`
and `<div class="bio-body">` sections — name, title, links, and the bio
paragraphs.

### CV
`assets/cv.pdf` is generated from `scripts/build_cv.py` — don't edit the PDF
directly, edit the Python script instead (it's plain data: job titles,
dates, bullet points, etc. near the bottom of the file) and regenerate:

```bash
python3 scripts/build_cv.py
```

This builds **two** files:
- `assets/cv.pdf` — the **public** version (no email), this is what's linked
  from the site and gets committed/pushed
- `source-docs/cv-full.pdf` — the **private** version (with your email),
  stays local only since `source-docs/` is gitignored

Needs the `reportlab` Python package: `pip install reportlab`.

### Speaking / engagements
Open `speaking.html`. Each talk is an `<article class="card">` block. Copy
an existing block, edit the title/date/venue/description, and paste it in
(newest at the top is the usual convention). Delete blocks you don't need.

### Contact
Open `contact.html` and edit the list of email/links/location.

### Blog posts
Posts are Markdown files in `posts/`, so writing one feels like writing in
a plain text editor — no HTML required.

**To publish a new post:**
1. Copy `posts/_template.md` to a new file, e.g. `posts/2026-09-01-my-post.md`
   (the filename doesn't matter much, but starting with the date keeps things sorted)
2. Fill in the frontmatter at the top (`title`, `date`, `excerpt`, `tags`) and
   write the post body in Markdown below it
3. Open `posts/manifest.js` and add your new filename to the `POST_FILES` list
4. Refresh the blog page — your post appears automatically, sorted by date

Markdown supports `# Headings`, `**bold**`, `*italic*`, `[links](url)`,
`![images](path)`, `- bullet lists`, `1. numbered lists`, and `> quotes`.

To edit or unpublish a post later: edit the `.md` file directly, or remove
its filename from `posts/manifest.js` (this hides it from the site without
deleting the file).

### Site name / nav / colors
- Every page repeats the same header/nav and footer — if you rename a nav
  link or your name, use find-and-replace across all `.html` files.
- Colors and fonts are set once in `css/style.css` under `:root` at the top
  — change `--color-accent` to switch the accent color.

## Deploying

The site is already live at **saadaamadu.com**, hosted via GitHub Pages from
the repo `Saadaamadu/saadaamadu.github.io` (branch `main`), with DNS managed
in Cloudflare. The `CNAME` file in this repo tells GitHub which custom
domain to serve.

To publish any change (a new post, an updated bio, a new CV):

```bash
git add -A
git commit -m "describe the change"
git push
```

The live site updates within a minute or two — no build step required.

# Saada Amadu — Personal Website

A simple academic website: bio, CV, speaking/engagements, blog, and contact
info. No build tools, no frameworks — just HTML, CSS, and a little
JavaScript, so you can edit everything in a text editor and it just works.

Currently filled with lorem ipsum placeholder text so you can see the look
and feel. Replace the placeholder content as described below.

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
and `<div class="bio-body">` sections — name, title, photo, links, and the
bio paragraphs. Swap `images/profile-placeholder.svg` for a real photo (any
`.jpg`/`.png` works — just update the `src=` path).

### CV
Replace `assets/cv.pdf` with your real CV (keep the filename `cv.pdf`, or
update the `href`/`src` in `cv.html` if you rename it). The page has a
download button and an inline preview — no other editing needed.

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

## Deploying (GitHub Pages)

Once you're happy with the content:

1. Push this folder to a GitHub repository (see setup instructions provided
   separately, or run `git add`, `git commit`, `git push` if it's already
   connected).
2. On GitHub, go to the repo's **Settings → Pages**.
3. Under "Build and deployment", set **Source** to "Deploy from a branch",
   branch `main`, folder `/ (root)`. Save.
4. GitHub will publish the site at `https://<your-username>.github.io/<repo-name>/`
   within a minute or two.

Every time you `git push` new changes (a new post, an updated bio, a new
CV), the live site updates automatically within a minute or two — no
rebuild step required.

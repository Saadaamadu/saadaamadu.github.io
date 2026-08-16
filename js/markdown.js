/*
 * Tiny markdown + frontmatter parser for blog posts.
 * Supports: frontmatter (--- key: value ---), #/##/### headings,
 * **bold**, *italic*, `code`, [links](url), ![images](url),
 * > blockquotes, - / * bullet lists, 1. numbered lists, paragraphs.
 * No external dependencies so posts render without a build step.
 */

function parseFrontmatter(raw) {
  const match = raw.match(/^---\s*\n([\s\S]*?)\n---\s*\n?([\s\S]*)$/);
  if (!match) return { meta: {}, body: raw };

  const meta = {};
  match[1].split("\n").forEach((line) => {
    const idx = line.indexOf(":");
    if (idx === -1) return;
    const key = line.slice(0, idx).trim();
    let value = line.slice(idx + 1).trim();
    value = value.replace(/^["']|["']$/g, "");
    meta[key] = value;
  });

  return { meta, body: match[2] };
}

function inlineMarkdown(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img alt="$1" src="$2">')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>");
}

function markdownToHtml(md) {
  const lines = md.replace(/\r\n/g, "\n").split("\n");
  const html = [];
  let listBuffer = [];
  let listType = null;
  let quoteBuffer = [];
  let paraBuffer = [];

  function flushList() {
    if (listBuffer.length) {
      const tag = listType === "ol" ? "ol" : "ul";
      html.push(`<${tag}>` + listBuffer.map((li) => `<li>${inlineMarkdown(li)}</li>`).join("") + `</${tag}>`);
      listBuffer = [];
      listType = null;
    }
  }
  function flushQuote() {
    if (quoteBuffer.length) {
      html.push(`<blockquote>${quoteBuffer.map(inlineMarkdown).join("<br>")}</blockquote>`);
      quoteBuffer = [];
    }
  }
  function flushPara() {
    if (paraBuffer.length) {
      html.push(`<p>${inlineMarkdown(paraBuffer.join(" "))}</p>`);
      paraBuffer = [];
    }
  }
  function flushAll() {
    flushList();
    flushQuote();
    flushPara();
  }

  for (const rawLine of lines) {
    const line = rawLine.trimEnd();

    if (!line.trim()) {
      flushAll();
      continue;
    }

    const heading = line.match(/^(#{1,4})\s+(.*)$/);
    if (heading) {
      flushAll();
      const level = heading[1].length;
      html.push(`<h${level}>${inlineMarkdown(heading[2])}</h${level}>`);
      continue;
    }

    const quote = line.match(/^>\s?(.*)$/);
    if (quote) {
      flushList();
      flushPara();
      quoteBuffer.push(quote[1]);
      continue;
    }

    const bullet = line.match(/^[-*]\s+(.*)$/);
    if (bullet) {
      flushQuote();
      flushPara();
      if (listType && listType !== "ul") flushList();
      listType = "ul";
      listBuffer.push(bullet[1]);
      continue;
    }

    const numbered = line.match(/^\d+\.\s+(.*)$/);
    if (numbered) {
      flushQuote();
      flushPara();
      if (listType && listType !== "ol") flushList();
      listType = "ol";
      listBuffer.push(numbered[1]);
      continue;
    }

    flushList();
    flushQuote();
    paraBuffer.push(line.trim());
  }

  flushAll();
  return html.join("\n");
}

function formatDate(dateStr) {
  if (!dateStr) return "";
  const d = new Date(dateStr + "T00:00:00");
  if (isNaN(d)) return dateStr;
  return d.toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
}

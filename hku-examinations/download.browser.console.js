(async () => {
  const CONCURRENCY = 2;
  const HOST_OK = (h) => h === 'exam.hku.hk' || h === 'www.exam.hku.hk';
  const PATH_OK = (p) => p.toLowerCase().includes('/timetable/');
  const EXT_OK  = (p) => /\.(html?)$/i.test(p);
  const NOTE_TEXT_RE = /Note:\s*This examination/i;

  // Collect candidate timetable URLs on the page
  const anchors = Array.from(document.querySelectorAll('a[href]'));
  const allUrls = anchors.map(a => {
    try { return new URL(a.getAttribute('href'), location.href); } catch { return null; }
  }).filter(Boolean);

  const filtered = [];
  const seen = new Set();
  for (const u of allUrls) {
    const nu = new URL(u.href);
    nu.protocol = 'http:'; // site is HTTP-only
    if (!HOST_OK(nu.hostname)) continue;
    if (!PATH_OK(nu.pathname)) continue;
    if (!EXT_OK(nu.pathname)) continue;
    const key = nu.href;
    if (!seen.has(key)) { seen.add(key); filtered.push(nu); }
  }

  // Minimal per-cell cleanup: collapse internal runs of spaces, drop NBSP
  const cellClean = (s) => (s || '').replace(/\u00A0/g, ' ').replace(/[ \t]+/g, ' ').replace(/[ \t]*\n[ \t]*/g, ' ').trim();

  // Identify the main timetable table by header labels
  function hasTimetableHeaders(t) {
    const firstRow = t.querySelector('tr');
    if (!firstRow) return false;
    const labels = Array.from(firstRow.querySelectorAll('th,td')).map(td => (td.textContent || '').toLowerCase());
    return (
      labels.some(x => /date/.test(x)) &&
      labels.some(x => /\btime\b/.test(x)) &&
      labels.some(x => /course\s*code/.test(x)) &&
      labels.some(x => /description/.test(x)) &&
      labels.some(x => /venue/.test(x))
    );
  }

  // Extract plain text preserving row/cell structure, no invented data
  function extractPlainText(html) {
    // Hard cut at "Note:" to exclude postscript sections
    const cutIdx = html.search(NOTE_TEXT_RE);
    const htmlCut = cutIdx >= 0 ? html.slice(0, cutIdx) : html;

    const doc = new DOMParser().parseFromString(htmlCut, 'text/html');
    doc.querySelectorAll('script,style,noscript,iframe').forEach(n => n.remove());

    const lines = [];
    const title = (doc.querySelector('h1,h2,h3')?.textContent || '').trim();
    if (title) lines.push(title, '');

    // Find the timetable table
    const tables = Array.from(doc.querySelectorAll('table'));
    const table = tables.find(hasTimetableHeaders) || tables[0] || null;
    if (!table) return lines.join('\n');

    const rows = Array.from(table.querySelectorAll('tr'));
    for (const tr of rows) {
      const cells = Array.from(tr.querySelectorAll('th,td'));
      if (!cells.length) continue;

      // Preserve exact sequence of cells; do not drop spacer cells or carry values
      const texts = cells.map(td => cellClean(td.textContent || ''));
      // Skip completely empty rows
      if (!texts.some(t => t.length)) continue;
      // Join with tabs for readability without altering semantics
      lines.push(texts.join('\t'));
    }

    return lines.join('\n').replace(/\n{3,}/g, '\n\n').trim();
  }

  async function processOne(urlObj) {
    const res = await fetch(urlObj.href, { cache: 'no-store', credentials: 'omit' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const html = await res.text();

    // Extract non-inventive, layout-preserving text
    let text = extractPlainText(html);

    // Lowercase filename from original .html
    let base = (urlObj.pathname.split('/').pop() || 'index.html').toLowerCase().replace(/\.(html?)$/i, '');
    const filename = (base || 'index') + '.txt';

    // Save as .txt via Blob + <a download>
    const blob = new Blob([text + '\n'], { type: 'text/plain;charset=utf-8' });
    const blobUrl = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = blobUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(blobUrl), 1000);
  }

  // Concurrency
  const jobs = filtered.slice();
  let idx = 0, ok = 0, fail = 0;
  async function worker() {
    while (true) {
      const job = jobs[idx++];
      if (!job) break;
      try { await processOne(job); ok++; } catch (e) { console.warn('Failed:', job.href, e); fail++; }
    }
  }

  const workers = Array.from({ length: Math.min(CONCURRENCY, jobs.length) }, worker);
  await Promise.allSettled(workers);
  console.log(`Done. Success: ${ok}, Failed: ${fail}, Total: ${filtered.length}`);
})();

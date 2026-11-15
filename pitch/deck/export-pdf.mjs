// Regenerates the two PDFs next to index.html. Needs Node 22+ and Google Chrome; no npm packages.
//   node pitch/deck/export-pdf.mjs
// space-normal-pitch.pdf        one page per slide, final state
// space-normal-pitch-steps.pdf  one page per click (stage backup)
// Chrome's plain `--print-to-pdf` flag prints before Reveal has laid out the pages and gives one
// blank page, so this drives Chrome over the DevTools protocol and waits for the layout instead.
import { spawn } from 'node:child_process';
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const port = 9340, profile = mkdtempSync(join(tmpdir(), 'deck-pdf-'));
const sleep = ms => new Promise(r => setTimeout(r, ms));

const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', `--remote-debugging-port=${port}`,
  `--user-data-dir=${profile}`, 'about:blank'], { stdio: 'ignore' });
try {
  let page;
  for (let i = 0; i < 60 && !page; i++) {
    try { page = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find(t => t.type === 'page'); } catch {}
    if (!page) await sleep(250);
  }
  if (!page) throw new Error('Chrome did not start: set CHROME=/path/to/chrome');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise(r => { ws.onopen = r; });
  let id = 0; const pending = new Map();
  ws.onmessage = m => { const d = JSON.parse(m.data); if (pending.has(d.id)) { pending.get(d.id)(d.result ?? d); pending.delete(d.id); } };
  const send = (method, params = {}) => new Promise(r => { pending.set(++id, r); ws.send(JSON.stringify({ id, method, params })); });
  await send('Page.enable');

  const base = pathToFileURL(join(here, 'index.html')).href;
  for (const [query, file] of [['?print-pdf', 'space-normal-pitch.pdf'], ['?print-pdf&steps', 'space-normal-pitch-steps.pdf']]) {
    await send('Page.navigate', { url: base + query });
    let pages = 0;
    for (let i = 0; i < 40 && !pages; i++) {
      await sleep(500);
      pages = (await send('Runtime.evaluate', { expression: "document.querySelectorAll('.pdf-page').length", returnByValue: true })).result?.value || 0;
    }
    if (!pages) throw new Error('Reveal print layout did not appear for ' + query);
    await sleep(1500);   // images and fonts
    const pdf = await send('Page.printToPDF', { printBackground: true, preferCSSPageSize: true, displayHeaderFooter: false });
    writeFileSync(join(here, file), Buffer.from(pdf.data, 'base64'));
    console.log(`${file}: ${pages} pages`);
  }
  ws.close();
} finally {
  chrome.kill();
  await sleep(300);
  rmSync(profile, { recursive: true, force: true });
}

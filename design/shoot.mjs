/**
 * Full-page screenshots at an exact CSS viewport, via the DevTools protocol.
 *
 * Expects a headless Chrome already listening on SHOOT_PORT (default 9333).
 *
 * `chrome --headless --window-size=390,844 --screenshot` does NOT give a 390px
 * layout: Chrome enforces a minimum window width (485px here) and then crops the
 * image to the requested size, so narrow shots silently show a wider layout with
 * the right-hand side cut off — which reads exactly like a responsive bug that
 * isn't there. Emulation.setDeviceMetricsOverride sets the real viewport, and
 * captureBeyondViewport gets the whole page instead of one screenful.
 *
 *   node shoot.mjs <url> <out.png> [width] [height] [mobile]
 */
import { writeFileSync } from 'node:fs';
import { get } from 'node:http';

const [, , url, out, wArg, hArg, mobileArg] = process.argv;
if (!url || !out) {
  console.error('usage: node shoot.mjs <url> <out.png> [width] [height] [mobile]');
  process.exit(2);
}
const width = Number(wArg || 1440);
const height = Number(hArg || 900);
const mobile = String(mobileArg || '') === 'mobile';
// Chrome is started separately and left running: spawning it from here and killing
// it in a finally block left the process hanging on Windows with nothing written.
const port = Number(process.env.SHOOT_PORT || 9333);

const json = (path) => new Promise((res, rej) => {
  get({ host: '127.0.0.1', port, path }, (r) => {
    let d = ''; r.on('data', (c) => (d += c)); r.on('end', () => res(JSON.parse(d)));
  }).on('error', rej);
});

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

{
  let tabs = null;
  for (let i = 0; i < 60 && !tabs; i++) {
    try { tabs = await json('/json/list'); } catch { await sleep(250); }
  }
  if (!tabs || !tabs.length) throw new Error('devtools never came up');

  const page = tabs.find((t) => t.type === 'page') || tabs[0];
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  let id = 0;
  const pending = new Map();
  const send = (method, params = {}) =>
    new Promise((res, rej) => {
      const i = ++id;
      pending.set(i, res);
      ws.send(JSON.stringify({ id: i, method, params }));
      setTimeout(() => rej(new Error(`CDP timeout: ${method}`)), 30000);
    });
  ws.onmessage = (e) => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); }
  };
  await new Promise((r, j) => { ws.onopen = r; setTimeout(() => j(new Error('ws open timeout')), 10000); });

  await send('Emulation.setDeviceMetricsOverride', {
    width, height, deviceScaleFactor: 1, mobile,   // 2x + captureBeyondViewport stalls on tall pages
    screenWidth: width, screenHeight: height,
  });
  await send('Page.enable');
  // The browser is reused across shots; without this a re-shot URL comes back from
  // cache and silently reports the OLD page's dimensions.
  await send('Network.enable');
  await send('Network.setCacheDisabled', { cacheDisabled: true });
  // Headless defaults to dark; the design is light, so pin the scheme explicitly.
  const scheme = process.env.SHOOT_SCHEME || 'light';
  await send('Emulation.setEmulatedMedia', {
    features: [{ name: 'prefers-color-scheme', value: scheme }],
  });
  await send('Page.navigate', { url });
  await sleep(2500);                       // let webfonts land

  // Report any genuine overflow while the real viewport is in force.
  const probe = await send('Runtime.evaluate', {
    returnByValue: true,
    expression: `(() => {
      const vw = document.documentElement.clientWidth;
      const bad = [];
      document.querySelectorAll('*').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.right > vw + 1) bad.push(el.tagName.toLowerCase() + '.' +
          String(el.className || '').trim().split(/\\s+/).join('.') + ' right=' + Math.round(r.right));
      });
      return { vw, scrollW: document.documentElement.scrollWidth,
               scrollH: document.documentElement.scrollHeight, bad: bad.slice(0, 6) };
    })()`,
  });
  const p = probe.result.value;

  const shot = await send('Page.captureScreenshot', {
    format: 'png', captureBeyondViewport: true,
  });
  writeFileSync(out, Buffer.from(shot.data, 'base64'));

  console.log(`${out}  viewport=${p.vw}x${height}${mobile ? ' (mobile)' : ''}  ` +
              `page=${p.scrollW}x${p.scrollH}  ` +
              (p.bad.length ? `OVERFLOW: ${p.bad.join(' | ')}` : 'no overflow'));
  ws.close();
  process.exit(0);          // the open socket would otherwise keep the loop alive
}

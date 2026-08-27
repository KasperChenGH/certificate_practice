/**
 * Drive the real app through a full run and capture each screen at a fixed viewport.
 *
 *   SHOOT_PORT=9333 node flowtest.mjs <width> <height> <suffix> [mobile]
 *
 * Screenshots are the point, but the assertions matter more: this fails loudly if the
 * navigator does not track answers, if jumping does not move the question, or if a
 * page renders without its ad container.
 */
import { writeFileSync } from 'node:fs';
import { get } from 'node:http';

const [, , wArg, hArg, suffix, mobileArg] = process.argv;
const width = Number(wArg || 1440);
const height = Number(hArg || 900);
const mobile = String(mobileArg || '') === 'mobile';
const port = Number(process.env.SHOOT_PORT || 9333);
const scheme = process.env.SHOOT_SCHEME || 'light';

const json = (path) => new Promise((res, rej) => {
  get({ host: '127.0.0.1', port, path }, (r) => {
    let d = ''; r.on('data', (c) => (d += c)); r.on('end', () => res(JSON.parse(d)));
  }).on('error', rej);
});
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const tabs = await json('/json/list');
const page = tabs.find((t) => t.type === 'page') || tabs[0];
const ws = new WebSocket(page.webSocketDebuggerUrl);
let id = 0; const pending = new Map();
const send = (method, params = {}) => new Promise((res, rej) => {
  const i = ++id; pending.set(i, res);
  ws.send(JSON.stringify({ id: i, method, params }));
  setTimeout(() => rej(new Error('CDP timeout: ' + method)), 30000);
});
ws.onmessage = (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); }
};
await new Promise((r, j) => { ws.onopen = r; setTimeout(() => j(new Error('ws timeout')), 10000); });

const errs = [];
const ev = async (expr) => {
  const r = await send('Runtime.evaluate', { expression: `(()=>{${expr}})()`, returnByValue: true, awaitPromise: true });
  if (r.exceptionDetails) errs.push(r.exceptionDetails.text + ' ' + ((r.exceptionDetails.exception || {}).description || ''));
  return r.result && r.result.value;
};
const shot = async (name) => {
  const s = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
  writeFileSync(`../shot-live-${name}-${suffix}.png`, Buffer.from(s.data, 'base64'));
};
const check = (label, ok, detail = '') => console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${label}${detail ? '  ' + detail : ''}`);

await send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile, screenWidth: width, screenHeight: height });
await send('Page.enable');
await send('Network.enable');
await send('Network.setCacheDisabled', { cacheDisabled: true });
await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: scheme }] });

console.log(`\n== ${suffix} (${width}x${height}${mobile ? ' mobile' : ''}, ${scheme}) ==`);
await send('Page.navigate', { url: 'http://localhost:8123/app.html' });
await sleep(2600);
await ev(`localStorage.clear(); return 1;`);
await send('Page.reload'); await sleep(2600);

check('banks loaded', (await ev(`return Object.keys(DATA).length;`)) === 5);
check('home has an ad container', await ev(`return !!document.querySelector('#page-home .adslot');`));
await shot('home');

// --- start a paper -------------------------------------------------------
await ev(`document.querySelector('[data-topic="futures"]').click(); return 1;`);
check('paper is 100 questions', (await ev(`return STATE.questions.length;`)) === 100);
check('navigator built 100 cells', (await ev(`return document.querySelectorAll('#qs-nav i').length;`)) === 100);
check('current cell marked', (await ev(`return document.querySelectorAll('#qs-nav i.now').length;`)) === 1);
check('quiz has an ad container', await ev(`return !!document.querySelector('#page-quiz .adslot');`));

// answer a few, navigator should track
await ev(`for (let k=0;k<5;k++){ STATE.idx=k; renderQuiz();
            document.querySelectorAll('#q-options .option')[0].click(); } return 1;`);
check('navigator tracks answers', (await ev(`return document.querySelectorAll('#qs-nav i.done').length;`)) >= 4);

// jump via the navigator
await ev(`document.querySelectorAll('#qs-nav i')[41].click(); return 1;`);
check('clicking a cell jumps', (await ev(`return STATE.idx;`)) === 41,
      'counter=' + await ev(`return el('quiz-counter').textContent;`));
await shot('quiz');

// --- submit --------------------------------------------------------------
await ev(`STATE.questions.forEach((q,i)=>{ if(STATE.answers[i]===null) STATE.answers[i]=q.answer; });
          window.confirm=()=>true; el('btn-submit-side').click(); return 1;`);
check('results shown', !(await ev(`return el('page-results').classList.contains('hidden');`)));
check('per-subject rows', (await ev(`return document.querySelectorAll('#result-subjects .row').length;`)) === 2);
check('results has an ad container', await ev(`return !!document.querySelector('#page-results .adslot');`));
await shot('results');

// --- history -------------------------------------------------------------
await ev(`el('btn-home').click(); document.querySelector('.topbar [data-nav="history"]').click(); return 1;`);
check('history row present', (await ev(`return document.querySelectorAll('.hist-row').length;`)) === 1);
check('per-subject column filled', ((await ev(`return (document.querySelector('.subj-cell')||{}).textContent||'';`)) || '').includes('%'));
check('history has an ad container', await ev(`return !!document.querySelector('#page-history .adslot');`));
await shot('history');

await ev(`document.querySelector('.hist-row').click(); return 1;`);
check('detail shown', !(await ev(`return el('page-history-detail').classList.contains('hidden');`)));
check('detail has an ad container', await ev(`return !!document.querySelector('#page-history-detail .adslot');`));
await shot('detail');

await ev(`document.querySelector('.topbar [data-nav="review"]').click(); return 1;`);
check('review has an ad container', await ev(`return !!document.querySelector('#page-review .adslot');`));
await shot('review');

console.log('  JS ERRORS:', errs.length ? errs : 'none');
ws.close();
process.exit(errs.length ? 1 : 0);

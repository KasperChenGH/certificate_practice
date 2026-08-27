/**
 * Check the landing page's exam directory actually opens the right quiz.
 *
 *   SHOOT_PORT=9333 node linktest.mjs
 *
 * Asserts the link targets, that a deep link starts the matching paper with the right
 * blueprint, that 收錄中 rows are inert, and — the one that matters — that arriving
 * with ?topic= while a paper is in progress does NOT discard it.
 */
import { get } from 'node:http';

const port = Number(process.env.SHOOT_PORT || 9333);
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
const send = (m, p = {}) => new Promise((res, rej) => {
  const i = ++id; pending.set(i, res);
  ws.send(JSON.stringify({ id: i, method: m, params: p }));
  setTimeout(() => rej(new Error('CDP timeout: ' + m)), 30000);
});
ws.onmessage = (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); }
};
await new Promise((r, j) => { ws.onopen = r; setTimeout(() => j(new Error('ws')), 10000); });

const errs = [];
const ev = async (expr) => {
  const r = await send('Runtime.evaluate', { expression: `(()=>{${expr}})()`, returnByValue: true, awaitPromise: true });
  if (r.exceptionDetails) errs.push(r.exceptionDetails.text);
  return r.result && r.result.value;
};
const go = async (url, wait = 2600) => { await send('Page.navigate', { url }); await sleep(wait); };
const check = (l, ok, d = '') => console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${l}${d ? '  ' + d : ''}`);

await send('Page.enable');
await send('Network.enable');
await send('Network.setCacheDisabled', { cacheDisabled: true });
await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false, screenWidth: 1440, screenHeight: 900 });

console.log('\n== landing directory links ==');
await go('http://localhost:8123/index.html');

const links = await ev(`return [...document.querySelectorAll('.exam a.rowinner')]
  .map(a => a.getAttribute('href'));`);
check('six rows link', links.length === 6, links.join(' '));
check('every live bank is reachable from the directory',
  ['futures','securities','securities_rep','sitca','finance_ethics','cfa_fra']
    .every(t => links.includes('/app.html?topic=' + t)));
check('every link carries a topic', links.every(h => h.startsWith('/app.html?topic=') && h.length > 16));
check('no bank is listed twice', new Set(links).size === links.length);
check('the two certificates that share a paper share one row',
  await ev(`const a = [...document.querySelectorAll('.exam a.rowinner')]
              .find(x => x.getAttribute('href').endsWith('securities_rep'));
            const n = a.querySelector('.nm').textContent;
            return n.includes('證券商業務員') && n.includes('證券交易相關法規與實務乙科');`));
check('收錄中 rows are inert',
  (await ev(`return document.querySelectorAll('.exam.soon a').length;`)) === 0);
check('link covers the whole row, not just the text',
  await ev(`const a = document.querySelector('.exam a.rowinner');
            return a.getBoundingClientRect().height > 30;`));

console.log('\n== deep links start the right paper ==');
const EXPECT = { futures: 100, securities: 150, securities_rep: 50, sitca: 50,
                 finance_ethics: 50, cfa_fra: 90 };
for (const [topic, size] of Object.entries(EXPECT)) {
  await go(`http://localhost:8123/app.html?topic=${topic}`);
  await ev(`localStorage.clear(); return 1;`);
  await go(`http://localhost:8123/app.html?topic=${topic}`);
  const onQuiz = await ev(`return !el('page-quiz').classList.contains('hidden');`);
  const got = await ev(`return STATE ? STATE.questions.length : 0;`);
  const t = await ev(`return STATE ? STATE.topic : null;`);
  check(`?topic=${topic}`, onQuiz && t === topic && got === size, `${t} ${got} questions`);
}

console.log('\n== an unfinished paper is not discarded ==');
await ev(`localStorage.clear(); return 1;`);
await go('http://localhost:8123/app.html?topic=futures');
await ev(`for (let k=0;k<7;k++){ STATE.idx=k; renderQuiz();
            document.querySelectorAll('#q-options .option')[0].click(); } return 1;`);
const before = await ev(`return (loadSavedQuiz()||{}).answers.filter(a=>a!==null).length;`);
await go('http://localhost:8123/app.html?topic=cfa_fra');
const onHome = await ev(`return !el('page-home').classList.contains('hidden');`);
const after = await ev(`return (loadSavedQuiz()||{}).answers.filter(a=>a!==null).length;`);
const banner = await ev(`return !el('resume-banner').classList.contains('hidden');`);
check('lands on home instead of starting over', onHome);
check('the in-progress answers survive', before === 7 && after === 7, `${before} -> ${after}`);
check('resume banner is offered', banner);

console.log('  JS ERRORS:', errs.length ? errs : 'none');
ws.close();
process.exit(errs.length ? 1 : 0);

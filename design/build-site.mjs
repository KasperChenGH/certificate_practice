/**
 * Build the live landing page from the design source.
 *
 *   node design/build-site.mjs
 *
 * Main.dc.html is the one home for the landing page: this unwraps its <helmet> and
 * <x-dc> into a standalone ../index.html with a real <head>. Editing the design and
 * editing the site are the same act, so the two cannot drift.
 *
 * Ad slots are emitted as empty reserved containers with the AdSense snippet's place
 * marked in a comment — the publisher/slot ids are not in the repo, so nothing here
 * pretends to be a working ad unit.
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, 'Main.dc.html');
const out = join(here, '..', 'index.html');

const raw = readFileSync(src, 'utf8');
const helmet = raw.match(/<helmet>([\s\S]*?)<\/helmet>/i);
const dc = raw.match(/<x-dc>([\s\S]*?)<\/x-dc>/i);
if (!dc) throw new Error('Main.dc.html: no <x-dc> block');

let body = dc[1].replace(/<helmet>[\s\S]*?<\/helmet>/i, '').trim();

// The design marks ad space with a labelled placeholder; the live page ships the
// reserved container and a comment showing exactly where the snippet goes.
let slots = 0;
body = body.replace(
  /<div class="adslot">[^<]*<\/div>/g,
  () => {
    slots++;
    return '<div class="adslot" data-ad-slot="' + slots + '">\n' +
      '        <!-- AdSense: paste the <ins class="adsbygoogle"> unit here.\n' +
      '             Keep this container: its reserved height stops the ad shifting\n' +
      '             the page when it loads (CLS). Desktop 728x90, mobile 300x250. -->\n' +
      '      </div>';
  });

writeFileSync(out, `<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#1e3a5f">
<title>金融證照練習 — 依正式考卷結構出題</title>
<meta name="description" content="台灣證券、期貨、投信投顧從業人員資格測驗與 CFA 練習題庫。依正式考試的科目配比抽題，分科計分，附逐選項解析。免費、免註冊。">
<link rel="canonical" href="https://certifications.courses/">
<meta property="og:title" content="金融證照練習 — 依正式考卷結構出題">
<meta property="og:description" content="台灣四張金融證照與 CFA Level I FRA，共 1,699 題。每份練習卷依正式考試的科目配比抽題，並分科計分。">
<meta property="og:type" content="website">
<meta property="og:url" content="https://certifications.courses/">
${(helmet ? helmet[1] : '').trim()}
</head>
<body>
${body}
</body>
</html>
`, 'utf8');

console.log(`built ${out} (${slots} ad slot${slots === 1 ? '' : 's'} reserved)`);

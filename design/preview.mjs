/**
 * Render a .dc.html artboard as a standalone page for screenshotting.
 *
 * The artboard is the source of truth; this only unwraps it, so the loop
 * (change -> screenshot -> critique -> change) never edits a second copy that
 * can drift from the one that actually gets published.
 *
 *   node preview.mjs Main.dc.html _preview.Main.html
 *
 * Only valid for artboards with no {{holes}} and no <script data-dc-script>:
 * those need the editor runtime, which this deliberately does not emulate.
 */
import { readFileSync, writeFileSync } from 'node:fs';

const [, , src, out] = process.argv;
if (!src || !out) {
  console.error('usage: node preview.mjs <in.dc.html> <out.html>');
  process.exit(2);
}

const raw = readFileSync(src, 'utf8');

const helmet = raw.match(/<helmet>([\s\S]*?)<\/helmet>/i);
const dc = raw.match(/<x-dc>([\s\S]*?)<\/x-dc>/i);
if (!dc) {
  console.error(`${src}: no <x-dc> block found`);
  process.exit(1);
}

const body = dc[1].replace(/<helmet>[\s\S]*?<\/helmet>/i, '').trim();

// A hole or logic block would render as literal text here and mislead the critique.
const holes = body.match(/\{\{[^}]+\}\}/g);
if (holes) {
  console.error(`${src}: contains ${holes.length} template hole(s) ` +
                `(${holes.slice(0, 3).join(', ')}) — preview cannot resolve them`);
  process.exit(1);
}
if (/<script\b[^>]*data-dc-script/i.test(raw)) {
  console.error(`${src}: has a data-dc-script logic block — preview cannot run it`);
  process.exit(1);
}

writeFileSync(out, `<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>preview — ${src}</title>
${(helmet ? helmet[1] : '').trim()}
</head>
<body>
${body}
</body>
</html>
`, 'utf8');

console.log(`preview: ${src} -> ${out} (${body.length} chars of markup)`);

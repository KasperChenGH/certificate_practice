/**
 * Generate the app-screen artboards.
 *
 * Artboards share nothing at runtime, so every screen needs its own copy of the
 * shell CSS. Maintaining six hand-written copies would drift within a day, so the
 * shell lives here once and each screen supplies only its body. The .dc.html files
 * this writes are still the artboard source that gets seeded.
 *
 *   node build-screens.mjs
 *
 * Tokens are lifted from the real app (index.html), not approximated: the mockups
 * have to match what ships. The one addition is Noto Serif TC on page titles, which
 * ties the app screens to the landing page.
 */
import { writeFileSync } from 'node:fs';

const SHELL = `
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@700&display=swap">
  <style>
    :root {
      --bg: #f5f5f7; --card: #ffffff; --text: #1d1d1f; --muted: #6e6e73;
      --accent: #1e3a5f; --accent-soft: #2a4d7c; --good: #1f8a3e; --bad: #c63838;
      --border: #d2d2d7; --ember: #b8551c;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0; background: var(--bg); color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Microsoft JhengHei", "PingFang TC", "Noto Sans CJK TC", sans-serif;
      font-size: 16px; line-height: 1.55; -webkit-font-smoothing: antialiased;
    }
    a { color: var(--accent); text-decoration: none; }
    a:hover { color: var(--accent-soft); }
    .app { max-width: 720px; margin: 0 auto; padding: 16px 16px 40px; }
    h1 { font-family: "Noto Serif TC", "Songti TC", serif; font-size: 22px; margin: 12px 0 16px; font-weight: 700; }
    h2 { font-size: 18px; margin: 16px 0 8px; font-weight: 600; }
    .meta { color: var(--muted); font-size: 14px; margin-top: 4px; }

    .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px; margin-bottom: 12px; }
    .btn {
      display: block; width: 100%; background: var(--accent); color: #fff; border: none;
      border-radius: 10px; padding: 16px; font-size: 17px; font-weight: 600;
      margin-bottom: 12px; text-align: center; font-family: inherit;
    }
    .btn.secondary { background: #e8e8ed; color: var(--text); }
    .btn.review { background: var(--ember); }
    .btn-row { display: flex; gap: 8px; }
    .btn-row .btn { flex: 1; margin-bottom: 0; }
    .topic-meta { font-size: 13px; opacity: 0.85; margin-top: 4px; font-weight: 400; }

    .stat-row { display: flex; gap: 8px; margin-bottom: 16px; }
    .stat { flex: 1; min-width: 0; background: var(--card); border: 1px solid var(--border);
            border-radius: 10px; padding: 10px 6px; text-align: center; }
    .stat .num { font-size: 20px; font-weight: 700; color: var(--accent); }
    .stat .lbl { font-size: 11px; color: var(--muted); margin-top: 2px; white-space: nowrap; }

    .progress-wrap { padding: 8px 0 4px; }
    .progress-bar { height: 4px; background: #e0e0e5; border-radius: 2px; overflow: hidden; }
    .progress-fill { height: 100%; background: var(--accent); }
    .progress-label { font-size: 13px; color: var(--muted); margin-top: 4px; display: flex; justify-content: space-between; }

    .question { font-size: 16px; font-weight: 600; margin-bottom: 14px; line-height: 1.55; }
    .options { display: flex; flex-direction: column; gap: 8px; }
    .option { background: var(--card); border: 1.5px solid var(--border); border-radius: 10px;
              padding: 14px; display: flex; align-items: flex-start; gap: 10px; font-size: 15px; }
    .option.correct { border-color: var(--good); background: #e6f4ea; }
    .option.wrong { border-color: var(--bad); background: #fbeaea; }
    .option .letter { font-weight: 700; min-width: 22px; color: var(--accent); }
    .option.correct .letter { color: var(--good); }
    .option.wrong .letter { color: var(--bad); }

    .feedback { margin-top: 14px; padding: 10px 12px; border-radius: 8px; font-size: 14px; line-height: 1.5; }
    .feedback.wrong { background: #fbeaea; color: var(--bad); border-left: 4px solid var(--bad); }
    .feedback .answer-text { color: var(--text); font-weight: 600; margin-top: 4px; }
    .expl-block { margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(0,0,0,0.12); }
    .expl-title { font-size: 11px; font-weight: 700; color: var(--muted); letter-spacing: 0.5px; margin-bottom: 8px; }
    .expl-item { font-size: 13px; line-height: 1.55; margin-bottom: 8px; display: flex; gap: 6px; color: var(--text); }
    .expl-item .expl-letter { font-weight: 700; min-width: 26px; flex-shrink: 0; }
    .expl-item.expl-correct .expl-letter { color: var(--good); }
    .expl-item.expl-sel-wrong .expl-letter { color: var(--bad); }

    .result-summary { text-align: center; padding: 20px; background: var(--card);
                      border: 1px solid var(--border); border-radius: 12px; margin-bottom: 16px; }
    .result-summary .big { font-size: 36px; font-weight: 700; margin: 8px 0; }
    .result-summary .pct { color: var(--accent); }
    .subject-table { margin: 12px 0 0; font-size: 14px; }
    .subject-table .row { display: flex; align-items: center; gap: 10px; padding: 7px 0; border-top: 1px solid var(--border); }
    .subject-table .row .nm { flex: 1; min-width: 0; text-align: left; }
    .subject-table .row .sc { font-variant-numeric: tabular-nums; font-weight: 600; }
    .subject-table .row .vd { font-size: 12px; padding: 2px 8px; border-radius: 999px; }
    .subject-table .row .vd.pass { color: var(--good); background: rgba(31,138,62,0.12); }
    .subject-table .row .vd.fail { color: var(--bad); background: rgba(198,56,56,0.12); }

    .result-q { border-left: 4px solid var(--bad); padding: 12px 14px; background: var(--card);
                margin-bottom: 10px; border-radius: 4px 10px 10px 4px; }
    .result-q .stem { font-weight: 600; margin-bottom: 8px; font-size: 15px; }
    .result-q .opt { font-size: 14px; padding: 2px 0; }
    .result-q .origin { color: var(--muted); font-size: 12px; margin-top: 6px; }
    .your-line { color: var(--bad); font-size: 14px; margin-top: 6px; }
    .review-q { border-left-color: var(--accent); }

    .hist-row { display: flex; align-items: center; gap: 12px; padding: 12px 14px; background: var(--card);
                border: 1px solid var(--border); border-radius: 10px; margin-bottom: 8px; }
    .hist-row .grow { flex: 1; min-width: 0; }
    .hist-row .topic { font-weight: 600; font-size: 15px; margin-bottom: 2px; }
    .hist-row .when { font-size: 13px; color: var(--muted); }
    .hist-row .chev { color: var(--muted); font-size: 18px; }
    .score-pill { font-weight: 700; font-size: 15px; padding: 4px 10px; border-radius: 999px; white-space: nowrap; }
    .score-pill.pass { color: var(--good); background: rgba(31,138,62,0.12); }
    .score-pill.fail { color: var(--bad); background: rgba(198,56,56,0.12); }
    .hist-summary { background: var(--card); border: 1px solid var(--border); border-radius: 10px;
                    padding: 10px 14px; margin-bottom: 8px; font-size: 13px; }
    .hist-summary .name { font-weight: 600; font-size: 14px; margin-bottom: 4px; }
    .hist-summary .figs { color: var(--muted); }
    .hist-summary .figs b { color: var(--text); font-weight: 600; }
    .footer-note { color: var(--muted); font-size: 12px; text-align: center; margin-top: 24px; }

    /* Reserved ad space. Height is fixed so a late-loading ad cannot push the page
       around (CLS), and .adband keeps a gap between the ad and any control. */
    .adband { padding: 22px 0 4px; }
    .adband.top-rule { margin-top: 20px; border-top: 1px solid var(--border); padding-top: 26px; }
    .adslot {
      min-height: 258px; display: flex; align-items: center; justify-content: center;
      border: 1px dashed #c9c9ce; border-radius: 10px; background: #fafafb;
      color: #a1a1a6; font-size: 12px; letter-spacing: 1px; text-align: center;
    }
  </style>`;

const SCREENS = {
  Home: `
<div class="app">
  <h1>金融證照練習</h1>
  <div class="stat-row">
    <div class="stat"><div class="num">1,284</div><div class="lbl">總作答數</div></div>
    <div class="stat"><div class="num">73%</div><div class="lbl">整體正確率</div></div>
    <div class="stat"><div class="num">38</div><div class="lbl">常錯題庫</div></div>
  </div>

  <div class="card" style="border-left: 4px solid var(--accent);">
    <div style="font-weight:600;margin-bottom:4px;">繼續上次測驗</div>
    <div class="meta">期貨商業務員　已作答 63 / 100 題</div>
    <div class="btn-row" style="margin-top:10px;">
      <div class="btn">繼續作答</div>
      <div class="btn secondary">捨棄</div>
    </div>
  </div>

  <h2>選擇測驗類別</h2>
  <div class="btn">期貨商業務員<div class="topic-meta">691 題　每回 100 題：期貨交易法規 50＋期貨交易理論與實務 50</div></div>
  <div class="btn">證券商高級業務員<div class="topic-meta">297 題　每回 150 題：投資學 50＋財務分析 50＋法規與實務 50</div></div>
  <div class="btn">證券商業務員<div class="topic-meta">100 題　每回 50 題：證券交易相關法規與實務 50</div></div>
  <div class="btn">投信投顧業務員<div class="topic-meta">97 題　每回 50 題：投信投顧相關法規 50</div></div>
  <div class="btn">CFA Level I — Financial Reporting &amp; Analysis<div class="topic-meta">514 題　每回 90 題：13 個主題</div></div>
  <div class="btn review">常錯題複習</div>
  <div class="btn secondary">測驗紀錄</div>
  <div class="adband top-rule"><div class="adslot">廣告版位　300×250</div></div>
  <p class="footer-note">作答紀錄存於本機瀏覽器（localStorage），不會上傳。</p>
</div>`,

  Quiz: `
<div class="app">
  <div class="progress-wrap">
    <div class="progress-bar"><div class="progress-fill" style="width: 8%"></div></div>
    <div class="progress-label"><span>期貨商業務員</span><span>8 / 100</span></div>
  </div>
  <div class="card">
    <div class="question">8. 提供客戶期貨交易諮詢服務且收取費用之專業投資顧問之英文簡稱為:</div>
    <div class="options">
      <div class="option correct"><span class="letter">(A)</span><span>CTA</span></div>
      <div class="option"><span class="letter">(B)</span><span>FCM</span></div>
      <div class="option wrong"><span class="letter">(C)</span><span>CPO</span></div>
      <div class="option"><span class="letter">(D)</span><span>IB</span></div>
    </div>
    <div class="feedback wrong">
      ✗ 答錯了
      <div class="answer-text">正解：(A) CTA</div>
      <div class="expl-block">
        <div class="expl-title">解析</div>
        <div class="expl-item expl-correct"><span class="expl-letter">(A)</span><span>正確。CTA（Commodity Trading Advisor）為提供期貨交易諮詢服務並收取費用之專業投資顧問。</span></div>
        <div class="expl-item"><span class="expl-letter">(B)</span><span>錯誤。FCM（Futures Commission Merchant）為期貨經紀商，代客買賣期貨。</span></div>
        <div class="expl-item expl-sel-wrong"><span class="expl-letter">(C)</span><span>錯誤。CPO（Commodity Pool Operator）為商品基金經理人，係募集基金操作期貨者。</span></div>
        <div class="expl-item"><span class="expl-letter">(D)</span><span>錯誤。IB（Introducing Broker）為期貨交易輔助人，不直接提供諮詢收費服務。</span></div>
      </div>
    </div>
  </div>
  <div class="btn-row" style="margin-top:16px;">
    <div class="btn secondary">上一題</div>
    <div class="btn">下一題</div>
  </div>
  <div style="margin-top:32px;padding-top:12px;border-top:1px solid var(--border);">
    <div class="btn secondary">儲存並回到首頁</div>
    <div class="btn secondary" style="color:var(--bad);margin-bottom:0;">放棄並回首頁</div>
  </div>
  <div class="adband top-rule"><div class="adslot">廣告版位　300×250</div></div>
</div>`,

  Results: `
<div class="app">
  <div class="result-summary">
    <div>本次得分</div>
    <div class="big"><span class="pct">78</span> / 100</div>
    <div class="meta">期貨商業務員　答錯 22 題</div>
    <div class="subject-table">
      <div class="row"><span class="nm">期貨交易法規</span><span class="sc">43/50　86%</span><span class="vd pass">及格</span></div>
      <div class="row"><span class="nm">期貨交易理論與實務</span><span class="sc">35/50　70%</span><span class="vd pass">及格</span></div>
    </div>
  </div>
  <div class="btn">檢視本次錯題</div>
  <div class="btn secondary">回首頁</div>

  <div class="card" style="margin-top:20px;background:#fdf6ef;border-color:#e8d5c0;border-left:4px solid var(--ember);border-radius:4px 12px 12px 4px;">
    <div style="font-size:13px;font-weight:700;color:var(--ember);margin-bottom:6px;">兩科都要過</div>
    <div style="font-size:14px;line-height:1.7;color:#6b4a30;">總分 78 分只是參考。正式測驗任一科未達 70% 即為不及格，所以這兩列才是你要看的。</div>
  </div>
  <div class="adband"><div class="adslot">廣告版位　300×250</div></div>
</div>`,

  Review: `
<div class="app">
  <h1>常錯題複習</h1>
  <p class="meta">2 題（最近 10 次作答中答錯率 ≥ 50%、且至少作答 3 次）</p>

  <div class="result-q review-q" style="margin-top:16px;">
    <div class="stem">1. 提供客戶期貨交易諮詢服務且收取費用之專業投資顧問之英文簡稱為:</div>
    <div class="opt" style="color:var(--good);font-weight:600;">✓ (A) CTA</div>
    <div class="opt" style="color:var(--muted);">　 (B) FCM</div>
    <div class="opt" style="color:var(--muted);">　 (C) CPO</div>
    <div class="opt" style="color:var(--muted);">　 (D) IB</div>
    <div class="origin">正解：(A)　近期錯誤 4/6　112 年第1 次｜期貨交易理論與實務｜第 8 題</div>
  </div>

  <div class="result-q review-q">
    <div class="stem">2. 最近油價飆漲,小涵完全根據之前的預期放空利率期貨而賺了不少,請問他屬於:</div>
    <div class="opt" style="color:var(--muted);">　 (A) 避險者</div>
    <div class="opt" style="color:var(--good);font-weight:600;">✓ (B) 投機者</div>
    <div class="opt" style="color:var(--muted);">　 (C) 價差交易者</div>
    <div class="opt" style="color:var(--muted);">　 (D) 賭客</div>
    <div class="origin">正解：(B)　近期錯誤 3/5　112 年第1 次｜期貨交易理論與實務｜第 1 題</div>
  </div>

  <div class="adband"><div class="adslot">廣告版位　300×250</div></div>
  <div class="btn" style="margin-top:16px;">回首頁</div>
</div>`,

  History: `
<div class="app">
  <h1>測驗紀錄</h1>
  <p class="meta">共 6 次測驗紀錄（最多保留 50 次）</p>

  <div class="hist-summary" style="margin-top:16px;">
    <div class="name">期貨商業務員</div>
    <div class="figs">作答 <b>4</b> 次　最佳 <b>86%</b>　平均 <b>77%</b>　最近 <b>78%</b></div>
  </div>
  <div class="hist-summary">
    <div class="name">CFA Level I — Financial Reporting &amp; Analysis</div>
    <div class="figs">作答 <b>2</b> 次　最佳 <b>71%</b>　平均 <b>66%</b>　最近 <b>71%</b></div>
  </div>

  <div class="hist-row" style="margin-top:14px;">
    <div class="grow"><div class="topic">期貨商業務員</div><div class="when">2026/08/26 21:40　答錯 22 題</div></div>
    <span class="score-pill pass">78/100　78%</span><span class="chev">›</span>
  </div>
  <div class="hist-row">
    <div class="grow"><div class="topic">CFA Level I — FRA</div><div class="when">2026/08/25 09:12　答錯 26 題</div></div>
    <span class="score-pill pass">64/90　71%</span><span class="chev">›</span>
  </div>
  <div class="hist-row">
    <div class="grow"><div class="topic">期貨商業務員</div><div class="when">2026/08/24 20:05　答錯 34 題</div></div>
    <span class="score-pill fail">66/100　66%</span><span class="chev">›</span>
  </div>
  <div class="hist-row">
    <div class="grow"><div class="topic">投信投顧業務員</div><div class="when">2026/08/23 18:22　答錯 9 題</div></div>
    <span class="score-pill pass">41/50　82%</span><span class="chev">›</span>
  </div>

  <div class="adband"><div class="adslot">廣告版位　300×250</div></div>
  <div class="btn" style="margin-top:16px;">回首頁</div>
  <div class="btn secondary" style="color:var(--bad);">清除測驗紀錄</div>
</div>`,

  HistoryDetail: `
<div class="app">
  <h1>期貨商業務員</h1>
  <p class="meta">2026/08/26 21:40　得分 78 / 100（78%）　答錯 22 題</p>

  <div class="subject-table" style="margin-bottom:18px;">
    <div class="row"><span class="nm">期貨交易法規</span><span class="sc">43/50　86%</span><span class="vd pass">及格</span></div>
    <div class="row"><span class="nm">期貨交易理論與實務</span><span class="sc">35/50　70%</span><span class="vd pass">及格</span></div>
  </div>

  <div class="adband"><div class="adslot">廣告版位　300×250</div></div>

  <div class="result-q">
    <div class="stem">1. 提供客戶期貨交易諮詢服務且收取費用之專業投資顧問之英文簡稱為:</div>
    <div class="opt" style="color:var(--good);font-weight:600;">✓ (A) CTA</div>
    <div class="opt" style="color:var(--muted);">　 (B) FCM</div>
    <div class="opt" style="color:var(--bad);font-weight:600;">✗ (C) CPO</div>
    <div class="opt" style="color:var(--muted);">　 (D) IB</div>
    <div class="your-line">你的答案：(C)</div>
    <div class="expl-block">
      <div class="expl-title">解析</div>
      <div class="expl-item expl-correct"><span class="expl-letter">(A)</span><span>正確。CTA（Commodity Trading Advisor）為提供期貨交易諮詢服務並收取費用之專業投資顧問。</span></div>
      <div class="expl-item expl-sel-wrong"><span class="expl-letter">(C)</span><span>錯誤。CPO（Commodity Pool Operator）為商品基金經理人，係募集基金操作期貨者。</span></div>
    </div>
    <div class="origin">112 年第1 次｜期貨交易理論與實務｜第 8 題</div>
  </div>

  <div class="result-q">
    <div class="stem">2. 最近油價飆漲,小涵完全根據之前的預期放空利率期貨而賺了不少,請問他屬於:</div>
    <div class="opt" style="color:var(--muted);">　 (A) 避險者</div>
    <div class="opt" style="color:var(--good);font-weight:600;">✓ (B) 投機者</div>
    <div class="opt" style="color:var(--muted);">　 (C) 價差交易者</div>
    <div class="opt" style="color:var(--bad);font-weight:600;">✗ (D) 賭客</div>
    <div class="your-line">你的答案：(D)</div>
    <div class="origin">112 年第1 次｜期貨交易理論與實務｜第 1 題</div>
  </div>

  <div class="btn-row" style="margin-top:16px;">
    <div class="btn secondary">← 測驗紀錄</div>
    <div class="btn">回首頁</div>
  </div>
</div>`,
};

function emit(file, extraCss, body) {
  writeFileSync(file, `<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>${SHELL.replace('</style>', extraCss + '  </style>')}
</helmet>
${body.trim()}
</x-dc>
</body>
</html>
`, 'utf8');
  console.log(`wrote ${file}`);
}

for (const [name, body] of Object.entries(SCREENS)) {
  emit(`${name}.dc.html`, '', body);
}

/**
 * Generate the DESKTOP app artboards.
 *
 * These are not the phone layout in a wider frame. The shipped app is a 720px column
 * centred in ~360px of dead margin each side — mobile stretched onto a big screen.
 * Desktop gets horizontal space and a keyboard, so these use both:
 *
 *   首頁        exam cards in a grid, all five visible at once, top nav
 *   作答中      question navigator sidebar — jump to any of 100 questions, see at a
 *               glance what is answered. The single biggest desktop win here.
 *   成績        score and per-subject bars side by side, wrong questions in two columns
 *   常錯題複習   two-column card grid
 *   測驗紀錄     a real table, not stacked cards, with the per-topic summary beside it
 *   紀錄明細     sticky score panel left, wrong questions right
 *
 * Ads: every screen carries one, always AFTER that screen's primary interaction and
 * in a different column or grid cell from it. 作答中 is the one to watch — people tap
 * fast through 100 questions and an ad near the options is the accidental-click
 * pattern AdSense penalises — so its slot sits at the foot of the side panel, below
 * 交卷 and 儲存並離開, never beside the options.
 *
 *   node build-desktop.mjs
 */
import { writeFileSync } from 'node:fs';

const CSS = `
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
    .serif { font-family: "Noto Serif TC", "Songti TC", serif; }

    /* Desktop chrome the phone build has no room for. */
    .topbar {
      background: var(--card); border-bottom: 1px solid var(--border);
      display: flex; align-items: center; gap: 28px; padding: 0 40px; height: 60px;
    }
    .topbar .brand { font-family: "Noto Serif TC", serif; font-weight: 700; font-size: 18px; }
    .topbar .spacer { flex: 1; }
    .topbar a { color: var(--muted); font-size: 14px; text-decoration: none; }
    .topbar a.on { color: var(--accent); font-weight: 600; }

    .page { max-width: 1240px; margin: 0 auto; padding: 32px 40px 56px; }
    .page h1 { font-family: "Noto Serif TC", serif; font-size: 26px; margin: 0 0 6px; font-weight: 700; }
    .page .sub { color: var(--muted); font-size: 14px; margin: 0 0 26px; }

    .split { display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 28px; align-items: start; }
    .split-wide { display: grid; grid-template-columns: 300px minmax(0, 1fr); gap: 28px; align-items: start; }

    .card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }
    .adslot {
      display: flex; align-items: center; justify-content: center; text-align: center;
      border: 1px dashed #c9c9ce; border-radius: 10px; background: #fafafb;
      color: #a1a1a6; font-size: 12px; letter-spacing: 1px;
    }

    /* ---- 首頁: a grid of exams, not a stack of full-width buttons ---- */
    .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 20px; }
    .stat { background: var(--card); border: 1px solid var(--border); border-radius: 10px; padding: 16px 18px; }
    .stat .num { font-size: 26px; font-weight: 700; color: var(--accent); line-height: 1.2; }
    .stat .lbl { font-size: 12px; color: var(--muted); margin-top: 2px; }
    .resume { display: flex; align-items: center; gap: 20px; border-left: 4px solid var(--accent); margin-bottom: 26px; }
    .resume .grow { flex: 1; }
    .resume .t { font-weight: 600; margin-bottom: 2px; }
    .resume .m { color: var(--muted); font-size: 14px; }
    .btn { border: none; border-radius: 9px; padding: 11px 20px; font-size: 15px; font-weight: 600;
           font-family: inherit; background: var(--accent); color: #fff; white-space: nowrap; }
    .btn.sec { background: #e8e8ed; color: var(--text); }
    .btn.wide { display: block; width: 100%; text-align: center; padding: 13px; }

    .exam-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }
    .exam-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px;
                 padding: 22px; display: flex; flex-direction: column; gap: 14px; }
    .exam-card .nm { font-size: 17px; font-weight: 700; line-height: 1.45; }
    .exam-card .n { font-size: 32px; font-weight: 700; color: var(--accent); line-height: 1; font-variant-numeric: tabular-nums; }
    .exam-card .n small { font-size: 13px; color: var(--muted); font-weight: 600; margin-left: 4px; }
    .exam-card .paper { font-size: 13px; line-height: 1.65; color: var(--muted);
                        margin-top: auto; padding-top: 14px; border-top: 1px solid var(--border); }

    /* ---- 作答中: the navigator is the point ---- */
    .quiz-grid { display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 28px; align-items: start; }
    .qhead { display: flex; align-items: baseline; gap: 12px; margin-bottom: 16px; }
    .qhead .no { font-size: 13px; font-weight: 700; color: var(--muted); letter-spacing: 1px; }
    .qstem { font-size: 19px; font-weight: 600; line-height: 1.6; margin-bottom: 22px; }
    .opts { display: flex; flex-direction: column; gap: 10px; }
    .opt { background: var(--card); border: 1.5px solid var(--border); border-radius: 10px;
           padding: 15px 18px; display: flex; align-items: center; gap: 14px; font-size: 16px; }
    .opt .key { font-size: 11px; font-weight: 700; color: var(--muted); border: 1px solid var(--border);
                border-radius: 5px; padding: 2px 7px; background: var(--bg); }
    .opt.correct { border-color: var(--good); background: #e6f4ea; }
    .opt.wrong { border-color: var(--bad); background: #fbeaea; }
    .opt.correct .key { border-color: var(--good); color: var(--good); }
    .opt.wrong .key { border-color: var(--bad); color: var(--bad); }
    .expl { margin-top: 18px; background: var(--card); border: 1px solid var(--border);
            border-left: 4px solid var(--bad); border-radius: 4px 12px 12px 4px; padding: 18px 20px; }
    .expl .h { font-size: 12px; font-weight: 700; color: var(--muted); letter-spacing: 1px; margin-bottom: 12px; }
    .expl .row { display: flex; gap: 10px; font-size: 14px; line-height: 1.65; margin-bottom: 9px; }
    .expl .row .l { font-weight: 700; min-width: 26px; }
    .expl .row.ok .l { color: var(--good); }
    .expl .row.no .l { color: var(--bad); }

    .navpanel { position: sticky; top: 24px; display: flex; flex-direction: column; gap: 16px; }
    .navpanel .bar { height: 5px; background: #e0e0e5; border-radius: 3px; overflow: hidden; margin-bottom: 8px; }
    .navpanel .bar span { display: block; height: 100%; background: var(--accent); }
    .navpanel .lbl { display: flex; justify-content: space-between; font-size: 13px; color: var(--muted); }
    .qnav { display: grid; grid-template-columns: repeat(10, 1fr); gap: 5px; margin-top: 14px; }
    .qnav i {
      font-style: normal; font-size: 11px; text-align: center; padding: 5px 0; border-radius: 5px;
      background: var(--bg); color: var(--muted); border: 1px solid var(--border);
      font-variant-numeric: tabular-nums;
    }
    .qnav i.done { background: var(--accent); color: #fff; border-color: var(--accent); }
    .qnav i.now { background: #fff; color: var(--accent); border-color: var(--accent); border-width: 2px; font-weight: 700; }
    .legend { display: flex; gap: 14px; font-size: 12px; color: var(--muted); margin-top: 12px; }
    .legend b { display: inline-block; width: 10px; height: 10px; border-radius: 3px; margin-right: 5px; vertical-align: -1px; }

    /* ---- 成績 ---- */
    .score-hero { display: flex; align-items: center; gap: 36px; }
    .score-hero .big { font-size: 60px; font-weight: 700; color: var(--accent); line-height: 1; font-variant-numeric: tabular-nums; }
    .score-hero .of { font-size: 15px; color: var(--muted); margin-top: 6px; }
    .subj { flex: 1; display: flex; flex-direction: column; gap: 14px; }
    .subj .r { display: grid; grid-template-columns: 200px 1fr 110px; gap: 14px; align-items: center; font-size: 14px; }
    .subj .track { height: 8px; background: #e8e8ed; border-radius: 4px; overflow: hidden; }
    .subj .track span { display: block; height: 100%; border-radius: 4px; }
    .subj .vd { font-size: 12px; padding: 2px 9px; border-radius: 999px; justify-self: end; }
    .subj .vd.pass { color: var(--good); background: rgba(31,138,62,0.12); }
    .subj .vd.fail { color: var(--bad); background: rgba(198,56,56,0.12); }

    /* ---- shared question cards ---- */
    .qcards { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
    .qcard { background: var(--card); border: 1px solid var(--border); border-left: 4px solid var(--bad);
             border-radius: 4px 12px 12px 4px; padding: 16px 18px; }
    .qcard.rev { border-left-color: var(--accent); }
    .qcard .s { font-weight: 600; font-size: 15px; margin-bottom: 10px; line-height: 1.55; }
    .qcard .o { font-size: 14px; padding: 2px 0; }
    .qcard .meta { color: var(--muted); font-size: 12px; margin-top: 8px; }
    .qcard .you { color: var(--bad); font-size: 13px; margin-top: 6px; }

    /* ---- 測驗紀錄: a table ---- */
    table { width: 100%; border-collapse: collapse; background: var(--card);
            border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
    th { text-align: left; font-size: 12px; font-weight: 700; color: var(--muted); letter-spacing: 0.5px;
         padding: 12px 18px; background: #fafafb; border-bottom: 1px solid var(--border); }
    td { padding: 14px 18px; border-bottom: 1px solid var(--border); font-size: 14px; }
    tr:last-child td { border-bottom: none; }
    td.sc { font-variant-numeric: tabular-nums; font-weight: 700; }
    .pill { font-size: 12px; padding: 3px 10px; border-radius: 999px; font-weight: 700; }
    .pill.pass { color: var(--good); background: rgba(31,138,62,0.12); }
    .pill.fail { color: var(--bad); background: rgba(198,56,56,0.12); }
    .sumcard { margin-bottom: 12px; }
    .sumcard .nm { font-weight: 600; font-size: 14px; margin-bottom: 6px; }
    .sumcard .fg { font-size: 13px; color: var(--muted); }
    .sumcard .fg b { color: var(--text); }
  </style>`;

const nav = () => {
  let out = '';
  for (let i = 1; i <= 100; i++) {
    const cls = i === 8 ? ' class="now"' : (i < 8 || (i < 64 && i % 3) ? ' class="done"' : '');
    out += `<i${cls}>${i}</i>`;
  }
  return out;
};

const TOPBAR = (on) => `
<div class="topbar">
  <span class="brand">金融證照練習</span>
  <a href="#" class="${on === 'home' ? 'on' : ''}">題庫</a>
  <a href="#" class="${on === 'review' ? 'on' : ''}">常錯題複習</a>
  <a href="#" class="${on === 'history' ? 'on' : ''}">測驗紀錄</a>
  <span class="spacer"></span>
  <a href="#">清除作答紀錄</a>
</div>`;

const SCREENS = {
  HomeDesktop: `${TOPBAR('home')}
<div class="page">
  <h1>題庫</h1>
  <p class="sub">選一張證照開始。每份練習卷依正式考試的科目配比抽題。</p>

  <div class="stats">
    <div class="stat"><div class="num">1,284</div><div class="lbl">總作答數</div></div>
    <div class="stat"><div class="num">73%</div><div class="lbl">整體正確率</div></div>
    <div class="stat"><div class="num">38</div><div class="lbl">常錯題庫</div></div>
  </div>

  <div class="card resume">
    <div class="grow">
      <div class="t">繼續上次測驗</div>
      <div class="m">期貨商業務員　已作答 63 / 100 題</div>
    </div>
    <button class="btn">繼續作答</button>
    <button class="btn sec">捨棄</button>
  </div>

  <div class="exam-grid">
    <div class="exam-card">
      <div class="nm">期貨商業務員</div>
      <div class="n">691<small>題</small></div>
      <div class="paper">每回 100 題<br>期貨交易法規 50 ＋ 期貨交易理論與實務 50</div>
      <button class="btn wide">開始練習</button>
    </div>
    <div class="exam-card">
      <div class="nm">證券商高級業務員</div>
      <div class="n">297<small>題</small></div>
      <div class="paper">每回 150 題<br>投資學 50 ＋ 財務分析 50 ＋ 法規與實務 50</div>
      <button class="btn wide">開始練習</button>
    </div>
    <div class="exam-card">
      <div class="nm">證券商業務員</div>
      <div class="n">100<small>題</small></div>
      <div class="paper">每回 50 題<br>證券交易相關法規與實務 50</div>
      <button class="btn wide">開始練習</button>
    </div>
    <div class="exam-card">
      <div class="nm">投信投顧業務員</div>
      <div class="n">97<small>題</small></div>
      <div class="paper">每回 50 題<br>投信投顧相關法規 50</div>
      <button class="btn wide">開始練習</button>
    </div>
    <div class="exam-card">
      <div class="nm">CFA Level I — Financial Reporting &amp; Analysis</div>
      <div class="n">514<small>題</small></div>
      <div class="paper">每回 90 題，涵蓋 13 個主題<br>英文，三選一</div>
      <button class="btn wide">開始練習</button>
    </div>
    <div class="adslot">廣告版位　300×250<br>（格線第六格，不佔內容）</div>
  </div>
</div>`,

  QuizDesktop: `${TOPBAR('home')}
<div class="page">
  <div class="quiz-grid">
    <div>
      <div class="qhead"><span class="no">第 8 題 / 共 100 題</span></div>
      <div class="qstem">提供客戶期貨交易諮詢服務且收取費用之專業投資顧問之英文簡稱為:</div>
      <div class="opts">
        <div class="opt correct"><span class="key">A</span><span>CTA</span></div>
        <div class="opt"><span class="key">B</span><span>FCM</span></div>
        <div class="opt wrong"><span class="key">C</span><span>CPO</span></div>
        <div class="opt"><span class="key">D</span><span>IB</span></div>
      </div>
      <div class="expl">
        <div class="h">解析　正解 (A) CTA</div>
        <div class="row ok"><span class="l">(A)</span><span>正確。CTA（Commodity Trading Advisor）為提供期貨交易諮詢服務並收取費用之專業投資顧問。</span></div>
        <div class="row"><span class="l">(B)</span><span>錯誤。FCM（Futures Commission Merchant）為期貨經紀商，代客買賣期貨。</span></div>
        <div class="row no"><span class="l">(C)</span><span>錯誤。CPO（Commodity Pool Operator）為商品基金經理人，係募集基金操作期貨者。</span></div>
        <div class="row"><span class="l">(D)</span><span>錯誤。IB（Introducing Broker）為期貨交易輔助人，不直接提供諮詢收費服務。</span></div>
      </div>
      <div style="display:flex;gap:10px;margin-top:22px;">
        <button class="btn sec">← 上一題</button>
        <button class="btn">下一題 →</button>
      </div>
    </div>

    <div class="navpanel">
      <div class="card">
        <div style="font-weight:600;font-size:15px;margin-bottom:10px;">期貨商業務員</div>
        <div class="bar"><span style="width:63%"></span></div>
        <div class="lbl"><span>已作答 63 題</span><span>63 / 100</span></div>
        <div class="qnav">${nav()}</div>
        <div class="legend">
          <span><b style="background:var(--accent)"></b>已作答</span>
          <span><b style="background:#fff;border:1px solid var(--border)"></b>未作答</span>
        </div>
      </div>
      <button class="btn wide">交卷</button>
      <button class="btn sec wide">儲存並離開</button>
      <div style="font-size:12px;color:var(--muted);line-height:1.7;">
        鍵盤：<b>A–D</b> 選答　<b>←/→</b> 換題　<b>Enter</b> 下一題
      </div>
      <div class="adslot" style="height:250px;margin-top:8px;">廣告版位　300×250</div>
    </div>
  </div>
</div>`,

  ResultsDesktop: `${TOPBAR('home')}
<div class="page">
  <h1>期貨商業務員　成績</h1>
  <p class="sub">2026/08/26 21:40　100 題</p>

  <div class="split">
    <div class="card">
      <div class="score-hero">
        <div>
          <div class="big">78</div>
          <div class="of">／ 100 題</div>
        </div>
        <div class="subj">
          <div class="r">
            <span>期貨交易法規</span>
            <span class="track"><span style="width:86%;background:var(--good)"></span></span>
            <span class="vd pass">43/50　及格</span>
          </div>
          <div class="r">
            <span>期貨交易理論與實務</span>
            <span class="track"><span style="width:70%;background:var(--good)"></span></span>
            <span class="vd pass">35/50　及格</span>
          </div>
        </div>
      </div>
      <div style="margin-top:20px;padding-top:16px;border-top:1px solid var(--border);font-size:14px;line-height:1.75;color:var(--muted);">
        正式測驗任一科未達 70% 即為不及格，總分只是參考——所以上面兩條才是你要看的。
      </div>
    </div>

    <div style="display:flex;flex-direction:column;gap:12px;">
      <button class="btn wide">檢視本次 22 題錯題</button>
      <button class="btn sec wide">再考一次</button>
      <div class="adslot" style="height:250px;">廣告版位　300×250</div>
    </div>
  </div>

  <h2 style="font-size:16px;margin:32px 0 14px;">本次錯題（前 4 題）</h2>
  <div class="qcards">
    <div class="qcard">
      <div class="s">提供客戶期貨交易諮詢服務且收取費用之專業投資顧問之英文簡稱為:</div>
      <div class="o" style="color:var(--good);font-weight:600;">✓ (A) CTA</div>
      <div class="o" style="color:var(--bad);font-weight:600;">✗ (C) CPO</div>
      <div class="meta">112 年第1 次｜期貨交易理論與實務｜第 8 題</div>
    </div>
    <div class="qcard">
      <div class="s">最近油價飆漲,小涵完全根據之前的預期放空利率期貨而賺了不少,請問他屬於:</div>
      <div class="o" style="color:var(--good);font-weight:600;">✓ (B) 投機者</div>
      <div class="o" style="color:var(--bad);font-weight:600;">✗ (D) 賭客</div>
      <div class="meta">112 年第1 次｜期貨交易理論與實務｜第 1 題</div>
    </div>
  </div>
</div>`,

  ReviewDesktop: `${TOPBAR('review')}
<div class="page">
  <h1>常錯題複習</h1>
  <p class="sub">最近 10 次作答中答錯率 ≥ 50%、且至少作答 3 次的題目，共 2 題</p>
  <div class="split">
    <div class="qcards" style="grid-template-columns: repeat(2, minmax(0,1fr));">
      <div class="qcard rev">
        <div class="s">提供客戶期貨交易諮詢服務且收取費用之專業投資顧問之英文簡稱為:</div>
        <div class="o" style="color:var(--good);font-weight:600;">✓ (A) CTA</div>
        <div class="o" style="color:var(--muted);">　 (B) FCM</div>
        <div class="o" style="color:var(--muted);">　 (C) CPO</div>
        <div class="o" style="color:var(--muted);">　 (D) IB</div>
        <div class="meta">近期錯誤 4/6　112 年第1 次｜期貨交易理論與實務｜第 8 題</div>
      </div>
      <div class="qcard rev">
        <div class="s">最近油價飆漲,小涵完全根據之前的預期放空利率期貨而賺了不少,請問他屬於:</div>
        <div class="o" style="color:var(--muted);">　 (A) 避險者</div>
        <div class="o" style="color:var(--good);font-weight:600;">✓ (B) 投機者</div>
        <div class="o" style="color:var(--muted);">　 (C) 價差交易者</div>
        <div class="o" style="color:var(--muted);">　 (D) 賭客</div>
        <div class="meta">近期錯誤 3/5　112 年第1 次｜期貨交易理論與實務｜第 1 題</div>
      </div>
    </div>
    <div class="adslot" style="height:600px;">廣告版位　300×600</div>
  </div>
</div>`,

  HistoryDesktop: `${TOPBAR('history')}
<div class="page">
  <h1>測驗紀錄</h1>
  <p class="sub">共 6 次，最多保留 50 次</p>
  <div class="split-wide">
    <div>
      <div class="card sumcard">
        <div class="nm">期貨商業務員</div>
        <div class="fg">作答 <b>4</b> 次　最佳 <b>86%</b><br>平均 <b>77%</b>　最近 <b>78%</b></div>
      </div>
      <div class="card sumcard">
        <div class="nm">CFA Level I — FRA</div>
        <div class="fg">作答 <b>2</b> 次　最佳 <b>71%</b><br>平均 <b>66%</b>　最近 <b>71%</b></div>
      </div>
      <div class="adslot" style="height:250px;margin-top:16px;">廣告版位　300×250</div>
    </div>
    <table>
      <tr><th>日期</th><th>證照</th><th>分科</th><th>得分</th><th></th></tr>
      <tr>
        <td>08/26 21:40</td><td>期貨商業務員</td>
        <td style="color:var(--muted);font-size:13px;">法規 86%　實務 70%</td>
        <td class="sc">78/100</td><td><span class="pill pass">78%</span></td>
      </tr>
      <tr>
        <td>08/25 09:12</td><td>CFA Level I — FRA</td>
        <td style="color:var(--muted);font-size:13px;">13 個主題</td>
        <td class="sc">64/90</td><td><span class="pill pass">71%</span></td>
      </tr>
      <tr>
        <td>08/24 20:05</td><td>期貨商業務員</td>
        <td style="color:var(--muted);font-size:13px;">法規 74%　實務 58%</td>
        <td class="sc">66/100</td><td><span class="pill fail">66%</span></td>
      </tr>
      <tr>
        <td>08/23 18:22</td><td>投信投顧業務員</td>
        <td style="color:var(--muted);font-size:13px;">法規 82%</td>
        <td class="sc">41/50</td><td><span class="pill pass">82%</span></td>
      </tr>
      <tr>
        <td>08/22 11:03</td><td>期貨商業務員</td>
        <td style="color:var(--muted);font-size:13px;">法規 90%　實務 82%</td>
        <td class="sc">86/100</td><td><span class="pill pass">86%</span></td>
      </tr>
    </table>
  </div>
</div>`,

  HistoryDetailDesktop: `${TOPBAR('history')}
<div class="page">
  <div class="split-wide">
    <div style="position:sticky;top:24px;">
      <div class="card">
        <div style="font-family:'Noto Serif TC',serif;font-weight:700;font-size:18px;margin-bottom:4px;">期貨商業務員</div>
        <div style="color:var(--muted);font-size:13px;margin-bottom:16px;">2026/08/26 21:40</div>
        <div style="font-size:40px;font-weight:700;color:var(--accent);line-height:1;">78<span style="font-size:15px;color:var(--muted);font-weight:600;"> / 100</span></div>
        <div style="margin-top:18px;padding-top:14px;border-top:1px solid var(--border);font-size:13px;display:flex;flex-direction:column;gap:10px;">
          <div style="display:flex;justify-content:space-between;"><span>期貨交易法規</span><span class="pill pass">43/50</span></div>
          <div style="display:flex;justify-content:space-between;"><span>期貨交易理論與實務</span><span class="pill pass">35/50</span></div>
        </div>
      </div>
      <button class="btn sec wide" style="margin-top:12px;">← 回測驗紀錄</button>
      <div class="adslot" style="height:250px;margin-top:16px;">廣告版位　300×250</div>
    </div>

    <div>
      <h1 style="font-size:20px;">本次錯題　22 題</h1>
      <p class="sub">顯示你當時選的選項，以及正解。</p>
      <div class="qcards" style="grid-template-columns: minmax(0,1fr);">
        <div class="qcard">
          <div class="s">1. 提供客戶期貨交易諮詢服務且收取費用之專業投資顧問之英文簡稱為:</div>
          <div class="o" style="color:var(--good);font-weight:600;">✓ (A) CTA</div>
          <div class="o" style="color:var(--muted);">　 (B) FCM</div>
          <div class="o" style="color:var(--bad);font-weight:600;">✗ (C) CPO</div>
          <div class="o" style="color:var(--muted);">　 (D) IB</div>
          <div class="you">你的答案：(C)</div>
          <div class="meta">112 年第1 次｜期貨交易理論與實務｜第 8 題</div>
        </div>
        <div class="qcard">
          <div class="s">2. 最近油價飆漲,小涵完全根據之前的預期放空利率期貨而賺了不少,請問他屬於:</div>
          <div class="o" style="color:var(--muted);">　 (A) 避險者</div>
          <div class="o" style="color:var(--good);font-weight:600;">✓ (B) 投機者</div>
          <div class="o" style="color:var(--muted);">　 (C) 價差交易者</div>
          <div class="o" style="color:var(--bad);font-weight:600;">✗ (D) 賭客</div>
          <div class="you">你的答案：(D)</div>
          <div class="meta">112 年第1 次｜期貨交易理論與實務｜第 1 題</div>
        </div>
      </div>
    </div>
  </div>
</div>`,
};

for (const [name, body] of Object.entries(SCREENS)) {
  const file = `${name}.dc.html`;
  writeFileSync(file, `<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>${CSS}
</helmet>
${body.trim()}
</x-dc>
</body>
</html>
`, 'utf8');
  console.log(`wrote ${file}`);
}

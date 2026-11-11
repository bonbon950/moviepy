/**
 * Bjorn's Shorts -> Google Drive helper. Version 7 (multi-channel: one copy of this script per channel's
 * Google account; nothing channel-specific is hard-coded — see CHANNEL SETTINGS below).
 * Can ONLY:
 *  - create/find "OUTPUT (...)" folders, list them, upload videos into them,
 *    restore (un-trash) files that belong to an OUTPUT folder;
 *  - read / add rows / update cells in the ONE spreadsheet named "POSTING PLAN";
 *  - delete ROWS of that sheet only when they are approved+posted or rejected (checked row by row);
 *  - v5: READ the YouTube channel (videos, status, view/like/comment counts) and READ YouTube Analytics;
 *    write hourly stat snapshots into a "STATS" tab of the POSTING PLAN.
 *  - v7: build a "DASHBOARD" tab (KPI tiles + charts + leaderboard) from those stats, every hour.
 * Cannot delete any file or folder. Cannot touch any other file or folder.
 * YouTube access is READ-ONLY (enforced by the scopes in appsscript.json): it cannot upload, edit,
 * delete, or change the visibility of anything on the channel.
 */
// ---- CHANNEL SETTINGS (the only part to change when copying this script for a new channel) ----------
// Must match the channel's settings file in the repo: shorts/channels/<id>/<id>_channel.json
var PLAN_NAME = 'POSTING PLAN';          // name of THIS channel's posting-plan sheet in its Drive
// Output folders: "OUTPUT (<date>)", optionally with a channel prefix, e.g. "KAI CENAT - OUTPUT (<date>)"
var OUT = /^(.+ - )?OUTPUT \(.+\)$/;
// -------------------------------------------------------------------------------------------------------

var PLAN_ID_CACHE = null;
function planId() {  // the one sheet named PLAN_NAME in this account's Drive (found by name, no hard-coded ID)
  if (PLAN_ID_CACHE) return PLAN_ID_CACHE;
  var it = DriveApp.getFilesByName(PLAN_NAME), ids = [];
  while (it.hasNext()) { var f = it.next(); if (!f.isTrashed() && f.getMimeType() === MimeType.GOOGLE_SHEETS) ids.push(f.getId()); }
  if (ids.length !== 1) throw 'expected exactly one sheet named "' + PLAN_NAME + '", found ' + ids.length;
  return (PLAN_ID_CACHE = ids[0]);
}

function isOutputFile(file) {
  var ps = file.getParents();
  while (ps.hasNext()) { if (OUT.test(ps.next().getName())) return true; }
  return false;
}

function planSheet(id) {
  var f = DriveApp.getFileById(id);
  if (f.getName() !== PLAN_NAME || f.getMimeType() !== MimeType.GOOGLE_SHEETS) throw 'not the POSTING PLAN sheet';
  return SpreadsheetApp.openById(id).getSheets()[0];
}

function stylePlan(sh) {  // keep it clean & easy to read (safe to run any time)
  var lastCol = 8, lastRow = Math.max(sh.getLastRow(), 1);
  sh.setFrozenRows(1);
  sh.getRange(1, 1, 1, lastCol).setFontWeight('bold').setBackground('#111111').setFontColor('#FFFFFF')
    .setHorizontalAlignment('center').setVerticalAlignment('middle');
  sh.setRowHeight(1, 36);
  var widths = [70, 90, 280, 380, 160, 190, 130, 210];
  for (var c = 0; c < widths.length; c++) sh.setColumnWidth(c + 1, widths[c]);
  if (lastRow > 1) {
    sh.getRange(2, 1, lastRow - 1, lastCol).setWrap(true).setVerticalAlignment('middle');
    sh.getRange(2, 1, lastRow - 1, 1).setFontWeight('bold').setHorizontalAlignment('center');
    sh.getRange(2, 7, lastRow - 1, 1).setHorizontalAlignment('center').setFontWeight('bold');
  }
}

function doPost(e) {
  var p = e.parameter;
  try {
    if (p.action === 'folder') {
      if (!OUT.test(p.name || '')) return out({error: 'folder name must be OUTPUT (...) or <PREFIX> - OUTPUT (...)'});
      var it = DriveApp.getFoldersByName(p.name);
      var f = it.hasNext() ? it.next() : DriveApp.createFolder(p.name);
      return out({id: f.getId(), url: f.getUrl()});
    }
    if (p.action === 'list') {
      var folder = DriveApp.getFolderById(p.folderId);
      if (!OUT.test(folder.getName())) return out({error: 'not an OUTPUT folder'});
      var files = [], fi = folder.getFiles();
      while (fi.hasNext()) {
        var x = fi.next();
        files.push({id: x.getId(), name: x.getName(), size: x.getSize(), trashed: x.isTrashed()});
      }
      return out({files: files});
    }
    if (p.action === 'restore') {
      var file = DriveApp.getFileById(p.fileId);
      if (!isOutputFile(file)) return out({error: 'file is not in an OUTPUT folder'});
      if (!file.isTrashed()) return out({ok: true, note: 'already not in trash', name: file.getName()});
      file.setTrashed(false);
      return out({ok: true, name: file.getName()});
    }
    if (p.action === 'sheet_read') {
      var sh = planSheet(p.sheetId);
      return out({values: sh.getDataRange().getDisplayValues()});
    }
    if (p.action === 'sheet_set') {  // one cell: row, col (1-based)
      var sh2 = planSheet(p.sheetId);
      sh2.getRange(Number(p.row), Number(p.col)).setValue(p.value);
      return out({ok: true});
    }
    if (p.action === 'sheet_append') {  // body = JSON array of rows (8 columns); inserted above "HOW TO USE:"
      var sh3 = planSheet(p.sheetId);
      var rows = JSON.parse(e.postData.contents);
      var vals = sh3.getDataRange().getValues(), at = vals.length + 1;
      for (var i = 0; i < vals.length; i++) { if (String(vals[i][0]).indexOf('HOW TO USE') === 0) { at = i; break; } }
      // keep one blank spacer row before HOW TO USE
      if (at <= vals.length) { sh3.insertRowsBefore(at, rows.length); } else { at = vals.length + 1; }
      sh3.getRange(at, 1, rows.length, rows[0].length).setValues(rows);
      stylePlan(sh3);
      return out({ok: true, firstRow: at, count: rows.length});
    }
    if (p.action === 'sheet_delete_rows') {
      // body = JSON [{row: 7, clip: 'CLIP6', approve: 'YES'}, ...]; a row is deleted only if it STILL shows
      // that clip name and that approval (YES = posted, NO = rejected). Header and HOW TO USE are never deleted.
      var sh4 = planSheet(p.sheetId);
      var reqs = JSON.parse(e.postData.contents).sort(function (a, b) { return b.row - a.row; });
      var v4 = sh4.getDataRange().getDisplayValues(), done = [], skipped = [];
      for (var k = 0; k < reqs.length; k++) {
        var q = reqs[k], row = Number(q.row), cur = v4[row - 1];
        var ap = cur ? String(cur[6]).trim().toUpperCase() : '';
        var ok = row > 1 && cur && String(cur[0]).trim() === q.clip && String(cur[0]).indexOf('HOW TO USE') !== 0 &&
                 ap === String(q.approve).toUpperCase() && (ap === 'YES' || ap === 'NO');
        if (ok) { sh4.deleteRow(row); done.push(q.clip); } else { skipped.push(q.clip); }
      }
      return out({ok: true, deleted: done, skipped: skipped});
    }
    if (p.action === 'sheet_style') {
      stylePlan(planSheet(p.sheetId));
      return out({ok: true});
    }
    // ---- v5: YouTube, read-only -------------------------------------------------------------------
    if (p.action === 'yt_videos') {      // latest uploads (public + scheduled/private) with live counts
      return out(ytVideos(Math.min(Number(p.max) || 50, 200)));
    }
    if (p.action === 'yt_analytics') {   // body = JSON {startDate, endDate, metrics, dimensions?, filters?, sort?, maxResults?}
      var q = JSON.parse(e.postData.contents || '{}');
      var opt = {ids: 'channel==MINE', startDate: q.startDate, endDate: q.endDate, metrics: q.metrics};
      ['dimensions', 'filters', 'sort', 'maxResults'].forEach(function (k) { if (q[k]) opt[k] = q[k]; });
      var rep = YouTubeAnalytics.Reports.query(opt);
      return out({columns: (rep.columnHeaders || []).map(function (c) { return c.name; }), rows: rep.rows || []});
    }
    if (p.action === 'dashboard') {      // v7: rebuild the DASHBOARD tab now
      return out(buildDashboard());
    }
    if (p.action === 'yt_stats_read') {  // the STATS tab (hourly snapshots)
      var st = statsSheet();
      return out({values: st.getDataRange().getDisplayValues()});
    }
    if (p.action === 'start') {
      var folder2 = DriveApp.getFolderById(p.folderId);
      if (!OUT.test(folder2.getName())) return out({error: 'not an OUTPUT folder'});
      if (!/^video\//.test(p.mime || '')) return out({error: 'videos only'});
      var dup = folder2.getFilesByName(p.name);
      while (dup.hasNext()) { if (!dup.next().isTrashed()) return out({error: 'duplicate: same name already in folder'}); }
      var r = UrlFetchApp.fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable', {
        method: 'post',
        contentType: 'application/json; charset=UTF-8',
        payload: JSON.stringify({name: p.name, parents: [p.folderId], mimeType: p.mime}),
        headers: {
          Authorization: 'Bearer ' + ScriptApp.getOAuthToken(),
          'X-Upload-Content-Type': p.mime,
          'X-Upload-Content-Length': String(p.size)
        },
        muteHttpExceptions: true
      });
      var h = r.getHeaders();
      return out({session: h['Location'] || h['location'] || null, code: r.getResponseCode()});
    }
    if (p.action === 'chunk') {
      if (!/^https:\/\/www\.googleapis\.com\/upload\/drive\//.test(p.session || '')) return out({error: 'bad session'});
      var bytes = Utilities.base64Decode(e.postData.contents);
      var start = Number(p.start), total = Number(p.size), end = start + bytes.length - 1;
      var r2 = UrlFetchApp.fetch(p.session, {
        method: 'put',
        contentType: 'application/octet-stream',
        payload: bytes,
        headers: {'Content-Range': 'bytes ' + start + '-' + end + '/' + total},
        muteHttpExceptions: true
      });
      var body = {};
      try { body = JSON.parse(r2.getContentText()); } catch (x) {}
      return out({code: r2.getResponseCode(), id: body.id || null});
    }
    return out({error: 'unknown action'});
  } catch (err) {
    return out({error: String(err)});
  }
}

function out(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

function authorizeSheets() {
  SpreadsheetApp.openById(planId()).getName();
}

// ---- v5: YouTube read-only helpers -----------------------------------------------------------------

function ytVideos(max) {
  var ch = YouTube.Channels.list('snippet,contentDetails,statistics', {mine: true}).items[0];
  var uploads = ch.contentDetails.relatedPlaylists.uploads, ids = [], token = '';
  do {
    var pl = YouTube.PlaylistItems.list('contentDetails', {playlistId: uploads, maxResults: 50, pageToken: token});
    pl.items.forEach(function (it) { ids.push(it.contentDetails.videoId); });
    token = pl.nextPageToken || '';
  } while (token && ids.length < max);
  ids = ids.slice(0, max);
  var vids = [];
  for (var i = 0; i < ids.length; i += 50) {
    var res = YouTube.Videos.list('snippet,status,statistics,contentDetails', {id: ids.slice(i, i + 50).join(',')});
    res.items.forEach(function (v) {
      vids.push({id: v.id, title: v.snippet.title, publishedAt: v.snippet.publishedAt,
                 privacy: v.status.privacyStatus, publishAt: v.status.publishAt || '',
                 duration: v.contentDetails.duration,
                 views: Number(v.statistics.viewCount || 0), likes: Number(v.statistics.likeCount || 0),
                 comments: Number(v.statistics.commentCount || 0)});
    });
  }
  return {channel: {title: ch.snippet.title, subscribers: Number(ch.statistics.subscriberCount || 0),
                    views: Number(ch.statistics.viewCount || 0), videos: Number(ch.statistics.videoCount || 0)},
          videos: vids};
}

function statsSheet() {  // "STATS" tab inside the POSTING PLAN (kept after the main tab)
  var ss = SpreadsheetApp.openById(planId()), sh = ss.getSheetByName('STATS');
  if (!sh) {
    sh = ss.insertSheet('STATS', ss.getSheets().length);
    sh.appendRow(['SNAPSHOT (PH time)', 'VIDEO ID', 'TITLE', 'WENT LIVE (PH time)', 'STATUS', 'VIEWS', 'LIKES', 'COMMENTS']);
    sh.setFrozenRows(1);
    sh.getRange(1, 1, 1, 8).setFontWeight('bold').setBackground('#111111').setFontColor('#FFFFFF');
  }
  return sh;
}

function snapshotStats() {  // runs every hour (installHourlyTrigger); public videos from the last 14 days
  var data = ytVideos(60), now = new Date(), cutoff = now.getTime() - 14 * 86400000, rows = [];
  var fmt = function (d) { return Utilities.formatDate(d, 'Asia/Manila', 'yyyy-MM-dd HH:mm'); };
  data.videos.forEach(function (v) {
    var live = new Date(v.publishAt || v.publishedAt);
    if (v.privacy === 'public' && live.getTime() >= cutoff) {
      rows.push([fmt(now), v.id, v.title, fmt(live), v.privacy, v.views, v.likes, v.comments]);
    }
  });
  if (rows.length) {
    var sh = statsSheet();
    sh.getRange(sh.getLastRow() + 1, 1, rows.length, rows[0].length).setValues(rows);
  }
  try { buildDashboard(); } catch (e) { console.error('dashboard: ' + e); }  // v7: charts never block the snapshot
}

function installHourlyTrigger() {  // run ONCE by hand: authorizes and starts the hourly snapshot (no duplicates)
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'snapshotStats') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('snapshotStats').timeBased().everyHours(1).create();
  snapshotStats();
}

// ---- v7: DASHBOARD tab — charts instead of plain numbers (rebuilt after every hourly snapshot) ------------
// Read-only like the rest: it only reads YouTube + the STATS tab and writes the DASHBOARD / DASH_DATA tabs
// of this channel's POSTING PLAN. All times are PH (Asia/Manila); ET = PH - 13 h (Nov-Mar).
var DASH = {bg: '#0F0F14', card: '#17171F', text: '#FFFFFF', sub: '#A9A9B8', grid: '#2A2A36',
            pink: '#FF2E88', green: '#39FF14', cyan: '#00E5FF', yellow: '#FFE14D', purple: '#9B5CFF', orange: '#FF8A00'};

function hourLabel(h) { h = ((h % 24) + 24) % 24; return (h % 12 || 12) + (h < 12 ? ' AM' : ' PM'); }

function ytRows(opt) {  // YouTube Analytics rows, [] when there is no data yet (new channel / delay)
  try {
    var o = {ids: 'channel==MINE'}; for (var k in opt) o[k] = opt[k];
    return YouTubeAnalytics.Reports.query(o).rows || [];
  } catch (e) { return []; }
}

function snapshotGains() {  // view gains between hourly snapshots: by PH hour of day + total of the last 7 days
  var vals = statsSheet().getDataRange().getDisplayValues(), per = {}, byHour = [], week = 0;
  for (var h = 0; h < 24; h++) byHour.push(0);
  var cutoff = Date.now() - 7 * 86400000;
  for (var i = 1; i < vals.length; i++) {
    var m = String(vals[i][0]).match(/^(\d{4})-(\d{2})-(\d{2})[ T](\d{1,2}):(\d{2})/);
    if (!m) continue;
    var t = Date.UTC(+m[1], +m[2] - 1, +m[3], +m[4] - 8, +m[5]);
    (per[vals[i][1]] = per[vals[i][1]] || []).push([t, +m[4], Number(String(vals[i][5]).replace(/,/g, '')) || 0]);
  }
  for (var id in per) {
    var s = per[id].sort(function (a, b) { return a[0] - b[0]; });
    for (var j = 1; j < s.length; j++) {
      var g = s[j][2] - s[j - 1][2];
      if (g > 0 && s[j][0] - s[j - 1][0] <= 2 * 3600000) { byHour[s[j][1]] += g; if (s[j][0] >= cutoff) week += g; }
    }
  }
  return {byHour: byHour, week: week};
}

function dashChart(sh, type, range, title, row, col, opts) {
  var b = sh.newChart().setChartType(type).addRange(range).setNumHeaders(1)
    .setHiddenDimensionStrategy(Charts.ChartHiddenDimensionStrategy.SHOW_BOTH)
    .setPosition(row, col, 6, 6)
    .setOption('title', title).setOption('width', 640).setOption('height', 340)
    .setOption('backgroundColor', DASH.card)
    .setOption('titleTextStyle', {color: DASH.text, fontSize: 15, bold: true})
    .setOption('legend', {position: 'none'})
    .setOption('hAxis', {textStyle: {color: DASH.sub}, gridlines: {color: DASH.grid}, baselineColor: DASH.grid})
    .setOption('vAxis', {textStyle: {color: DASH.sub}, gridlines: {color: DASH.grid}, baselineColor: DASH.grid, minValue: 0});
  for (var k in (opts || {})) b.setOption(k, opts[k]);
  sh.insertChart(b.build());
}

function buildDashboard() {
  var ss = SpreadsheetApp.openById(planId()), tz = 'Asia/Manila', now = new Date();
  var day = function (d) { return Utilities.formatDate(d, tz, 'yyyy-MM-dd'); };
  var yt = ytVideos(100), ch = yt.channel;
  var vids = yt.videos.filter(function (v) { return v.privacy === 'public'; });
  var live = function (v) { return new Date(v.publishAt || v.publishedAt); };
  var short = function (t, n) {  // drop #hashtags (not '#1'), cut on whole characters so emoji never break
    var c = Array.from(String(t).replace(/#[A-Za-z]\w*/g, '').replace(/\s+/g, ' ').trim());
    return c.length > n ? c.slice(0, n - 1).join('') + '…' : c.join('');
  };
  var gains = snapshotGains();
  var d90 = day(new Date(now.getTime() - 90 * 86400000)), d30 = day(new Date(now.getTime() - 30 * 86400000));

  // ---- data blocks (hidden DASH_DATA tab) -------------------------------------------------------------------
  var latest = vids.slice().sort(function (a, b) { return live(b) - live(a); }).slice(0, 12);
  var B = {
    shorts: [['Short', 'Views']].concat(latest.map(function (v) { return [short(v.title, 34), v.views]; })),
    daily: [['Day', 'Views']].concat(ytRows({startDate: d30, endDate: day(now), metrics: 'views', dimensions: 'day',
              sort: 'day'}).map(function (r) { return [String(r[0]).slice(5), r[1]]; })),
    country: [['Country', 'Views']].concat(ytRows({startDate: d90, endDate: day(now), metrics: 'views',
              dimensions: 'country', sort: '-views', maxResults: 15})),
    hours: [['Hour (PH)', 'Views gained']].concat(gains.byHour.map(function (g, h) {
              return [hourLabel(h), g]; })),
    age: [['Age', '% of viewers']].concat(ytRows({startDate: d90, endDate: day(now), metrics: 'viewerPercentage',
              dimensions: 'ageGroup'}).map(function (r) { return [String(r[0]).replace('age', ''), r[1]]; })),
    device: [['Device', 'Views']].concat(ytRows({startDate: d90, endDate: day(now), metrics: 'views',
              dimensions: 'deviceType', sort: '-views'}))
  };
  var slot = {};  // post-time test: average views by the PH hour a Short went live
  vids.forEach(function (v) { var h = +Utilities.formatDate(live(v), tz, 'H'); (slot[h] = slot[h] || []).push(v.views); });
  var slots = Object.keys(slot).map(Number).sort(function (a, b) { return a - b; }).map(function (h) {
    var a = slot[h], avg = Math.round(a.reduce(function (x, y) { return x + y; }, 0) / a.length);
    return [hourLabel(h) + ' (' + a.length + ')', avg, h, a.length];
  });
  B.slots = [['Went live (PH) · posts', 'Avg views']].concat(slots.map(function (s) { return [s[0], s[1]]; }));
  var best = slots.slice().sort(function (a, b) { return b[1] - a[1]; })[0];
  Object.keys(B).forEach(function (k) { if (B[k].length < 2) B[k].push(['no data yet', 0]); });

  var data = ss.getSheetByName('DASH_DATA') || ss.insertSheet('DASH_DATA', ss.getSheets().length);
  data.clear();
  var order = ['shorts', 'daily', 'country', 'hours', 'slots', 'age', 'device'], R = {}, col = 1;
  order.forEach(function (k) {
    data.getRange(1, col, B[k].length, 2).setValues(B[k]);
    R[k] = data.getRange(1, col, B[k].length, 2); col += 3;
  });
  data.hideSheet();

  // ---- DASHBOARD tab (2nd tab: the POSTING PLAN stays first) ------------------------------------------------
  var sh = ss.getSheetByName('DASHBOARD') || ss.insertSheet('DASHBOARD', 1);
  sh.getCharts().forEach(function (c) { sh.removeChart(c); });
  if (sh.getMaxRows() < 100) sh.insertRowsAfter(sh.getMaxRows(), 100 - sh.getMaxRows());
  if (sh.getMaxColumns() < 12) sh.insertColumnsAfter(sh.getMaxColumns(), 12 - sh.getMaxColumns());
  var all = sh.getRange(1, 1, sh.getMaxRows(), sh.getMaxColumns());
  all.breakApart(); sh.clear();
  all.setBackground(DASH.bg).setFontColor(DASH.text).setFontFamily('Montserrat').setVerticalAlignment('middle');
  sh.setHiddenGridlines(true);
  for (var c = 1; c <= 12; c++) sh.setColumnWidth(c, 110);

  sh.getRange('A1:L1').merge().setValue('📊  ' + String(ch.title).toUpperCase() + '  —  CHANNEL DASHBOARD')
    .setFontSize(22).setFontWeight('bold').setFontColor(DASH.pink).setHorizontalAlignment('center');
  sh.setRowHeight(1, 58);
  sh.getRange('A2:L2').merge().setValue('Updated ' + Utilities.formatDate(now, tz, 'EEE MMM d, h:mm a') +
    ' (PH)  ·  refreshes every hour  ·  all times PH, ET = PH − 13 h')
    .setFontColor(DASH.sub).setFontSize(10).setHorizontalAlignment('center');

  var top = vids.slice().sort(function (a, b) { return b.views - a.views; })[0];
  var tiles = [
    ['SUBSCRIBERS', ch.subscribers, 'channel total', DASH.pink],
    ['TOTAL VIEWS', ch.views, 'all time', DASH.cyan],
    ['SHORTS LIVE', vids.length, 'public uploads', DASH.yellow],
    ['VIEWS · 7 DAYS', gains.week, 'from hourly snapshots', DASH.green],
    ['BEST GO-LIVE TIME', best ? hourLabel(best[2]) + ' PH' : '—',
     best ? hourLabel(best[2] - 13) + ' ET · avg ' + best[1] + ' views (' + best[3] + ' posts)' : 'needs more posts', DASH.purple],
    ['TOP SHORT', top ? top.views : 0, top ? short(top.title, 30) : '—', DASH.orange]];
  tiles.forEach(function (t, i) {
    var c0 = 1 + i * 2;
    sh.getRange(4, c0, 1, 2).merge().setValue(t[0]).setFontSize(10).setFontWeight('bold').setFontColor(t[3]);
    sh.getRange(5, c0, 1, 2).merge().setValue(t[1]).setFontSize(26).setFontWeight('bold').setNumberFormat('#,##0');
    sh.getRange(6, c0, 1, 2).merge().setValue(t[2]).setFontSize(9).setFontColor(DASH.sub).setWrap(true);
    sh.getRange(4, c0, 3, 2).setBackground(DASH.card).setHorizontalAlignment('center')
      .setBorder(true, true, true, true, null, null, t[3], SpreadsheetApp.BorderStyle.SOLID_MEDIUM);
  });
  sh.setRowHeight(5, 52); sh.setRowHeight(6, 34);

  var CT = Charts.ChartType, donut = function (colors) {
    return {pieHole: 0.45, pieSliceBorderColor: DASH.card, colors: colors,
            legend: {position: 'right', textStyle: {color: DASH.text}}};
  };
  dashChart(sh, CT.BAR, R.shorts, 'Views per Short (latest 12)', 8, 1, {colors: [DASH.pink]});
  dashChart(sh, CT.AREA, R.daily, 'Daily channel views (30 days · YouTube Analytics, 2–3 day delay)', 8, 7,
            {colors: [DASH.cyan], areaOpacity: 0.25, lineWidth: 3});
  dashChart(sh, CT.GEO, R.country, 'Where your viewers are (90 days)', 26, 1,
            {colorAxis: {colors: ['#3A1030', DASH.pink]}, datalessRegionColor: DASH.grid});
  dashChart(sh, CT.PIE, R.country, 'Top countries (90 days)', 26, 7,
            donut([DASH.pink, DASH.cyan, DASH.yellow, DASH.green, DASH.purple, DASH.orange, '#FF5E5E', '#5EA8FF']));
  dashChart(sh, CT.COLUMN, R.hours, 'When views come in (views gained per PH hour · ET = PH − 13 h)', 44, 1, {colors: [DASH.green]});
  dashChart(sh, CT.COLUMN, R.slots, 'Post-time test: avg views by go-live hour (PH) · (posts)', 44, 7,
            {colors: [DASH.purple]});
  dashChart(sh, CT.PIE, R.age, 'Viewer age (90 days)', 62, 1,
            donut([DASH.yellow, DASH.pink, DASH.cyan, DASH.green, DASH.purple, DASH.orange]));
  dashChart(sh, CT.PIE, R.device, 'Devices (90 days)', 62, 7, donut([DASH.cyan, DASH.pink, DASH.yellow, DASH.green]));

  // ---- leaderboard with in-cell bars ------------------------------------------------------------------------
  var L0 = 81, board = vids.slice().sort(function (a, b) { return b.views - a.views; }).slice(0, 10);
  sh.getRange(L0 - 1, 1, 1, 12).merge().setValue('🏆  SHORTS LEADERBOARD (all time)')
    .setFontSize(16).setFontWeight('bold').setFontColor(DASH.yellow);
  sh.getRange(L0, 1, 1, 12).setValues([['#', 'SHORT', '', '', '', '', 'VIEWS', 'LIKES', 'WENT LIVE (PH)', '', '', '']])
    .setFontWeight('bold').setFontColor(DASH.sub).setBackground(DASH.card);
  sh.getRange(L0, 2, 1, 5).merge(); sh.getRange(L0, 9, 1, 2).merge(); sh.getRange(L0, 11, 1, 2).merge();
  var maxV = board.length ? (board[0].views || 1) : 1, bar = [DASH.pink, DASH.cyan, DASH.yellow, DASH.green, DASH.purple];
  board.forEach(function (v, i) {
    var r = L0 + 1 + i;
    sh.getRange(r, 1).setValue(i + 1).setHorizontalAlignment('center').setFontWeight('bold');
    sh.getRange(r, 2, 1, 5).merge().setValue(short(v.title, 60));
    sh.getRange(r, 7).setValue(v.views).setNumberFormat('#,##0').setFontWeight('bold');
    sh.getRange(r, 8).setValue(v.likes).setNumberFormat('#,##0');
    sh.getRange(r, 9, 1, 2).merge().setValue(Utilities.formatDate(live(v), tz, 'MMM d, h:mm a'));
    sh.getRange(r, 11, 1, 2).merge().setFormula('=SPARKLINE(G' + r + ',{"charttype","bar";"max",' + maxV +
      ';"color1","' + bar[i % bar.length] + '"})');
    sh.setRowHeight(r, 26);
  });

  // ---- raw STATS tab: color scale on VIEWS so it reads at a glance ------------------------------------------
  var st = statsSheet(), rng = st.getRange(2, 6, Math.max(st.getLastRow() - 1, 1), 1);
  st.setConditionalFormatRules([SpreadsheetApp.newConditionalFormatRule().setRanges([rng])
    .setGradientMinpoint('#FFFFFF')
    .setGradientMidpointWithValue('#FFE14D', SpreadsheetApp.InterpolationType.PERCENTILE, '50')
    .setGradientMaxpoint('#39FF14').build()]);
  return {ok: true, charts: sh.getCharts().length, shorts: vids.length, best: best ? hourLabel(best[2]) + ' PH' : null};
}

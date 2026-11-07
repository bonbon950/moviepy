/**
 * Bjorn's Shorts -> Google Drive helper. Version 4.
 * Can ONLY:
 *  - create/find "OUTPUT (...)" folders, list them, upload videos into them,
 *    restore (un-trash) files that belong to an OUTPUT folder;
 *  - read / add rows / update cells in the ONE spreadsheet named "POSTING PLAN";
 *  - delete ROWS of that sheet only when they are approved+posted or rejected (checked row by row).
 * Cannot delete any file or folder. Cannot touch any other file or folder.
 */
var OUT = /^OUTPUT \(.+\)$/;
var PLAN_NAME = 'POSTING PLAN';

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
      if (!OUT.test(p.name || '')) return out({error: 'folder name must be OUTPUT (...)'});
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
  SpreadsheetApp.openById('12th0-8z61cYyA0eT0HxaCjsn5Avy0DW5H6PyGTnVtx4').getName();
}

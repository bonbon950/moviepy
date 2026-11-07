/**
 * Bjorn's Shorts -> Google Drive helper (Google Apps Script web app). Version 2.
 *
 * Can ONLY: create/find folders named "OUTPUT (...)", list what is inside them, upload video files
 * into them, and restore (un-trash) files that belong to an OUTPUT folder.
 * It has NO delete/trash ability and cannot see or touch anything outside OUTPUT folders.
 *
 * Update an existing deployment (keeps the same URL):
 *   Paste this file over Code.gs -> Save -> Deploy -> Manage deployments -> pencil (Edit)
 *   -> Version: New version -> Deploy (re-authorize if asked).
 */

var OUT = /^OUTPUT \(.+\)$/;

function isOutputFile(file) {
  var ps = file.getParents();
  while (ps.hasNext()) { if (OUT.test(ps.next().getName())) return true; }
  return false;
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
    if (p.action === 'list') {  // everything in one OUTPUT folder, including trashed items
      var folder = DriveApp.getFolderById(p.folderId);
      if (!OUT.test(folder.getName())) return out({error: 'not an OUTPUT folder'});
      var files = [], fi = folder.getFiles();
      while (fi.hasNext()) {
        var x = fi.next();
        files.push({id: x.getId(), name: x.getName(), size: x.getSize(), trashed: x.isTrashed()});
      }
      return out({files: files});
    }
    if (p.action === 'restore') {  // un-trash a file that lives in an OUTPUT folder
      var file = DriveApp.getFileById(p.fileId);
      if (!isOutputFile(file)) return out({error: 'file is not in an OUTPUT folder'});
      if (!file.isTrashed()) return out({ok: true, note: 'already not in trash', name: file.getName()});
      file.setTrashed(false);
      return out({ok: true, name: file.getName()});
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

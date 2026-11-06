/**
 * Bjorn's Shorts -> Google Drive uploader (Google Apps Script web app).
 *
 * One-time setup (about 3 minutes, on a computer):
 *   1. Go to https://script.google.com -> New project. Name it "Shorts Uploader".
 *   2. Delete everything in Code.gs, paste this whole file, click Save.
 *   3. Deploy -> New deployment -> type "Web app".
 *        Execute as: Me      Who has access: Anyone
 *      -> Deploy -> Authorize access (choose blovesarmiento@gmail.com -> Advanced -> Go to project -> Allow).
 *   4. Copy the "Web app URL" (https://script.google.com/macros/s/.../exec) and send it to Claude.
 *
 * What it can do: ONLY create folders named "OUTPUT (...)" and upload video files into them.
 * It cannot read, list, change or delete anything else in your Drive.
 * Treat the URL like a password; to revoke it: Deploy -> Manage deployments -> Archive.
 */

function doPost(e) {
  var p = e.parameter;
  try {
    if (p.action === 'folder') {
      if (!/^OUTPUT \(.+\)$/.test(p.name || '')) return out({error: 'folder name must be OUTPUT (...)'});
      var it = DriveApp.getFoldersByName(p.name);
      var f = it.hasNext() ? it.next() : DriveApp.createFolder(p.name);
      return out({id: f.getId(), url: f.getUrl()});
    }
    if (p.action === 'start') {
      var folder = DriveApp.getFolderById(p.folderId);
      if (!/^OUTPUT \(.+\)$/.test(folder.getName())) return out({error: 'not an OUTPUT folder'});
      if (!/^video\//.test(p.mime || '')) return out({error: 'videos only'});
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

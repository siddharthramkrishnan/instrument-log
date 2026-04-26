// ============================================================
//  INSTRUMENT USAGE LOG — Google Apps Script
//  Paste this entire file into Apps Script editor
//  (script.google.com → New Project → paste → Deploy)
// ============================================================

const SHEET_NAME = 'Log';
const ALERT_EMAIL = 'siddharth.r@achiralabs.com';

// Conditions that trigger an email alert
const ALERT_CONDITIONS = ['Minor issue', 'Needs attention', 'Out of order'];

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const sheet = getOrCreateSheet();

    sheet.appendRow([
      new Date(),                    // A: Timestamp (server)
      data.submitted_at || '',       // B: Submitted at (client)
      data.asset_id || '',           // C: Asset ID
      data.instrument || '',         // D: Instrument
      data.department || '',         // E: Department
      data.make || '',               // F: Make
      data.model || '',              // G: Model
      data.serial || '',             // H: Serial No.
      data.logged_by || '',          // I: Logged By
      data.emp_id || '',             // J: Employee ID
      data.datetime || '',           // K: Usage Date/Time
      data.purpose || '',            // L: Purpose
      data.condition || '',          // M: Condition
      data.remarks || '',            // N: Remarks
    ]);

    if (ALERT_CONDITIONS.includes(data.condition)) {
      sendIssueAlert(data);
    }

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function sendIssueAlert(data) {
  const condition = data.condition || 'Unknown';
  const instrument = data.instrument || 'Unknown Instrument';
  const assetId = data.asset_id || '-';
  const department = data.department || '-';
  const loggedBy = data.logged_by || '-';
  const empId = data.emp_id ? ` (${data.emp_id})` : '';
  const usageTime = data.datetime || '-';
  const purpose = data.purpose || '-';
  const remarks = data.remarks || '(none)';
  const make = data.make || '-';
  const model = data.model || '-';
  const serial = data.serial || '-';

  const urgencyColor = condition === 'Out of order' ? '#c0392b'
                     : condition === 'Needs attention' ? '#e67e22'
                     : '#f39c12';

  const subject = `[Instrument Alert] ${condition} — ${instrument} (${assetId})`;

  const htmlBody = `
<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;border:1px solid #ddd;border-radius:8px;overflow:hidden;">
  <div style="background:${urgencyColor};padding:20px 24px;">
    <h2 style="margin:0;color:#fff;font-size:18px;">Instrument Issue Reported</h2>
    <p style="margin:6px 0 0;color:#fff;opacity:0.9;font-size:14px;">${new Date().toLocaleString('en-IN', {timeZone:'Asia/Kolkata'})}</p>
  </div>
  <div style="padding:24px;">
    <table style="width:100%;border-collapse:collapse;font-size:14px;">
      <tr><td style="padding:8px 0;color:#555;width:40%;">Condition</td>
          <td style="padding:8px 0;font-weight:bold;color:${urgencyColor};">${condition}</td></tr>
      <tr style="background:#f9f9f9;"><td style="padding:8px 4px;color:#555;">Instrument</td>
          <td style="padding:8px 4px;font-weight:bold;">${instrument}</td></tr>
      <tr><td style="padding:8px 0;color:#555;">Asset ID</td>
          <td style="padding:8px 0;">${assetId}</td></tr>
      <tr style="background:#f9f9f9;"><td style="padding:8px 4px;color:#555;">Department</td>
          <td style="padding:8px 4px;">${department}</td></tr>
      <tr><td style="padding:8px 0;color:#555;">Make / Model</td>
          <td style="padding:8px 0;">${make} / ${model}</td></tr>
      <tr style="background:#f9f9f9;"><td style="padding:8px 4px;color:#555;">Serial No.</td>
          <td style="padding:8px 4px;">${serial}</td></tr>
      <tr><td style="padding:8px 0;color:#555;">Logged By</td>
          <td style="padding:8px 0;">${loggedBy}${empId}</td></tr>
      <tr style="background:#f9f9f9;"><td style="padding:8px 4px;color:#555;">Usage Date/Time</td>
          <td style="padding:8px 4px;">${usageTime}</td></tr>
      <tr><td style="padding:8px 0;color:#555;">Purpose</td>
          <td style="padding:8px 0;">${purpose}</td></tr>
      <tr style="background:#f9f9f9;"><td style="padding:8px 4px;color:#555;vertical-align:top;">Remarks</td>
          <td style="padding:8px 4px;">${remarks}</td></tr>
    </table>
  </div>
  <div style="background:#f5f5f5;padding:14px 24px;font-size:12px;color:#888;text-align:center;">
    Instrument Usage Log — Achira Labs
  </div>
</div>`;

  const plainBody = `Instrument Issue Reported\n\nCondition: ${condition}\nInstrument: ${instrument}\nAsset ID: ${assetId}\nDepartment: ${department}\nMake/Model: ${make} / ${model}\nSerial: ${serial}\nLogged By: ${loggedBy}${empId}\nUsage Time: ${usageTime}\nPurpose: ${purpose}\nRemarks: ${remarks}`;

  MailApp.sendEmail({
    to: ALERT_EMAIL,
    subject: subject,
    body: plainBody,
    htmlBody: htmlBody,
  });
}

function getOrCreateSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    const headers = [
      'Server Timestamp', 'Client Timestamp', 'Asset ID', 'Instrument',
      'Department', 'Make', 'Model', 'Serial No.',
      'Logged By', 'Employee ID', 'Usage Date/Time',
      'Purpose', 'Condition', 'Remarks'
    ];
    sheet.appendRow(headers);
    
    // Style header row
    const headerRange = sheet.getRange(1, 1, 1, headers.length);
    headerRange.setBackground('#1a3a5c');
    headerRange.setFontColor('#ffffff');
    headerRange.setFontWeight('bold');
    sheet.setFrozenRows(1);
    sheet.setColumnWidths(1, headers.length, 160);
  }
  
  return sheet;
}

// Test function — run this from the editor to verify setup
function testSetup() {
  const sheet = getOrCreateSheet();
  Logger.log('Sheet ready: ' + sheet.getName());
  Logger.log('Rows: ' + sheet.getLastRow());
}

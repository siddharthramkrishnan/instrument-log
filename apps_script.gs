// ============================================================
//  INSTRUMENT USAGE LOG — Google Apps Script
//  Paste this entire file into Apps Script editor
//  (script.google.com → New Project → paste → Deploy)
// ============================================================

const SHEET_NAME = 'Log';

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

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
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

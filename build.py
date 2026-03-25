import json, os, re

with open('/home/claude/instruments.json') as f:
    instruments = json.load(f)

os.makedirs('/home/claude/instrument-log/log', exist_ok=True)

# Read template once
TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>{inst_name} — Instrument Log</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg: #f5f4f0;
  --surface: #ffffff;
  --border: #d8d4cc;
  --accent: #1a3a5c;
  --accent2: #c8392b;
  --text: #1c1c1c;
  --muted: #7a7670;
  --success: #1e6b40;
  --success-bg: #e6f4ec;
  --tag-mfg: #e8f0f8;
  --tag-mfg-text: #1a3a5c;
  --tag-dd: #fdf0ee;
  --tag-dd-text: #8b2c1e;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'IBM Plex Sans', sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
}}
.view {{ display: none; }}
.view.active {{ display: flex; flex-direction: column; min-height: 100vh; }}

/* FORM */
.form-header {{
  background: var(--accent);
  color: white;
  padding: 28px 24px 20px;
}}
.dept-badge {{
  display: inline-block;
  font-family: 'IBM Plex Mono', monospace;
  font-size: 10px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 4px;
  letter-spacing: 0.06em;
  margin-bottom: 10px;
}}
.dept-MFG {{ background: rgba(255,255,255,0.15); color: #b8d4f0; }}
.dept-DD {{ background: rgba(255,100,80,0.2); color: #ffb8a8; }}
.form-header h1 {{
  font-size: 20px;
  font-weight: 600;
  line-height: 1.25;
  margin-bottom: 4px;
}}
.form-header .asset-id {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 11px;
  opacity: 0.65;
}}

.inst-card {{
  margin: 16px 20px 0;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px 16px;
}}
.inst-card h3 {{
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  margin-bottom: 10px;
  font-family: 'IBM Plex Mono', monospace;
}}
.detail-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
.detail-field label {{
  font-size: 10px;
  font-weight: 600;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  display: block;
  margin-bottom: 2px;
}}
.detail-field span {{
  font-size: 13px;
  font-family: 'IBM Plex Mono', monospace;
  word-break: break-all;
  color: var(--text);
}}
.detail-field span.empty {{ color: var(--muted); font-style: italic; font-family: inherit; }}

.form-body {{ padding: 16px 20px 110px; flex: 1; }}
.form-section {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 14px;
}}
.form-section h3 {{
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  margin-bottom: 14px;
  font-family: 'IBM Plex Mono', monospace;
}}
.form-group {{ margin-bottom: 14px; }}
.form-group:last-child {{ margin-bottom: 0; }}
.form-group label {{
  display: block;
  font-size: 12px;
  font-weight: 500;
  margin-bottom: 6px;
}}
.form-group label .req {{ color: var(--accent2); }}
.form-group input,
.form-group select,
.form-group textarea {{
  width: 100%;
  border: 1.5px solid var(--border);
  border-radius: 6px;
  padding: 10px 12px;
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 15px;
  color: var(--text);
  background: var(--bg);
  outline: none;
  -webkit-appearance: none;
  appearance: none;
  transition: border-color 0.15s;
}}
.form-group select {{
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%237a7670' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 36px;
}}
.form-group textarea {{ resize: vertical; min-height: 72px; }}
.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {{ border-color: var(--accent); }}

.chips {{ display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; }}
.chip {{
  padding: 7px 13px;
  border: 1.5px solid var(--border);
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  background: var(--bg);
  color: var(--muted);
  transition: all 0.15s;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}}
.chip.selected {{ border-color: var(--accent); background: var(--accent); color: white; }}

.submit-bar {{
  position: fixed;
  bottom: 0; left: 0; right: 0;
  padding: 16px 20px;
  background: var(--surface);
  border-top: 1px solid var(--border);
}}
.submit-btn {{
  width: 100%;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 16px;
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.15s;
}}
.submit-btn:disabled {{ opacity: 0.6; }}
.submit-btn:active {{ opacity: 0.85; }}

.spinner {{
  display: inline-block;
  width: 16px; height: 16px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  vertical-align: middle;
  margin-right: 8px;
}}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}

/* SUCCESS */
#success {{
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  text-align: center;
}}
.success-icon {{
  width: 72px; height: 72px;
  background: var(--success-bg);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  margin: 0 auto 24px;
}}
.success-title {{ font-size: 22px; font-weight: 600; color: var(--success); margin-bottom: 8px; }}
.success-sub {{ font-size: 14px; color: var(--muted); margin-bottom: 28px; line-height: 1.5; }}
.success-card {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  width: 100%;
  max-width: 360px;
  text-align: left;
  margin-bottom: 28px;
}}
.success-row {{
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 6px 0;
  border-bottom: 1px solid var(--border);
  font-size: 13px;
  gap: 12px;
}}
.success-row:last-child {{ border-bottom: none; }}
.success-row .key {{ color: var(--muted); font-size: 11px; flex-shrink: 0; }}
.success-row .val {{
  font-family: 'IBM Plex Mono', monospace;
  font-size: 12px;
  font-weight: 500;
  text-align: right;
  word-break: break-word;
}}
.log-again-btn {{
  background: none;
  border: 2px solid var(--accent);
  color: var(--accent);
  border-radius: 8px;
  padding: 13px 28px;
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}}

/* ERROR */
.error-banner {{
  display: none;
  background: #fdf0ee;
  border: 1px solid #e8b4ae;
  border-radius: 6px;
  padding: 10px 14px;
  font-size: 13px;
  color: var(--accent2);
  margin-bottom: 12px;
}}

.toast {{
  position: fixed;
  top: 16px; left: 50%;
  transform: translateX(-50%) translateY(-80px);
  background: #1e1e1e;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  transition: transform 0.3s;
  z-index: 999;
  white-space: nowrap;
}}
.toast.show {{ transform: translateX(-50%) translateY(0); }}
</style>
</head>
<body>
<div id="toast" class="toast"></div>

<!-- FORM VIEW -->
<div id="formview" class="view active">
  <div class="form-header">
    <div class="dept-badge dept-{dept_class}">{dept_label}</div>
    <h1>{inst_name}</h1>
    <div class="asset-id">{asset_id}</div>
  </div>

  <div class="inst-card">
    <h3>Instrument Details</h3>
    <div class="detail-grid">
      <div class="detail-field">
        <label>Make</label>
        <span class="{make_cls}">{make_val}</span>
      </div>
      <div class="detail-field">
        <label>Model</label>
        <span class="{model_cls}">{model_val}</span>
      </div>
      <div class="detail-field">
        <label>Serial No.</label>
        <span class="{serial_cls}">{serial_val}</span>
      </div>
      <div class="detail-field">
        <label>Department</label>
        <span>{dept_label}</span>
      </div>
    </div>
  </div>

  <div class="form-body">
    <div class="error-banner" id="errBanner"></div>

    <div class="form-section">
      <h3>Your Details</h3>
      <div class="form-group">
        <label>Name <span class="req">*</span></label>
        <input type="text" id="f-name" placeholder="Full name" autocomplete="name" inputmode="text">
      </div>
      <div class="form-group">
        <label>Employee ID</label>
        <input type="text" id="f-empid" placeholder="e.g. EMP-1234" autocomplete="off">
      </div>
    </div>

    <div class="form-section">
      <h3>Usage Details</h3>
      <div class="form-group">
        <label>Date &amp; Time <span class="req">*</span></label>
        <input type="datetime-local" id="f-datetime">
      </div>
      <div class="form-group">
        <label>Purpose <span class="req">*</span></label>
        <div class="chips" id="chips">
          <div class="chip" onclick="toggleChip(this)">Routine Use</div>
          <div class="chip" onclick="toggleChip(this)">Calibration</div>
          <div class="chip" onclick="toggleChip(this)">Maintenance</div>
          <div class="chip" onclick="toggleChip(this)">Testing</div>
          <div class="chip" onclick="toggleChip(this)">R&amp;D</div>
          <div class="chip" onclick="toggleChip(this)">Other</div>
        </div>
      </div>
      <div class="form-group">
        <label>Instrument Condition</label>
        <select id="f-condition">
          <option value="">— Select condition —</option>
          <option>Good — Working normally</option>
          <option>Minor issue — Functional with small problem</option>
          <option>Needs attention — Should be checked</option>
          <option>Out of order — Not usable</option>
        </select>
      </div>
      <div class="form-group">
        <label>Remarks / Notes</label>
        <textarea id="f-remarks" placeholder="Optional — any observations or issues…"></textarea>
      </div>
    </div>
  </div>

  <div class="submit-bar">
    <button class="submit-btn" id="submitBtn" onclick="submitLog()">Submit Log Entry</button>
  </div>
</div>

<!-- SUCCESS VIEW -->
<div id="success" class="view">
  <div class="success-icon">✓</div>
  <div class="success-title">Entry Logged</div>
  <div class="success-sub">Saved to Google Sheets successfully.</div>
  <div class="success-card" id="successCard"></div>
  <button class="log-again-btn" onclick="logAgain()">Log Again</button>
</div>

<script>
const SCRIPT_URL = 'REPLACE_WITH_APPS_SCRIPT_URL';
const INST = {{
  asset_id: "{asset_id}",
  name: "{inst_name_js}",
  make: "{make_js}",
  model: "{model_js}",
  serial: "{serial_js}",
  department: "{department}"
}};

// Set default datetime
(function() {{
  const now = new Date();
  const pad = n => String(n).padStart(2,'0');
  document.getElementById('f-datetime').value =
    now.getFullYear() + '-' + pad(now.getMonth()+1) + '-' + pad(now.getDate()) +
    'T' + pad(now.getHours()) + ':' + pad(now.getMinutes());
}})();

function toggleChip(el) {{ el.classList.toggle('selected'); }}

let toastTimer;
function showToast(msg) {{
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2800);
}}

function showErr(msg) {{
  const b = document.getElementById('errBanner');
  b.textContent = msg;
  b.style.display = 'block';
  b.scrollIntoView({{behavior:'smooth', block:'center'}});
}}
function hideErr() {{ document.getElementById('errBanner').style.display = 'none'; }}

async function submitLog() {{
  hideErr();
  const name = document.getElementById('f-name').value.trim();
  const dt = document.getElementById('f-datetime').value;
  const purpose = [...document.querySelectorAll('.chip.selected')].map(c => c.textContent).join(', ');
  const condition = document.getElementById('f-condition').value;
  const remarks = document.getElementById('f-remarks').value.trim();

  if (!name) {{ showErr('Please enter your name.'); document.getElementById('f-name').focus(); return; }}
  if (!dt) {{ showErr('Please select date and time.'); return; }}
  if (!purpose) {{ showErr('Please select at least one purpose.'); return; }}

  const btn = document.getElementById('submitBtn');
  btn.disabled = true;
  btn.innerHTML = '<span class="spinner"></span>Submitting…';

  const payload = {{
    asset_id: INST.asset_id,
    instrument: INST.name,
    department: INST.department,
    make: INST.make,
    model: INST.model,
    serial: INST.serial,
    logged_by: name,
    emp_id: document.getElementById('f-empid').value.trim(),
    datetime: dt.replace('T',' '),
    purpose,
    condition,
    remarks,
    submitted_at: new Date().toISOString()
  }};

  try {{
    await fetch(SCRIPT_URL, {{
      method: 'POST',
      mode: 'no-cors',
      headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify(payload)
    }});
    showSuccess(payload);
  }} catch(e) {{
    btn.disabled = false;
    btn.innerHTML = 'Submit Log Entry';
    showErr('Network error. Please check your connection and try again.');
  }}
}}

function showSuccess(p) {{
  const rows = [
    ['Instrument', p.instrument],
    ['Asset ID', p.asset_id],
    ['Date / Time', p.datetime],
    ['Logged by', p.logged_by + (p.emp_id ? ' · ' + p.emp_id : '')],
    ['Purpose', p.purpose],
    p.condition ? ['Condition', p.condition] : null,
    p.remarks ? ['Remarks', p.remarks] : null,
  ].filter(Boolean);

  document.getElementById('successCard').innerHTML = rows.map(([k,v]) =>
    `<div class="success-row"><span class="key">${{k}}</span><span class="val">${{v}}</span></div>`
  ).join('');

  document.getElementById('formview').classList.remove('active');
  document.getElementById('success').classList.add('active');
  window.scrollTo(0,0);
}}

function logAgain() {{
  document.getElementById('f-name').value = '';
  document.getElementById('f-empid').value = '';
  document.getElementById('f-remarks').value = '';
  document.getElementById('f-condition').value = '';
  document.querySelectorAll('.chip').forEach(c => c.classList.remove('selected'));
  const btn = document.getElementById('submitBtn');
  btn.disabled = false;
  btn.innerHTML = 'Submit Log Entry';
  const now = new Date();
  const pad = n => String(n).padStart(2,'0');
  document.getElementById('f-datetime').value =
    now.getFullYear() + '-' + pad(now.getMonth()+1) + '-' + pad(now.getDate()) +
    'T' + pad(now.getHours()) + ':' + pad(now.getMinutes());
  document.getElementById('success').classList.remove('active');
  document.getElementById('formview').classList.add('active');
  window.scrollTo(0,0);
}}
</script>
</body>
</html>'''

def clean(s, fallback='—'):
    s = str(s).strip().replace('\n', ' ')
    return s if s and s != 'nan' else fallback

def js_escape(s):
    return clean(s, '').replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")

def html_escape(s):
    return clean(s, '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

count = 0
for inst in instruments:
    dept = inst['department']
    dept_class = 'DD' if dept == 'D&D' else 'MFG'
    dept_label = html_escape(dept)
    
    name = clean(inst['name'])
    asset_id = inst['asset_id']
    
    make = clean(inst['make'], '')
    model = clean(inst['model'], '')
    serial = clean(inst['serial'], '')
    
    # safe filename from asset_id: ENG/MFG/001 -> eng_mfg_001
    fname = asset_id.lower().replace('/', '_').replace('&', '_').replace(' ', '_')
    
    html = TEMPLATE.format(
        inst_name=html_escape(name),
        inst_name_js=js_escape(name),
        asset_id=html_escape(asset_id),
        dept_class=dept_class,
        dept_label=dept_label,
        make_val=html_escape(make) if make else '—',
        make_cls='' if make else 'empty',
        model_val=html_escape(model) if model else '—',
        model_cls='' if model else 'empty',
        serial_val=html_escape(serial) if serial else '—',
        serial_cls='' if serial else 'empty',
        make_js=js_escape(make),
        model_js=js_escape(model),
        serial_js=js_escape(serial),
        department=js_escape(dept),
    )
    
    path = f'/home/claude/instrument-log/log/{fname}.html'
    with open(path, 'w') as f:
        f.write(html)
    count += 1

print(f'Generated {count} HTML files')

import subprocess
import os
import re

workspace_dir = r"d:\malevolent_kitchen"
index_file = os.path.join(workspace_dir, "index.html")

with open(index_file, "r", encoding="utf-8") as f:
    orig_html = f.read()

chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# 1. Figure 1: Sample Code & Interface
sample_editor_code = """<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: system-ui, sans-serif; padding: 24px; background: #ffffff; color: #1e293b; }
    h2 { margin-top: 0; color: #0f172a; font-size: 20px; }
    p { color: #64748b; font-size: 14px; }
    button {
      padding: 10px 18px;
      background: #2563eb;
      color: #ffffff;
      font-weight: 600;
      border: 0;
      border-radius: 6px;
      cursor: pointer;
      box-shadow: 0 2px 4px rgba(37,99,235,0.2);
      transition: background 0.2s;
    }
    button:hover { background: #1d4ed8; }
  </style>
</head>
<body>
  <h2>Live Playground Test</h2>
  <p>Click the button below to test console logging:</p>
  <button onclick="console.log('Action triggered! Button clicked at 16:30:15')">
    Click Me to Log
  </button>
</body>
</html>"""

sample_preview_body = """
  <div style="font-family:system-ui,sans-serif;padding:24px;background:#ffffff;color:#1e293b;min-height:100%;box-sizing:border-box;">
    <h2 style="margin-top:0;color:#0f172a;font-size:20px;">Live Playground Test</h2>
    <p style="color:#64748b;font-size:14px;">Click the button below to test console logging:</p>
    <button style="padding:10px 18px;background:#2563eb;color:#ffffff;font-weight:600;border:0;border-radius:6px;cursor:pointer;box-shadow:0 2px 4px rgba(37,99,235,0.2);">
      Click Me to Log
    </button>
  </div>
"""

sample_logs = [
    ("i", "16:30:14", "Compiling HTML, CSS and JavaScript..."),
    ("s", "16:30:14", "Application compiled and executed successfully (0.3ms)."),
    ("i", "16:30:15", "Action triggered! Button clicked at 16:30:15")
]

# 2. Case Study 1: Student Profile Card
cs1_editor_code = """<h2>Case Study 1: Student Profile Card</h2>
<table border="1" cellpadding="6">
<tr><th>Field</th><th>Value</th><th>Data Type</th></tr>
</table>
<script>
let studentName = "Rahul Sharma"; // string 
const registerNumber = 2105123; // number 
let semester = 5; // number
let percentage = 82.5; // number
let feePaid = true; // boolean
let backlogs; // undefined

function show(label, value) {
  console.log(label + ": " + value + " (" + typeof value + ")"); 
  document.querySelector("table").innerHTML +=
    "<tr><td>" + label + "</td><td>" + value + 
    "</td><td>" + typeof value + "</td></tr>";
}

show("Name", studentName); 
show("Register No", registerNumber); 
show("Semester", semester); 
show("Percentage", percentage); 
show("Exam Fee Paid", feePaid); 
show("Backlogs", backlogs);
</script>"""

cs1_preview_body = """
  <div style="font-family:system-ui,sans-serif;padding:20px;background:#ffffff;color:#0f172a;box-sizing:border-box;">
    <h2 style="margin-top:0;margin-bottom:14px;color:#1e293b;font-size:20px;">Case Study 1: Student Profile Card</h2>
    <table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:13.5px;border:1px solid #cbd5e1;">
      <tr style="background:#f1f5f9;text-align:left;">
        <th style="padding:8px 12px;border:1px solid #cbd5e1;">Field</th>
        <th style="padding:8px 12px;border:1px solid #cbd5e1;">Value</th>
        <th style="padding:8px 12px;border:1px solid #cbd5e1;">Data Type</th>
      </tr>
      <tr><td style="padding:7px 12px;border:1px solid #cbd5e1;font-weight:600;">Name</td><td style="padding:7px 12px;border:1px solid #cbd5e1;">Rahul Sharma</td><td style="padding:7px 12px;border:1px solid #cbd5e1;color:#2563eb;font-family:monospace;">string</td></tr>
      <tr><td style="padding:7px 12px;border:1px solid #cbd5e1;font-weight:600;">Register No</td><td style="padding:7px 12px;border:1px solid #cbd5e1;">2105123</td><td style="padding:7px 12px;border:1px solid #cbd5e1;color:#2563eb;font-family:monospace;">number</td></tr>
      <tr><td style="padding:7px 12px;border:1px solid #cbd5e1;font-weight:600;">Semester</td><td style="padding:7px 12px;border:1px solid #cbd5e1;">5</td><td style="padding:7px 12px;border:1px solid #cbd5e1;color:#2563eb;font-family:monospace;">number</td></tr>
      <tr><td style="padding:7px 12px;border:1px solid #cbd5e1;font-weight:600;">Percentage</td><td style="padding:7px 12px;border:1px solid #cbd5e1;">82.5</td><td style="padding:7px 12px;border:1px solid #cbd5e1;color:#2563eb;font-family:monospace;">number</td></tr>
      <tr><td style="padding:7px 12px;border:1px solid #cbd5e1;font-weight:600;">Exam Fee Paid</td><td style="padding:7px 12px;border:1px solid #cbd5e1;">true</td><td style="padding:7px 12px;border:1px solid #cbd5e1;color:#2563eb;font-family:monospace;">boolean</td></tr>
      <tr><td style="padding:7px 12px;border:1px solid #cbd5e1;font-weight:600;">Backlogs</td><td style="padding:7px 12px;border:1px solid #cbd5e1;">undefined</td><td style="padding:7px 12px;border:1px solid #cbd5e1;color:#2563eb;font-family:monospace;">undefined</td></tr>
    </table>
  </div>
"""

cs1_logs = [
    ("i", "16:31:02", "Compiling HTML, CSS and JavaScript..."),
    ("i", "16:31:02", "Name: Rahul Sharma (string)"),
    ("i", "16:31:02", "Register No: 2105123 (number)"),
    ("i", "16:31:02", "Semester: 5 (number)"),
    ("i", "16:31:02", "Percentage: 82.5 (number)"),
    ("i", "16:31:02", "Exam Fee Paid: true (boolean)"),
    ("i", "16:31:02", "Backlogs: undefined (undefined)"),
    ("s", "16:31:02", "Application compiled and executed successfully (0.4ms).")
]

# 3. Case Study 2: Simple Shopping Bill
cs2_editor_code = """<h2>Case Study 2: Simple Shopping Bill</h2>
<pre id="bill"></pre>
<script>
const notebookQty = 3, notebookPrice = 45; 
const penQty = 2, penPrice = 20;
const notebookTotal = notebookQty * notebookPrice; 
const penTotal = penQty * penPrice;
const subtotal = notebookTotal + penTotal; 
const gst = subtotal * 5 / 100;
const finalTotal = subtotal + gst;

const lines = [
  "Notebooks : " + notebookQty + " x Rs." + notebookPrice + " = Rs." + notebookTotal, 
  "Pens : " + penQty + " x Rs." + penPrice + " = Rs." + penTotal,
  "Subtotal = Rs." + subtotal,
  "GST (5%) = Rs." + gst,
  "Final Bill Amount = Rs." + finalTotal
];

lines.forEach(l => console.log(l)); 
document.getElementById("bill").textContent = lines.join("\\n");
</script>"""

cs2_preview_body = """
  <div style="font-family:system-ui,sans-serif;padding:22px;background:#ffffff;color:#0f172a;box-sizing:border-box;">
    <h2 style="margin-top:0;margin-bottom:14px;color:#1e293b;font-size:20px;">Case Study 2: Simple Shopping Bill</h2>
    <pre style="background:#f8fafc;border:1px solid #e2e8f0;padding:16px;border-radius:8px;font-family:'JetBrains Mono',monospace;font-size:13px;line-height:1.7;color:#1e293b;box-shadow:0 1px 3px rgba(0,0,0,0.05);margin:0;">Notebooks : 3 x Rs.45 = Rs.135
Pens : 2 x Rs.20 = Rs.40
Subtotal = Rs.175
GST (5%) = Rs.8.75
Final Bill Amount = Rs.183.75</pre>
  </div>
"""

cs2_logs = [
    ("i", "16:32:40", "Compiling HTML, CSS and JavaScript..."),
    ("i", "16:32:40", "Notebooks : 3 x Rs.45 = Rs.135"),
    ("i", "16:32:40", "Pens : 2 x Rs.20 = Rs.40"),
    ("i", "16:32:40", "Subtotal = Rs.175"),
    ("i", "16:32:40", "GST (5%) = Rs.8.75"),
    ("i", "16:32:40", "Final Bill Amount = Rs.183.75"),
    ("s", "16:32:40", "Application compiled and executed successfully (0.3ms).")
]

def render_standalone_view(editor_code, preview_body, logs, active_tab_title="index.html"):
    # Calculate line numbers
    lines_count = editor_code.count("\n") + 1
    nums = "\n".join(str(i) for i in range(1, lines_count + 1))
    
    # Generate log rows
    log_rows_html = ""
    for typ, tm, txt in logs:
        cls_name = "s" if typ == "s" else ("e" if typ == "e" else "i")
        log_rows_html += f'<div class="log-entry {cls_name}"><span class="time">{tm}</span><span>{txt}</span></div>'
    
    # Modify template
    res = orig_html
    
    # 1. Update text area content and line numbers
    res = re.sub(
        r'<textarea id="editor-unified"[^>]*>.*?</textarea>',
        f'<textarea id="editor-unified" class="code-area active" spellcheck="false">{editor_code}</textarea>',
        res,
        flags=re.DOTALL
    )
    res = re.sub(
        r'<div class="line-numbers" id="line-numbers">.*?</div>',
        f'<div class="line-numbers" id="line-numbers">{nums}</div>',
        res,
        flags=re.DOTALL
    )
    
    # 2. Update tab buttons
    res = res.replace(
        '<button class="tab-btn active" id="tab-view-preview">Website Only</button>',
        '<button class="tab-btn" id="tab-view-preview">Website Only</button>'
    )
    res = res.replace(
        '<button class="tab-btn" id="tab-view-both">Preview &amp; Console</button>',
        '<button class="tab-btn active" id="tab-view-both">Preview &amp; Console</button>'
    )
    
    # 3. Update outputSplitBody class to enable both preview and console
    res = res.replace('class="output-split-body website-only"', 'class="output-split-body"')
    
    # 4. Inject preview iframe content via srcdoc
    # In srcdoc, we can put standard HTML
    srcdoc_content = f'<!DOCTYPE html><html><head><meta charset="utf-8"></head><body style="margin:0;padding:0;">{preview_body}</body></html>'
    escaped_srcdoc = srcdoc_content.replace('"', '&quot;')
    res = re.sub(
        r'<iframe id="preview-frame"[^>]*></iframe>',
        f'<iframe id="preview-frame" class="preview-frame" srcdoc="{escaped_srcdoc}"></iframe>',
        res
    )
    
    # 5. Populate log items and counter
    res = re.sub(
        r'<span class="console-pill" id="log-count">0 items</span>',
        f'<span class="console-pill" id="log-count">{len(logs)} items</span>',
        res
    )
    res = re.sub(
        r'<pre id="log-output"></pre>',
        f'<pre id="log-output">{log_rows_html}</pre>',
        res
    )
    
    # 6. Override loadState / executeCode so it doesn't overwrite our pre-rendered DOM
    res = res.replace('loadState();', '// loadState();')
    res = res.replace('executeCode();', '// executeCode();')
    
    return res

items = [
    ("fig1_compiler_interface", sample_editor_code, sample_preview_body, sample_logs),
    ("fig4_case_study_1", cs1_editor_code, cs1_preview_body, cs1_logs),
    ("fig5_case_study_2", cs2_editor_code, cs2_preview_body, cs2_logs)
]

for name, ed_code, prev_body, logs in items:
    out_html = render_standalone_view(ed_code, prev_body, logs)
    temp_path = os.path.join(workspace_dir, f"_{name}_view.html")
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(out_html)
    
    img_path = os.path.join(workspace_dir, f"{name}.png")
    cmd = [
        chrome_exe,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--window-size=1260,720",
        f"--screenshot={img_path}",
        f"file:///{temp_path}"
    ]
    res = subprocess.run(cmd, capture_output=True, timeout=15)
    print(f"Generated {img_path}: exit {res.returncode}, size: {os.path.getsize(img_path) if os.path.exists(img_path) else 0}")
    
    if os.path.exists(temp_path):
        os.remove(temp_path)

print("Pre-rendered screenshot generation complete!")

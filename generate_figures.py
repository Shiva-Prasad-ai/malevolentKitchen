import subprocess
import os
import re
import time

workspace_dir = r"d:\malevolent_kitchen"
index_file = os.path.join(workspace_dir, "index.html")

with open(index_file, "r", encoding="utf-8") as f:
    template_html = f.read()

chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Case Study 1 Code
cs1_code = """<h2>Case Study 1: Student Profile Card</h2>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-family:system-ui,-apple-system,sans-serif;">
  <tr style="background:#e2e8f0;text-align:left;">
    <th>Field</th><th>Value</th><th>Data Type</th>
  </tr>
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

# Case Study 2 Code
cs2_code = """<h2>Case Study 2: Simple Shopping Bill</h2>
<pre id="bill" style="background:#f1f5f9;padding:14px;border-radius:6px;font-family:monospace;font-size:13px;line-height:1.6;color:#0f172a;"></pre>

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
  "Pens      : " + penQty + " x Rs." + penPrice + " = Rs." + penTotal,
  "---------------------------------------------",
  "Subtotal         = Rs. " + subtotal.toFixed(2), 
  "GST (5%)         = Rs. " + gst.toFixed(2), 
  "Final Bill Amount = Rs. " + finalTotal.toFixed(2)
];

lines.forEach(l => console.log(l)); 
document.getElementById("bill").textContent = lines.join("\\n");
</script>"""

# Sample Code for Figure 1
sample_code = """<!DOCTYPE html>
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
    }
    button:hover { background: #1d4ed8; }
  </style>
</head>
<body>
  <h2>Live Playground Test</h2>
  <p>Click the button below to test real-time console logging:</p>
  <button onclick="console.log('Action triggered! Welcome to Malevolent Kitchen Code Studio.')">
    Click Me to Log
  </button>
</body>
</html>"""

def generate_page(code_text, auto_trigger_btn=False):
    # Escape for JS template literal
    clean_code = code_text.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
    
    btn_click_script = """
    setTimeout(function() {
        var frame = document.getElementById('preview-frame');
        if (frame && frame.contentWindow && frame.contentDocument) {
            var btn = frame.contentDocument.querySelector('button');
            if (btn) btn.click();
        }
    }, 600);
    """ if auto_trigger_btn else ""

    script_inject = f"""
    <script>
    window.addEventListener('load', function() {{
        setTimeout(function() {{
            // Set split web mode with tabs or single
            var ta = document.getElementById('editor-unified');
            if (ta) {{
                ta.value = `{clean_code}`;
                ta.dataset.webCode = ta.value;
            }}
            var btnBoth = document.getElementById('tab-view-both');
            if (btnBoth) btnBoth.click();
            var btnRun = document.getElementById('btn-run');
            if (btnRun) btnRun.click();
            {btn_click_script}
        }}, 400);
    }});
    </script>
    """
    return template_html.replace("</head>", script_inject + "</head>")

# Write files and generate screenshots
shots = [
    ("fig1_compiler_interface", sample_code, True),
    ("fig4_case_study_1", cs1_code, False),
    ("fig5_case_study_2", cs2_code, False),
]

for name, code, trigger in shots:
    html_content = generate_page(code, trigger)
    temp_html_path = os.path.join(workspace_dir, f"_temp_{name}.html")
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    img_path = os.path.join(workspace_dir, f"{name}.png")
    # Execute Chrome with a delay to let iframe run and console messages appear
    # We use a wrapper or sleep via Chrome args if needed
    cmd = [
        chrome_exe,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--window-size=1240,700",
        f"--screenshot={img_path}",
        f"file:///{temp_html_path}"
    ]
    # To allow JS to execute, let's use virtual-time-budget
    cmd.insert(4, "--virtual-time-budget=2000")
    
    print(f"Generating {img_path}...")
    res = subprocess.run(cmd, capture_output=True, timeout=20)
    print(f"Done {name}: status {res.returncode}, size: {os.path.getsize(img_path) if os.path.exists(img_path) else 'NOT FOUND'}")
    
    # Clean up temp html
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

print("All screenshots generated successfully!")

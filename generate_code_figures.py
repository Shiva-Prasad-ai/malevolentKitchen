import subprocess
import os
import html

workspace_dir = r"d:\malevolent_kitchen"
chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

code_lines = [
    '<!DOCTYPE html>',
    '<html lang="en">',
    '<head>',
    '  <meta charset="utf-8">',
    '  <title>Browser Code Compiler</title>',
    '  <style>',
    '    * { box-sizing: border-box; }',
    '    body { margin: 0; font-family: system-ui, sans-serif; display: flex; flex-direction: column;',
    '           height: 100vh; background: #0f172a; color: #f8fafc; }',
    '    .toolbar { display: flex; gap: 8px; padding: 10px 14px; background: #1e293b;',
    '               border-bottom: 1px solid #334155; align-items: center; }',
    '    button { padding: 6px 14px; border: 1px solid #475569; background: #334155;',
    '             color: #fff; border-radius: 6px; cursor: pointer; font-weight: 500; font-size: 13px; }',
    '    button:hover { background: #475569; }',
    '    .btn-run { background: #10b981; border-color: #059669; font-weight: 700; }',
    '    .tab.active { background: #2563eb; border-color: #1d4ed8; }',
    '    .container { display: flex; flex: 1; overflow: hidden; }',
    '    .editor-box { flex: 1; display: flex; flex-direction: column; border-right: 1px solid #334155; }',
    '    textarea { width: 100%; height: 100%; background: #090d16; color: #e2e8f0; font-family: monospace;',
    '               font-size: 13.5px; padding: 14px; border: 0; resize: none; outline: none; display: none; line-height: 1.5; }',
    '    textarea.active { display: block; }',
    '    .output-box { flex: 1; display: flex; flex-direction: column; }',
    '    iframe { flex: 2; border: 0; background: #ffffff; }',
    '    .console { flex: 1; background: #020617; border-top: 1px solid #334155; padding: 10px;',
    '               font-family: monospace; font-size: 12.5px; overflow-y: auto; color: #38bdf8; }',
    '    .console div { padding: 2px 0; border-bottom: 1px solid #1e293b; }',
    '  </style>',
    '</head>',
    '<body>',
    '  <div class="toolbar">',
    '    <button class="btn-run" onclick="run()">▶ Run</button>',
    '    <button onclick="clipboard(\'cut\')">Cut</button>',
    '    <button onclick="clipboard(\'copy\')">Copy</button>',
    '    <button onclick="clipboard(\'paste\')">Paste</button>',
    '    <button class="tab active" onclick="tab(\'html\')">HTML</button>',
    '    <button class="tab" onclick="tab(\'css\')">CSS</button>',
    '    <button class="tab" onclick="tab(\'js\')">JavaScript</button>',
    '  </div>',
    '  <div class="container">',
    '    <div class="editor-box">',
    # Line 40 ends here
    '      <textarea id="html" class="active" placeholder="<!-- HTML Code -->"></textarea>',
    '      <textarea id="css" placeholder="/* CSS Code */"></textarea>',
    '      <textarea id="js" placeholder="// JavaScript Code"></textarea>',
    '    </div>',
    '    <div class="output-box">',
    '      <iframe id="preview"></iframe>',
    '      <div id="console" class="console"><strong>Console Output:</strong></div>',
    '    </div>',
    '  </div>',
    '  <script>',
    '    let active = \'html\', timer = null;',
    '    function tab(type) {',
    '      active = type;',
    '      document.querySelectorAll(\'.tab\').forEach((b, i) => b.classList.toggle(\'active\', [\'html\',\'css\',\'js\'][i] === type));',
    '      document.querySelectorAll(\'textarea\').forEach(t => t.classList.toggle(\'active\', t.id === type));',
    '    }',
    '    function clipboard(action) {',
    '      const ta = document.getElementById(active);',
    '      if (action === \'cut\') {',
    '        navigator.clipboard.writeText(ta.value.substring(ta.selectionStart, ta.selectionEnd));',
    '        ta.setRangeText(\'\', ta.selectionStart, ta.selectionEnd, \'end\'); run();',
    '      } else if (action === \'copy\') {',
    '        navigator.clipboard.writeText(ta.value.substring(ta.selectionStart, ta.selectionEnd));',
    '      } else if (action === \'paste\') {',
    '        navigator.clipboard.readText().then(txt => {',
    '          ta.setRangeText(txt, ta.selectionStart, ta.selectionEnd, \'end\'); run();',
    '        });',
    '      }',
    '    }',
    '    function run() {',
    '      const h = document.getElementById(\'html\').value, c = document.getElementById(\'css\').value, j = document.getElementById(\'js\').value;',
    '      const bridge = `<script>',
    '        const _log = console.log;',
    '        console.log = (...a) => { parent.postMessage({msg: a.join(\' \')}, \'*\'); _log(...a); };',
    '        window.onerror = (m, u, l) => parent.postMessage({msg: \'Error: \' + m + \' (line \' + l + \')\'}, \'*\');',
    '      <\\/script>`;',
    '      document.getElementById(\'preview\').srcdoc = `<!DOCTYPE html><html><head><style>${c}</style>${bridge}</head><body>${h}<script>${j}<\\/script></body></html>`;',
    '    }',
    '    document.querySelectorAll(\'textarea\').forEach(t => t.addEventListener(\'input\', () => {',
    '      clearTimeout(timer); timer = setTimeout(run, 500);',
    '    }));',
    '    window.addEventListener(\'message\', e => {',
    '      if (e.data && e.data.msg) {',
    '        const d = document.createElement(\'div\'); d.textContent = e.data.msg;',
    '        document.getElementById(\'console\').appendChild(d);',
    '      }',
    '    });',
    '    run();',
    '  </script>',
    '</body>',
    '</html>'
]

def make_code_card(lines_slice, start_line, title):
    rows = []
    for idx, line in enumerate(lines_slice, start=start_line):
        safe_line = html.escape(line)
        # Simple color keywords
        safe_line = safe_line.replace('&lt;!DOCTYPE html&gt;', '<span style="color:#f43f5e">&lt;!DOCTYPE html&gt;</span>')
        safe_line = safe_line.replace('&lt;html', '<span style="color:#f43f5e">&lt;html</span>')
        safe_line = safe_line.replace('&lt;/html&gt;', '<span style="color:#f43f5e">&lt;/html&gt;</span>')
        safe_line = safe_line.replace('&lt;body', '<span style="color:#f43f5e">&lt;body</span>')
        safe_line = safe_line.replace('&lt;/body&gt;', '<span style="color:#f43f5e">&lt;/body&gt;</span>')
        safe_line = safe_line.replace('&lt;head&gt;', '<span style="color:#f43f5e">&lt;head&gt;</span>')
        safe_line = safe_line.replace('&lt;/head&gt;', '<span style="color:#f43f5e">&lt;/head&gt;</span>')
        safe_line = safe_line.replace('&lt;style&gt;', '<span style="color:#f43f5e">&lt;style&gt;</span>')
        safe_line = safe_line.replace('&lt;/style&gt;', '<span style="color:#f43f5e">&lt;/style&gt;</span>')
        safe_line = safe_line.replace('&lt;script&gt;', '<span style="color:#f43f5e">&lt;script&gt;</span>')
        safe_line = safe_line.replace('&lt;/script&gt;', '<span style="color:#f43f5e">&lt;/script&gt;</span>')
        safe_line = safe_line.replace('function', '<span style="color:#38bdf8;font-weight:600;">function</span>')
        safe_line = safe_line.replace('const ', '<span style="color:#818cf8;font-weight:600;">const </span>')
        safe_line = safe_line.replace('let ', '<span style="color:#818cf8;font-weight:600;">let </span>')
        safe_line = safe_line.replace('document.', '<span style="color:#a78bfa;">document.</span>')
        safe_line = safe_line.replace('navigator.', '<span style="color:#a78bfa;">navigator.</span>')
        safe_line = safe_line.replace('console.', '<span style="color:#34d399;">console.</span>')
        
        row = f'''
        <tr style="line-height:1.45;">
          <td style="padding:0 12px 0 6px;color:#475569;text-align:right;user-select:none;font-family:monospace;font-size:12px;border-right:1px solid #1e293b;width:34px;">{idx}</td>
          <td style="padding-left:14px;white-space:pre;font-family:'JetBrains Mono',Consolas,monospace;font-size:12.5px;color:#e2e8f0;">{safe_line}</td>
        </tr>
        '''
        rows.append(row)
    
    table_content = "".join(rows)
    return f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{
      margin: 0;
      padding: 16px;
      background: #020617;
      font-family: 'JetBrains Mono', Consolas, monospace;
    }}
    .window {{
      background: #090d16;
      border: 1px solid #1e293b;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }}
    .window-header {{
      background: #0f172a;
      padding: 10px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #1e293b;
    }}
    .dots {{
      display: flex;
      gap: 6px;
    }}
    .dot {{
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }}
    .dot.r {{ background: #ef4444; }}
    .dot.y {{ background: #f59e0b; }}
    .dot.g {{ background: #10b981; }}
    .title {{
      color: #94a3b8;
      font-size: 12px;
      font-weight: 600;
      letter-spacing: 0.05em;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      padding: 10px 0;
      margin: 10px 0;
    }}
  </style>
</head>
<body>
  <div class="window">
    <div class="window-header">
      <div class="dots">
        <div class="dot r"></div>
        <div class="dot y"></div>
        <div class="dot g"></div>
      </div>
      <div class="title">{title}</div>
      <div style="font-size:11px;color:#64748b;font-weight:500;">compiler.html</div>
    </div>
    <table>
      {table_content}
    </table>
  </div>
</body>
</html>'''

# Lines 1-40
part1_html = make_code_card(code_lines[0:40], 1, "Compiler Source Code (Lines 1-40): HTML Structure, Styling & Toolbar")
part1_file = os.path.join(workspace_dir, "_temp_part1.html")
with open(part1_file, "w", encoding="utf-8") as f:
    f.write(part1_html)

cmd1 = [chrome_exe, "--headless=new", "--no-sandbox", "--disable-gpu", "--window-size=1080,820", f"--screenshot={os.path.join(workspace_dir, 'fig2_source_code_part1.png')}", f"file:///{part1_file}"]
subprocess.run(cmd1, capture_output=True, timeout=15)
if os.path.exists(part1_file): os.remove(part1_file)

# Lines 41-79
part2_html = make_code_card(code_lines[40:79], 41, "Compiler Source Code (Lines 41-79): Editors, Bridge & Execution Logic")
part2_file = os.path.join(workspace_dir, "_temp_part2.html")
with open(part2_file, "w", encoding="utf-8") as f:
    f.write(part2_html)

cmd2 = [chrome_exe, "--headless=new", "--no-sandbox", "--disable-gpu", "--window-size=1080,820", f"--screenshot={os.path.join(workspace_dir, 'fig3_source_code_part2.png')}", f"file:///{part2_file}"]
subprocess.run(cmd2, capture_output=True, timeout=15)
if os.path.exists(part2_file): os.remove(part2_file)

print("Figure 2 and Figure 3 images generated successfully!")

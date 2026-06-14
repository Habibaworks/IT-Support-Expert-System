import streamlit as st

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IT Support Expert System",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Knowledge Base ───────────────────────────────────────────────────────────
RULES = [
    {"id":"R01","conclusion":"no_internet_access",         "conditions":["cannot_browse_websites","ping_fails"],                          "explanation":"Cannot browse AND ping fails → no internet access."},
    {"id":"R02","conclusion":"dns_problem",                "conditions":["cannot_browse_websites","ping_succeeds_by_ip"],                 "explanation":"Browsing fails but IP ping works → DNS resolution broken."},
    {"id":"R03","conclusion":"network_adapter_fault",      "conditions":["no_internet_access","wifi_icon_shows_error"],                   "explanation":"No internet AND adapter error icon → network adapter fault."},
    {"id":"R04","conclusion":"router_issue",               "conditions":["no_internet_access","other_devices_also_offline"],              "explanation":"Multiple devices offline → router or ISP issue."},
    {"id":"R05","conclusion":"isp_outage",                 "conditions":["router_issue","router_lights_abnormal"],                        "explanation":"Router lights abnormal + all offline → ISP outage."},
    {"id":"R06","conclusion":"local_network_config_error", "conditions":["no_internet_access","other_devices_online"],                    "explanation":"Other devices work → misconfiguration on this machine."},
    {"id":"R07","conclusion":"high_cpu_usage",             "conditions":["system_very_slow","cpu_usage_above_90"],                        "explanation":"Slow system AND CPU > 90% → high CPU usage."},
    {"id":"R08","conclusion":"high_ram_usage",             "conditions":["system_very_slow","ram_usage_above_90"],                        "explanation":"Slow system AND RAM > 90% → high RAM usage."},
    {"id":"R09","conclusion":"malware_infection",          "conditions":["high_cpu_usage","unknown_processes_running"],                   "explanation":"High CPU with unknown processes → malware infection."},
    {"id":"R10","conclusion":"disk_fragmentation",         "conditions":["system_very_slow","hdd_not_ssd","disk_not_defragged_recently"], "explanation":"Slow HDD not recently defragged → disk fragmentation."},
    {"id":"R11","conclusion":"insufficient_ram",           "conditions":["high_ram_usage","ram_less_than_4gb"],                           "explanation":"RAM maxed on < 4 GB system → insufficient RAM."},
    {"id":"R12","conclusion":"startup_programs_overload",  "conditions":["system_slow_only_at_boot","many_startup_programs"],             "explanation":"Slow only at boot with many startup items → startup overload."},
    {"id":"R13","conclusion":"driver_conflict",            "conditions":["blue_screen_of_death","recently_installed_driver"],             "explanation":"BSOD after driver install → driver conflict."},
    {"id":"R14","conclusion":"ram_hardware_fault",         "conditions":["blue_screen_of_death","random_restarts","memtest_errors"],      "explanation":"BSOD + restarts + MemTest errors → faulty RAM."},
    {"id":"R15","conclusion":"overheating",                "conditions":["blue_screen_of_death","cpu_temp_above_90c"],                    "explanation":"BSOD with CPU > 90°C → overheating."},
    {"id":"R16","conclusion":"corrupted_system_files",     "conditions":["blue_screen_of_death","sfc_scan_found_errors"],                 "explanation":"BSOD + SFC errors → system file corruption."},
    {"id":"R17","conclusion":"software_crash",             "conditions":["specific_app_closes_unexpectedly","error_message_shown"],       "explanation":"App crashes with error → software-level crash."},
    {"id":"R18","conclusion":"corrupted_installation",     "conditions":["software_crash","reinstall_did_not_fix"],                      "explanation":"Crash persists after reinstall → corrupted installation."},
    {"id":"R19","conclusion":"compatibility_issue",        "conditions":["software_crash","app_not_supported_on_os_version"],             "explanation":"App crashes on unsupported OS → compatibility issue."},
    {"id":"R20","conclusion":"antivirus_blocking_app",     "conditions":["software_crash","antivirus_quarantine_log_entry"],              "explanation":"Antivirus quarantine log entry → AV blocking app."},
    {"id":"R21","conclusion":"disk_full",                  "conditions":["cannot_save_files","disk_space_less_than_1gb"],                 "explanation":"Cannot save AND < 1 GB free → disk is full."},
    {"id":"R22","conclusion":"disk_hardware_failure",      "conditions":["files_corrupted_randomly","smart_test_failed"],                 "explanation":"Random corruption + SMART failure → disk failing."},
    {"id":"R23","conclusion":"file_system_error",          "conditions":["cannot_access_files","chkdsk_found_errors"],                    "explanation":"Access errors + CHKDSK errors → file system corruption."},
    {"id":"R24","conclusion":"printer_driver_issue",       "conditions":["printer_not_printing","printer_driver_outdated"],               "explanation":"Printer won't print with outdated driver → driver issue."},
    {"id":"R25","conclusion":"printer_queue_stuck",        "conditions":["printer_not_printing","print_queue_has_old_jobs"],              "explanation":"Stuck jobs in queue → print spooler blocked."},
    {"id":"R26","conclusion":"printer_offline",            "conditions":["printer_not_printing","printer_status_shows_offline"],          "explanation":"Printer status is Offline → needs to be set online."},
]

QUESTIONS = {
    "cannot_browse_websites":          "Are you UNABLE to open any website in a browser?",
    "ping_fails":                      "Does 'ping 8.8.8.8' in CMD fail (request timed out)?",
    "ping_succeeds_by_ip":             "Does 'ping 8.8.8.8' SUCCEED but websites still don't open?",
    "wifi_icon_shows_error":           "Does the network icon in taskbar show a red X or warning?",
    "other_devices_also_offline":      "Are other devices (phone/tablet) ALSO unable to connect?",
    "other_devices_online":            "Are other devices on the SAME network working fine?",
    "router_lights_abnormal":          "Are the router lights unusual (red, off, or abnormal)?",
    "system_very_slow":                "Is the system running unusually slowly?",
    "cpu_usage_above_90":              "Does Task Manager show CPU above 90% most of the time?",
    "ram_usage_above_90":              "Does Task Manager show RAM above 90% most of the time?",
    "unknown_processes_running":       "Are there unfamiliar/suspicious processes in Task Manager?",
    "hdd_not_ssd":                     "Is the drive a mechanical HDD (NOT an SSD)?",
    "disk_not_defragged_recently":     "Has the disk NOT been defragmented in the last 3 months?",
    "ram_less_than_4gb":               "Does the system have LESS than 4 GB of RAM?",
    "system_slow_only_at_boot":        "Is it slow ONLY during startup, but fine afterward?",
    "many_startup_programs":           "Are many programs launching at startup (Task Manager → Startup)?",
    "blue_screen_of_death":            "Has a Blue Screen of Death (BSOD) appeared?",
    "recently_installed_driver":       "Was a hardware driver installed recently before the BSOD?",
    "random_restarts":                 "Does the system restart randomly without warning?",
    "memtest_errors":                  "Did MemTest86 or Windows Memory Diagnostic report errors?",
    "cpu_temp_above_90c":              "Does HWMonitor show CPU temperature above 90°C?",
    "sfc_scan_found_errors":           "Did running 'sfc /scannow' in CMD find errors?",
    "specific_app_closes_unexpectedly":"Does a specific application crash or close unexpectedly?",
    "error_message_shown":             "Is an error message shown when the app crashes?",
    "reinstall_did_not_fix":           "Did reinstalling the application NOT fix the crash?",
    "app_not_supported_on_os_version": "Is the app documented as unsupported on your Windows version?",
    "antivirus_quarantine_log_entry":  "Does your antivirus show a quarantine entry for that app?",
    "cannot_save_files":               "Are you unable to save new files to the disk?",
    "disk_space_less_than_1gb":        "Is free disk space below 1 GB?",
    "files_corrupted_randomly":        "Are files becoming corrupted or unreadable randomly?",
    "smart_test_failed":               "Did CrystalDiskInfo or SMART test report 'Caution' or 'Bad'?",
    "cannot_access_files":             "Are you unable to open or access files on the disk?",
    "chkdsk_found_errors":             "Did 'chkdsk /f' report errors on the disk?",
    "printer_not_printing":            "Is the printer failing to print any documents?",
    "printer_driver_outdated":         "Is the printer driver outdated or improperly installed?",
    "print_queue_has_old_jobs":        "Does the print queue show stuck or old print jobs?",
    "printer_status_shows_offline":    "Does Windows show the printer as 'Offline'?",
}

RECOMMENDATIONS = {
    "no_internet_access":         "Check cables/Wi-Fi. Run Windows Network Troubleshooter. Restart router.",
    "dns_problem":                "Open CMD → run: ipconfig /flushdns\nChange DNS to 8.8.8.8 in adapter settings.",
    "network_adapter_fault":      "Update/reinstall network adapter driver via Device Manager.",
    "router_issue":               "Reboot router (unplug 30 sec). Check all cable connections.",
    "isp_outage":                 "Contact your ISP. Check their outage status page.",
    "local_network_config_error": "Run as Admin: netsh int ip reset AND netsh winsock reset → restart.",
    "high_cpu_usage":             "Task Manager → identify high-CPU process → end task or investigate.",
    "high_ram_usage":             "Close unused apps. Check for memory leaks. Consider adding RAM.",
    "malware_infection":          "Run full scan with Windows Defender or Malwarebytes. Quarantine threats.",
    "disk_fragmentation":         "Run Disk Defragmenter (Start → 'Defragment'). Consider upgrading to SSD.",
    "insufficient_ram":           "Upgrade to at least 8 GB RAM for modern Windows usage.",
    "startup_programs_overload":  "Task Manager → Startup tab → Disable non-essential programs.",
    "driver_conflict":            "Uninstall recent driver. Device Manager → Roll Back Driver.",
    "ram_hardware_fault":         "Replace faulty RAM. Test sticks individually with MemTest86.",
    "overheating":                "Clean CPU fan/heatsink. Replace thermal paste. Improve case airflow.",
    "corrupted_system_files":     "CMD (Admin): sfc /scannow\nThen: DISM /Online /Cleanup-Image /RestoreHealth",
    "software_crash":             "Update the app. Check vendor's support page for known issues.",
    "corrupted_installation":     "Delete leftover files/registry entries, then fresh reinstall.",
    "compatibility_issue":        "Run app in compatibility mode (right-click → Properties → Compatibility).",
    "antivirus_blocking_app":     "Add the application to your antivirus exclusions list.",
    "disk_full":                  "Delete files, empty Recycle Bin, run Disk Cleanup, move files externally.",
    "disk_hardware_failure":      "⚠️ BACK UP DATA IMMEDIATELY. Replace the failing drive. Restore from backup.",
    "file_system_error":          "CMD (Admin): chkdsk C: /f /r (requires restart).",
    "printer_driver_issue":       "Download latest driver from manufacturer's website and reinstall.",
    "printer_queue_stuck":        "Services → restart 'Print Spooler' → clear the queue.",
    "printer_offline":            "Right-click printer → 'See what's printing' → Printer → Uncheck 'Use Printer Offline'.",
}

SEVERITY = {
    "disk_hardware_failure":"critical","ram_hardware_fault":"critical","overheating":"critical",
    "malware_infection":"high","corrupted_system_files":"high","isp_outage":"high",
    "driver_conflict":"medium","insufficient_ram":"medium","file_system_error":"medium",
}

CATEGORIES = {
    "Network":     {"icon":"🌐","goals":["isp_outage","local_network_config_error","dns_problem","network_adapter_fault","router_issue"]},
    "Performance": {"icon":"⚡","goals":["malware_infection","insufficient_ram","disk_fragmentation","startup_programs_overload"]},
    "BSOD":        {"icon":"💙","goals":["overheating","ram_hardware_fault","driver_conflict","corrupted_system_files"]},
    "Software":    {"icon":"💿","goals":["antivirus_blocking_app","compatibility_issue","corrupted_installation","software_crash"]},
    "Storage":     {"icon":"💾","goals":["disk_hardware_failure","file_system_error","disk_full"]},
    "Printer":     {"icon":"🖨️","goals":["printer_queue_stuck","printer_offline","printer_driver_issue"]},
}

SEV_CONFIG = {
    "critical": {"color":"#ef4444","bg":"#2a0a0a","label":"CRITICAL"},
    "high":     {"color":"#f97316","bg":"#2a1407","label":"HIGH"},
    "medium":   {"color":"#eab308","bg":"#2a1e06","label":"MEDIUM"},
    "low":      {"color":"#22c55e","bg":"#052e16","label":"LOW"},
}

# ─── Backward Chaining Engine ─────────────────────────────────────────────────
class BackwardChainer:
    def __init__(self):
        self.facts = {}
        self.trace = []
        self.goals_tried = set()
        self.proof_tree = []
        self.conclusion_index = {}
        for r in RULES:
            self.conclusion_index.setdefault(r["conclusion"], []).append(r)

    def prove(self, goal, known_facts, depth=0):
        pad = "  " * depth
        if goal in known_facts:
            self.trace.append(f"{pad}✓ [KNOWN] {goal} = {known_facts[goal]}")
            return {"done": True, "result": known_facts[goal]}
        if goal in self.goals_tried:
            return {"done": True, "result": False}
        self.goals_tried.add(goal)
        self.trace.append(f"{pad}? [GOAL] Trying to prove: {goal}")
        if goal in self.conclusion_index:
            for rule in self.conclusion_index[goal]:
                self.trace.append(f"{pad}  → Testing {rule['id']}: {rule['explanation']}")
                all_ok = True
                for cond in rule["conditions"]:
                    sub = self.prove(cond, known_facts, depth + 1)
                    if not sub["done"]:
                        return sub
                    if not sub["result"]:
                        all_ok = False
                        break
                if all_ok:
                    self.facts[goal] = True
                    self.trace.append(f"{pad}  ✅ PROVED: {goal} via {rule['id']}")
                    self.proof_tree.append({
                        "rule_id": rule["id"],
                        "explanation": rule["explanation"],
                        "conclusion": goal,
                        "conditions": rule["conditions"],
                    })
                    return {"done": True, "result": True}
        if goal in QUESTIONS:
            why_chain = [
                {"rule_id": r["id"], "to_prove": r["conclusion"], "explanation": r["explanation"]}
                for r in RULES if goal in r["conditions"]
            ]
            return {"done": False, "fact": goal, "why_chain": why_chain}
        known_facts[goal] = False
        return {"done": True, "result": False}


def run_engine(goals, known_facts):
    """Run backward chainer over all goals; stop when a question is needed."""
    engine = BackwardChainer()
    diagnoses = []
    for goal in goals:
        engine.goals_tried = set()
        result = engine.prove(goal, known_facts)
        if result["done"]:
            if result.get("result"):
                diagnoses.append(goal)
        else:
            return {
                "status": "question",
                "fact": result["fact"],
                "why_chain": result.get("why_chain", []),
                "current_goal": goal,
                "remaining_goals": goals[goals.index(goal):],
                "diagnoses_so_far": diagnoses,
                "trace": engine.trace,
                "proof_tree": engine.proof_tree,
            }
    return {
        "status": "done",
        "diagnoses": diagnoses,
        "trace": engine.trace,
        "proof_tree": engine.proof_tree,
    }


# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
}
.stApp { background: #060a14; color: #c9d1d9; }

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 960px; }

/* Header */
.sys-header {
    background: linear-gradient(135deg,#0d1117,#161b22);
    border-bottom: 1px solid #21262d;
    padding: 18px 28px;
    margin: -1rem -1rem 2rem -1rem;
    display: flex; align-items: center; gap: 14px;
}
.sys-header-title { font-size: 18px; font-weight: 700; color: #58a6ff; letter-spacing: 2px; }
.sys-header-sub { font-size: 9px; color: #484f58; letter-spacing: 3px; margin-top: 2px; }

/* Cards */
.card {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 22px 26px;
    margin-bottom: 14px;
}
.card-blue  { border-color: #1a2d4a; }
.card-green { border-color: #1a4731; }

/* Section label */
.sec-label {
    font-size: 9px; color: #484f58;
    letter-spacing: 3px; text-transform: uppercase;
    margin-bottom: 12px;
}

/* Category tile */
.cat-tile {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 22px 18px;
    cursor: pointer;
    transition: all .2s;
    text-align: left;
    width: 100%;
}
.cat-tile:hover { border-color: #58a6ff; background: #161b22; transform: translateY(-3px); }
.cat-icon  { font-size: 30px; margin-bottom: 10px; }
.cat-name  { font-size: 13px; font-weight: 700; color: #e6edf3; margin-bottom: 4px; }
.cat-count { font-size: 10px; color: #484f58; margin-bottom: 10px; }

/* Tags */
.tag-yes { display:inline-block; font-size:10px; padding:2px 8px; border-radius:4px; background:#0f2a1d; color:#56d364; border:1px solid #1a4731; margin:2px; }
.tag-no  { display:inline-block; font-size:10px; padding:2px 8px; border-radius:4px; background:#2a0f0f; color:#f85149; border:1px solid #4a1a1a; margin:2px; }
.rule-tag { display:inline-block; font-size:10px; padding:2px 8px; border-radius:4px; background:#1f2937; border:1px solid #374151; color:#60a5fa; margin-right:8px; white-space:nowrap; }

/* IF-THEN block */
.ifthen {
    background: #0a0d13;
    border: 1px solid #1a2332;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 11px;
    line-height: 2;
    white-space: pre-wrap;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 10px;
}
.kw   { color: #ff7b72; font-weight: 700; }
.cond { color: #79c0ff; }
.then { color: #56d364; font-weight: 600; }

/* Progress bar */
.prog-bar-wrap { height: 3px; background: #21262d; border-radius: 2px; margin: 8px 0 20px; }
.prog-bar-fill { height: 3px; background: linear-gradient(90deg,#1f6feb,#58a6ff); border-radius: 2px; transition: width .4s; }

/* Question card */
.q-card {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 36px 28px;
    text-align: center;
    margin-bottom: 14px;
}
.q-text { font-size: 16px; color: #e6edf3; line-height: 1.7; margin: 16px auto 28px; max-width: 520px; }

/* Diagnosis result */
.diag-card {
    background: #0d1117;
    border-radius: 12px;
    padding: 22px 26px;
    margin-bottom: 14px;
}
.diag-title { font-size: 14px; font-weight: 700; color: #e6edf3; }
.fix-box { background: #0a0d13; border-radius: 8px; padding: 12px 16px; margin: 12px 0; }
.fix-label { font-size: 10px; color: #238636; letter-spacing: 1px; margin-bottom: 6px; }
.fix-text { font-size: 11px; color: #7ee787; white-space: pre-line; line-height: 1.8; }

/* Trace box */
.trace-box {
    background: #060a14;
    border: 1px solid #161b22;
    border-radius: 10px;
    padding: 16px;
    max-height: 320px;
    overflow-y: auto;
    font-size: 10px;
    font-family: monospace;
    line-height: 1.9;
}

/* Stats bar */
.stat-box { background:#0d1117; border:1px solid #21262d; border-radius:10px; padding:18px 12px; text-align:center; }
.stat-num  { font-size:28px; font-weight:700; color:#58a6ff; }
.stat-lbl  { font-size:11px; color:#e6edf3; margin-top:4px; }
.stat-sub  { font-size:10px; color:#484f58; margin-top:4px; }

/* Nav tabs override */
div[data-testid="stHorizontalBlock"] { gap: 8px; }

/* Buttons */
.stButton > button {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    border-radius: 7px !important;
    transition: all .2s !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 7px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    color: #8b949e !important;
}

/* Search input */
.stTextInput > div > div > input {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sys-header">
  <span style="font-size:28px">🖥️</span>
  <div>
    <div class="sys-header-title">IT SUPPORT EXPERT SYSTEM</div>
    <div class="sys-header-sub">KNOWLEDGE-BASED SYSTEM · BACKWARD CHAINING · 26 RULES</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Session State ────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "tab": "🏠 Home",
        "phase": "select",        # select | questioning | results
        "category": None,
        "facts": {},
        "history": [],            # list of {fact, answer}
        "diagnoses": [],
        "trace": [],
        "proof_tree": [],
        "current_q": None,        # {fact, why_chain, current_goal, remaining_goals, diagnoses_so_far}
        "progress": 0,
        "show_trace": False,
        "rule_filter": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── Navigation ───────────────────────────────────────────────────────────────
tabs = ["🏠 Home", "🔍 Diagnose", "📋 Rules", "🧮 Logic", "ℹ️ About"]
col_tabs = st.columns(len(tabs))
for i, t in enumerate(tabs):
    with col_tabs[i]:
        if st.button(t, key=f"nav_{t}", use_container_width=True,
                     type="primary" if st.session_state.tab == t else "secondary"):
            st.session_state.tab = t
            if t != "🔍 Diagnose":
                st.session_state.phase = "select"
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ─── Helper: start diagnosis ──────────────────────────────────────────────────
def start_diagnosis(cat):
    goals = CATEGORIES[cat]["goals"]
    st.session_state.category = cat
    st.session_state.facts = {}
    st.session_state.history = []
    st.session_state.diagnoses = []
    st.session_state.trace = []
    st.session_state.proof_tree = []
    st.session_state.progress = 0
    st.session_state.phase = "questioning"
    advance(goals)


def advance(goals_remaining):
    result = run_engine(goals_remaining, dict(st.session_state.facts))
    if result["status"] == "done":
        st.session_state.diagnoses = result["diagnoses"]
        st.session_state.trace = result["trace"]
        st.session_state.proof_tree = result["proof_tree"]
        st.session_state.phase = "results"
        st.session_state.current_q = None
    else:
        total = len(CATEGORIES[st.session_state.category]["goals"])
        done_count = total - len(result["remaining_goals"])
        st.session_state.progress = int(done_count / total * 100)
        st.session_state.diagnoses = result["diagnoses_so_far"]
        st.session_state.trace = result["trace"]
        st.session_state.proof_tree = result["proof_tree"]
        st.session_state.current_q = {
            "fact": result["fact"],
            "why_chain": result["why_chain"],
            "current_goal": result["current_goal"],
            "remaining_goals": result["remaining_goals"],
        }


def answer_question(answer):
    q = st.session_state.current_q
    fact = q["fact"]
    st.session_state.facts[fact] = answer
    st.session_state.history.append({"fact": fact, "answer": answer})
    advance(q["remaining_goals"])


def go_back():
    if not st.session_state.history:
        return
    # Remove last answer
    last = st.session_state.history.pop()
    st.session_state.facts.pop(last["fact"], None)
    # Re-run from scratch to restore state
    goals = CATEGORIES[st.session_state.category]["goals"]
    advance(goals)


def reset_all():
    st.session_state.phase = "select"
    st.session_state.category = None
    st.session_state.facts = {}
    st.session_state.history = []
    st.session_state.diagnoses = []
    st.session_state.trace = []
    st.session_state.proof_tree = []
    st.session_state.current_q = None
    st.session_state.progress = 0
    st.session_state.show_trace = False


def ifthen_html(rule, highlight_fact=None):
    conditions_html = ""
    for i, c in enumerate(rule["conditions"]):
        label = c.replace("_", " ")
        style = "text-decoration:underline;font-weight:700;" if c == highlight_fact else ""
        conditions_html += f'<span class="cond" style="{style}">{label}</span>'
        if i < len(rule["conditions"]) - 1:
            conditions_html += '<span class="kw"> AND\n      </span>'
    conclusion = rule["conclusion"].replace("_", " ")
    return f"""<div class="ifthen"><span class="kw">IF    </span>{conditions_html}\n<span class="kw">THEN  </span><span class="then">{conclusion}</span></div>"""


# ══════════════════════════════════════════════════════════════════════════════
# HOME TAB
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.tab == "🏠 Home":
    st.markdown("""
    <div style="text-align:center;padding:32px 0 40px">
      <div style="font-size:52px;margin-bottom:14px">🧠</div>
      <div style="font-size:24px;font-weight:700;color:#58a6ff;margin-bottom:10px">IT Support Expert System</div>
      <div style="font-size:13px;color:#8b949e;max-width:520px;margin:0 auto;line-height:1.9">
        A <span style="color:#79c0ff">Knowledge-Based System</span> that diagnoses common
        Windows IT problems using <span style="color:#79c0ff">Backward Chaining</span> inference
        over 26 IF-THEN production rules.
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, (val, lbl, sub) in zip(
        [c1, c2, c3, c4],
        [("26","Rules","IF-THEN knowledge base"),
         ("6","Domains","IT problem categories"),
         ("38","Facts","Observable conditions"),
         ("BC","Engine","Backward Chaining")],
    ):
        with col:
            st.markdown(f"""
            <div class="stat-box">
              <div class="stat-num">{val}</div>
              <div class="stat-lbl">{lbl}</div>
              <div class="stat-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
      <div class="sec-label">How Backward Chaining Works</div>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    steps = [
        ("1️⃣ Set Goal", "The system picks a possible diagnosis (e.g. malware_infection) as the current goal to prove."),
        ("2️⃣ Check Conditions", "It recursively checks each condition in the matching rule — asking the user only when a fact is unknown."),
        ("3️⃣ Conclude", "If all conditions hold, the goal is proved and added to the diagnosis list with its full explanation."),
    ]
    for col, (title, desc) in zip([col1, col2, col3], steps):
        with col:
            st.markdown(f"""
            <div style="background:#0a0d13;border:1px solid #1a2332;border-radius:8px;padding:14px 16px">
              <div style="font-size:13px;margin-bottom:8px">{title}</div>
              <div style="font-size:11px;color:#8b949e;line-height:1.7">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍  START DIAGNOSIS  →", use_container_width=True, type="primary"):
        st.session_state.tab = "🔍 Diagnose"
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# DIAGNOSE TAB
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.tab == "🔍 Diagnose":

    # ── SELECT ──
    if st.session_state.phase == "select":
        st.markdown('<div class="sec-label">Select Problem Category</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        cat_list = list(CATEGORIES.items())
        for i, (cat, meta) in enumerate(cat_list):
            with cols[i % 3]:
                goals_preview = " · ".join(g.replace("_", " ") for g in meta["goals"][:3])
                st.markdown(f"""
                <div class="card" style="text-align:left">
                  <div class="cat-icon">{meta['icon']}</div>
                  <div class="cat-name">{cat} Issues</div>
                  <div class="cat-count">{len(meta['goals'])} possible diagnoses</div>
                  <div style="font-size:9px;color:#484f58">{goals_preview}</div>
                </div>""", unsafe_allow_html=True)
                if st.button(f"Diagnose {cat}", key=f"cat_{cat}", use_container_width=True, type="primary"):
                    start_diagnosis(cat)
                    st.rerun()

    # ── QUESTIONING ──
    elif st.session_state.phase == "questioning" and st.session_state.current_q:
        q = st.session_state.current_q
        cat = st.session_state.category

        # Progress bar
        prog = st.session_state.progress
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;font-size:10px;color:#484f58;margin-bottom:6px">
          <span>DIAGNOSING: {cat.upper()} — BACKWARD CHAINING</span>
          <span>{prog}% COMPLETE</span>
        </div>
        <div class="prog-bar-wrap"><div class="prog-bar-fill" style="width:{prog}%"></div></div>
        """, unsafe_allow_html=True)

        # Explanation facility
        fact_label = q["fact"].replace("_", " ")
        why_html = f"""
        <div class="card card-blue">
          <div class="sec-label">📖 Explanation — Why Is This Question Being Asked?</div>
          <div style="font-size:12px;color:#8b949e;margin-bottom:10px">
            The system needs to determine: <span style="color:#79c0ff;font-weight:700">"{fact_label}"</span>
          </div>"""

        if q["why_chain"]:
            why_html += '<div style="font-size:10px;color:#484f58;margin-bottom:8px">This fact is required to evaluate:</div>'
            for item in q["why_chain"]:
                to_prove = item["to_prove"].replace("_", " ")
                why_html += f"""
                <div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:6px;
                            background:#0a0d13;border-radius:6px;padding:8px 12px">
                  <span class="rule-tag">{item['rule_id']}</span>
                  <div>
                    <div style="font-size:10px;color:#8b949e">Trying to prove: <span style="color:#56d364">{to_prove}</span></div>
                    <div style="font-size:10px;color:#484f58;margin-top:2px">{item['explanation']}</div>
                  </div>
                </div>"""

            # Show first matching rule as IF-THEN
            first_rule_id = q["why_chain"][0]["rule_id"] if q["why_chain"] else None
            if first_rule_id:
                rule_obj = next((r for r in RULES if r["id"] == first_rule_id), None)
                if rule_obj:
                    why_html += '<div style="font-size:10px;color:#484f58;margin:12px 0 6px">Relevant rule (underlined = fact being asked):</div>'
                    why_html += ifthen_html(rule_obj, highlight_fact=q["fact"])
        else:
            why_html += '<div style="font-size:11px;color:#484f58">Primitive observable fact needed to continue the reasoning chain.</div>'

        why_html += "</div>"
        st.markdown(why_html, unsafe_allow_html=True)

        # Question
        question_text = QUESTIONS.get(q["fact"], q["fact"].replace("_", " "))
        st.markdown(f"""
        <div class="q-card">
          <div style="font-size:34px;margin-bottom:12px">❓</div>
          <div class="q-text">{question_text}</div>
        </div>""", unsafe_allow_html=True)

        col_yes, col_no, col_back = st.columns([2, 2, 1])
        with col_yes:
            if st.button("✓  YES", key="ans_yes", use_container_width=True, type="primary"):
                answer_question(True)
                st.rerun()
        with col_no:
            if st.button("✗  NO", key="ans_no", use_container_width=True):
                answer_question(False)
                st.rerun()
        with col_back:
            if st.session_state.history:
                if st.button("← Back", key="go_back", use_container_width=True):
                    go_back()
                    st.rerun()

        # Facts gathered
        if st.session_state.history:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="sec-label">Facts Gathered</div>', unsafe_allow_html=True)
            tags_html = "".join(
                f'<span class="{"tag-yes" if h["answer"] else "tag-no"}">{"✓" if h["answer"] else "✗"} {h["fact"].replace("_"," ")}</span>'
                for h in st.session_state.history
            )
            st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:4px">{tags_html}</div>', unsafe_allow_html=True)

    # ── RESULTS ──
    elif st.session_state.phase == "results":
        diagnoses = st.session_state.diagnoses
        cat = st.session_state.category

        emoji = "🔍" if diagnoses else "✅"
        count_msg = f"{len(diagnoses)} issue(s) identified" if diagnoses else "No issues identified"
        st.markdown(f"""
        <div style="text-align:center;margin-bottom:28px">
          <div style="font-size:42px;margin-bottom:12px">{emoji}</div>
          <div style="font-size:22px;font-weight:700;color:#58a6ff">DIAGNOSIS COMPLETE</div>
          <div style="font-size:11px;color:#484f58;margin-top:4px">{cat} Issues · Backward Chaining · {count_msg}</div>
        </div>""", unsafe_allow_html=True)

        if not diagnoses:
            st.markdown("""
            <div class="card card-green" style="text-align:center">
              <div style="font-size:14px;color:#56d364">No specific issue identified from your responses.</div>
              <div style="font-size:11px;color:#484f58;margin-top:6px">Consider contacting IT support for manual inspection.</div>
            </div>""", unsafe_allow_html=True)
        else:
            for i, d in enumerate(diagnoses):
                sev = SEVERITY.get(d, "low")
                cfg = SEV_CONFIG[sev]
                rec = RECOMMENDATIONS.get(d, "Consult IT support.")
                proof = next((p for p in st.session_state.proof_tree if p["conclusion"] == d), None)
                proof_html = ""
                if proof:
                    proof_html = f'<div class="ifthen" style="margin-top:10px"><span class="kw">PROVED BY </span><span style="color:#60a5fa">{proof["rule_id"]}</span><span style="color:#484f58">: {proof["explanation"]}</span></div>'

                st.markdown(f"""
                <div class="diag-card" style="border:1px solid {cfg['color']}44">
                  <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;flex-wrap:wrap">
                    <span class="rule-tag">#{i+1}</span>
                    <span class="diag-title">{d.replace('_',' ').upper()}</span>
                    <span style="font-size:10px;padding:3px 10px;border-radius:12px;
                                 background:{cfg['bg']};color:{cfg['color']};
                                 border:1px solid {cfg['color']}44;font-weight:700;margin-left:auto">
                      {cfg['label']}
                    </span>
                  </div>
                  <div class="fix-box">
                    <div class="fix-label">RECOMMENDED FIX</div>
                    <div class="fix-text">{rec}</div>
                  </div>
                  {proof_html}
                </div>""", unsafe_allow_html=True)

        # Proof tree
        proof_tree = st.session_state.proof_tree
        if proof_tree:
            with st.expander(f"🌳 Proof Tree — {len(proof_tree)} rule(s) fired"):
                for p in proof_tree:
                    st.markdown(f"""
                    <div style="display:flex;gap:12px;padding:10px 0;border-bottom:1px solid #161b22">
                      <span class="rule-tag">{p['rule_id']}</span>
                      <div style="flex:1">
                        <div style="font-size:11px;color:#8b949e;margin-bottom:6px">{p['explanation']}</div>
                        {ifthen_html(p)}
                      </div>
                    </div>""", unsafe_allow_html=True)

        # Reasoning trace
        trace = st.session_state.trace
        if trace:
            with st.expander(f"📜 Full Reasoning Trace — {len(trace)} steps"):
                trace_lines = ""
                for line in trace:
                    if "✅" in line:
                        color = "#56d364"
                    elif "[KNOWN]" in line:
                        color = "#79c0ff"
                    elif "?" in line:
                        color = "#58a6ff"
                    else:
                        color = "#484f58"
                    trace_lines += f'<div style="color:{color};font-size:10px;font-family:monospace;line-height:1.9">{line}</div>'
                st.markdown(f'<div class="trace-box">{trace_lines}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄  DIAGNOSE ANOTHER PROBLEM", use_container_width=True, type="primary"):
            reset_all()
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# RULES TAB
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.tab == "📋 Rules":
    col_search, col_count = st.columns([4, 1])
    with col_search:
        rule_filter = st.text_input("", placeholder="Search by rule ID, conclusion, or description...", label_visibility="collapsed")
    filtered = [r for r in RULES if
                rule_filter.lower() in r["id"].lower() or
                rule_filter.lower() in r["conclusion"].lower() or
                rule_filter.lower() in r["explanation"].lower()] if rule_filter else RULES
    with col_count:
        st.markdown(f'<div style="font-size:11px;color:#484f58;padding-top:12px;text-align:right">{len(filtered)} / {len(RULES)} rules</div>', unsafe_allow_html=True)

    for rule in filtered:
        conclusion_label = rule["conclusion"].replace("_", " ")
        st.markdown(f"""
        <div class="card" style="margin-bottom:10px">
          <div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:10px;flex-wrap:wrap">
            <span class="rule-tag" style="font-size:12px">{rule['id']}</span>
            <div style="flex:1;font-size:12px;color:#e6edf3;font-weight:600">{rule['explanation']}</div>
            <span style="font-size:10px;padding:2px 8px;background:#0f2a1d;color:#56d364;
                         border:1px solid #1a4731;border-radius:4px;white-space:nowrap">
              → {conclusion_label}
            </span>
          </div>
          {ifthen_html(rule)}
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LOGIC TAB  —  Propositional Logic Representation
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.tab == "🧮 Logic":

    st.markdown("""
    <div class="card">
      <div class="sec-label">Propositional Logic Representation</div>
      <div style="font-size:12px;color:#8b949e;line-height:1.9;margin-bottom:14px">
        Every IF-THEN production rule in this system can be expressed formally as a
        <span style="color:#79c0ff">propositional logic formula</span>.
        Each observable fact is a boolean proposition (True / False).
        The inference engine uses <span style="color:#56d364">Modus Ponens</span>
        to derive new facts from known ones.
      </div>
      <div class="ifthen">
<span class="kw">Notation:</span>
  <span class="cond">p</span>        — primitive proposition (observable fact)
  <span class="cond">p ∧ q</span>    — conjunction  (p AND q must both be True)
  <span class="cond">p → q</span>    — implication  (if p then q)
  <span class="cond">¬p</span>       — negation     (NOT p)

<span class="kw">Inference rule used — Modus Ponens:</span>
  <span class="cond">p ∧ (p → q)</span>  ⊢  <span class="then">q</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Group rules by category for display
    cat_rules = {}
    for cat, meta in CATEGORIES.items():
        cat_rules[cat] = {"icon": meta["icon"], "rules": []}

    for rule in RULES:
        placed = False
        for cat, meta in CATEGORIES.items():
            # find which category this rule's conclusion belongs to (direct or via chain)
            if rule["conclusion"] in meta["goals"]:
                cat_rules[cat]["rules"].append(rule)
                placed = True
                break
        if not placed:
            # intermediate rules — find by category keyword
            for cat, meta in CATEGORIES.items():
                if any(rule["conclusion"] in r["conditions"]
                       for r in RULES
                       if r["conclusion"] in meta["goals"]):
                    cat_rules[cat]["rules"].append(rule)
                    placed = True
                    break
        if not placed:
            cat_rules[list(CATEGORIES.keys())[0]]["rules"].append(rule)

    def logic_formula(rule):
        """Build a propositional logic string for a rule."""
        conds = rule["conditions"]
        conclusion = rule["conclusion"]
        if len(conds) == 1:
            premise = conds[0]
        else:
            premise = " ∧ ".join(conds)
        return premise, conclusion

    rule_counter = 1
    for cat, data in cat_rules.items():
        if not data["rules"]:
            continue
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin:20px 0 10px">
          <span style="font-size:18px">{data['icon']}</span>
          <span style="font-size:10px;color:#484f58;letter-spacing:3px;text-transform:uppercase">{cat} Domain</span>
        </div>""", unsafe_allow_html=True)

        for rule in data["rules"]:
            premise, conclusion = logic_formula(rule)
            # build colored HTML
            conds = rule["conditions"]
            if len(conds) == 1:
                premise_html = f'<span class="cond">{conds[0]}</span>'
            else:
                parts = [f'<span class="cond">{c}</span>' for c in conds]
                premise_html = f' <span class="kw">∧</span> '.join(parts)

            conclusion_html = f'<span class="then">{conclusion}</span>'

            st.markdown(f"""
            <div class="card" style="margin-bottom:8px;padding:16px 20px">
              <div style="display:flex;gap:10px;align-items:center;margin-bottom:10px;flex-wrap:wrap">
                <span class="rule-tag">{rule['id']}</span>
                <span style="font-size:10px;color:#484f58">{rule['explanation']}</span>
              </div>
              <div class="ifthen" style="font-size:12px;line-height:2.2">
<span class="kw">Formula:  </span>{premise_html} <span class="kw">→</span> {conclusion_html}

<span class="kw">Expanded: </span><span style="color:#484f58">∀x: (</span>{premise_html}<span style="color:#484f58">) → </span>{conclusion_html}
              </div>
            </div>""", unsafe_allow_html=True)
            rule_counter += 1

    st.markdown("""
    <div class="card" style="margin-top:10px">
      <div class="sec-label">Derived Facts — Rule Chaining in Logic</div>
      <div style="font-size:11px;color:#8b949e;line-height:1.9;margin-bottom:12px">
        Some conclusions become premises in higher-level rules, enabling
        <span style="color:#79c0ff">multi-step propositional inference</span>:
      </div>
      <div class="ifthen" style="font-size:11px;line-height:2.2">
<span class="kw">Step 1 — R01: </span><span class="cond">cannot_browse_websites</span> <span class="kw">∧</span> <span class="cond">ping_fails</span> <span class="kw">→</span> <span class="then">no_internet_access</span>

<span class="kw">Step 2 — R03: </span><span class="then">no_internet_access</span> <span class="kw">∧</span> <span class="cond">wifi_icon_shows_error</span> <span class="kw">→</span> <span class="then">network_adapter_fault</span>

<span class="kw">Step 3 — R04: </span><span class="then">no_internet_access</span> <span class="kw">∧</span> <span class="cond">other_devices_also_offline</span> <span class="kw">→</span> <span class="then">router_issue</span>

<span class="kw">Step 4 — R05: </span><span class="then">router_issue</span> <span class="kw">∧</span> <span class="cond">router_lights_abnormal</span> <span class="kw">→</span> <span class="then">isp_outage</span>

<span style="color:#484f58;font-size:10px">
  ∴  cannot_browse_websites ∧ ping_fails ∧ other_devices_also_offline ∧ router_lights_abnormal  ⊢  isp_outage
</span>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ABOUT TAB
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.tab == "ℹ️ About":
    st.markdown('<div class="card"><div class="sec-label">System Architecture</div></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    arch = [
        ("Knowledge Base", "26 IF-THEN production rules covering 6 IT domains: Network, Performance, BSOD, Software, Storage, and Printer issues."),
        ("Inference Engine", "Backward Chaining — goal-driven, depth-first. Starts from a hypothesis and works backward to find supporting facts."),
        ("Explanation Facility", "Explains WHY each question is asked (which rules require that fact) and HOW conclusions were reached (proof tree + full trace)."),
        ("User Interface", "Interactive Q&A with Yes/No answers, progress tracking, back-navigation, and IF-THEN rule display on every screen."),
    ]
    for i, (title, desc) in enumerate(arch):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div style="background:#0a0d13;border:1px solid #1a2332;border-radius:8px;padding:14px 16px;margin-bottom:12px">
              <div style="font-size:11px;font-weight:700;color:#58a6ff;margin-bottom:6px">{title}</div>
              <div style="font-size:11px;color:#8b949e;line-height:1.7">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="margin-top:4px">
      <div class="sec-label">Knowledge Representation</div>
      <div style="font-size:11px;color:#8b949e;line-height:1.9;margin-bottom:12px">
        Rules are represented as <span style="color:#79c0ff">production rules</span>:
      </div>
      <div class="ifthen"><span class="kw">IF    </span><span class="cond">condition_1</span><span class="kw"> AND
      </span><span class="cond">condition_2  ...</span>
<span class="kw">THEN  </span><span class="then">conclusion</span></div>
      <div style="font-size:11px;color:#8b949e;line-height:1.9;margin-top:12px">
        Facts are boolean propositions (true/false). Rules chain together — a derived conclusion
        can become a condition for a higher-level rule (e.g., R01 → R03/R04 → R05).
      </div>
    </div>""", unsafe_allow_html=True)

    limitations = [
        "Binary facts only (Yes/No) — no probabilistic or fuzzy reasoning",
        "Static knowledge base — requires manual updates for new problem types",
        "No learning capability — cannot improve automatically from past diagnoses",
        "Single-fault assumption — may miss complex issues with multiple causes",
        "No natural language input — relies on structured Yes/No questions",
    ]
    lim_html = "".join(
        f'<div style="font-size:11px;color:#8b949e;padding:8px 0;border-bottom:1px solid #161b22;display:flex;gap:8px"><span style="color:#f85149">▸</span>{l}</div>'
        for l in limitations
    )
    st.markdown(f'<div class="card"><div class="sec-label">Limitations</div>{lim_html}</div>', unsafe_allow_html=True)

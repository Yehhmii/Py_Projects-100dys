import os
import subprocess
from flask import Flask, request, abort
from dotenv import load_dotenv
import ctypes, ctypes.wintypes

# ─── Setup ─────────────────────────────────────────────────────
load_dotenv()    # loads SECRET_TOKEN
SECRET = os.getenv("SECRET_TOKEN")

app = Flask(__name__)

# ─── Helpers ────────────────────────────────────────────────────

def lock_workstation():
    # Locks the Windows session
    subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])

def schedule_wake(seconds_from_now: int):
    # Create a manual-reset, waitable timer
    CreateWaitableTimer = ctypes.windll.kernel32.CreateWaitableTimerW
    SetWaitableTimer    = ctypes.windll.kernel32.SetWaitableTimer
    # FALSE = auto-reset? We want man-reset = True so it stays valid
    timer = CreateWaitableTimer(None, True, "WakeTimer")
    if not timer:
        raise ctypes.WinError()

    # Negative value = relative time, in 100-ns intervals
    # seconds * 10^7 (10 million)
    due_time = ctypes.wintypes.LARGE_INTEGER(-seconds_from_now * 10**7)
    # Documentation: (HANDLE hTimer, LARGE_INTEGER *pDueTime,
    #                 LONG Period, PTIMERAPCROUTINE pfnCompletionRoutine,
    #                 LPVOID lpArgToCompletionRoutine, BOOL fResume)
    if not SetWaitableTimer(timer, ctypes.byref(due_time), 0, None, None, True):
        raise ctypes.WinError()

def sleep_then_wake(seconds: int):
    # Schedule wake
    schedule_wake(seconds)
    # Enter sleep (S3)
    # Parameters: Hibernate=False, Force=True, DisableWakeEvent=False
    ctypes.windll.powrprof.SetSuspendState(False, True, False)


# ─── Routes ─────────────────────────────────────────────────────

@app.route("/lock", methods=["POST"])
def lock_route():
    token = request.headers.get("Authorization", "")
    if token != f"Bearer {SECRET}":
        abort(403)
    lock_workstation()
    return "Locked", 200

@app.route("/sleep", methods=["POST"])
def sleep_route():
    token = request.headers.get("Authorization", "")
    sec   = request.args.get("sec", type=int, default=300)
    if token != f"Bearer {SECRET}":
        abort(403)
    sleep_then_wake(sec)
    return f"Sleeping now, will wake in {sec}s", 200

# ─── Run ────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Listen on all interfaces so your phone (on the same hotspot)
    # can reach it at http://<PC_IP>:5000
    app.run(host="0.0.0.0", port=5000)

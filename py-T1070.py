import os
import subprocess
import shutil

def run(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[+] Executed: {cmd}")
    except subprocess.CalledProcessError:
        print(f"[!] Failed: {cmd}")

def wipe_log_files():
    log_paths = [
        "/var/log/syslog",
        "/var/log/auth.log",
        "/var/log/messages",
        "/var/log/secure",
        "/var/log/user.log",
        "/var/log/wtmp",
        "/var/log/btmp",
        "/var/log/lastlog"
    ]
    print("[*] Truncating common log files...")
    for path in log_paths:
        if os.path.exists(path):
            run(f"> {path}")
        else:
            print(f"[-] Missing: {path}")

    print("[*] Vacuuming journalctl logs...")
    run("journalctl --rotate")
    run("journalctl --vacuum-time=1s")
    run("journalctl --vacuum-size=1M")

def remove_shell_histories():
    history_files = [
        "~/.bash_history",
        "~/.zsh_history",
        "/root/.bash_history",
        "/root/.zsh_history"
    ]
    print("[*] Deleting shell history files...")
    for file in history_files:
        full_path = os.path.expanduser(file)
        if os.path.exists(full_path):
            os.remove(full_path)
            print(f"[+] Deleted: {full_path}")
        else:
            print(f"[-] Not found: {full_path}")

    print("[*] Unsetting persistent history environment variables...")
    os.environ['HISTFILE'] = ''
    os.environ['HISTSIZE'] = '0'
    os.environ['HISTFILESIZE'] = '0'
    run("unset HISTFILE; unset HISTSIZE; unset HISTFILESIZE")

    print("[*] Clearing in-memory history (requires manual logout for full effect)...")
    run("history -c")

def main():
    if os.geteuid() != 0:
        print("[!] Run this script as root for full effect.")
        return

    wipe_log_files()
    remove_shell_histories()
    print("\n[*] Log and history cleanup complete. Consider restarting your shell.")

if __name__ == "__main__":
    main()

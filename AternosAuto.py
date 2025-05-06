import os
import shutil
import tkinter as tk
from tkinter import messagebox
from seleniumbase import Driver
import psutil
from time import sleep
import sys


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USERDATA_DIR = os.path.join(SCRIPT_DIR, "Userdata")
PROFILE = os.path.join(USERDATA_DIR, "Default")
OPTION_FILE = os.path.join(SCRIPT_DIR, "selected_option.txt")
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, "credentials.txt")
DEBUG_FILE = os.path.join(SCRIPT_DIR, "debug.txt")

if not os.path.exists(USERDATA_DIR):
    os.makedirs(USERDATA_DIR)

username = ""
password = ""
selected_option = None
server_number = ""

def log(msg):
    print(f"[LOG] {msg}")

def load_selected_option():
    global selected_option, username, password
    if os.path.exists(OPTION_FILE):
        with open(OPTION_FILE, "r") as f:
            selected_option = f.read().strip()
            log(f"Loaded selected option: {selected_option}")
    else:
        selected_option = "Login"
        save_selected_option()
        log("No option found. Defaulted to Login.")

    if selected_option == "Login" and os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                username = lines[0].strip()
                password = lines[1].strip()
                log(f"Loaded login credentials: {username}/{password}")

def save_selected_option():
    global selected_option
    if selected_option:
        with open(OPTION_FILE, "w") as f:
            f.write(selected_option)
            log(f"Saved selected option: {selected_option}")

def save_credentials(username, password):
    with open(CREDENTIALS_FILE, "w") as f:
        f.write(username + "\n" + password)
    log("Saved login credentials")

def kill_chrome():
    for p in psutil.process_iter(['pid', 'name']):
        name = p.info['name'] or ""
        if 'chrome' in name.lower():
            try:
                p.terminate()
            except Exception:
                pass

def copy_profile():
    if os.path.exists(PROFILE):
        messagebox.showinfo("Info", "Profile already exists")
        return
    try:
        kill_chrome()
        if not os.path.exists(USERDATA_DIR):
            os.makedirs(USERDATA_DIR)
        src = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default")
        shutil.copytree(src, PROFILE, dirs_exist_ok=True)
        messagebox.showinfo("Info", "Profile copied")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to copy profile:\n{e}")

def start():
    log("Username Is : " + username)
    log("Password Is : " + password)
    if not os.path.exists(USERDATA_DIR):
        os.makedirs(USERDATA_DIR)
    
    headless = not os.path.exists(DEBUG_FILE)
    if not os.path.exists(PROFILE):
        messagebox.showwarning("Warning", "Copy profile first")
        return
    try:
        with Driver(uc=True, headless=headless, user_data_dir=USERDATA_DIR) as driver:
            log("Driver Up")
            driver.get("https://aternos.org/go/")
            log("Aternos Reached")
            sleep(2)
            current_url = str(driver.get_current_url())
            log("Current Url Is : " + current_url)
            sleep(2)
            if current_url != "https://aternos.org/go/" or "https://aternos.org/servers/":
                log("Please Wait...")
                sleep(5)
                driver.get("https://aternos.org/go/")
                current_url = str(driver.get_current_url())
                log("Current Url Is : " + current_url)
                if current_url == "https://aternos.org/go/" or "https://aternos.org/servers/":
                    x = 1
                else:
                    driver.get("https://aternos.org/go/")
            if "https://aternos.org/go/" in current_url:
                log("Logging In")
                if selected_option in ["Bot", "Login", "Google"]:
                    if selected_option == "Bot":
                        driver.type("/html/body/div[3]/div/div/div[3]/div[4]/div[1]/div[2]/input", username)
                        sleep(1)
                        driver.type("/html/body/div[3]/div/div/div[3]/div[4]/div[2]/div[2]/input", password)
                        sleep(1)
                        driver.click("/html/body/div[3]/div/div/div[3]/div[4]/button")
                    if selected_option == "Login":
                        driver.type("/html/body/div[3]/div/div/div[3]/div[4]/div[1]/div[2]/input", username)
                        sleep(1)
                        driver.type("/html/body/div[3]/div/div/div[3]/div[4]/div[2]/div[2]/input", password)
                        sleep(1)
                        driver.click("/html/body/div[3]/div/div/div[3]/div[4]/button")
                    if selected_option == "Google":
                        driver.click("/html/body/div[3]/div/div/div[3]/div[6]/div")
                        sleep(5)
                        driver.click("/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[1]/form/span/section/div/div/div/div/ul/li[1]/div")
                        sleep(1)
            sleep(2)
            current_url = str(driver.get_current_url())
            if current_url == "https://aternos.org/servers/":
                log("Logged In")
            else:
                log("Failed To Log In")
            sleep(5)
            current_url = str(driver.get_current_url())
            if "https://aternos.org/servers/" in current_url:
                log("Selecting Server")
                serverselector = "/html/body/div[2]/main/div/div[2]/section/div[1]/div/div[3]/div[2]/div[%s]/div[1]" % server_number
                driver.click(serverselector)
                log("Server No.%s Selected" %server_number)
                sleep(2)
                x = 1
                while x == 1:
                    try:
                        driver.click("/html/body/div[3]/main/section/div[3]/div[5]/div[1]")  # Start
                        log("D1-1 (Server Started)")
                    except Exception:
                        log("D1-2 (Server Launching Or Already Up)")
                    try:
                        driver.click("/html/body/dialog/header/span[2]/i")  # Ad
                        log("D2-1 (Ad Bypassed)")
                    except Exception:
                        log("D2-2 (Continuing...)")
                    try:
                        driver.click("/html/body/dialog/header/span[2]/i")  # Notification
                        log("D3-1 (Notification Bypassed)")
                    except Exception:
                        log("D3-2 (Continuing...)")
                    try:
                        driver.click("/html/body/dialog/main/div[2]/button[1]")  # EULA\
                        log("D4-1 (EULA Bypassed)")
                    except Exception:
                        log("D4-2 (Continuing...)")
                    try:
                        driver.click("/html/body/div[3]/main/section/div[3]/div[5]/div[5]")  # Confirm
                        log("D5-1 (Confirmed Startup)")
                    except Exception:
                        if driver.is_element_visible("/html/body/div[3]/main/section/div[3]/div[5]/div[2]"):
                            log("D5-* (Server Launching, Waiting In Queue, Or Already Up)")
                        else:
                            log("D5-2 (Server Launching, Waiting In Queue, Or Already Up)")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_profile():
    if os.path.exists(USERDATA_DIR):
        try:
            shutil.rmtree(USERDATA_DIR)
            messagebox.showinfo("Info", "Profile deleted")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete profile:\n{e}")
    else:
        messagebox.showinfo("Info", "No profile to delete")

def set_option(option):
    global selected_option, username, password
    selected_option = option
    if selected_option == "Bot":
        username = "BCDBootGuy1"
        password = "BCDBootGuy123"
    if selected_option == "Google":
        username = "Google"
        password = "Google"
    save_selected_option()
    messagebox.showinfo("Info", f"{selected_option} selected")
    if selected_option == "Login":
        open_login_window()

def open_login_window():
    def submit_credentials():
        global username, password
        username = username_entry.get()
        password = password_entry.get()
        save_credentials(username, password)
        login_window.destroy()
        messagebox.showinfo("Info", "Login credentials saved.")

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    login_window.geometry("300x175")

    tk.Label(login_window, text="Username").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)

    tk.Button(login_window, text="Submit", command=submit_credentials).pack(pady=10)

def setup_google_account():
    try:
        with Driver(uc=True, headless=False, user_data_dir=USERDATA_DIR) as driver:
            root.destroy()
            driver.get("https://accounts.google.com/ServiceLogin")
            driver.sleep(5)
            while True:
                current_url = driver.get_current_url()
                if "https://myaccount.google.com/?utm_source=sign_in_no_continue" in current_url:
                    driver.quit()
                    log("Google Login Successful, Restart The Script And Log In With Google")
                    break
                sleep(1)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to setup Google account:\n{e}")

def set_server_number():
    global server_number
    server_number = server_number_entry.get()
    if server_number == "":
        server_number = 1
    messagebox.showinfo("Info", f"Server number set to : {server_number}")

# GUI Setup
root = tk.Tk()
root.title("Aternos Automation")
root.geometry("300x350")

load_selected_option()

menu = tk.Menu(root)
root.config(menu=menu)

options_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Login Methods", menu=options_menu)
options_menu.add_command(label="USR/PSW", command=lambda: set_option("Login"))
options_menu.add_command(label="Google", command=lambda: set_option("Google"))
options_menu.add_command(label="Bot", command=lambda: set_option("Bot"))
options_menu.add_command(label="Setup Google Account", command=setup_google_account)

tk.Label(root, text="Server Number").pack(pady=5)
server_number_entry = tk.Entry(root)
server_number_entry.pack(pady=5)
tk.Button(root, text="Set Server Number", command=set_server_number).pack(pady=5)

tk.Button(root, text="Start", command=start).pack(fill='x', padx=20, pady=5)
tk.Button(root, text="Copy Profile", command=copy_profile).pack(fill='x', padx=20, pady=5)
tk.Button(root, text="Delete Profile", command=delete_profile).pack(fill='x', padx=20, pady=5)

# Kill any "uc_driver" processes after GUI loads
for proc in psutil.process_iter(['name']):
    if proc.info['name'] and "uc_driver" in proc.info['name'].lower():
        try:
            proc.kill()
            log(f"Killed uc_driver process: {proc.pid}")
        except Exception as e:
            log(f"Failed to kill uc_driver process {proc.pid}: {e}")

root.mainloop()


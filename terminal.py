import subprocess
import datetime
import signal
import os

timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_file = "/tmp/user-terminal.txt"

forbidden_combinations = ["\t", "ctrl+c", "ctrl+v", "ctrl+z"]
signal.signal(signal.SIGINT, lambda sig, frame: None)

while True:
    try:
        command = input(f"\033[92muser@\033[96mlocalhost\033[0m:{os.getcwd()}\033[92m#\033[0m ")
    except EOFError:
        command = ""
    with open(log_file, "a") as f:
        f.write(f"{timestamp} - command: {command}\n")
    if command == "exit":
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - session ended\n")
        break
    elif command.startswith("cd "):
        try:
            os.chdir(command[3:])
        except Exception as e:
            print(e)
    else:
        if all(comb not in command.lower() for comb in forbidden_combinations):
            try:
                child_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result, error = child_process.communicate()
                if error:
                    print("\033[91m" + error.decode() + "\033[0m")
                    with open(log_file, "a") as f:
                        f.write(f"{timestamp} - error: {error.decode()}")
                else:
                    print("\033[92m" + result.decode() + "\033[0m")
                    with open(log_file, "a") as f:
                        f.write(f"{timestamp} - result: {result.decode()}")
                if command.startswith("nano "):
                    subprocess.call(['nano',command[5:]])
            except Exception as e:
                print(e)
        else:
            print("Forbidden combination used. Please try again.")

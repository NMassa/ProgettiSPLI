from sys import executable
import subprocess
import os

import subprocess

cmd = subprocess.Popen(args=[
    "gnome-terminal hold -e '/bin/bash -c \"ls -al\"'"])



# from subprocess import check_output
# check_output("ls", shell=True).decode()

# p = subprocess.Popen('ls', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
# for line in p.stdout.readlines():
#     print(line)
# retval = p.wait()

#os.system('ls -al')
# from subprocess import Popen, CREATE_NEW_CONSOLE
#
# Popen('cmd', creationflags=CREATE_NEW_CONSOLE)
#
# input('Enter to exit from Python script...')


# import subprocess
# import shlex
# process = subprocess.Popen(
#     shlex.split("""x-terminal-emulator -e 'bash -c "test.py"'"""), stdout=subprocess.PIPE)
# process.wait()
# print(process.returncode)
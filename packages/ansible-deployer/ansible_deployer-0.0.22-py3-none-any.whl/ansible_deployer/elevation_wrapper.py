"""Main module wrapper for privilege elevation"""
import os
import sys

exe = os.path.join(os.environ["PATH"].split(":")[0], "python3")
pyexe = os.path.abspath("./ansible_deployer/command_line.py")
cmd = []
cmd.append(pyexe)
for arg in sys.argv:
    cmd.append(arg)

os.execvp('sudo', ['sudo', exe, *cmd])

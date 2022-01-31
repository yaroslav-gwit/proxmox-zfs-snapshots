#!/usr/bin/env python3
import typer
import sys
import os
import subprocess

command = "qm list"
command_output = subprocess.check_output(command, shell=True)

print(command_output)
#!/usr/bin/env python3
import typer
import sys
import os
import subprocess

command = "qm list"
command_output = subprocess.check_output(command, shell=True)
command_output = command_output.decode("utf-8").split("\r")

print(command_output)
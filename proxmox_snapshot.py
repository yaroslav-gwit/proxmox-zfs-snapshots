#!/usr/bin/env python3
import typer
import sys
import os
import subprocess
import datetime



class All:
    """This class creates a list of dicts of VMs"""
    def __init__(self, snapshot_type:str = "custom", snapshots_to_keep:int = 3, debug:bool=False):
        dev = debug
        if not dev:
            command = "qm list | tail -n +2"
            command_output = subprocess.check_output(command, shell=True)
            command_output = command_output.decode("utf-8").split("\n")
        else:
            """Example output for testing"""
            command_output = ['       107 haku12.icr.ac.uk     running    16384             50.00 1283519   ', '       118 haku04.icr.ac.uk     running    8500            1024.00 3267143   ', '']

        vm_list = []
        for item in command_output:
            if item:
                _line = item.split()
                vm_list.append(_line)
        
        for _vm in vm_list:
            if not dev:
                command = "qm listsnapshot " + _vm[0] + "| awk '{print $2}' | grep -Gv \"^current$\" | grep " + snapshot_type
                command_output = subprocess.check_output(command, shell=True)
                command_output = command_output.decode("utf-8").split()
            else:
                command_output = [ "rsnap_custom_20220131_1331", "rsnap_custom_20220131_1332", "rsnap_daily_20220131_1332", "rsnap_weekly_20220131_1332" ]
            if _vm:
                _vm.append(command_output)

        vm_dict_list = []
        for item in vm_list:
            _vm_dict = {}
            _vm_dict["vm_id"] = item[0]
            _vm_dict["vm_name"] = item[1]
            _vm_dict["vm_status"] = item[2]
            _vm_dict["vm_snapshots"] = item[-1]
            vm_dict_list.append(_vm_dict)

        snapshot_types = ["hourly","daily", "weekly", "monthly", "yearly", "custom"]
        if snapshot_type not in snapshot_types:
            print("Bad snapshot type!")
            sys.exit(1)
        snapshot_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_name = "rsnap_" + snapshot_type + "_" + snapshot_date

        # print(vm_dict_list)

        self.vm_dict_list = vm_dict_list
        self.snapshot_name = snapshot_name
        self.snapshots_to_keep = snapshots_to_keep

    def snapshot_all(self):
        snapshot_complete = []
        for _dict in self.vm_dict_list:
            snapshot_complete.append("qm snapshot " + _dict["vm_id"] + " " + self.snapshot_name)
        return snapshot_complete
    
    def remove_snapshot(self):
        snapshot_list = []
        for _dict in self.vm_dict_list:
            end_number = len(_dict["vm_snapshots"]) - self.snapshots_to_keep
            if self.snapshots_to_keep < len(_dict["vm_snapshots"]):
                for _snapshot in _dict["vm_snapshots"][0:end_number]:
                    snapshot_list.append("qm delsnapshot " + _dict["vm_id"] + " " + _snapshot)
        
        return snapshot_list


class Single:
    """This class is resonsible for single VM snapshot manipulations"""


app = typer.Typer(context_settings=dict(max_content_width=800))

@app.command()
def snapshot_all(take:bool=typer.Option(False, help="Generate, test and reload the config"),
        snapshot_type:str=typer.Option(False, help="Generate, test and reload the config"),
        debug:bool=typer.Option(False, help="Generate, test and reload the config"),
        snapshots_to_keep:int=typer.Option(3, help="Generate, test and reload the config"),
        ):

    '''
    Example: program
    '''
    for command in All(snapshot_type=snapshot_type, debug=debug, snapshots_to_keep=snapshots_to_keep).snapshot_all():
        print("Running: " + command)
        if not debug:
            subprocess.check_output(command, shell=True)
    
    for command in All(snapshot_type=snapshot_type, debug=debug, snapshots_to_keep=snapshots_to_keep).remove_snapshot():
        print("Running: " + command)
        if not debug:
            subprocess.check_output(command, shell=True)

@app.command()
def snapshot(vm_id:str=typer.Argument(False, help="Generate, test and reload the config"),
        ):

    '''
    Example: program
    '''

    if not vm_id:
        print("No VM_ID was provided!")
        sys.exit(1)
    else:
        print("Your VM_ID is: " + vm_id)

if __name__ == "__main__":
    app()
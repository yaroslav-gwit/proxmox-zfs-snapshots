#!/usr/bin/env python3
import typer
import sys
import os
import subprocess
import datetime



class All:
    """This class creates a list of dicts of VMs"""
    
    def __init__(self, exclude:str, snapshot_type:str = "custom", snapshots_to_keep:int = 3, running_vms_only:bool = False, debug:bool = False):
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
                command = "qm listsnapshot " + _vm[0] + "| awk '{print $2}' | grep -Gv \"^current$\" | grep _" + snapshot_type + "_ || true"
                command_output = subprocess.check_output(command, shell=True)
                command_output = command_output.decode("utf-8").split()
            else:
                command_output = [ "rsnap_custom_20220131_1331", "rsnap_custom_20220131_1332", "rsnap_daily_20220131_1332", "rsnap_weekly_20220131_1332" ]
            if _vm:
                _vm.append(command_output)

        vm_exclude_list = []
        if exclude:
            for i in (exclude.split(",")):
                vm_exclude_list.append(i)

        vm_dict_list = []
        for item in vm_list:
            if item[0] in vm_exclude_list:
                pass
            elif item[1] in vm_exclude_list:
                pass
            else:
                _vm_dict = {}
                _vm_dict["vm_id"] = item[0]
                _vm_dict["vm_name"] = item[1]
                _vm_dict["vm_status"] = item[2]
                _vm_dict["vm_snapshots"] = item[-1]

            if running_vms_only:
                if item[2] == "running":
                    vm_dict_list.append(_vm_dict)
            elif not running_vms_only:
                vm_dict_list.append(_vm_dict)


        snapshot_types = ["hourly","daily", "weekly", "monthly", "yearly", "custom"]
        if snapshot_type not in snapshot_types:
            print("Bad snapshot type!")
            sys.exit(1)
        snapshot_date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_name = "rsnap_" + snapshot_type + "_" + snapshot_date

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
    """This class will be resonsible for single VM snapshot manipulations"""



app = typer.Typer(context_settings=dict(max_content_width=800))


@app.command()
def snapshot_all(
        snapshot_type:str=typer.Option(..., help="Specify the snapshot type: hourly, daily, weekly, monthly, yearly or custom"),
        running_vms_only:bool=typer.Option(False, help="Only snapshot running VMs"),
        snapshots_to_keep:int=typer.Option(3, help="Specify a number of snapshots to keep"),
        debug:bool=typer.Option(False, help="Turn on debug mode (does not run 'qm' commands, only prints them on the screen)"),
        exclude:str=typer.Option(help="Exclude the VM from being backed up/snapshotted, coma separated, like so: 123,444,100"),
    ):
    
    """ Example: proxmox_snapshot snapshot-all --snapshot-type daily --snapshots-to-keep 5 --running-vms-only """

    for command in All(snapshot_type=snapshot_type, debug=debug, snapshots_to_keep=snapshots_to_keep, running_vms_only=running_vms_only, exclude=exclude).snapshot_all():
        print("Running: " + command)
        if not debug:
            subprocess.check_output(command, shell=True)
    
    for command in All(snapshot_type=snapshot_type, debug=debug, snapshots_to_keep=snapshots_to_keep).remove_snapshot():
        print("Running: " + command)
        if not debug:
            subprocess.check_output(command, shell=True)


@app.command()
def snapshot(
        vm_id:str=typer.Argument(..., help="Specify the VM ID"),
    ):

    """ WARNING! This function has not been implemented yet! """

    print("Your VM_ID is: " + vm_id)
    print("Sorry, this function has not been implemented yet")
    sys.exit(1)



if __name__ == "__main__":
    app()

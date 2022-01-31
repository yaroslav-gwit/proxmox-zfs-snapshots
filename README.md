## This is a small Python3 script created to deal with automatic Proxmox snapshots
### Installation:
Run this one liner to install the script:
```
curl https://raw.githubusercontent.com/yaroslav-gwit/proxmox-zfs-snapshots/main/proxmox_snapshot_installer.sh | bash 
```
To update the script run the installer again, or execute the command below:
```
bash /opt/proxmox-zfs-snapshots/proxmox_snapshot_updater.sh
```
### Running:
This will make a snapshot of every single VM on the current node, set the type to `daily` and will keep 5 snapshots of the snapshot type daily:
```
proxmox_snapshot snapshot-all --snapshot-type daily --snapshots-to-keep 5
```
By adding `--running-vms-only` flag, the script will only snapshot the running VMs:
```
proxmox_snapshot snapshot-all --snapshot-type daily --snapshots-to-keep 5 --running-vms-only
```

Example output:
```
root@proxmox-node-03:~# proxmox_snapshot snapshot-all --snapshot-type daily --snapshots-to-keep 5
Running: qm snapshot 107 rsnap_daily_20220131_190342
Running: qm snapshot 118 rsnap_daily_20220131_190342
Running: qm delsnapshot 107 rsnap_daily_20220131_164141
Running: qm delsnapshot 118 rsnap_daily_20220131_164141
```

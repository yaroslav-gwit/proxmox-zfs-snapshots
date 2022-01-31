#!/usr/bin/env bash
cd /opt/proxmox-zfs-snapshots
source bin/activate
python3 proxmox_snapshot.py $@
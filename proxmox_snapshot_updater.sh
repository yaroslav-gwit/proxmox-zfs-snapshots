#!/usr/bin/env bash
cd /opt/proxmox-zfs-snapshots
git pull
cat proxmox_snapshot.sh > /bin/proxmox_snapshot
chmod +x /bin/proxmox_snapshot

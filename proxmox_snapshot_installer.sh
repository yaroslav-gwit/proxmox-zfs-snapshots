#!/usr/bin/env bash
apt-get install -y python3 python3-venv python3-pip

cd /opt/
git clone https://github.com/yaroslav-gwit/proxmox-zfs-snapshots.git
cd /opt/proxmox-zfs-snapshots

python3 -m venv .
source bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

cat proxmox_snapshot.sh > /bin/proxmox_snapshot
chmod +x /bin/proxmox_snapshot

echo "The program was installed successfully!"
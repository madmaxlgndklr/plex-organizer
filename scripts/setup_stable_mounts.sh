#!/bin/bash
# Adds fstab entries for the three external NTFS drives so they always mount
# to /mnt/media2, /mnt/media3, /mnt/classic_who — independent of udisks2.
# x-gvfs-show makes them visible in Nautilus/GNOME file manager.
set -e

OPTS="defaults,nofail,uid=1000,gid=1000,umask=002,x-gvfs-show"

echo "=== Backing up /etc/fstab ==="
cp /etc/fstab /etc/fstab.backup.$(date +%Y%m%d%H%M%S)

echo "=== Creating stable mount points ==="
mkdir -p /mnt/media2 /mnt/media3 /mnt/classic_who

echo "=== Unmounting drives from udisks2 paths (if mounted) ==="
for path in \
  /media/madmaxlgndklr/media2  \
  /media/madmaxlgndklr/media21 \
  /media/madmaxlgndklr/media22 \
  /media/madmaxlgndklr/media23 \
  /media/madmaxlgndklr/media3  \
  /media/madmaxlgndklr/media31 \
  /media/madmaxlgndklr/media32 \
  /media/madmaxlgndklr/classic_who  \
  /media/madmaxlgndklr/classic_who2 \
  /mnt/media2 /mnt/media3 /mnt/classic_who; do
  if mountpoint -q "$path" 2>/dev/null; then
    umount "$path" && echo "  unmounted $path"
  fi
done

echo "=== Adding/updating fstab entries ==="
# Remove any existing entries for these UUIDs so we can re-add with correct options
sed -i '/C444E98344E97916/d' /etc/fstab
sed -i '/421AF6B91AF6A955/d' /etc/fstab
sed -i '/7C4EB7724EB72434/d' /etc/fstab

cat >> /etc/fstab << EOF
UUID=C444E98344E97916  /mnt/media2       ntfs-3g  $OPTS  0  0
UUID=421AF6B91AF6A955  /mnt/media3       ntfs-3g  $OPTS  0  0
UUID=7C4EB7724EB72434  /mnt/classic_who  ntfs-3g  $OPTS  0  0
EOF

echo "=== Mounting via fstab ==="
mount -a

echo ""
echo "=== Verification ==="
for p in /mnt/media2 /mnt/media3 /mnt/classic_who; do
  if mountpoint -q "$p"; then
    echo "  OK  $p"
    ls "$p" | head -2
  else
    echo "  FAIL  $p — not mounted (drive may not be connected)"
  fi
done

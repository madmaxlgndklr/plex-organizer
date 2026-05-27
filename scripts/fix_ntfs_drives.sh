#!/bin/bash
# Recovery script for NTFS drives that show up but fail to mount due to a dirty bit.
# For each drive: attempts mount → on failure runs ntfsfix -d → retries mount.
# Run with: sudo bash fix_ntfs_drives.sh

declare -A DRIVES=(
  ["C444E98344E97916"]="/mnt/media2"
  ["421AF6B91AF6A955"]="/mnt/media3"
  ["7C4EB7724EB72434"]="/mnt/classic_who"
)

any_failed=0

for uuid in "${!DRIVES[@]}"; do
  mnt="${DRIVES[$uuid]}"
  label=$(basename "$mnt")

  # Resolve UUID to device path
  dev=$(blkid -l -t UUID="$uuid" -o device 2>/dev/null)
  if [ -z "$dev" ]; then
    echo "  SKIP  $label — drive not connected (UUID $uuid not found)"
    continue
  fi

  echo "=== $label ($dev) ==="

  if mountpoint -q "$mnt"; then
    echo "  OK  already mounted at $mnt"
    continue
  fi

  # First mount attempt
  mkdir -p "$mnt"
  if mount "$mnt" 2>/dev/null; then
    echo "  OK  mounted at $mnt"
    continue
  fi

  # Mount failed — run ntfsfix to clear dirty bit
  echo "  WARN  mount failed, running ntfsfix -d on $dev"
  if ! ntfsfix -d "$dev"; then
    echo "  ERROR  ntfsfix failed on $dev"
    any_failed=1
    continue
  fi

  # Retry mount
  if mount "$mnt"; then
    echo "  OK  mounted at $mnt after ntfsfix"
  else
    echo "  ERROR  still can't mount $mnt after ntfsfix — may need chkdsk on Windows"
    any_failed=1
  fi
done

echo ""
echo "=== Summary ==="
for uuid in "${!DRIVES[@]}"; do
  mnt="${DRIVES[$uuid]}"
  if mountpoint -q "$mnt"; then
    echo "  OK  $mnt"
  else
    dev=$(blkid -l -t UUID="$uuid" -o device 2>/dev/null)
    [ -z "$dev" ] && echo "  --  $mnt (not connected)" || echo "  FAIL  $mnt"
  fi
done

exit $any_failed

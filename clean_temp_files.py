from datetime import datetime, timedelta
import os
import sys


def cleanup_directory(target_dir, days_old=7, dry_run=True):
  """Scans a directory and removes files older than a specified number of days."""
  if not os.path.exists(target_dir):
    print(f"[ERROR] Directory not found: {target_dir}")
    return

  cutoff_date = datetime.now() - timedelta(days=days_old)
  print(f"[SCAN] Scanning: {target_dir}")
  print(f"[SCAN] Threshold: Files modified before {cutoff_date.date()}")
  print(f"[MODE] Dry Run: {'ENABLED (No files will be deleted)' if dry_run else 'DISABLED (Files will be permanently removed)'}\n")

  deleted_count = 0
  freed_bytes = 0

  for root, _, files in os.walk(target_dir):
    for filename in files:
      file_path = os.path.join(root, filename)
      try:
        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
        file_size = os.path.getsize(file_path)

        if file_mtime < cutoff_date:
          if dry_run:
            print(f"[WOULD DELETE] {file_path} ({file_size} bytes)")
          else:
            os.remove(file_path)
            print(f"[DELETED] {file_path}")

          deleted_count += 1
          freed_bytes += file_size
      except PermissionError:
        print(f"[SKIP] Permission denied: {file_path}")
      except Exception as e:
        print(f"[SKIP] Could not process {file_path}: {e}")

  freed_kb = freed_bytes / 1024
  print(
      f"\n[SUMMARY] Found {deleted_count} candidate file(s), total size:"
      f" {freed_kb:.2f} KB."
  )


if __name__ == "__main__":
  # Change '.' to any directory path you want to test
  # Set dry_run=False when you actually want files removed
  test_directory = "."
  cleanup_directory(test_directory, days_old=7, dry_run=True)

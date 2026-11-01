import os
import shutil
import sys


def check_disk_usage(disk_path="/"):
  """Check total, used, and free disk space."""
  total, used, free = shutil.disk_usage(disk_path)
  free_gb = free // (2**30)
  total_gb = total // (2**30)
  used_percent = (used / total) * 100

  print(f"[DISK] Path: {disk_path}")
  print(f"       Used: {used_percent:.1f}% ({free_gb} GB free of {total_gb} GB)")
  return used_percent < 85


def check_network_host(host="8.8.8.8"):
  """Ping Google DNS (8.8.8.8) to verify network connectivity."""
  param = "-n 1" if sys.platform.lower().startswith("win") else "-c 1"
  command = f"ping {param} {host} > {'nul' if sys.platform.lower().startswith('win') else '/dev/null'} 2>&1"
  response = os.system(command)

  status = "ONLINE" if response == 0 else "OFFLINE"
  print(f"[NET]  Gateway check ({host}): {status}")
  return response == 0


if __name__ == "__main__":
  print("--- System Health Report ---")
  disk_ok = check_disk_usage()
  net_ok = check_network_host()

  if disk_ok and net_ok:
    print("[STATUS] System is healthy.")
  else:
    print("[STATUS] Warning: System resource or network issues detected.")

import time
from scanner import run_daily_scan

while True:
    run_daily_scan()
    print("Daily scan complete")
    time.sleep(86400)  # 24 hours

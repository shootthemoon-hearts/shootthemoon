import sched
import time
import threading

scheduler = sched.scheduler(time.time, time.sleep)

def run_thread_forever():
    global scheduler
    while True:
        scheduler.run()

threading.Thread(target=run_thread_forever, name="game_sched", daemon=True).start()
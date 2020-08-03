from threading import Timer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from simpy import Event

class WatchDogTimer:
    def __init__(self, ttimeout, eevent):  # timeout in seconds
        self.timeout = ttimeout
        self.event = eevent
        self.timer = Timer(self.timeout, self.alarm)
        self.timer.start()

    def alarm(self):
        self.event.succeed()

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.timeout, self.alarm)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def defaultHandler(self):
        raise self



class ModificationHandler(FileSystemEventHandler):
    def __init__(self,wdt,logname):
        super().__init__()
        self.filename = logname
        self.timer = wdt

    def on_modified(self, event):
        if event.src_path.endswith(self.filename):
            self.timer.reset()



class WatchDog():
    def __init__(self,logname,timeout,enviro):
        self.terminating = Event(enviro)
        w = WatchDogTimer(timeout,self.terminating)
        event_handler = ModificationHandler(w,logname)
        self.observer = Observer()
        self.observer.schedule(event_handler, path='.', recursive=False)
        self.observer.start()

    def getObserver(self):
        return self.observer

    def getTrigger(self):
        return self.terminating

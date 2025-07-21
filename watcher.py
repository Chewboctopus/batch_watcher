import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .processor import process_files

WATCHED_FOLDERS = ["/path/to/watch1", "/path/to/watch2"]

class BatchHandler(FileSystemEventHandler):
    def __init__(self):
        self.queue = set()
        self.last_event_time = time.time()

    def on_created(self, event):
        if not event.is_directory:
            self.queue.add(event.src_path)
            self.last_event_time = time.time()

    def on_modified(self, event):
        if not event.is_directory:
            self.queue.add(event.src_path)
            self.last_event_time = time.time()

def start_watching():
    handler = BatchHandler()
    observer = Observer()
    for folder in WATCHED_FOLDERS:
        observer.schedule(handler, folder, recursive=False)
    observer.start()
    print("Watching folders:", WATCHED_FOLDERS)
    try:
        while True:
            # Batch process every 10 seconds if files are present and no new events for 5 seconds
            if handler.queue and (time.time() - handler.last_event_time > 5):
                files = list(handler.queue)
                handler.queue.clear()
                process_files(files)
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

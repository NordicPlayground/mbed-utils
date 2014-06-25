import time
import sys
import os
import ntpath
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler
from win32com.shell import shell, shellcon

class FilecopyHandler(PatternMatchingEventHandler):
    patterns = ['*.hex']
    drive = None

    def on_modified(self, event):
        _, filename = ntpath.split(event.src_path)

        print event.src_path, event.event_type
        
        dest = self.drive + '\\' + filename
        shell.SHFileOperation(
            (0, shellcon.FO_COPY, event.src_path, dest, shellcon.FOF_NOCONFIRMATION, None, None)
        )

        if os.path.isfile(dest):
            print 'Success'
            try:
                os.remove(path + '/' + filename)
            except:
                pass


if __name__ == '__main__':
    args = sys.argv[1:]
    path = args[0] if args else '.'
    drive = args[1] if len(args) > 1 else 'E:'

    handler=FilecopyHandler()
    handler.drive = drive
    observer = Observer()
    observer.schedule(handler, path=path)
    observer.start()

    print 'Watching folder', path, 'copying to', drive

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

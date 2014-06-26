import time
import sys
import os
import ntpath
import datetime
import colorama
from termcolor import colored
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler
from win32com.shell import shell, shellcon

def log(*args):
    print '[%s]' % datetime.datetime.now(),
    for arg in args:
        print arg,
    print

class FilecopyHandler(PatternMatchingEventHandler):
    patterns = ['*.hex']
    drive = None

    def on_modified(self, event):
        _, filename = ntpath.split(event.src_path)

        log(colored('Flashing %s...' % filename, 'cyan'))
        
        dest = self.drive + '\\' + filename
        shell.SHFileOperation(
            (0, shellcon.FO_COPY, event.src_path, dest, shellcon.FOF_NOCONFIRMATION, None, None)
        )

        if os.path.isfile(dest):
            log(colored('Success', 'green'))
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

    colorama.init()

    print colored('Watching folder', 'cyan'),
    print colored(path, 'yellow'),
    print colored('copying to', 'cyan'),
    print colored(drive, 'yellow')

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

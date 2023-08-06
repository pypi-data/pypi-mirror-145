import argparse
import contextlib
import django
import getpass
import multiprocessing as mp
import os
import pathlib
import rumps
import signal
import subprocess
import webbrowser

from django.core.management import call_command

PROCESS_IDS = []


class App(rumps.App):
    @rumps.clicked('Emma')
    def emma(self, _):
        webbrowser.open('http://127.0.0.1:15050')

    @rumps.clicked('Quit')
    def quit(self, _):
        for pid in PROCESS_IDS:
            os.kill(pid, signal.SIGTERM)
        rumps.quit_application()


def run():
    record_proc = mp.Process(target=call_command, args=['record'])
    record_proc.start()
    PROCESS_IDS.append(record_proc.pid)
    runserver_args = ['runserver', '--noreload', '15050']
    runserver_proc = mp.Process(target=call_command, args=runserver_args)
    runserver_proc.start()
    PROCESS_IDS.append(runserver_proc.pid)
    app = App('E', quit_button=None)
    app.run()


def load():
    plist_path = pathlib.Path(__file__).parent / 'emma.daemon.plist'
    with plist_path.open() as reader:
        template = reader.read()
    launch_path = pathlib.Path('~/Library/LaunchAgents/emma.daemon.plist')
    launch_path = launch_path.expanduser()
    with launch_path.open('w') as writer:
        text = template.format(user=getpass.getuser())
        writer.write(text)
    subprocess.run(['launchctl', 'load', str(launch_path)])


def unload():
    launch_path = pathlib.Path('~/Library/LaunchAgents/emma.daemon.plist')
    launch_path = launch_path.expanduser()
    subprocess.run(['launchctl', 'unload', str(launch_path)])
    with contextlib.suppress(FileNotFoundError):
        launch_path.unlink()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'command',
        nargs='?',
        choices=['', 'load', 'unload', 'reload'],
    )
    args = parser.parse_args()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emma.settings')
    django.setup()

    call_command('migrate', '--verbosity', '0')

    if args.command is None:
        run()
    elif args.command == 'load':
        load()
    elif args.command == 'unload':
        unload()
    elif args.command == 'reload':
        unload()
        load()


if __name__ == '__main__':
    main()

import argparse
import app.config


def prompt_video_id() -> str:
    answer: str = input('Video ID: ')
    return answer.strip('v')


def prompt_client_id():
    print('Twitch requires a client ID to use their API.'
          '\nRegister an application on https://dev.twitch.tv/dashboard to get yours.')
    app.config.settings['client_id'] = input('Client ID: ')
    answer: str = input('Save client ID? (Y/n): ')
    if answer.lower() != "n":
        app.config.save(app.config.SETTINGS_FILE, app.config.settings)


parser: argparse.ArgumentParser = argparse.ArgumentParser(description='Twitch Chat Downloader v{version}'.format(version=app.config.settings['version']))
parser.add_argument('-v', '--video', type=str, help='Video id')
parser.add_argument('--client_id', type=str, help='Twitch client id', default=None)
parser.add_argument('--verbose', action='store_true', help='Print chat lines')
parser.add_argument('-q', '--quiet', action='store_true')
parser.add_argument('-o', '--output', type=str, help='Output folder', default='./output')
parser.add_argument('-f', '--format', type=str, help='Message format', default='default')
# parser.add_argument('--start', type=int, help='Start time in seconds from video start')
# parser.add_argument('--stop', type=int, help='Stop time in seconds from video start')
parser.add_argument('--timezone', type=str, help='Timezone name', default=None)
parser.add_argument('--init', action='store_true', help='Script setup')
parser.add_argument('--update', action='store_true', help='Update settings')
parser.add_argument('--version', action='store_true', help='Settings version')
parser.add_argument('--formats', action='store_true', help='List available formats')

arguments = parser.parse_args()

# Fix format
arguments.format = str(arguments.format).lower()

# Initialize
if arguments.init:
    prompt_client_id()
    exit(1)

# Update
if arguments.update:
    exit(1)

# Version
if arguments.version:
    print('Twitch Chat Downloader v{version}'.format(version=str(app.config.settings['version'])))
    exit(1)

if arguments.formats:
    for format_name in app.config.settings['formats']:
        print(format_name)
        _format = app.config.settings['formats'][format_name]
        if 'comments' in _format:
            print('\tcomment: {}'.format(app.config.settings['formats'][format_name]['comments']['format']))
        if 'output' in _format:
            print('\toutput: {}'.format(app.config.settings['formats'][format_name]['output']['format']))
        print('\n')

    exit(1)

# Video ID
if arguments.video is None:
    arguments.video = prompt_video_id()

# Client ID
if app.config.settings['client_id'] is None and arguments.client_id is None:
    prompt_client_id()

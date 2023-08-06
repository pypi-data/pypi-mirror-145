""" Checks PyPi for version updates """
import sys
import textwrap
import time
from datetime import datetime, timedelta
from typing import Tuple

import requests

from mcli import config, version
from mcli.config import MCLIConfig


def get_latest_mcli_version() -> Tuple[int, int, int]:
    r = requests.get('https://pypi.org/pypi/mosaicml-cli/json').json()
    version_number = r.get('info', {}).get('version', None)
    major, minor, patch = version_number.split('.')
    return int(major), int(minor), int(patch)


def check_new_update_available() -> None:
    try:
        conf = MCLIConfig.load_config()
    except Exception:  # pylint: disable=broad-except
        return
    last_update_time_days = (datetime.now() - conf.last_update_check).total_seconds() / (60 * 60 * 24)
    if last_update_time_days < config.UPDATE_CHECK_FREQUENCY_DAYS or conf.dev_mode:
        if conf.dev_mode:
            print('DEV: Skipping update check')
        # Skipping check
        return

    print('Checking for new MCLI updates')
    major, minor, patch = get_latest_mcli_version()
    conf.last_update_check = datetime.now()

    if major != version.__version_major__ or minor != version.__version_minor__ or patch != version.__version_patch__:
        print('New Version of MCLI detected\n')
        print('-' * 30)
        print(f'Local version: \t\t{version.__version__}')
        print(f'Most Recent version: \tv{major}.{minor}.{patch}')
        print('-' * 30 + '\n')
    else:
        print('MCLI Version up to date!\n')

    version_update_required_message = textwrap.dedent("""
    Please update your mcli version to continue using mcli
    To do so, run:

    pip install --upgrade mosaicml-cli
    """)
    if major != version.__version_major__:
        print('Major version out of sync.')
        print(version_update_required_message)
        sys.exit(1)

    if minor != version.__version_minor__:
        print('Minor version out of sync.')
        print(version_update_required_message)
        sys.exit(1)

    if patch - version.__version_patch__ >= 2:
        print('Patch version >= 2 versions out of date.')
        print(version_update_required_message)
        sys.exit(1)

    if patch != version.__version_patch__:
        print('Patch version out of date.')
        print(
            textwrap.dedent("""
        You can continue, but we recommend updating mcli ASAP
        This message will reset every hour

        To update mcli run:

        pip install --upgrade mosaicml-cli

        Ctrl-c to exit and update now
        """))
        time.sleep(10)
        conf.last_update_check = datetime.now() - timedelta(days=config.UPDATE_CHECK_FREQUENCY_DAYS, minutes=-60)

    conf.save_config()

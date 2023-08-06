""" Add Composer Model """
import argparse
import shutil
import sys
from pathlib import Path
from typing import Optional

import composer

from mcli.sweeps.config_backend import MCLIConfigBackend

COMPOSER_YAML_DIR = Path(composer.__file__).parents[0].joinpath('yamls')
controller = MCLIConfigBackend()


def main(model: str,
         composer_dir: Path,
         hektar_dir: Path,
         instance_model: Optional[str] = None,
         overwrite: bool = False):
    orig = composer_dir.joinpath('models', f'{model}.yaml')
    if not orig.exists():
        raise ValueError(f'No model named {model} in local composer')
    defaults_dest = hektar_dir.joinpath('defaults', 'models', f'{model}.yaml')
    specific_dest_dir = hektar_dir.joinpath('model-specific', model)

    if defaults_dest.exists() and not overwrite:
        print(f'Defaults yaml for {model} already exists.')
    else:
        print(f'Copying yaml from {orig} to {defaults_dest}')
        shutil.copy2(orig, defaults_dest)
        print('Done.')
    specific_dest_dir.mkdir(exist_ok=True)
    specific_dest_dir.joinpath('instances').mkdir(exist_ok=True)
    if instance_model is not None:
        instance_ref = hektar_dir.joinpath('model-specific', instance_model, 'instances')
        if not instance_ref.exists():
            raise ValueError(f'No model named {instance_model} to use as reference for instance configs.')
        for instance_file in instance_ref.iterdir():
            dest = specific_dest_dir.joinpath('instances', instance_file.name)
            if not dest.exists() or overwrite:
                print(f'Copying yaml from {instance_file} to {dest}')
                shutil.copyfile(instance_file, dest)
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser('add_composer_model', description='Add a model from local composer')
    parser.add_argument('model', help='Name of the model')
    parser.add_argument('--instances-from', help='Name of a model to copy instance configs from')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite yaml if it exists')
    args = parser.parse_args()

    # pylint: disable-next=protected-access
    sys.exit(main(args.model, COMPOSER_YAML_DIR, controller._root, args.instances_from, args.overwrite))

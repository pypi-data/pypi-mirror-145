""" Compare Composer Configs """
from pathlib import Path
from textwrap import indent as indent_text

import composer
import yaml

from mcli.sweeps.config_backend import MCLIConfigBackend
from mcli.utils.utils_wandb import get_diff

COMPOSER_YAML_DIR = Path(composer.__file__).parents[0].joinpath('yamls')
controller = MCLIConfigBackend()

models = [f.name for f in COMPOSER_YAML_DIR.joinpath('models').iterdir() if f.is_file() and f.suffix == '.yaml']


def dump_diff_str(diff_data, indent=2, start_indent=0):

    def get_line(s, start_symbol, indent):
        return indent_text(indent_text(s, ' ' * indent), start_symbol)

    lines = []
    for k, v in diff_data.items():
        if isinstance(v, tuple):
            p, m = v
            if p != 'UNSPECIFIED':
                s = yaml.safe_dump({k: p}).rstrip()
                lines.append(get_line(s, '+', start_indent))
            if m != 'UNSPECIFIED':
                s = yaml.safe_dump({k: m}).rstrip()
                lines.append(get_line(s, '-', start_indent))
        elif isinstance(v, dict):
            lines.append(get_line(f'{k}:', ' ', start_indent))
            lines.extend(dump_diff_str(v, indent, start_indent + indent).splitlines())
    return '\n'.join(lines)


differences = []
missing = []
for f in COMPOSER_YAML_DIR.joinpath('models').iterdir():
    if not (f.is_file() and f.suffix == '.yaml'):
        continue
    model = f.stem
    hektar_config = controller.get_model_config(model)
    if hektar_config:
        with open(f, 'r', encoding='utf8') as fh:
            config1 = yaml.safe_load(fh)
        diff = get_diff(hektar_config, config1)
        if diff:
            differences.append((model, diff))
            print(f'Model {model} had differences: ')
            print(dump_diff_str(diff, indent=4))
        else:
            print(f'Model {model} was the same')
    else:
        print(f'Missing model {model}')
        missing.append(str(f.name))
    print('')

differences = []
missing = []
known_algos = controller.list_algorithms()
for f in COMPOSER_YAML_DIR.joinpath('algorithms').iterdir():
    if not (f.is_file() and f.suffix == '.yaml'):
        continue
    algo = f.stem
    with open(f, 'r', encoding='utf8') as fh:
        config1 = yaml.safe_load(fh)

    if algo not in known_algos:
        print(f'Missing algorithm {algo}')
        missing.append(str(f.name))
        continue

    hektar_config = controller.get_algorithm_config(algo)
    diff = get_diff(hektar_config, config1)
    if diff:
        differences.append((algo, diff))
        print(f'Algorithm {algo} had differences: ')
        print(dump_diff_str(diff, indent=4))
    else:
        print(f'Algorithm {algo} was the same')
    print('')

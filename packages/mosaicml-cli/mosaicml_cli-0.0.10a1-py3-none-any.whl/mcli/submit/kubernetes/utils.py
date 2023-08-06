""" Kubernetes Utils """
import logging
import random
import uuid

import coolname

# logging.basicConfig()
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


def generate_uuid(nchars: int = 5):
    short_uuid = str(uuid.uuid4().hex[:nchars])
    return short_uuid


# TODO(Niklas): Should be used by MCLIJob
def sanitize_name(name: str):
    """ Sanitize name for kubernetes """
    name = name.replace('_', '-')
    name = name.lower()
    return name[:63].strip('-')


# TODO: wordlist generator that limits lengths
def generate_coolname(n=2):
    if n >= 2:
        slug = coolname.generate_slug(n)
        if random.random() < 0.05:
            slug = slug.split('-')
            slug[1] = random.choice(['dogecoin', 'bitcoin', 'ethereum', 'cryptocurrency'])
            return '-'.join(slug)
        else:
            return slug
    elif n == 1:
        choices = coolname.generate(4)
        choices = [c for c in choices if c not in ('of', 'from')]
        return random.choice(choices)
    else:
        raise ValueError(f'Invalid n: {n}')

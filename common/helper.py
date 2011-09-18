"""
Miscellaneous helper/convenience functions.
"""

import glob
import os
import re
import sys

from compressed import unzip

def file_exists(path, files):
    for _file in files:
        if os.path.exists(os.path.join(path, _file)):
            return True

    return False

def htime(time):
    """Returns a human readable time."""
    seconds = time % 60
    minutes = time / 60
    if minutes >= 60:
        hours = minutes/60
        minutes = minutes % 60
        fmt = '%dh %dm %ds' % (hours, minutes, seconds)
    elif minutes >= 1:
        fmt = '%dm %ds' % (minutes, seconds)
    else:
        fmt = '%ds' % seconds
        
    return fmt

def get_nzb_file(path):
    """Returns a nzb file or files for given a path."""
    if isinstance(path, str):
        if path.lower().endswith('.zip'):
            return unzip(path)
        elif os.path.isdir(path):
            nzb_files = glob.glob(os.path.join(path, '*.nzb'))
            return nzb_files
        return path
    elif isinstance(path, list):
        files = []
        for f in path:
            files += get_nzb_file(f)
        return files
    else:
        return [path]

def get_download_path(base_path, new_dir):
    """Returns a full path from combining base_path and new_dir."""
    new_dir = os.path.split(new_dir)[1]
    new_dir = new_dir.rstrip('.nzb')

    return os.path.join(base_path, new_dir)

SUBJECT_RE = re.compile('(?:"|&quot|&quot;)([\.\w\[\]\ \(\)\+]+\.\w+)')
SUBJECT_RE_FAILOVER = re.compile('(?:\s*)([\.\w\[\]\ \(\)\+]+\.\w+)')

def get_filename_from(subject):
    """Return a filename from a subject."""
    # Using two regular expressions becaause including the space in the positive
    # lookahead matches the wrong target in some subjects.
    res = SUBJECT_RE.search(subject)
    if res:
        return res.groups()

    return SUBJECT_RE_FAILOVER.findall(subject) or ''

def get_size(size, suffix_only=False):
    """Return a human readble size."""
    hs = ('KB', 'MB', 'GB', 'TB')
    hsize = int(size) / 1024.0
    for suffix in hs:
        if hsize / 1024.0 > 1:
            hsize /= 1024.0
        elif suffix_only:
            return suffix
        else:
            if hsize > 1:
                return '%s %s' % (format(hsize, '3.1f'), suffix)
            else:
                return '%s %s' % (format(hsize, '3.2f'), suffix)
    return ''

def print_static(string, width=80):
    sys.stdout.write('\r%s%s' % (string, ' ' * (width-len(string))))
    sys.stdout.flush()

def re_filter(skip_regex, invert=False):
    patterns = []
    for regex in skip_regex:
        patterns.append(re.compile(regex, re.I))
    def _re_filter(subject):
        for pattern in patterns:
            if pattern.search(subject):
                return True is not invert
        return False is not invert
    return _re_filter

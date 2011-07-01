"""
Miscellaneous helper/convenience functions.
"""
import glob
import os
import re
import sys
from compressed import unzip

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
    if path.lower().endswith('.zip'):
        return unzip(path)
    elif os.path.isdir(path):
        nzb_files = glob.glob(os.path.join(path, '*.nzb'))
        return nzb_files
    else:
        return [path]

def get_download_path(base_path, new_dir):
    """Returns a full path from combining base_path and new_dir."""
    new_dir = os.path.split(new_dir)[1]
    new_dir = new_dir.rstrip('.nzb')

    return os.path.join(base_path, new_dir)

def get_filename_from(subject):
    """Return a filename from a subject."""
    # # Use multiple regexs because I can't figure one that works.
    res = re.match('.*?(?:"|&quot|&quot;|\s*)([\.0-9A-Za-z\[\]_\ \(\)]+\.\w+).*', subject)
    if res:
        return res.groups()[0]

    return ''

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

if __name__ == '__main__':
    print get_filename_from("""New subject name "Filename goes here (v5.0) (echo).rar" (1/3)""")
    print get_filename_from("""[U4A] 150411-22:59:42[01/26] - &quot;150411-22:59:42.par2&quot; yEnc (1/1)""")

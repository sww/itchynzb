#
import json
from os.path import exists

def read_config(config='settings.conf'):
    if not exists(config):
        raise IOError('Could not find settings file %s.' % config)
    
    try:
        settings = json.loads(open(config).read())
    except ValueError:
        raise
    finally:
        return settings

if __name__ == '__main__':
    import sys
    
    print read_config(sys.argv[1])

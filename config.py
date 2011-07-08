import json

def read_config(config='settings.conf'):
    with open(config) as cfg:
        settings = json.loads(cfg.read())

    keys = [
        'host',
        'username',
        'password',
        'port',
        'connections',
        'download_dir',
        'temp_dir',
        'skip_regex'
    ]

    # Enforce that the config has the right set of keys.
    for key in keys:
        if key not in settings:
            raise KeyError('Config does not have key "%s"' % key)

    return settings

if __name__ == '__main__':
    import sys
    
    print read_config(sys.argv[1])

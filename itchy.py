#!/usr/bin/python

"""ItchyNZB"""

import os

from optparse import OptionParser

import common.helper as helper
import config
import download

def main(nzb_files, options):
    if not nzb_files:
        parser.print_help()
        return

    settings = config.read_config(options.config_file)
    if not settings:
        print '%s has no settings!' % options.config_file
        return

    if options.debug:
        settings['debug'] = options.debug
        print settings

    if options.pattern:
        settings['skip_regex'] = options.pattern
        settings['invert'] = True
    elif options.par2:
        settings['skip_regex'] = ['\.par2']
        settings['invert'] = True

    nzbs = [nzb for nzb in helper.get_nzb_file(nzb_files)]
    for nzb in nzbs:
        nzb_name = os.path.split(nzb)[1]
        new_dir = helper.get_download_path(settings.get('download_dir'), nzb_name)
        settings['download_path'] = new_dir
        if not os.path.exists(new_dir):
            if settings.get('debug'):
                print 'made new dir %s ' % new_dir
            os.mkdir(new_dir)

        if settings.get('debug'):
            print settings['download_path']

        download.start(nzb, settings)

if __name__ == '__main__':
    parser = OptionParser(usage='usage: %prog [options] nzb1 nzb2 ...')

    parser.add_option('-c', '--config', dest='config_file', help='Use config FILE.',
                      default='settings.json', metavar='FILE')
    parser.add_option('--debug', dest='debug', action='store_true',
                      help='Print debug information', default=False)
    parser.add_option('-p', '--par2', action='store_true', dest='par2',
                      help='Downloads parity files only.', default=False)
    parser.add_option('-g', '--pattern', dest='pattern', help='Get files only matching PATTERN',
                      metavar='PATTERN')

    (options, nzb_files) = parser.parse_args()

    main(nzb_files, options)

#
"""
hll wrld
"""
import os
import common.helper as helper

from optparse import OptionParser
from config import read_config
from download import start
#from postprocess import postprocess

def main():
    parser = OptionParser(usage='usage: %prog [options] nzb1 nzb2 ...')

    parser.add_option('-c', '--config', dest='config_file', help='Use config FILE.',
                      default='settings.conf', metavar='FILE')
    parser.add_option('-d', '--debug', dest='debug', action='store_true',
                      help='Print debug information', default=False)
    parser.add_option('-p', '--par2', action='store_true', dest='par2',
                      help='Downloads parity files only.', default=False)
    parser.add_option('-g', '--get', dest='get', help='Get files only matching PATTERN',
                      metavar='PATTERN')
    
    (options, nzb_files) = parser.parse_args()

    if len(nzb_files) == 0:
        parser.print_help()
        return

    # Read config.
    settings = read_config(options.config_file)
    
    if not settings:
        print '%s has no settings!' % options.config_file
        return

    if options.debug:
        settings['debug'] = options.debug
        print settings
    if options.par2:
        settings['par2'] = options.par2
        settings['skip_regex'] = []

    nzbs = []
    
    for nzb in nzb_files:
        nzb = helper.get_nzb_file(nzb)
        nzbs += nzb
        
    for nzb in nzbs:
        # TODO: strip out characters...
        nzb_name = os.path.split(nzb)[1]
        new_dir = helper.get_download_path(settings['download_path'], nzb_name)

        settings['download_path'] = new_dir

        if not os.path.exists(new_dir):
            #print 'made new dir %s ' % new_dir
            os.mkdir(new_dir)
            
        #print settings['download_path']
        start(nzb, settings)

        # if settings['delete_nzb_when_done']:
        #     if settings['debug']:
        #         print '[DEBUG] removing %s' % nzb
                
        #     os.remove(nzb)

if __name__ == '__main__':
    main()

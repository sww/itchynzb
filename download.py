import collections
import os.path
import subprocess
import common.helper as helper
from datetime import datetime
from time import time
from eventlet import greenthread, sleep, tpool
from eventlet.greenpool import GreenPool
from eventlet.queue import Queue
from decode import Decode
from nntp import NNTP
from parser import parse_nzb

COMPLETE_CHAR = '='

# class Tracker(object):

#     total_size = 0
#     downloaded = 0
Tracker = collections.namedtuple('Tracker', 'total_size, downloaded')

class DownloadPool(object):

    def __init__(self, settings):
        self.temp_dir = settings['temp_dir']
        self.download_path = settings['download_path']
        self.connection_pool = Queue(settings['connections'])

        for _ in xrange(settings['connections']):
            self.connection_pool.put(NNTP(settings['host'], settings['port'], settings['username'], settings['password']))

    def download(self, segment):
        #print 'getting', segment['segment']
        # Get an availble connection; if there are none, block until available.
        connection = self.connection_pool.get()
        segment_path = connection.get_body(segment['segment'], self.temp_dir)
        # Connection is done, put it back in the ready queue.
        self.connection_pool.put(connection)
        #print 'got', segment_path
        Tracker.downloaded += segment['segment_bytes']
        #print Tracker.downloaded
        return segment_path

def show_progress():
    start = time()
    p = subprocess.Popen(['stty size'], shell=True, stdout=subprocess.PIPE)
    length, width = (int(i) for i in p.stdout.read().strip().split())
    progress_bar_length = int(width * 0.5)
    p.stdout.close()
    eta = 0
    speed = 0

    while Tracker.downloaded < Tracker.total_size:
        # Get terminal dimensions.
        p = subprocess.Popen(['stty size'], shell=True, stdout=subprocess.PIPE)
        length, width = (int(i) for i in p.stdout.read().strip().split())
        progress_bar_length = int(width * 0.5)
        p.stdout.close()

        speed = (Tracker.downloaded/1024.0)/(time() - start)
        percentage = (Tracker.downloaded / float(Tracker.total_size)) * 100.0
        # Progress bar output.
        progress = COMPLETE_CHAR * int(percentage * progress_bar_length/100.0)
        # Pad progress bar.
        progress = progress.ljust(progress_bar_length, ' ')

        if speed > 0:
            eta = (Tracker.total_size - Tracker.downloaded) / (speed * 1024)
        else:
            speed = 0
            
        helper.print_static(' %s%% [%s] %s KB/s' % (percentage, progress, speed))
        helper.print_static(' %s%% [%s] %s KB/s  %s ETA' % (format(percentage, '3.1f'), progress, format(speed, '3.1f'), helper.htime(eta)), width)
        sleep(1)

    # For the completion progress bar and statistics.
    if Tracker.total_size:
        speed = format((Tracker.downloaded / 1024.0)/(time() - start), '3.1f')
        speed = speed + ' ' + helper.get_size(float(speed), suffix_only=True) + '/s'
    helper.print_static(' %s%% [%s] %s' % ('100', COMPLETE_CHAR * progress_bar_length, speed), width)

    # Print out completion download info.
    print '\n\n%s (%s KB/s)' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), speed),
    print '[%s/%s] in %s s\n' % (Tracker.downloaded, Tracker.total_size, helper.htime(time() - start))

def download(files, settings):
    temp_dir = settings['temp_dir']
    download_path = settings['download_path']

    download = DownloadPool(settings)
    decode = Decode()
    pool = GreenPool(settings['connections'])
    progress_tracker = greenthread.spawn(show_progress)

    for file_ in files:
        # Check if file from subject exists.
        subject_filename = helper.get_filename_from(file_['file_subject'])
        if os.path.exists(os.path.join(download_path, subject_filename)):
            Tracker.total_size -= sum([i['segment_bytes'] for i in file_['segments']])
            print subject_filename, 'already exists'
            continue

        # Download.
        for segment_path in pool.imap(download.download, file_['segments']):
            # Decode.
            if segment_path:
                tpool.execute(decode.decode, segment_path, temp_dir, download_path)

    if decode.tracker:
        print 'have broken files...'
        #return False
        print decode.tracker
        broken_files = decode.tracker.keys()
        for fname in broken_files:
            #print 'decoding', fname
            decode.join_files(fname, temp_dir, download_path)

    #progress_tracker.kill()
    progress_tracker.wait()

    # All OK.
    return 0

def start(filename, settings):
    Tracker.total_size, files, skipped_files = parse_nzb(filename, settings['skip_regex'])
    Tracker.downloaded = 0

    print 'Downloading:', filename
    print 'Size: %s \n' % helper.get_size(Tracker.total_size)
    res = download(files, settings)
    if res:
        # Got some broken files
        #download(skipped_files, settings)
        print 'got some broken files!'

if __name__ == '__main__':
    import sys
    from config import read_config
    settings = read_config()
    settings['download_path'] = 'downloads'

    start(sys.argv[1], settings)

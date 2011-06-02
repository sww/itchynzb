nntplib = __import__('nntplib')
from eventlet.green import socket
# Monkey patch nntplib.
nntplib.socket = socket
import os.path

class NNTP(object):
    def __init__(self, server='', port=0, username='', password=''):
        try:
            self.nntp = nntplib.NNTP(server, port, username, password)
        except:
            raise

    def change_group(self, groups):
        for group in groups:
            try:
                self.nntp.group(group)
            except:
                continue
            finally:
                return

    def get_body(self, segment, dest):
        segment_path = os.path.join(dest, segment)
        #print segment_path
        #self.nntp.body('<%s>' % segment, segment_path)
        try:
            self.nntp.body('<%s>' % segment, str(segment_path))
        except IOError:
            # Fall back directory.
            segment_path = os.path.join('temp', str(segment))
            self.nntp.body('<%s>' % segment, segment_path)
        except Exception, e:
            # Delete the segment if there's an error (since we don't know if the segment will be complete).
            #from os import remove
            #print '[ERROR] removing %s' % segment_path
            #remove(segment_path)
            print e

        return segment_path

    def close(self):
        self.nntp.quit()

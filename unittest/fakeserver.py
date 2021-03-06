"""A test NNTP server that serves certain specified files."""

import os
import signal

import eventlet

DEBUG = False
PORT = 5000
SERVE_DIRECTORY = 'files/segments'
SERVE_FILES = [
    os.path.join(SERVE_DIRECTORY, 'gplsegment@something.com'),
    os.path.join(SERVE_DIRECTORY, 'prjtgtnbrg01@something.com'),
    os.path.join(SERVE_DIRECTORY, 'prjtgtnbrg02@something.com')
]

def test_server(socket, address):
    if DEBUG: print '*', address[0], 'connected'

    fileobj = socket.makefile()
    fileobj.write('\n')
    fileobj.flush()

    while True:
        client_command = fileobj.readline()
        client_command = client_command.strip()
        if DEBUG: print '* Client sent "%s"' % client_command
        if not client_command:
            if DEBUG: print '* Client disconnected'
            break
        elif client_command == 'quit':
            if DEBUG: print '* Client quitting'
            break
        elif client_command == 'squit':
            raise eventlet.StopServe

        # Get response codes based on command sent from client.
        resp = resp_handler(client_command, address[0])
        if resp == '481 Quitter\n':
            break

        if resp.startswith('222'):
            # Serve the file.
            filename = resp.split()[-1].strip('<>')
            fileobj.write(resp)

            #eventlet.sleep(10)
            bytes = 0
            for line in serve_file(os.path.join(SERVE_DIRECTORY, filename)):
                bytes += len(line)
                fileobj.write(line)
                fileobj.flush()

            if DEBUG: print '* Read %d bytes' % bytes

            fileobj.write('.\r\n')
            fileobj.flush()
        elif resp:
            fileobj.write(resp)
            fileobj.flush()

def resp_handler(command, address):
    resp = ''
    command = command.lower().strip()
    if command.startswith('authinfo user'):
        resp = '381 OK\n'
    elif command.startswith('authinfo pass'):
        resp = '281 OK\n'
    elif command.startswith('group'):
        resp = '281 OK\n'
    elif command.startswith('body'):
        filename = command.split()[-1].strip('<>')
        full_filepath = os.path.join(SERVE_DIRECTORY, filename)
        if full_filepath in SERVE_FILES and os.path.exists(full_filepath):
            resp = '222 0 <%s>\r\n' % filename
        else:
            resp = '430 No such article.\n'
    elif command.startswith('quit'):
        resp = '481 Quitter\n'
    
    return resp

def serve_file(filename):
    with open(filename, 'rb') as f:
        for line in f:
            yield line

def start():
    server = eventlet.listen(('0.0.0.0', PORT))
    if DEBUG: print '* Listening on', PORT
    try:
        eventlet.serve(server, test_server)
    except Exception, msg:
        if DEBUG: print Exception, msg
        raise

def stop(*args):
    if DEBUG: print '* Stopping'
    raise eventlet.StopServe

if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option('-d', '--debug', action='store_true', dest="debug")
    (options, args) = parser.parse_args()

    if options.debug:
        DEBUG = True

    signal.signal(signal.SIGINT, stop)
    start()

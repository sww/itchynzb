"""A test server."""

import eventlet
import os
import signal

DEBUG = False
PORT = 5000
SERVE_FILES = ['files/gplsegment@something.com']

def test_server(socket, address):
    if DEBUG: print '*', address[0], 'connected'

    fileobj = socket.makefile()
    fileobj.write('\n')
    fileobj.flush()

    while True:
        client_command = fileobj.readline()
        client_command = client_command.strip()
        if DEBUG: print client_command
        if not client_command:
            if DEBUG: print 'disconnected'
            break
        elif client_command == 'quit':
            if DEBUG: print 'quitting'
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
            for line in serve_file(os.path.join('files', filename)):
                fileobj.write(line + "\r\n")
                fileobj.flush()

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
        temp = os.path.join('files', filename)
        if temp in SERVE_FILES and os.path.exists(temp):
            resp = '222 0 <%s>\r\n' % filename
        else:
            resp = '430 No such article.\n'
    elif command.startswith('quit'):
        resp = '481 Quitter\n'
    
    return resp

def serve_file(filename):
    data = []
    with open(filename, 'rb') as f:
        for line in f:
            data.append(line.strip())

    return data

def start():
    server = eventlet.listen(('0.0.0.0', PORT))
    if DEBUG: print '* Listening on', PORT
    try:
        eventlet.serve(server, test_server)
    except Exception, msg:
        if DEBUG: print Exception, msg

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

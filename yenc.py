#
TABLE = (
    ('=@', '\x00'),
    ('=I', '\t'),
    ('=J', '\n'),
    ('=M', '\r'),
    ('=[', '\x1b'),
    ('=`', ' '),
    ('=n', '.'),
    ('=}', '='),
)

YD = ''.join([chr((i + 256 - 42) % 256) for i in range(256)])

def _yenc_decode(data):
    metadata = {}

    for i in xrange(-1, 3):
        line = data[i].strip()

        if not line:
            continue

        values = line.split(' ', line.count('=')-1)
        for attr in values[1:]:
            key, value = attr.split('=')

            if line.startswith('=yend') and key == 'size':
                key = 'yend_size'

            if key and key not in metadata:
                metadata[key] = value.strip()

        if values[0] == '=ypart':
            break

    data = data[i+1:-1]

    encoded_data = ''.join(map(lambda x: x.rstrip('\r\n'), data))

    for k, v in TABLE:
        encoded_data = encoded_data.replace(k, v)

    dd = encoded_data.translate(YD)
    
    return dd, metadata

def yenc_decode(filename):
    with open(filename) as f:
        data = f.readlines()

    # Remove newline/blank lines from beginning and end.
    for line in data:
        if not line.strip():
            data.remove(line)
        else:
            break

    for line in data[::-1]:
        if not line.strip():
            data.remove(line)
        else:
            break

    decoded_data, metadata = _yenc_decode(data)

    return decoded_data, metadata

def profile():
    import cProfile
    cProfile.run("""test_decode()""")

def test_decode():
    import binascii
    import struct
    import sys
    data, metadata = yenc_decode(sys.argv[1])
    actual_crc = binascii.hexlify(struct.pack('!l', binascii.crc32(''.join(data))))
    if 'crc32' in metadata:
        expected_crc = metadata['crc32']
    else:
        expected_crc = metadata['pcrc32']
    if actual_crc == expected_crc:
        print 'file OK'
    else:
        print 'actual \'%s\' does not match expected \'%s\'' % (actual_crc, expected_crc)

    print metadata

if __name__ == '__main__':
    #test_decode()
    profile()

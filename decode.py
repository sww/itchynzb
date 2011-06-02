import binascii
import os
import struct
from yenc import yenc_decode

class SegmentTracker(object):
    def __init__(self, count=0, expected=0, broken=0):
        self.count = count
        self.expected = expected
        self.broken = broken

    def __repr__(self):
        return 'SegmentTracker<count: %d, expected: %d, broken: %d>' % (self.count, self.expected, self.broken)
    
    def is_complete(self):
        if self.expected > 0 and self.count == self.expected:
            return True
        return False

class Decode(object):
    def __init__(self):
        self.tracker = {}

    def decode(self, raw_segment_path, temp_dir, download_path):
        #print 'decoding', raw_segment_path
        decoded_data, metadata = yenc_decode(raw_segment_path)

        if not decoded_data or not metadata:
            # Return for now; later do something about the file tracker count.
            return
        
        decoded_data = ''.join(decoded_data)

        # Actual decoded data's checksum.
        checksum = binascii.hexlify(struct.pack('!l', binascii.crc32(decoded_data)))

        # Get key values here.
        dest_filename = metadata['name']
        segment_part_size = metadata['size']
        total_parts = metadata.get('total', None)
        segment_part = metadata.get('part', 1)
        segment_end_size = metadata.get('end', 1)

        if 'crc32' in metadata:
            # Single-part files do not have pcrc32 keys.
            crc_key = metadata['crc32']
        else:
            crc_key = metadata['pcrc32']

        if len(crc_key) < 8:
            crc_key = crc_key.rjust(8, '0')

        if crc_key.lower() != checksum.lower():
            print 'broken: expected: %s, got: %s' % (crc_key, checksum)
        
        segment_filename = os.path.join(temp_dir, '%s.%s' % (dest_filename, segment_part))
        with open(segment_filename, 'wb') as segment_fp:
            segment_fp.write(decoded_data)

        # Cleanup.
        os.remove(raw_segment_path)

        if dest_filename not in self.tracker:
            self.tracker.setdefault(dest_filename, SegmentTracker())

        if (total_parts and total_parts == segment_part) or (segment_part_size == segment_end_size):
            # Found the last segment number.
            self.tracker[dest_filename].expected = int(segment_part)
            
        self.tracker[dest_filename].count += 1
        
        if self.tracker[dest_filename].is_complete():
            self.join_files(dest_filename, temp_dir, download_path)
        
    def join_files(self, filename, temp_dir, download_path):
        dest_filename = os.path.join(download_path, os.path.join(os.path.split(filename)[1]))
        # 'or 1' just in case if join is called on a single part file that has no last segment number.
        number = self.tracker[filename].expected or 1

        with open(dest_filename, 'wb') as f:
            for i in range(1, number + 1):
                segment_filename = os.path.join(temp_dir, '%s.%d' % (filename, i))
                with open(segment_filename, 'rb') as segment_file:
                    f.write(segment_file.read())
                # Cleanup.
                os.remove(segment_filename)

        del self.tracker[filename]

if __name__ == '__main__':
    import sys
    d = Decode()
    d.decode(sys.argv[1], 'temp', 'download')
    # import cProfile
    # cProfile.run("""test_join()""")

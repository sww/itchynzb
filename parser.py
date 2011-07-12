import re
from xml.etree.cElementTree import ElementTree

NZB_DTD = '{http://www.newzbin.com/DTD/2003/nzb}'

def re_filter(skip_regex, invert=False):
    patterns = []
    for regex in skip_regex:
        patterns.append(re.compile(regex, re.I))
    def _re_filter(subject):
        for pattern in patterns:
            if pattern.search(subject):
                return True is not invert
        return False is not invert
    return _re_filter

def parse_nzb(filename, skip_regex=[], invert=False):
    nzb_files = []
    skipped_files = []
    segment_metadata = {}
    refilter = re_filter(skip_regex, invert)
    skip = False

    tree = ElementTree()
    tree.parse(filename)
    root = tree.getroot()
    if not root:
        raise StandardError('Could not parse NZB file %s' % filename)

    file_size = 0
    for element in root.getiterator():
        if element.tag.endswith('file'):
            # New file object.
            file_element = {'segments': [], 'groups': []}
            if element.items():
                for k, v in element.items():
                    file_element['file_%s' % k] = v
            skip = refilter(file_element['file_subject'])
        elif element.tag.endswith('group'):
            file_element['groups'].append(element.text.strip())
        elif element.tag.endswith('segment'):
            segment_metadata = {}
            segment_metadata['segment'] = element.text.strip()
            if element.items():
                for attr, value in element.items():
                    segment_metadata['segment_%s' % attr] = int(value)
            file_element['segments'].append(segment_metadata)
            if not skip:
                file_size += segment_metadata['segment_bytes']
        elif element.tag.endswith('segments'):
            if skip:
                skipped_files.append(file_element)
            else:
                nzb_files.append(file_element)

    return file_size, nzb_files, skipped_files

if __name__ == '__main__':
    import sys
    from config import read_config

    settings = read_config()
    size, q, sq = parse_nzb(sys.argv[1], settings['skip_regex'])
    print size, len(q), len(sq)
    for files in q:
        print files['file_subject'], sum([i['segment_bytes'] for i in files['segments']])

        for segment in files['segments']:
            print '    ->', segment

import re
from copy import deepcopy
from xml.etree.cElementTree import ElementTree

NZB_DTD = '{http://www.newzbin.com/DTD/2003/nzb}'

def parse_nzb(filename, skip_regex=None):
    nzb_files = []
    skipped_files = []
    segment_metadata = {}
    skip = False

    tree = ElementTree()
    tree.parse(filename)

    root = tree.getroot()
    if not root:
        print 'not root'
        return

    # for element in root.getiterator():
    #     if element.tag.endswith('file'):
    #         # New file object.
    #         file_element = {'segment': [], 'groups': []}
    #         if element.items():
    #             for k, v in element.items():
    #                 file_element['file_%s' % k] = v
    #         if skip_regex:
    #             for regex in skip_regex:
    #                 if re.search(regex, file_element['file_subject'], re.I):
    #                     skip = True
    #                     break
    #                 skip = False
    #     elif element.tag.endswith('group'):
    #         file_element['groups'].append(element.text.strip())
    #     elif element.tag.endswith('segment'):
    #         segment_metadata = deepcopy(file_element)
    #         segment_metadata['segment'] = element.text.strip()
    #         if element.items():
    #             for k, v in element.items():
    #                 segment_metadata['segment_%s' % k] = int(v)
    #         if skip:
    #             skipped_files.append(segment_metadata)
    #         else:
    #             nzb_files.append(segment_metadata)
    file_size = 0
    for element in root.getiterator():
        if element.tag.endswith('file'):
            # New file object.
            file_element = {'segments': [], 'groups': []}
            if element.items():
                for k, v in element.items():
                    file_element['file_%s' % k] = v
            if skip_regex:
                for regex in skip_regex:
                    if re.search(regex, file_element['file_subject'], re.I):
                        skip = True
                        break
                    skip = False
        elif element.tag.endswith('group'):
            file_element['groups'].append(element.text.strip())
        elif element.tag.endswith('segment'):
            segment_metadata = {}
            segment_metadata['segment'] = element.text.strip()
            if element.items():
                for k, v in element.items():
                    segment_metadata['segment_%s' % k] = int(v)
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

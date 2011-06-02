import os.path
import zipfile

def unzip(filename):
    nzb_list = []
    bunch = zipfile.ZipFile(filename, 'r')

    # Test the zip file, if it fails, return.
    if bunch.testzip():
        return None

    destination = os.path.split(filename)[0]
    
    # Unzip the .nzb files, if any.
    for f in bunch.namelist():
        if f.lower().endswith('.nzb'):
            # Extract the leading pathname from filename.
            bunch.extract(f, destination)
            nzb_list.append(os.path.join(destination, f))

    return nzb_list

if __name__ == '__main__':
    import sys

    print unzip(sys.argv[1])

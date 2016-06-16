import os
from uuid import uuid4


def randomPhotoName(instance, filename):
    ext = filename.split('.')[-1]

    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)

    # return the whole path to the file
    return os.path.join('profile-pictures', filename)

def randomFileName(instance, filename):
    ext = filename.split('.')[-1]

    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)

    # return the whole path to the file
    return os.path.join('patient-files', filename)

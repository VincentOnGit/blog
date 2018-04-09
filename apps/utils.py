# -*- coding: utf-8 -*-

import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_IMAGE_EXT = set(['png', 'jpb', 'jpeg', 'gif', 'bmp'])
ALLOWED_VIDEO_EXT = set(['mp4', 'avi'])
ALLOWED_AUDIO_EXT = set(['mp3', 'm4a', 'flac', 'wav'])


def check_files_ext(filenames, allowedexts):
	for fname in filenames:
		checkstate = '.' in fname and fname.rsplit('.', 1)[1] in allowedexts
		if not checkstate:
			return False
	return True


def change_filename_to_uuid(filename):
	name, ext = os.path.splitext(filename)
	res = secure_filename(name) + '_' + str(uuid.uuid4().hex) + ext
	return res

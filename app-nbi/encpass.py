# -*- coding: utf-8 -*-
"""
Password encoding and decoding module
"""
import pickle
import base64

def read_file(path):
	"""Open serialized object"""
	with open(path, 'rb') as f:
		obj = pickle.load(f)
		return obj

def write_pickle(path, obj):
	"""Write serialized picke file"""
	with open(path, 'wb') as handle:
		pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

def decode_pass_base64(b64_msg):
	"""Decode password base64"""
	password = base64.b64decode(b64_msg).decode('ascii')
	return password

def enconde_pass_base64(password):
	"""Encode password base64"""
	encoded = base64.b64encode(password.encode('ascii')) 
	return encoded

def encode_pass(path_to_file, password):
	enc_pass =enconde_pass_base64(password)
	cred = {'pass':enc_pass}
	write_pickle(path=path_to_file, obj=cred)

def decode_pass(path_to_file):
	obj = read_file(path=path_to_file)
	return decode_pass_base64(b64_msg=obj['pass'])

if __name__ == '__main__':
	try:
		pass
		
	except KeyboardInterrupt:
		pass
import re
import os,sys
import random
import subprocess

def checkPath(path):
	if os.path.exists(str(path)):
		return True;
	else:
		newD    = path.split('/');
		if newD[0] == '':
			if os.path.exists(str(newD[1])):
				os.system(f"touch {path}");
			else:
				os.system(f"mkdir /{newD[1]};touch {path} ");
		else:
			if os.path.exists(str(newD[0])):
				os.system(f"touch {path}");
			else:
				os.system(f"mkdir {newD[0]};touch {path}")

		return False;


def get(key,last_key=None,path='database/index.json'):
	key              = str(key);
	LK               = '';
	LKR             = LK;
	if last_key is not None:
		LK           = f"[{last_key}]";
		LKR         = "\["+last_key+"\]";
	
	checkPath(path);
	openDB   = open(str(path),'r');
	regEx       = "\n\["+key+"\]"+LKR+"=(.+)";
	content    = openDB.read();
	result        = re.findall(regEx,content);
	openDB.close();

	if result:
		return result[0];
	else:
		return False;


def set(key,last_key,option_value=None,path='database/index.json'):
	key              = str(key);
	LK               = '';
	value          = last_key;
	LKR             = LK;
	if option_value is not None:
		LK           = f"[{last_key}]";
		value      = option_value;
		LKR             = "\["+last_key+"\]";
		
	response  = False;
	checkPath(path);
	openDB   = open(str(path),'r');
	regEx       = "\n\["+key+"\]"+LKR+"=(.*)";
	content    = openDB.read();
	result        = re.findall(regEx,content);
	newV        = f"[{key}]{LK}={value}";
	DB             = open(str(path),'w');
	
	if result:
		newC        = content.replace(f"[{key}]{LK}={result[0]}",newV);
	else:
		content  += f"\n{newV}";
		newC       = content;
	try:
		DB.write(newC);
		response = True;
	except PermissionDenied:
		response = False;
	
	DB.close();
	openDB.close();
	
	return response;


def delete(key,last_key=None,path='database/index.json'):
	key              = str(key);
	response = True;
	LK               = '';
	LKR             = "(\[.*\])*"
	if last_key is not None:
		LK           = f"[{last_key}]";
		LKR         = "\["+last_key+"\]";
		
	
	checkPath(path);
	openDB   = open(str(path),'r');
	regEx       = "\n\["+key+"\]"+LKR+"=(.*)";
	content    = openDB.read();
	result        = re.findall(regEx,content);
	DB            = open(str(path),'w');
	
	if result:
		
		if LK == '':
			RMC    = LK;
			delL  = content;
			for iv in result:
				delL  = delL.replace(f"\n[{key}]{iv[0]}={iv[1]}",RMC);
			DB.write(delL);
			DB.close();
			
		else :
			RMC    = f"\n[{key}]{LK}=";
			delL  = content.replace(f"\n[{key}]{LK}={result[0]}",RMC);
			DB.write(delL);
	else:
		response =  False;
		DB.write(content);
	try:
		DB.close();
	except ValueError as nus:
		response = True;
	openDB.close();
	return response;

def is_int(par):
    result = True;
    try:
        int(par);
    except ValueError:
        result = False;
    return result;

	
def makeKey():
    for i in range(10):
        key = ""
        for j in range(10):
            key += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    return key;

def URLc(URL):
	response   = False;
	searchU     = re.findall("^@[a-zA-Z](_?[a-zA-Z0-9]_?)+[a-zA-Z0-9]$",URL);
	if len(searchU) > 0:
		response   = ['public',URL];
	else:
		searchU     = re.findall("^(http.?:\/\/)?t.me\/\+[a-zA-Z0-9\_\+\-]{5,35}$",URL);
		if len(searchU) > 0:
			response   = ['private',URL];
		else:
			searchU     = re.findall("^(http.?:\/\/)?t.me\/([a-zA-Z](_?[a-zA-Z0-9]_?)+[a-zA-Z0-9])$",URL);
			if len(searchU) > 0:
				response   = ['public',f"@{searchU[0][1]}"];

	return response;

def run_script(command):
	return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0];





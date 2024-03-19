from telethon.sync import TelegramClient
import sys, time, os, random
import json
import configparser
import requests
from database import *
from texts import *
import re
import json

opreats    = ['join','check','joining','joinPro','leaveChat','View', 'JoinList', 'LeaveList', 'like', 'likee', 'Poll', 'reaction', 'leavesss'];
opreat      = sys.argv[1];

if opreat not in opreats:
	exit();



LIST_DONE    = "✅ تم اضافة المجلد بنجاح\nرابط المجلد  : ++CC++\nعدد الحسابات التي اضافة المجلد بنجاح ++ADD++ من اصل ++ALL++";
LEAVE_RUN    = "جاري حذف المجلد...... ♻️\n عدد الحسابات التي حذفت المجلد بنجاح لحد الان ++LEA++ حساب من اصل ++ALL++ حساب ✅.";
LEAVE_DONE   = "تم الانتهاء من عملية حذف المجلد بنجاح ✅\nعدد الحسابات الذي حذفت المجلد بدون مشاكل ++LEA++ حساب من أصل ++ALL++ حساب 😊.";
JOINED       = "🎢 جاري اضافة المجلد....\n♻️ يتم اضافة المجلد ++CC++ من جميع الحسابات المتاحة\n✅ تم اضافة المجلد بنجاح من ++ADD++ حساب";
pleasewait   = "⚡️ لحظات من فضلك .....";
TESTER	 = "✅ تم عمل الفحص بنجاح\nإجمالي عدد الحسابات على السيرفر ++ALL++\nعدد الحسابات النشطة ++SUCCESS++\nعدد الحسابات المنتهية ++AUTH++\nعدد الحسابات المحذوفة ++DELETED++\nعدد الحسابات التي تحتوي على مشاكل ++OTHER++";
TESTING	= "⚡️ يتم الفحص الآن........\nإجمالي عدد الحسابات على السيرفر ++ALL++\nعدد الحسابات النشطة ++SUCCESS++\nعدد الحسابات المنتهية ++AUTH++\nعدد الحسابات المحذوفة ++DELETED++\nعدد الحسابات التي تحتوي على مشاكل ++OTHER++";

SUPPORT   = "⚡️ جار الرشق ......\n♻️ يتم تمويل ++CH++ ب ++TOTAL++ عضو\n\n✅ تم التمويل حتى اللحظة ب ++JOINED++ عضو من أصل ++TOTAL++ عضو \nمعرف العملية كالتالي\n++ID++";
SUP_DONE = "✅ تم الرشق بنجاح\n♻️ إلى ++CH++ تم رشق ++JOINED++ عضو بنجاح من أصل ++TOTAL++ عضو";
#opreatID   =
ALLL = "⚡️ يتم المغادرة الآن........\nإجمالي عدد الحسابات على السيرفر ++ALLS++\nعدد الحسابات مكتملة المغادرة ++DONE++\nعدد الحسابات السيئة ++BAD++";
ALLLDONE = "تمت المغادرة بنجاح ✅.\nإجمالي عدد الحسابات على السيرفر ++ALLS++";



config = configparser.ConfigParser()
config.read("config.ini")

api_id       = config['owner']['id'];
api_hash = config['owner']['hash'];
token	= config['API_KEYs']['mover'];

raw1    = [
	[
		{'text':'Hello', "callback_data": 'NotBad'}
	]
]


def sendMessage(chat_id, text):
	URL	  = "https://api.telegram.org/bot"+token+"/sendmessage"
	PARAMS = {'chat_id': chat_id, 'text': text}
	RGET       = requests.get(url=URL, params=PARAMS);
	return json.loads(RGET.text)

def sendMessageM(chat_id, text):
	URL	  = "https://api.telegram.org/bot"+token+"/sendmessage"
	PARAMS = {'chat_id': chat_id, 'text': text,
	'parse_mode': 'MarkDown'}
	RGET       = requests.get(url=URL, params=PARAMS);
	return json.loads(RGET.text)

def sendInlineKeyboard(chat_id, text, keyboard, parse_mode):
	URL	  = "https://api.telegram.org/bot"+token+"/sendmessage"
	PARAMS = {'chat_id': chat_id, 'text': text,
	'parse_mode': parse_mode,
	'reply_markup': keyboard}
	RGET       = requests.get(url=URL, params=PARAMS);
	return json.loads(RGET.text)

def editInlineKeyboard(chat_id, text, keyboard, parse_mode, message_id):
	URL	  = "https://api.telegram.org/bot"+token+"/editMessageText"
	PARAMS = {'chat_id': chat_id, 'text': text,
	'parse_mode': parse_mode,
	'reply_markup': keyboard,
	'message_id': message_id}
	RGET       = requests.get(url=URL, params=PARAMS);
	return json.loads(RGET.text)


def replyMessage(chat_id, text, message_id):
	URL	  = "https://api.telegram.org/bot"+token+"/sendmessage"
	PARAMS = {'chat_id': chat_id, 'text': text, 'reply_to_message_id': message_id}
	RGET       = requests.get(url=URL, params=PARAMS);
	TG_RESPONSE     = False;
	try:
		TG_RESPONSE   =  json.loads(RGET);
	except:
		return TG_RESPONSE;
	return TG_RESPONSE;

def editMessage(chat_id,text,message_id):
	URL	   = "https://api.telegram.org/bot"+token+"/editMessageText";
	PARAMS  = {'chat_id': chat_id, 'text': text, 'message_id': message_id};
	RGET       = requests.get(url=URL, params=PARAMS);
	TG_RESPONSE     = False;
	try:
		TG_RESPONSE   =  json.loads(RGET);
	except:
		return TG_RESPONSE;
	return TG_RESPONSE;

def editMessageMK(chat_id,text,message_id):
	URL	   = "https://api.telegram.org/bot"+token+"/editMessageText";
	PARAMS  = {'chat_id': chat_id, 'text': text, 'message_id': message_id, 'parse_mode': 'MarkDown'};
	RGET       = requests.get(url=URL, params=PARAMS);
	TG_RESPONSE     = False;
	try:
		TG_RESPONSE   =  json.loads(RGET);
	except:
		return TG_RESPONSE;
	return TG_RESPONSE;

sessions	      = os.listdir('sessions');
random.shuffle(sessions);
THE_SESSIONS = os.listdir('sessions');
cSessions	   = len(THE_SESSIONS);



if opreat == 'LeaveList':
	opreatID = sys.argv[2];
	link = sys.argv[3];
	OWN_ID = sys.argv[4];

	try :
		owner_id = get(opreatID,'owner','database/list.json')
		links = get(opreatID,'linklists','database/list.json')
		LINK = set(opreatID, 'listslinks', link, 'database/list.json')

	except :
		pass

	#done_value = db.get(query.opreatID == 'JoinList')['done']
	#print(done_value)

	DONE = 0
	BAD = 0
	SESSIONSS = cSessions

	EB_ID = sendMessage(owner_id,pleasewait)
	try:
		B_ID = EB_ID['result']['message_id']
	except:
		B_ID = 4
	LOOPB = 0
	IDB =    'false';
	while True:
		LOOPB += 1
		if LOOPB > cSessions or DONE >= cSessions:
			TEXT      = LEAVE_DONE.replace('++LEA++',str(DONE)).replace('++ALL++',str(SESSIONSS))
			sendMessage(owner_id,TEXT)
			exit()
			break

		try :
			LEAVED_LIST   =  get(IDB,'joined').split(',')
		except :
			LEAVED_LIST   = []
		
		SESSION_AB = sessions[LOOPB - 1].split('.')[0]
		if SESSION_AB in LEAVED_LIST:
			continue

		LEAVE   		 = 	run_script(f"python3 addAccount.py leavelist {SESSION_AB} {link} {opreatID} {OWN_ID}")
		try:
			palles  = re.findall("\[\'true\'",LEAVE)
			if len(palles) > 0:
				IDB  = '-'+str(palles[0])
				DONE += 1
				ERROR = "\n ___TRUE____"
				set(IDB,'joined',get(IDB,'joined')+SESSION_AB+',')
			else:
				ERROR = f"\n {LEAVE}"
		except Exception as Error:
			ERROR = f"\n {Error}"

		TEXT   = LEAVE_RUN.replace('++LEA++',str(DONE)).replace('++ALL++',str(SESSIONSS))
		editMessage(owner_id,TEXT+ERROR,B_ID)


if opreat == 'JoinList':
	opreatID = sys.argv[2];
	link = sys.argv[3];
	OWN_ID = sys.argv[6];
	IDL = sys.argv[5];

	try :
		owner_id = get(opreatID,'owner','database/list.json')
		links = get(opreatID, 'linklist','database/list.json')
		#link = get(opreatID,'linklist','database/list.json')
		LINK = set(opreatID, 'listslink', link, 'database/list.json')
		
	except :
		pass

	DONE = 0
	BAD = 0
	SESSIONS = cSessions

	ES_ID = sendMessage(owner_id,pleasewait)
	try:
		S_ID = ES_ID['result']['message_id']
	except:
		S_ID = 4
	LOOPT = 0
	IDS =     'false';
	while True:
		LOOPT += 1

		if LOOPT > cSessions or DONE >= cSessions:
			TEXT      = LIST_DONE.replace('++CC++',str(link)).replace('++ADD++',str(DONE)).replace('++ALL++',str(SESSIONS))
			sendMessage(owner_id,TEXT)
			#delete(from_id,None,'database/list.json');
			exit()
			break

		try :
			JOINED_LIST   = get(IDS,'joined').split(',')
		except :
			JOINED_LIST   = []
		
		SESSION_AS  =  sessions[LOOPT - 1].split('.')[0]
		if SESSION_AS in JOINED_LIST:
			continue

		JOIN       			= run_script(f"python3 addAccount.py joinlist {SESSION_AS} {link} {opreatID} {OWN_ID} {IDL}")
		try:
			paless   = re.findall("\[\'true\'",JOIN)
			if len(paless) > 0:
				IDS   = '-'+str(paless[0])
				DONE   += 1
				ERROR = "\n ___TRUE____"
				set(IDS,'joined',get(IDS,'joined')+SESSION_AS+',')
			else:
				ERROR = f"\n {JOIN}"
		except Exception as Jello:
			ERROR = f"\n {Jello}"
		
		TEXT   = JOINED.replace('++CC++',str(links)).replace('++ADD++',str(DONE)).replace('++ALL++',str(SESSIONS))
		editMessage(owner_id,TEXT+ERROR,S_ID)
				#palees  = re.findall("\[\'false\'\,\s\-(\d+)")
				#if len(palees) > 0:





if opreat == 'joining':
	opreatID       = sys.argv[2];
	try :
		owner_id     = get(opreatID,'owner','database/support.json');
		requested    = int(get(opreatID,'requested_count','database/support.json'));
		user_name  = get(opreatID,'supported_username','database/support.json');
	except :
		pass
	#sendMessage(owner_id,pleasewait);
	
	SUCCESS     = 0;
	REQUESTED     = requested;
	if requested >= cSessions:
		REQUESTED   = cSessions;
	
	
	EM_ID	 = sendMessage(owner_id,pleasewait);
	try:
		M_ID = EM_ID['result']['message_id']
	except:
		M_ID = 4;
	LOOPS   = 0;
	IDU          = 'False';
	while True:
		LOOPS   += 1;
		
		if LOOPS > cSessions or SUCCESS >= REQUESTED:
			TEXT      = SUP_DONE.replace('++CH++',str(user_name)).replace('++JOINED++',str(SUCCESS)).replace('++TOTAL++',str(REQUESTED));
			sendMessage(owner_id,TEXT);
			exit();
			break;
		
		try :
			JOINED_SESSIONS    = get(IDU,'joined').split(',');
		except :
			JOINED_SESSIONS     = [];
		
		SESSION_AT  = sessions[LOOPS - 1].split('.')[0];
		if SESSION_AT in JOINED_SESSIONS:
			continue;
		
		JOIN                = run_script(f"python3 addAccount.py joining {SESSION_AT} {user_name}");
		try:
			pales      = re.findall("\[\'true\'\,\s\-(\d+)",JOIN);
			if len(pales) > 0:
				IDU      = '-'+str(pales[0]);
				SUCCESS     += 1;
				ERROR = "\n ___TRUE____";
				set(IDU,'joined',get(IDU,'joined')+SESSION_AT+',');
			else:
				ERROR = f"\n {JOIN}";
		except Exception as Jello:
			ERROR = f"\n {Jello}";
		
		TEXT      = SUPPORT.replace('++CH++',user_name).replace('++JOINED++',str(SUCCESS)).replace('++TOTAL++',str(REQUESTED)).replace('++ID++',IDU);
		editMessage(owner_id,TEXT+ERROR,M_ID);
		


if opreat == 'View':
	UN        = str(sys.argv[2]);
	IDM       = int(sys.argv[3]);
	CNT       = int(sys.argv[4]);
	ID_OWN = int(sys.argv[5]);
	EM_ID	 = sendMessage(ID_OWN,pleasewait);
	try:
		M_ID = EM_ID['result']['message_id']
	except:
		M_ID = 4;
	
	zero       = 0;
	for session in sessions:
		if zero >= CNT :
			break;
		zero    += 1;
		disp     = CNT - zero;
		NAME_SESSION     = session.split('.')[0];
		RESPONSE	       = run_script(f"python3 addAccount.py View {NAME_SESSION} {UN} {IDM}");
		VIEWD    = AdderTexts['ViewingSc'].replace('++DONE++',str(zero)).replace('++DIS++',str(disp));
		editMessageMK(ID_OWN,VIEWD,M_ID);
	

if opreat == 'Poll':
	UT = str(sys.argv[2])
	IDT = int(sys.argv[3])
	COT = int(sys.argv[4])
	owner_id = int(sys.argv[5])
	II = int(sys.argv[6])
	COiD = sendMessage(owner_id,pleasewait)
	try:
		MID = COiD['result']['message_id']
	except:
		MID = 4

	Zero = 0
	for session in sessions:
		if Zero >= COT:
			break;
		Zero += 1
		AA     = COT - Zero
		NAME_SESSION     = session.split('.')[0];
		RESPONSE	       = run_script(f"python3 addAccount.py Poll {NAME_SESSION} {UT} {IDT} {II}");
		VIEWD    = ExtraTexts['pollsend'].replace('++DONE++',str(Zero)).replace('++DS++',str(AA));
		editMessageMK(owner_id,VIEWD,MID);


if opreat == 'like':
	UT = str(sys.argv[2])
	IDT = int(sys.argv[3])
	COT = int(sys.argv[5])
	owner_id = int(sys.argv[4])
	#II = int(sys.argv[6])
	COiD = sendMessage(owner_id,pleasewait)
	try:
		MID = COiD['result']['message_id']
	except:
		MID = 4

	Zero = 0
	for session in sessions:
		if Zero >= COT:
			break;
		Zero += 1
		AA     = COT - Zero
		NAME_SESSION     = session.split('.')[0];
		RESPONSE	       = run_script(f"python3 addAccount.py like {NAME_SESSION} {UT} {IDT} {owner_id}");
		VIEWD    = ExtraTexts['pollsend'].replace('++DONE++',str(Zero)).replace('++DS++',str(AA));
		editMessageMK(owner_id,VIEWD,MID);

if opreat == 'likee':
	LINK = str(sys.argv[2])
	IDT = int(sys.argv[3])
	COT = int(sys.argv[5])
	owner_id = int(sys.argv[4])
	#II = int(sys.argv[6])
	COiD = sendMessage(owner_id,pleasewait)
	try:
		MID = COiD['result']['message_id']
	except:
		MID = 4

	Zero = 0
	for session in sessions:
		if Zero >= COT:
			break;
		Zero += 1
		AA     = COT - Zero
		NAME_SESSION     = session.split('.')[0];
		RESPONSE	       = run_script(f"python3 addAccount.py likee {NAME_SESSION} {LINK} {IDT} {owner_id}");
		VIEWD    = ExtraTexts['pollsend'].replace('++DONE++',str(Zero)).replace('++DS++',str(AA));
		editMessageMK(owner_id,VIEWD,MID);



if opreat == 'reaction':
	UT = str(sys.argv[2])
	IDT = int(sys.argv[3])
	EM = str(sys.argv[5])
	COT = int(sys.argv[6])
	owner_id = int(sys.argv[4])
	COiD = sendMessage(owner_id,pleasewait)
	try:
		MID = COiD['result']['message_id']
	except:
		MID = 4

	Zero = 0
	for session in sessions:
		if Zero >= COT:
			break;
		Zero += 1
		AA     = COT - Zero
		NAME_SESSION     = session.split('.')[0];
		RESPONSE	       = run_script(f"python3 addAccount.py reaction {NAME_SESSION} {UT} {IDT} {EM}");
		VIEWD    = ExtraTexts['reactionsend'].replace('++DONE++',str(Zero)).replace('++DD++',str(AA));
		editMessageMK(owner_id,VIEWD,MID);

if opreat == 'leavesss':
	owner_id = int(sys.argv[2])
	DONE = 0
	BAD = 0
	HOW = False
	ALLS = 0
	EM_EIDD	 = sendMessage(owner_id,'Waiiiiit')
	try:
		M_IDD = EM_EIDD['result']['message_id']
	except:
		M_IDD = 4
	for session in sessions:
		ALLS += 1
		RES = False
		NAME_SESSIONN     = session.split('.')[0]
		RES	       = run_script(f"python3 addAccount.py leavess {NAME_SESSIONN}")
		if RES is not False:
			HOW = True
			RESS = RES.split("\n")
			if 'true' in RESS:
					DONE   += 1;
			elif 'false' in RESS:
				BAD	  += 1
		DD = ALLL.replace('++ALLS++',str(ALLS)).replace('++DONE++',str(DONE)).replace('++BAD++',str(BAD))
		editMessage(owner_id,DD,EM_EIDD)
	DDS = ALLLDONE.replace('++ALLS++',str(ALLS)).replace('++DONE++',str(DONE)).replace('++BAD++',str(BAD))
	sendMessage(owner_id,DDS);


if opreat == 'leaveChat':
	IDleave     = int(sys.argv[2]);
	for session in sessions:
		NAME_SESSION     = session.split('.')[0];
		RESPONSE	       = run_script(f"python3 addAccount.py left {NAME_SESSION} {IDleave} {IDleave}");


if opreat == 'check':
	owner_id  = int(sys.argv[2]);
	SUCCESS = 0;
	DELETED = 0;
	AUTH	= 0;
	OTHER      = 0;
	STATUS     = False;
	ALL	     = 0;
	EM_EID	 = sendMessage(owner_id,'Waiiiiit');
	try:
		M_ID = EM_EID['result']['message_id']
	except:
		M_ID = 4;
	for session in sessions:
		ALL			  += 1;
		RESPONSE	       = False;
		NAME_SESSION     = session.split('.')[0];
		RESPONSE	       = run_script(f"python3 addAccount.py check {NAME_SESSION}");
		if RESPONSE is not False:
			STATUS     = True;
			RESULT     = RESPONSE.split("\n");
			if 'true' in RESULT:
				SUCCESS   += 1;
			elif 'false' in RESULT:
				AUTH	  += 1;
			elif 'deleted' in RESULT:
				DELETED     += 1;
			else:
				OTHER	  += 1;
		DSR      = TESTING.replace('++ALL++',str(ALL)).replace('++SUCCESS++',str(SUCCESS)).replace('++AUTH++',str(AUTH)).replace('++DELETED',str(DELETED)).replace('++OTHER++',str(OTHER));
		editMessage(owner_id,DSR,M_ID);
	DSS      = TESTER.replace('++ALL++',str(ALL)).replace('++SUCCESS++',str(SUCCESS)).replace('++AUTH++',str(AUTH)).replace('++DELETED',str(DELETED)).replace('++OTHER++',str(OTHER));
	sendMessage(owner_id,DSS);




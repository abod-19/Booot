from telethon.sync import TelegramClient
from telethon import events, Button
import json
import configparser
import subprocess
import telethon
import os,sys
import re
import requests
from database import *
from texts import *
import zipfile
from zipfile import ZipFile


welcome            = "أهلا وسهلا عزيزي المشرف في لوحة التحكم\n\nلبدء عملية نقل عادية ارسل /copy\n\nلبدء عملية نقل متطورة ( للجروبات المقفولة ) ارسل /MovePro\n\n\nللفحص وعرض عدد الحسابات /check";
to_cancle           = "\nللإلغاء ارسل /cancle";
move_is_busy   = "هناك عملية نقل حالياً\nلإلغائها ارسل /stop_all";
try_send_url       = "خطأ\nهذا ليس رابطا لجروب تيليجرام\nارسل رابط كالتالي\nhttps://t.me/ALRAGI1";
try_send_int       = "خطأ\nهذا ليس عددا صحيحا\nارسل عدد كالتالي\n22";
cancled               = "تم الإلغاء";
no_cancled        = " لا يوجد عملية لإلغائها";
checking             = "⚡️ جار فحص ++COUNT++ حسابا\n♻️ يرجى التحلي بالصبر ... يمكنك رؤية العمليات مباشرة عبر الرسالة التالية";
send_sup_url     = "⚡️ قم بإرسال رابط القناة أو المجموعة التي سيتم ضخ الأعضاء إليها......";
send_sup_count = "♻️ قم بإرسال عدد الأعضاء الذين سيتم ضخهم إلى ++URL++";
SS = "**- جاري تحميل ملف الجلسات ♻️**"

  


config = configparser.ConfigParser() 
config.read("config.ini")

THE_SESSIONS = os.listdir('sessions');
cSessions           = len(THE_SESSIONS);

api_id       = config['owner']['id'];
api_hash = config['owner']['hash'];
client        = telethon.TelegramClient('center', api_id, api_hash);


token = config['API_KEYs']['mover'];
botID  =  int(token.split(':')[0]);
admin = config['owner']['admin'];


def sendMessage(chat_id, text):
	URL	  = "https://api.telegram.org/bot"+token+"/sendmessage"
	PARAMS = {'chat_id': chat_id, 'text': text}
	RGET       = requests.get(url=URL, params=PARAMS);
	return json.loads(RGET.text)

def zip_folder(folder_path, zip_name):
	with ZipFile(zip_name, 'w') as zipf:
		for root, _, files in os.walk(folder_path):
			for file in files:
				file_path = os.path.join(root, file)
				arc_name = os.path.relpath(file_path, folder_path)
				zipf.write(file_path, arcname=arc_name)



bt_start     = [
		[
				Button.inline(buttonsAdder['lists'],'lists')
		],
		[
				Button.inline(buttonsAdder['JoinM'],'JoinM'),
				Button.inline(buttonsAdder['AddViews'],'AddViews')
		],
		[
				Button.inline(buttonsAdder['CheckAccounts'],'CheckAccounts'),
				Button.inline(extraButtons['Leave'],'Leave')
		],
		[
				Button.inline(extraButtons['leaves'], 'leaves')
		]
]

bt_cancle    = [
		[
				Button.inline(extraButtons['Cancle'],'Cancle')
		],
]


bt_back = [
		[
				Button.inline(extraButtons['Back'],'Back')
		]
]

# ازرار اضافة وحذف المجلدات 
buttonlist = [
	[
		 Button.inline(buttonsAdder['Join_list'], 'Join_list'),
		 Button.inline(buttonsAdder['Leave_list'], 'Leave_list'),
	],
	[
		 Button.inline(extraButtons['Back'],'Back'),
	],
]

client.start(bot_token=token);
client.connect();

@client.on(events.CallbackQuery())
async def callback(event):
    try:
        chat = event.original_update.peer.user_id
        fData = event.data
        data = fData.decode("utf-8")
        f_data = data.split('_')
    except:
        data = False
    from_id = str(event.sender_id)
    chat_id = event.chat_id

    status = get(from_id, 'status', 'database/mover.json')

    if data == 'lists':
        await event.edit(ExtraTexts['textlists'], parse_mode='md', buttons=buttonlist)
        return
	
    if data == 'Join_list':
        await event.edit(ExtraTexts['joinlisturl'], parse_mode='md', buttons=bt_cancle)
        set(from_id, 'status', 'Joinlist', 'database/mover.json')
        return
	
    if data == 'Leave_list':
        await event.edit(ExtraTexts['leavelisturl'], parse_mode='md', buttons=bt_cancle)
        set(from_id, 'status', 'Leavelist', 'database/mover.json')
        return

    if data == 'Back':
        await event.edit(textsStart, buttons=bt_start, parse_mode='md')
        return
			
    if data == 'Cancle':
        await event.edit(textsStart, buttons=bt_start, parse_mode='md')
        delete(from_id, None, 'database/mover.json')
        return

    if data == 'CheckAccounts':
        subprocess.Popen(["python3", "control.py", "check", from_id])
        await event.edit(checking.replace('++COUNT++', str(cSessions)), parse_mode='md', buttons=bt_back)
        return

    if data == 'JoinM':
        if status is not False:
            await event.edit(ExtraTexts['serverIsBusy'], parse_mode='md', buttons=bt_cancle)
        else:
            await event.edit(ExtraTexts['supportCHGP'], parse_mode='md', buttons=bt_cancle)
            set(from_id, 'status', 'support', 'database/mover.json')
        return

    if data == 'Leave':
        await event.edit(ExtraTexts['Leave'], buttons=bt_cancle, parse_mode='md')
        set(from_id, 'status', 'leave', 'database/mover.json')
        return

    if data == 'AddViews':
        await event.edit(ExtraTexts['ViewURL'], buttons=bt_cancle, parse_mode='md')
        set(from_id, 'status', 'viewUrl', 'database/mover.json')
        return
	
    if data == 'leaves':
        await event.reply(ExtraTexts['leavestext'], parse_mode='md', buttons=bt_back)
        subprocess.Popen(["python3", "control.py", "leavesss", from_id])
        return



	
@client.on(events.NewMessage())

async def main(event):
	chattt = await event.get_chat();
	if chattt.__class__.__name__ != 'User':
		return
	try:
		b = event.message.peer_id.channel_id
		b = f"-100{b}"
	except:
		pass

	text                 = event.raw_text;
	message_id  = event.message.id;
	from_id          = str(event.sender_id);
	chat_id           = event.chat_id;
	
	if from_id == botID:
		return
	
	
	if from_id not in admin:
		#await event.reply('♻️');
		return
	status       = get(from_id,'status','database/mover.json');
	FROM       = get(from_id,'from','database/mover.json');
	TO             = get(from_id,'to','database/mover.json');
	COUNT    = get(from_id,'count','database/mover.json');
	TIMER      = get(from_id,'timer','database/mover.json');
	MMove     = get(from_id,'ModeMove','database/mover.json');
	
	
	if text == '/start':
		await event.reply(textsStart,buttons=bt_start,parse_mode='md');
		return
	if text == '/list':
		await event.reply(ExtraTexts['textlists'], buttons=buttonlist, parse_mode='md');
		return
	if text == '/cancle':
		if status is not False:
			delete(from_id,None,'database/mover.json');
			await event.reply(cancled);
		else:
			await event.reply(no_cancled);
		return
	
	if text == '/sessions':
		entity = await event.get_input_sender()
		await event.reply(SS, parse_mode='md')
		zip_folder("sessions", "sessions.zip")
		await client.send_file(entity=entity,file="sessions.zip", caption="The Sessions")
		return
	
	if text == '/likee':
		await event.reply(ExtraTexts['likeetext'], parse_mode='md', buttons=bt_cancle)
		set(from_id,'status','likee','database/mover.json')
		return
	
	if text and status == 'likee':
		test_url    = URLc(text);
		if test_url is not False:
			US      = text
			set(from_id,'channel_link', US,'database/mover.json');
			set(from_id,'link',text,'database/mover.json');
			set(from_id,'status','likeeid','database/mover.json');
			await event.reply(ExtraTexts['likeeid'],buttons=bt_cancle,parse_mode='md');
			return
		
	if text and status == 'likeeid':
		regExNu = re.findall("^[0-9]+$", text)
		if len(regExNu) > 0:
			set(from_id,'ID_likee',text,'database/mover.json')
			set(from_id,'status','likeecount','database/mover.json')
			await event.reply(ExtraTexts['likecount'],buttons=bt_cancle,parse_mode='md')
			return
		

	if text and status == 'likeecount':
		regExNu = re.findall("^[0-9]+$", text)
		if len(regExNu) > 0:
			LINK = get(from_id, 'channel_link', 'database/mover.json')
			ID = get(from_id, 'ID_likee', 'database/mover.json')
			await event.reply(ExtraTexts['reactioning'], buttons=bt_back, parse_mode='md')
			run_script(f"python3 control.py likee {LINK} {ID} {from_id} {text}")
			delete(from_id, None, 'database/mover.json')
			return
		

	if text == '/like':
		await event.reply(ExtraTexts['liketext'], parse_mode='md', buttons=bt_cancle)
		set(from_id,'status','like','database/mover.json')
		return
	

	if text and status == 'like':
		regExNu   = re.findall("^https?:\/\/t\.me\/([a-zA-Z0-9_]+)\/([0-9]+)",text);
		if len(regExNu) > 0:
			opID = makeKey()
			UNCC    = '@'+str(regExNu[0][0]);
			IDCC      = regExNu[0][1]
			set(from_id,'username_like',UNCC,'database/mover.json');
			set(from_id,'ID_like',IDCC,'database/mover.json');
			set(from_id,'status','likeCount','database/mover.json');
			await event.reply(ExtraTexts['likecount'],buttons=bt_cancle,parse_mode='md');
			return
		

	if text and status == 'likeCount':
		regExNu = re.findall("^[0-9]+$", text)
		if len(regExNu) > 0:
			d = str(regExNu[0])
			us = get(from_id, 'username_like', 'database/mover.json')
			idc = get(from_id, 'ID_like', 'database/mover.json')
			await event.reply(ExtraTexts['reactioning'], buttons=bt_back, parse_mode='md')
			run_script(f"python3 control.py like {us} {idc} {from_id} {text}")
			delete(from_id, None, 'database/mover.json')
			return
		

	if text == '/reaction':
		await event.reply(ExtraTexts['reactiontext'], parse_mode='md', buttons=bt_cancle)
		set(from_id,'status','reaction','database/mover.json')
		return
	
	if text and status == 'reaction':
		regExNu   = re.findall("^https?:\/\/t\.me\/([a-zA-Z0-9_]+)\/([0-9]+)",text);
		if len(regExNu) > 0:
			opID = makeKey()
			UNCC    = '@'+str(regExNu[0][0]);
			IDCC      = regExNu[0][1]
			set(from_id,'username_reaction',UNCC,'database/mover.json');
			set(from_id,'ID_reaction',IDCC,'database/mover.json');
			set(from_id,'status','reactionnum','database/mover.json');
			await event.reply(ExtraTexts['reactioncount'],buttons=bt_cancle,parse_mode='md');
			return
		
	if text and status == 'reactionnum':
		regExNu = re.findall("^[0-9]+$", text)
		if len(regExNu) > 0:
			set(from_id,'count_reaction',text,'database/mover.json');
			#us = get(from_id, 'username_reaction', 'database/mover.json')
			#idc = get(from_id, 'ID_reaction', 'database/mover.json')
			set(from_id,'status','reactionemogi','database/mover.json');
			await event.reply(ExtraTexts['reactionemogi'], buttons=bt_back, parse_mode='md')
			return
	
	if text and status == 'reactionemogi':
		us = get(from_id, 'username_reaction', 'database/mover.json')
		idc = get(from_id, 'ID_reaction', 'database/mover.json')
		em = get(from_id, 'count_reaction', 'database/mover.json')
		await event.reply(ExtraTexts['reactioning'], buttons=bt_back, parse_mode='md')
		run_script(f"python3 control.py reaction {us} {idc} {from_id} {text} {em}")
		delete(from_id, None, 'database/mover.json')
		return


	if text == '/poll':
		await event.reply(ExtraTexts['polltext'], parse_mode='md', buttons=bt_cancle)
		set(from_id,'status','poll','database/mover.json')
		return
	
	if text and status == 'poll':
		regExNu   = re.findall("^https?:\/\/t\.me\/([a-zA-Z0-9_]+)\/([0-9]+)",text);
		if len(regExNu) > 0:
			opID = makeKey()
			UNCC    = '@'+str(regExNu[0][0]);
			IDCC      = regExNu[0][1]
			set(from_id,'username_poll',UNCC,'database/mover.json');
			set(from_id,'ID_poll',IDCC,'database/mover.json');
			set(from_id,'status','pollCount','database/mover.json');
			await event.reply(ExtraTexts['pollcount'],buttons=bt_cancle,parse_mode='md');
			return
		
	if text and status == 'pollCount':
		regExNu   = re.findall("^[0-9]+$",text);
		if len(regExNu) > 0:
			set(from_id,'pollcount',text,'database/mover.json');
			await event.reply(ExtraTexts['pollnum'],buttons=bt_cancle,parse_mode='md');
			set(from_id,'status','pollnum','database/mover.json');
			return
		
	if text and status == 'pollnum':
		regExNu = re.findall("^[0-9]+$", text)
		if len(regExNu) > 0:
			d = str(regExNu[0])
			us = get(from_id, 'username_poll', 'database/mover.json')
			idc = get(from_id, 'ID_poll', 'database/mover.json')
			po = get(from_id, 'pollcount', 'database/mover.json')
			await event.reply(ExtraTexts['polling'], buttons=bt_back, parse_mode='md')
			run_script(f"python3 control.py Poll {us} {idc} {po} {from_id} {text}")
			delete(from_id, None, 'database/mover.json')
			return

	

	if text == '/support':
		if status is not False:
			await event.reply(move_is_busy);
		else:
			await event.reply(send_sup_url+to_cancle);
			set(from_id,'status','support','database/mover.json');
		return
		
	if text and status == 'Joinlist':
		regExNu = re.findall("^https:\/\/t\.me\/addlist\/([a-zA-Z0-9_]+)$", text);
		if len(regExNu) > 0:
			opID = makeKey();

			listID = text
			IDlist = regExNu[0][1];
			await event.reply(ExtraTexts['ListJoin'], parse_mode='md', buttons=bt_back);
			set(opID,'owner', from_id, 'database/list.json');
			set(opID,'linklist', listID, 'database/list.json');
			set(opID,'list_link', IDlist, 'database/list.json');
			run_script(f"python3 control.py JoinList {opID} {text} {listID} {IDlist} {from_id}");
			#subprocess.Popen(["python3", "control.py", "JoinList", text, from_id]);
		else:
			await event.reply(ExtraTexts['listcancle'], parse_mode='md', buttons=bt_back);
		return
	
	if text and status == 'Leavelist':
		regExNu = re.findall("^https:\/\/t\.me\/addlist\/([a-zA-Z0-9_]+)$", text);
		if len(regExNu) > 0:
			opID = makeKey();

			LL = text

			await event.reply(ExtraTexts['ListLeave'], parse_mode='md', buttons=bt_cancle);
			set(opID,'owner', from_id, 'database/list.json');
			set(opID,'linklists', LL, 'database/list.json');
			run_script(f"python3 control.py LeaveList {opID} {text} {from_id}");
			#subprocess.Popen(["python3", "control.py", "LeaveList", text, from_id]);
		else:
			await event.reply(ExtraTexts['listcancle'], parse_mode='md', buttons=bt_back);
		return

	if text == '/check':
		###run_script(f"python3 control.py check {from_id}");
		subprocess.Popen(["python3", "control.py", "check",from_id]);
		await event.reply(checking.replace('++COUNT++',str(cSessions)));
		
	if text and status == 'viewUrl':
		regExNu   = re.findall("^https?:\/\/t\.me\/([a-zA-Z0-9_]+)\/([0-9]+)",text);
		if len(regExNu) > 0:
			UNC    = '@'+str(regExNu[0][0]);
			IDC      = regExNu[0][1];
			set(from_id,'username_view',UNC,'database/mover.json');
			set(from_id,'ID_view',IDC,'database/mover.json');
			set(from_id,'status','viewCount','database/mover.json');
			await event.reply(ExtraTexts['ViewCount'],buttons=bt_cancle,parse_mode='md');
			return
	
	if text and status == 'viewCount':
		regExNu   = re.findall("^[0-9]+$",text);
		if len(regExNu) > 0:
			ugn    = get(from_id,'username_view','database/mover.json');
			idn      = get(from_id,'ID_view','database/mover.json');
			await event.reply(ExtraTexts['Viewing'],buttons=bt_back,parse_mode='md');
			subprocess.Popen(["python3", "control.py", "View", ugn, idn, text, from_id]);
			delete(from_id,None,'database/mover.json');
			return
	
			
	if text and status == 'leave':
		regExNu   = re.findall("^\-[0-9]+",text);
		if len(regExNu) > 0:
			await event.reply(ExtraTexts['Leaved'],buttons=bt_back);
			subprocess.Popen(["python3", "control.py", "leaveChat", text]);
			delete(from_id,None,'database/mover.json');
	
	if text and status == 'support':
		test_url    = URLc(text);
		if test_url is not False:
			await event.reply(send_sup_count.replace('++URL++',test_url[1]),parse_mode='md',buttons=bt_cancle);
			set(from_id,'status','select_sup_members','database/mover.json');
			set(from_id,'username_sup',test_url[1],'database/mover.json');
		else:
			await event.reply(try_send_url+to_cancle);
		return
	if text and status == 'select_sup_members':
		regExNu   = re.findall("^[0-9]+",text);
		if len(regExNu) > 0:
			opID       = makeKey();
			set(opID,'owner',from_id,'database/support.json');
			set(opID,'requested_count',text,'database/support.json');
			set(opID,'supported_username',get(from_id,'username_sup','database/mover.json'),'database/support.json');
			run_script(f"python3 control.py joining {opID}");
			delete(from_id,None,'database/mover.json');
		else:
			await event.reply(try_send_int,parse_mode='md',buttons=bt_cancle);
		return


client.run_until_disconnected();


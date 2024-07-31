from pyrogram import Client , utils, filters, compose
from pyrogram.raw import functions, types, base
import sys, time
import asyncio
import json
import configparser
from time import sleep
import uvloop
import requests
from pyrogram.errors import FloodWait, UserPrivacyRestricted, UserRestricted, PeerFlood, UserNotMutualContact, UserChannelsTooMuch
from pyrogram.raw.functions.chatlists import CheckChatlistInvite, JoinChatlistInvite,LeaveChatlist
from pyrogram.raw.types import InputChatlistDialogFilter
from database import *
from pyrogram.utils import get_peer_id
from pyrogram.raw.base import input_peer
from pyrogram.raw.functions.messages import AddChatUser

opreat      = sys.argv[1];
opreats    = ['left','check','send','joining','CX','View','joinlist','leavelist','likee','like','Poll','reaction', 'leavess'];
LIST_DONE    = "✅ تم اضافة المجلد بنجاح\nرابط المجلد  : ++CC++\nعدد الحسابات التي اضافة المجلد بنجاح ++ADD++ من اصل ++ALL++";
LEAVE_RUN    = "جاري حذف المجلد...... ♻️\n عدد الحسابات التي حذفت المجلد بنجاح لحد الان ++LEA++ حساب من اصل ++ALL++ حساب ✅.";
LEAVE_DONE   = "تم الانتهاء من عملية حذف المجلد بنجاح ✅\nعدد الحسابات الذي حذفت المجلد بدون مشاكل ++LEA++ حساب من أصل ++ALL++ حساب 😊.";
JOINED       = "🎢 جاري اضافة المجلد....\n♻️ يتم اضافة المجلد ++CC++ من جميع الحسابات المتاحة\n✅ تم اضافة المجلد بنجاح من ++ADD++ حساب";



if opreat not in opreats:
	exit();

ses    = sys.argv[2].split('.')[0];



config = configparser.ConfigParser()
config.read("config.ini")



api_id       = config['owner']['id'];
api_hash = config['owner']['hash'];
token	= config['API_KEYs']['mover'];

sessions	      = os.listdir('sessions');
random.shuffle(sessions);
THE_SESSIONS = os.listdir('sessions');
cSessions	   = len(THE_SESSIONS);




def sendMessage(chat_id, text):
	URL	  = "https://api.telegram.org/bot"+token+"/sendmessage"
	PARAMS = {'chat_id': chat_id, 'text': text}
	RGET       = requests.get(url=URL, params=PARAMS);
	return json.loads(RGET.text)

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


async def join_chatlist(client, invite):
	hash = invite.split("/")[-1]
	chats = await client.invoke(CheckChatlistInvite(slug=hash))
	await client.invoke(
		JoinChatlistInvite(
			slug=hash,
			peers=[await client.resolve_peer(get_peer_id(c)) for c in chats.peers]
		)
	)

async def leave_chatlist(client, invite):
  hash = invite.split('/')[-1]
  info = await client.invoke(CheckChatlistInvite(slug=hash))
  await client.invoke(
	LeaveChatlist( chatlist=InputChatlistDialogFilter(filter_id=info.filter_id),
	  peers=[await client.resolve_peer(get_peer_id(c)) for c in info.already_peers]
	)
  )

async def leave_all_chats(acc):
	async for dialog in acc.get_dialogs():
		chat_type = dialog.chat.type.value
		print(chat_type)
		if chat_type == "channel" or chat_type == "group" or chat_type == "supergroup":
			iD = str(dialog.chat.id)
			await acc.leave_chat(iD)


async def Controll():
	try:
		app	  = Client(f"sessions/{ses}",api_id=api_id, api_hash=api_hash);		connect  = await app.connect();

		if opreat == 'check':
			try:
				await app.get_me();
				print('true');
			except:
				print('false');

		await app.get_me();
	except Exception as Errors:
		RESPONSE      = str(Errors).replace('Telegram says: ', '').split(' - ')[0];

		if RESPONSE in ['[401 AUTH_KEY_UNREGISTERED]', '[401 USER_DEACTIVATED]', '[401 USER_DEACTIVATED_BAN]', '[401 SESSION_REVOKED]']:
			try:
				print('deleted');
				os.remove(f"sessions/{ses}.session");
			except:
				pass
		if opreat == 'check':
			print(RESPONSE);
		print('false',Errors);
		connect   = False;
		#print(ses);
		return
	if not connect:
		print('NO_CONNECTED');
		return

	try:
		await app.invoke(functions.account.UpdateStatus(
			offline=False
		));
	except:
		pass

	if opreat == 'CX':
		
		UNChat     = "phpmm"
		IDsUsers    = [];
		ListUsers   = [];
		
		async for message in app.get_chat_history(UNChat):
			if message.from_user.username is not None:
				print(message.from_user.username);


	
	
			       
	if opreat == 'left':
		leaveID   = int(sys.argv[3]);
		leaveID2 = int(sys.argv[4]);

		try:
			await app.leave_chat(leaveID);
			if leaveID != leaveID2:
				await app.leave_chat(leaveID2);
			print('true');
		except Exception as Error:
			print('false',Error);
			pass
		pass
	
	
	if opreat == 'View':
		chID    = str(sys.argv[3]);
		mgID   = int(sys.argv[4]);
		awr    = await app.resolve_peer(chID),
		rdd     = await app.invoke(
			functions.messages.GetMessagesViews(
				peer=await app.resolve_peer(chID),
				id=[mgID],
				increment=True
			)
		)

	if opreat == 'reaction':
		CHID = str(sys.argv[3])
		MSID = int(sys.argv[4])
		U = str(sys.argv[5])
		await app.send_reaction(CHID, MSID, U)
		


	if opreat == 'Poll':
		CHID = str(sys.argv[3])
		MSID = int(sys.argv[4])
		U = int(sys.argv[5])
		await app.vote_poll(CHID, MSID, U)

	if opreat == 'like':
		CHID = str(sys.argv[3])
		MSID = int(sys.argv[4])
		owner = int(sys.argv[5])
		try:
			a = await app.join_chat(CHID)
			b = await app.get_messages(CHID, message_ids=MSID)
			await b.click(0)
			sleep(1)
			print('true')
		except Exception as e:
			sendMessage(owner, f" error {e}")

	if opreat == 'leavess':
		seee = sys.argv[2]
		try:
			done = 0;bad = 0
			await leave_all_chats(app)
			done += 1
			print(['true'])
		except Exception as e:
				bad += 1
				print(['false', e])	

	if opreat == 'likee':
		LINK = str(sys.argv[3])
		MSID = int(sys.argv[4])
		owner = int(sys.argv[5])
		try:
			C = await app.join_chat(LINK)
			IDD = C.id
			print(IDD)
			D = await app.get_messages(IDD, message_ids=MSID)
			await D.click(0)
			sleep(2)
		except Exception as e:
			sendMessage(owner, f" error {e}")
		
	
	
	if opreat == 'send':
		senderID	= sys.argv[3];
		messageID   = sys.argv[4];
		recivedID       = sys.argv[5];
		try:
			await app.copy_message(recivedID,senderID,messageID);
			print('true');
		except FloodWait as Error:
			print('flood');
		except UserRestricted as Error:
			print('continue');
		except PeerFlood as Error:
			print('flood');
		except Exception as Errors:
			print(Errors,'all');
		pass
	
	if opreat == 'joinlist':
		

		opreatID = sys.argv[4];
		listL = sys.argv[3];
		owner = sys.argv[5];
		LID = sys.argv[6];
		SEL = sys.argv[2];
		#apps = sys.argv[2]
		#apps = SEL


		try:
			done = 0;bad = 0
			SEEE = cSessions

			await join_chatlist(app,listL)
			done += 1
			print(['true'])
		except Exception as e:
				bad += 1
				print(['false', e])
		except:
			TEXT = "- حدث خطا اثناء الدخول الى المجلد ❗"
			sendMessage(owner,TEXT)
			pass
				
				
	if opreat == 'leavelist':

		listE = sys.argv[3];
		opreatID = sys.argv[4];
		owner = sys.argv[5];
		SED = sys.argv[2];


		try:
			done = 0;
			bad = 0;
			await leave_chatlist(app,listE)
			done += 1
			print(['true'])
		except Exception as e:
			bad += 1
			print(['false', e])
		except:
			TEXT = "- حدث خطا اثناء الخروج من المجلد ❗"
			sendMessage(owner,TEXT)
			pass

	if opreat == 'joining':
		username     = sys.argv[3];
		try:
			join_to_username    = await app.join_chat(username);
			joining_id                    = join_to_username.id;
			print(['true',joining_id]);
		except Exception as prim:
			print(['false',prim]);
		pass
			
	if opreat == 'CX':
		
		UNChat     = "phpmm"
		IDsUsers    = [];
		ListUsers   = [];
		
		async for message in app.get_chat_history(UNChat):
			if message.from_user.id not in IDsUsers:
				IDsUsers.append(message.from_user.id);
				if message.from_user.username is not None:
					ListUsers.append(message.from_user.username)
				elif message.from_user.phone_number is not None:
					ListUsers.append(message.from_user.phone_number)
		print("Useranames\n\n");
		print(ListUsers);

asyncio.get_event_loop().run_until_complete(Controll());


uvloop.install()

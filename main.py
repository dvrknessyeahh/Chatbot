import amanobot
import amanobot.namedtuple
from amanobot.namedtuple import File, InlineKeyboardMarkup, InlineKeyboardButton
from amanobot.namedtuple import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, ForceReply
import random
import requests
from bs4 import BeautifulSoup
import time
import os
import json
from glob import glob
import pytz
from datetime import datetime
from config import TOKEN, ADMIN, OWNER, CHANNEL, GROUP, PROJECT_NAME

token = TOKEN
bot = amanobot.Bot(token)

queue = {
	"free":[],
	"occupied":{}
}
users = []
user3 = []

def saveConfig(data):
	return open('app.json', 'w').write(json.dumps(data))

if __name__ == '__main__':
	s = time.time()
	print(f'[#] Buatan\n[i] Created by @{OWNER}\n')
	print('[#] mengecek config...')
	if not os.path.isfile('app.json'):
		print('[#] memebuat config file...')
		open('app.json', 'w').write('{}')
		print('[#] Done')
	else:
		print('[#] Config found!')
	print('[i] Bot online ' + str(time.time() - s) + 's')
def exList(list, par):
	a = list
	a.remove(par)
	return a

def handle(update):
		
	global queue
	try:
		config = json.loads(open('app.json', 'r').read())
		if 'text' in update:
			text = update["text"]
		else:
			text = ""
		uid = update["chat"]["id"]
		
		if uid not in user3:
			users.append(uid)
		
		if not uid in config and text != "/nopics":
			config[str(uid)] = {"pics":True}
			saveConfig(config)

		if uid in queue["occupied"]:
			if 'text' in update:
				if text != "/exit" and text != "❌ Exit" and text != "Next ▶️" and text != "/next":
					bot.sendMessage(queue["occupied"][uid], "" + text)
			
			if 'photo' in update:
				photo = update['photo'][0]['file_id']
				bot.sendPhoto(queue["occupied"][uid], photo, caption=captionphoto)
                                
			if 'video' in update:
				video = update['video']['file_id']
				bot.sendVideo(queue["occupied"][uid], video, caption=captionvideo)
			
			if 'document' in update:
				document = update['document']['file_id']
				bot.sendDocument(queue["occupied"][uid], document, caption=captionducument)
				
			if 'audio' in update:
				audio = update['audio']['file_id']
				bot.sendAudio(queue["occupied"][uid], audio, caption=captionaudio)
				
			if 'video_note' in update:
				video_note = update['video_note']['file_id']
				bot.sendVideoNote(queue["occupied"][uid], video_note)
			        
			if 'voice' in update:
				voice = update['voice']['file_id']
				bot.sendVoice(queue["occupied"][uid], voice, caption=captionvoice)
                                
			if 'sticker' in update:
				sticker = update['sticker']['file_id']
				bot.sendSticker(queue["occupied"][uid], sticker)

			if 'contact' in update:
				nama = update["contact"]["first_name"]
				contact = update['contact']['phone_number']
				bot.sendContact(queue["occupied"][uid], contact, first_name=nama, last_name=None)
		                

		if text == "/start" or text == "/refresh":
			if not uid in queue["occupied"]:
				keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="👨‍💻Owner", url=f"https://t.me/{OWNER}"),InlineKeyboardButton(text="💬Grup", url=f"https://t.me/{GROUP}"),InlineKeyboardButton(text="📣Channel", url=f"https://t.me/{CHANNEL}")]])
				bot.sendMessage(uid, f"👋🏻 Hai, Selamat Datang Di {PROJECT_NAME} \n\n💬 Untuk mencari teman obrolan gunakan perintah /search pada bot_\n\n*Selamat Mencari!* 🥳", parse_mode='MarkDown', disable_web_page_preview=True , reply_markup=keyboard)
		if 'message_id' in update:
			if not uid in queue["occupied"]:
				if text != "/start" and text !="Next ▶️" and text != "/refresh" and text != "/help" and text != "/search" and text != "Search 🔍" and text != "🛠 MENU BOT" and text != "🔙 Main Menu" and text != "Info Profile 📌"  and text != "/user":
					news = ReplyKeyboardRemove()
					bot.sendMessage(uid, "🤖 *Bot :* _Maap kamu sedang tidak dalam obrolan\nSilahkan Klik /refresh atau /search pada bot_", parse_mode="MarkDown",reply_markup=news, reply_to_message_id=update['message_id'])
		

		if text == "/test":
			if not uid in queue["occupied"]:
				lolt = ReplyKeyboardMarkup(keyboard=[
                    ['Plain text', KeyboardButton(text='Text only')],
					[dict(text='phone', request_contact=True), KeyboardButton(text='Location', request_location=True)]], resize_keyboard=True)
				bot.sendMessage(uid, "contoh", reply_markup=lolt)

		elif text == 'Search 🔍' or text == "/search":
			if not uid in queue["occupied"]:
				keyboard = ReplyKeyboardRemove()
				bot.sendMessage(uid, '🤖 *Bot :* 🔍 _Sedang mencari lawan ngobrol kamu..._',parse_mode='MarkDown', reply_markup=keyboard)
				print("[SB] " + str(uid) + " Join ke obrolan")
				queue["free"].append(uid)

		elif text == '❌ Exit' or text == '/exit' and uid in queue["occupied"]:
			print('[SB] ' + str(uid) + ' meninggalkan jodohnya ' + str(queue["occupied"][uid]))
			keyboard = ReplyKeyboardMarkup(keyboard=[['Search 🔍'],['Menu Bot 🛠']], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, "🤖 *Bot :* ❌ _Kamu keluar dari obrolan_", parse_mode='MarkDown', reply_markup=keyboard)
			bot.sendMessage(queue["occupied"][uid], "🤖 *Bot :* ❌ _Lawan ngobrol keluar dari obrolan_", parse_mode='MarkDown', reply_markup=keyboard)
			del queue["occupied"][queue["occupied"][uid]]
			del queue["occupied"][uid]

		elif text == 'Menu Bot 🛠':
			keyboard = ReplyKeyboardMarkup(keyboard=[
				['Info Profile 📌'],['Main Menu 🔙']
			], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, f"🛠 *Menu Bot*\n\n_Hai Kalian Kami Menyediakan Menu Bot Yang Bikin Kalian Senang , Gabung Group Support Kami Agar Kami Meng Update Fitur Lebih Keren Lagi_\n\n*Group Support :* [{GROUP}](https://t.me/{GROUP})", reply_markup=keyboard)
			
		elif text == 'Main Menu 🔙':
			keyboard = ReplyKeyboardMarkup(keyboard=[['Search 🔍'],['Menu Bot 🛠']], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, "_🔄 Kembali_", parse_mode='MarkDown', disable_web_page_preview=True, reply_markup=keyboard)
		elif text == "Next ▶️" or text == "/next" and uid in queue["occupied"]:
			print('[SB] ' + str(uid) + ' meninggalkan obrolan dengan ' + str(queue["occupied"][uid]))
			keyboard = ReplyKeyboardMarkup(keyboard=[['Search 🔍', 'Main Menu 🔙']], resize_keyboard=True, one_time_keyboard=True)
			bot.sendMessage(uid, "🤖 *Bot :* ❌ _Kamu keluar dari obrolan_",parse_mode="MarkDown")
			bot.sendMessage(queue["occupied"][uid], "🤖 *Bot :* ❌ _Lawan ngobrol keluar dari obrolan_",parse_mode="MarkDown", reply_markup=keyboard)
			del queue["occupied"][queue["occupied"][uid]]
			del queue["occupied"][uid] 
			if not uid in queue["occupied"]:
				key = ReplyKeyboardRemove()
				bot.sendMessage(uid, '🤖 *Bot :* 🔍 _Melewati lawan ngobrol kamu..._',parse_mode="MarkDown" ,reply_markup=key)
				print("[SB] " + str(uid) + " Join ke obrolan") 
				queue["free"].append(uid)
		
		if text == "/nopics":
			config[str(uid)]["pics"] = not config[str(uid)]["pics"] 
			if config[str(uid)]["pics"]:
				bot.sendMessage(uid, "🤖 *Bot :* Lawan Ngobrol Bisa Mengirim Foto")
			else:
				bot.sendMessage(uid, "🤖 *Bot :* Lawan Ngobrol Tidak Bisa Mengirim Foto")
			saveConfig(config)

		if len(queue["free"]) > 1 and not uid in queue["occupied"]:
			partner = random.choice(exList(queue["free"], uid))
			if partner != uid:
				keyboard = ReplyKeyboardMarkup(keyboard=[
					['Next ▶️', '❌ Exit'],[dict(text='Send my phone', request_contact=True)]
				],resize_keyboard=True, one_time_keyboard=True)
				print('[SB] ' + str(uid) + ' Berjodoh dengan ' + str(partner))
				queue["free"].remove(partner)
				queue["occupied"][uid] = partner
				queue["occupied"][partner] = uid
				bot.sendMessage(uid, '🤖 *Bot :* 🎉 _Selamat Pasangan kamu telah ditemukan..._\n\n⚠️ *PERINGATAN UNTUK ANDA* ⚠️\n_Jangan Chat Yang Membahas Tentang Porn, psikopat, LGBT, melecehkan, dan penghinaan agama, jika ada yang seperti itu , silahkan lapor admin aja ya_\n\n*Owner :* _@{OWNER}_\n*Selamat Chat!*',parse_mode='MarkDown', reply_markup=keyboard)
				bot.sendMessage(partner, '🤖 *Bot :* 🎉 _Selamat Pasangan kamu telah ditemukan..._\n\n⚠️ *PERINGATAN UNTUK ANDA* ⚠️\n_Jangan Chat Yang Membahas Tentang Porn, psikopat, LGBT, melecehkan, dan penghinaan agama, jika ada yang seperti itu , silahkan lapor admin aja ya_\n\n*Owner :* _@{OWNER}_\n*Selamat Chat!*',parse_mode='MarkDown', reply_markup=keyboard)
	except 	Exception as e:
		print('[!] Error: ' + str(e))

if __name__ == '__main__':
	bot.message_loop(handle)

	while 1:
		time.sleep(3)

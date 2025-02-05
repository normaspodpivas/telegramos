# -*- coding: utf-8 -*-
from telethon import TelegramClient, events
from random import choice as _choice
import asyncio
from datetime import datetime, timedelta
import os
import requests
import chardet
import io
from telethon import types, functions
import psutil
from telethon import TelegramClient, events



class TelegramAutoreplyBot():


	def __init__(self):
		self.api_id: int = 21390123
		self.api_hash: str = '194b2c8f0d8ac59cd757a18d5c59f8e7'
		self.phone: int = 79292416255
		self.client: TelegramClient = TelegramClient("autoreply_bot", self.api_id, self.api_hash, system_version='4.16.30-vxRedme', device_model='Redme note 8', app_version='10.6.1')
		self.client.start(self.phone)
		self.users: dict = {}
		self.ran: dict = {}
		self.run_file: str = ""
		self.rundom_photo: str = None
		self.rundom_file: str = ""
		self.running_users: list = []
		self.start_time: datetime = datetime.now()
		self.state: int = 0
		self.time: int = 0
		self.uptime: bool = False
		self.states: dict = {"spamone": {}}
		self.chats: dict = {}
		self.dir: str = "shablons/"
		self.album: dict = {"images": [], "count": 0, "count_photos": 0}


	def run(self):


		async def schedule(msg, time_sleep: int, chat_id: int, count_photos: int, file_name: str, header: str):
			await asyncio.sleep(5)
			state = 0
			if count_photos != len(self.album["images"]):
				await msg.edit(
					f"<b>Погодите, для чего вы ввели число <code>{count_photos}</code>, если в сообщении <code>{len(self.album['images'])}</code> фотографий ?</b>",
					parse_mode='html'
				)
				self.album["images"]: list = []
				return
			if len(self.album['images']) < count_photos:
				await msg.edit(
					"<b>Для чего вы отправили фотографий меньше заданного числа ?</b>",
					parse_mode='html'
				)
				self.album["images"]: list = []
				return

			orig_time: int = time_sleep
			me = await self.client.get_me()
			while True:
				if len(self.album["images"]) >= count_photos:
					try:
						for i in range(99):
							await self.client.send_message(
								chat_id,
								f"{header} {_choice(list(open(f'{self.dir}{file_name}', encoding='utf8')))}",
								file=None if self.album["images"] == [] else self.album["images"],
								schedule=timedelta(minutes=time_sleep),
							)
							state+=1
							if state >= 99:
								await self.client.send_message(
									me.id,
									f".mediarun {orig_time} {chat_id.id} {count_photos} {file_name} {header}",
									file=None if self.album["images"] == [] else self.album["images"],
									schedule=timedelta(minutes=time_sleep),
								)
							time_sleep+=orig_time
							await asyncio.sleep(0.2)

						self.album["images"]: list = []
						self.album["count_photos"]: int = 0
						self.album["count"]: int = 0
						break
					except Exception:
						if state != 99:
							await self.client.send_message(
								me.id,
								f".mediarun {orig_time} {chat_id.id} {count_photos} {file_name} {header}",
								file=None if self.album["images"] == [] else self.album["images"],
								schedule=timedelta(minutes=time_sleep),
							)
						self.album["images"]: list = []
						self.album["count_photos"]: int = 0
						self.album["count"]: int = 0
						break
				else:
					continue


		async def rundomrun_users_handler(msg, file_name):
			try:

				await asyncio.sleep(self.time)

				text: str = _choice(list(open(file_name, encoding='utf8')))
				await msg.reply(
					text,
					file=self.rundom_photo
				)
			except Exception:
				pass

		async def running_users_handler(msg, time, file_name, photo):
			try:
				await asyncio.sleep(time)

				text: str = _choice(list(open(file_name, encoding='utf8')))

				await msg.reply(
					text,
					file=photo
				)
			except Exception:
				pass
		


		@self.client.on(events.NewMessage(pattern=r'\.take'))
		async def delete_scheduled_messages(msg):
			try:
				_M_args: list = msg.message.message.split(maxsplit=1)[1]
			except IndexError:
				return await msg.edit(
					"<b>Введите аргументы</b>",
					parse_mode='html'
				)

			try:
				if _M_args:
					_M_chat_id: int = int(_M_args.split()[0])
					_M_chat = await self.client.get_entity(_M_chat_id)
					
					_M_messages = await self.client(functions.messages.GetScheduledHistoryRequest(
						peer=_M_chat,
						hash=0
					))

					for _M_message in _M_messages.messages:
						await asyncio.sleep(0.1)
						await self.client(functions.messages.DeleteScheduledMessagesRequest(
							peer=_M_chat,
							id=[_M_message.id]
						))

					entity = ''
					
					try:
						entity = _M_chat.first_name
					except Exception:
						entity = _M_chat.title

					await msg.edit(
						"<b>Удалил отложенные сообщения в чате: <code>{}</code> [<code>{}</code>]</b>".format(entity, _M_chat_id),
						parse_mode='html'
					)

			except Exception as e:
				print(e)
				


		@self.client.on(events.NewMessage(pattern=r'\.ran'))
		async def ran_handler(msg):
			_M_chat_id = msg.chat_id
			try:
				_M_args: list = msg.message.message.split(maxsplit=1)[1]
			except IndexError:
				if _M_chat_id not in self.ran:
					return await msg.edit(
						"<b>Укажите аргументы</b>",
						parse_mode='html'
					)
				else:
					del self.ran[_M_chat_id]
					return await msg.delete()
			try:
				link = None
				if msg.message.photo:
					_M_photo = msg.message.photo
					_M_photo_file_name = msg.date
					_M_file = await self.client.download_media(_M_photo, "ran_config/")
					url = "https://telegra.ph/upload"
					files = {'file': ('image.jpg', open(_M_file, 'rb'))}
					response = requests.post(url, files=files)
					if response.status_code != 200:
						return
					link = 'https://telegra.ph' + response.json()[0]['src']
					_M_file_obj = files["file"][1]
					_M_file_obj.close()
					print(f"фото {_M_file}.jpg скачано.")
					print(_M_file)

				_M_files = os.listdir("ran_config/")

				for _M_file in _M_files:
					_M_file_path = os.path.join("ran_config/", _M_file)
					if os.path.isfile(_M_file_path):
						os.remove(_M_file_path)
						print("файл {} успешно удален".format(_M_file))

					
				if _M_args:
					_M_file_name: str = str(_M_args.split()[0])
					_M_header: str = ' '.join(_M_args.split()[1:])

					self.ran[_M_chat_id]: bool = True

					await msg.delete()
					await asyncio.sleep(3)

					if self.ran[_M_chat_id] is True and isinstance(self.ran[_M_chat_id], bool):
						while self.ran[_M_chat_id]:
							if self.ran[_M_chat_id] is False:
								_M_file_name = ''
								break
							_M_template: str = _choice(list(open(f"{self.dir}{_M_file_name}", encoding='utf8')))
							if self.ran[_M_chat_id] is True:

								await self.client.send_message(
									_M_chat_id,
									_M_header+" "+_M_template,
									file=link
								)
								await asyncio.sleep(1500)
						

			except Exception as e:
				print(e)





		@self.client.on(events.NewMessage(pattern=r'\!uptime'))
		async def uptime_handler(msg):
			me = await self.client.get_me()
			if msg.sender_id == me.id:
				if self.uptime:
					await msg.edit(
						"<b>[Uptime]: Off</b>",
						parse_mode='html'
					)
					self.uptime = False
				else:
					await msg.edit(
						"<b>[Uptime]: on</b>",
						parse_mode='html'
					)
					self.uptime = True

		@self.client.on(events.NewMessage(pattern=r'\.idfav'))
		async def get_id(msg):
			me = await self.client.get_me()
			if msg.sender_id == me.id:
				reply = await msg.get_reply_message()
				msg_id = reply.id if reply else "Reply None"
				await msg.delete()
				try:
					chat = await self.client.get_entity(msg.chat_id)
					await self.client.send_message(
						me.id,
						f"<b>Название чата: <code>{chat.title}</code>\nID чата: <code>{msg.chat_id}</code>\nID Сообщения: <code>{msg_id}</code></b>",
						parse_mode='html'
					)
				except Exception:
					user = await self.client.get_entity(msg.chat_id)
					await self.client.send_message(
						me.id,
						f"<b>Название чата: <code>{user.first_name}</code>\nID чата: <code>{msg.chat_id}</code>\nID Сообщения: <code>{msg_id}</code></b>",
						parse_mode='html'
					)
			else:
				...


		@self.client.on(events.NewMessage(pattern=r'\.spamone'))
		async def spam_handler(msg):
			me = await self.client.get_me()
			if msg.sender_id == me.id:
				try:
					args: list = msg.message.message.split(maxsplit=1)[1]
				except IndexError:
					return await msg.edit(
						'<b>Укажите аргументы</b>',
						parse_mode='html'
					)
				try:
					if args:
						time_sleep: int = int(args.split()[0])
						chat_id: int = int(args.split()[1])
						user_id: int = int(args.split()[2])
						file_name: str = str(args.split()[3])
						photo = None if str(args.split()[4]) == '0' else str(args.split()[4])
						header: str = " ".join(args.split()[5:])
						time: datetime = datetime.now()
						self.states["spamone"][chat_id]: bool = True
						chat_entity = ''
						chat = await self.client.get_entity(chat_id)
						try:
							chat_entity = chat.title
						except Exception:
							chat_entity = chat.first_name
						try:

							users = await self.client.get_entity(user_id)
						except Exception:
							users = None
						user_entity = ''
						try:
							user_entity = users.first_name if users is not None else "None"
						except Exception:
							user_entity = users.title if users is not None else "None"

						await msg.edit(
							f"<b>Запустил в чате: <code>{chat_entity}</code> [<code>{chat_id}</code>]\nНа юзера: <code>{user_entity}</code> [<code>{user_id}</code>]\nЧтобы вырубить: <code>.oneoff spamone {chat_id}</code></b>",
							parse_mode='html'
						)
							

							

							

						if self.states["spamone"][chat_id] is True and isinstance(self.states["spamone"][chat_id], bool):
							while True:
								if self.states["spamone"][chat_id] is False and isinstance(self.states["spamone"][chat_id], bool):
									del self.states["spamone"][chat_id]
									break
								if self.states["spamone"][chat_id] is True:

									if self.uptime:
										time_now: datetime = datetime.now()
										timing = time_now - time
										time_string: str = str(timing)
										time_result: list = time_string.split('.')[0]
										await self.client.send_message(
											chat_id,
											f"[<code>{time_result}</code>] <a href='tg://user?id={user_id}'>{header} {_choice(list(open(f'{self.dir}{file_name}', encoding='utf8')))}</a>",
											file=photo,
											parse_mode="html"
										)

									else:

										await self.client.send_message(
											chat_id,
											f"<a href='tg://user?id={user_id}'>{header} {_choice(list(open(f'{self.dir}{file_name}', encoding='utf8')))}</a>",
											file=photo,
											parse_mode="html"
										)
									await asyncio.sleep(time_sleep)

				except Exception:
					pass

		@self.client.on(events.NewMessage(pattern=r'\.ges'))
		async def ges_handler(msg):
			me = await self.client.get_me()
			if msg.sender_id == me.id:

				try:
					args: list = msg.message.message.split(maxsplit=1)[1]
				except IndexError:
					return await msg.edit(
						"<b>Укажите аргументы</b>",
						parse_mode='html'
					)

				try:

					if args:

						time_sleep: int = int(args.split()[0])
						chat_id: int = int(args.split()[1])
						message_id: int = int(args.split()[2])
						file_name: str = str(args.split()[3])
						photo = None if str(args.split()[4]) == '0' else str(args.split()[4])
						header: str = " ".join(args.split()[5:])

						self.chats[message_id]: bool = True

						chat_title = ""
						chat = await self.client.get_entity(chat_id)

						try:
							chat_title = chat.title
						except Exception:
							chat_title = chat.first_name

						await msg.edit(
							f"<b>Запустил в чате: <code>{chat_title}</code> [<code>{chat_id}</code>]\nНа сообщение: <code>{message_id}</code>\nЧтобы выключить: <code>.oneoff ges {message_id}</code></b>",
							parse_mode='html'
						)

						if self.chats[message_id] is True and isinstance(self.chats[message_id], bool):
							while True:
								if self.chats[message_id] is False and isinstance(self.chats[message_id], bool):
									del self.chats[message_id]
									break
								if self.chats[message_id] is True:
										
									await self.client.send_message(
										chat_id,
										f"{header} {_choice(list(open(f'{self.dir}{file_name}', encoding='utf8')))}",
										file=photo,
										reply_to=message_id
									)
									await asyncio.sleep(time_sleep)
				except Exception:
					pass



		@self.client.on(events.NewMessage(pattern=r'\.mediarun'))
		async def calendar_handler(msg):
			self.album["images"]: list = []
			me = await self.client.get_me()
			if msg.sender_id == me.id:
				try:
					args: list = msg.message.message.split(maxsplit=1)[1]
				except IndexError:
					return await msg.edit(
						"<b>Укажите аргументы</b>",
						parse_mode='html'
					)
				try:

					if args:

						if msg.chat_id != me.id:
							return await msg.edit(
								"<b>Данную команду можно использовать лишь в избранном</b>",
								parse_mode='html'
							)
						time_sleep: int = int(args.split()[0])
						orig_time: int = time_sleep
						chat_id: int = int(args.split()[1])
						count_photos: int = int(args.split()[2])
						file_name: str = str(args.split()[3])
						header: str = " ".join(args.split()[4:])
						chat = await self.client.get_entity(chat_id)
						entity = ''
						try:
							entity = chat.title
							chat_id = chat
						except Exception:
							entity = chat.first_name
							chat_id = chat
						
						if count_photos != 0:
							if msg.media:
								await msg.edit(
									"<b>Пополнил в чате: <code>{}</code> [<code>{}</code>]</b>".format(entity, chat_id.id),
									parse_mode='html'
								)
								self.album["count"]: int = count_photos
							else:
								return await msg.edit(
									"<b>Не вижу фотографий</b>",
									parse_mode='html'
								)
						else:
							if msg.media:
								return await msg.edit(
									"<b>Вижу фотографии, однако почему значение <code>0</code> ?</b>",
									parse_mode='html'
								)
							else:
								await msg.edit(
									f"<b>Отложенные сообщения заполнены в чате: <code>{entity}</code> [<code>{chat_id.id}</code>]",
									parse_mode='html'
								)
								
						asyncio.create_task(schedule(msg, time_sleep, chat_id, count_photos, file_name, header))
				except Exception as e:
					print(e)

		@self.client.on(events.NewMessage(pattern=r'\.dict'))
		async def directory_handler(msg):
			me = await self.client.get_me()
			if msg.sender_id == me.id:

				file_list = os.listdir(self.dir)

				directory = "\n".join([f"<code>{files}</code>" for files in file_list])

				await msg.edit(
					"<b>directory:\n{}</b>".format(directory),
					parse_mode='html'
				)




		@self.client.on(events.NewMessage(pattern=r'\.goall'))
		async def rundomrun_handler(msg):
			try:
				args: msg = msg.message.message.split(maxsplit=1)[1]
			except IndexError:
				return await msg.edit(
					"<b>Укажите аргументы</b>",
					parse_mode='html'
				)

			if args:

				self.time = int(args.split()[0])

				self.rundom_file = self.dir + str(args.split()[1])
				self.rundom_photo = str(args.split()[2]) if str(args.split()[2]) != "0" else None				
				

				await msg.edit(
					"<b>Чтобы вырубить: <code>.oneoff goall</code></b>",
					parse_mode='html'
				)

				self.state = 1


		@self.client.on(events.NewMessage(pattern=r'\.letsgo'))
		async def running_handler(msg):
			try:
				args: msg = msg.message.message.split(maxsplit=1)[1]
			except IndexError:

				return await msg.edit(
					"<b>Write arguments</b>",
					parse_mode='html'
				)


			if args:

				time: int = int(args.split()[0])

				user_id: int = int(args.split()[1])

				file_name: str = str(args.split()[2])
				photo = None if str(args.split()[3]) == '0' else str(args.split()[3])
				user = await self.client.get_entity(user_id)
				if user_id not in self.running_users:

					await msg.edit(
						"<b>Запустил на юзера: <code>{}</code> [<code>{}</code>]\nЧтобы вырубить: <code>.oneoff letsgo {}</code></b>".format(user.first_name, user_id, user_id),
						parse_mode='html'
					)
					self.running_users.append(user_id)
					self.users[user_id]: dict = {"time_sleep": time, "file_name": f"{self.dir}{file_name}", "photo": photo, "function": None}
				else:

					await msg.edit(
						"<b>Данный пользователь уже в списке</b>",
						parse_mode='html'
					)

		@self.client.on(events.NewMessage(pattern=r'\.oneoff'))
		async def stop_handler(msg):
			try:
				args: msg = msg.message.message.split(maxsplit=1)[1]
			except IndexError:
				return await msg.edit(
					"<b>Укажите аргументы</b>",
					parse_mode='html'
				)

			if args:


				if str(args.split()[0]) == "goall":
					await msg.edit(
						"<b>Остановил во всех чатах</b>",
						parse_mode='html'
					)
					self.state = 0
					self.time = 0

				elif str(args.split()[0]) == "letsgo":
					user_id: int = int(args.split()[1])

					if user_id in self.running_users:
						...
					else:
						return await msg.edit(
							"<b>Данный ID не найден в словаре</b>",
							parse_mode='html'
						)

					entity = ''
					try:
						chat = await self.client.get_entity(user_id)
						entity = chat.title
					except Exception:
						user = await self.client.get_entity(user_id)
						entity = user.first_name
					await msg.edit(
						"<b>Выключил на юзера: <code>{}</code>\nID юзера: <code>{}</code>".format(entity, str(user_id)),
						parse_mode='html'
					)

					self.running_users.remove(user_id)
					del self.users[user_id]

				elif str(args.split()[0]) == "spamone":
					chat_id: int = int(args.split()[1])
					if chat_id in self.states["spamone"]:
						...
					else:
						return await msg.edit(
							"<b>Данный ID не найден в словаре</b>",
							parse_mode='html'
						)
					try:
						user = await self.client.get_entity(chat_id)
					except Exception:
						user = None


					entity = ''
					try:
						entity = user.first_name
					except Exception:
						entity = user.title
					await msg.edit(
						"<b>Вырубил в чате: <code>{}</code>\nID чата: <code>{}</code></b>".format(entity, user.id),
						parse_mode='html'
					)

					self.states["spamone"][chat_id] = False

				elif str(args.split()[0]) == "ges":
					message_id = int(args.split()[1])
					if message_id in self.chats:
						self.chats[message_id] = False
						await msg.edit(
							"<b>Остановлено на сообщение c ID: {} </b>".format(message_id),
							parse_mode='html'
						)
					else:
						return await msg.edit(
							"<b>Данный Message ID не найден в словаре.</b>",
							parse_mode='html'
						)


				else:
					await msg.edit(
						"<b>Действие не найдено</b>",
						parse_mode='html'
					)


		@self.client.on(events.NewMessage(pattern=r'\.ref'))
		async def get_media_link(msg):
			try:
				reply = await msg.get_reply_message()
				if not reply:
					return
				if reply.media and reply.photo:
					photo = reply.photo
					file_name = await reply.download_media("phots/")
					url = "https://telegra.ph/upload"
					files = {'file': ('image.jpg', open(file_name, 'rb'))}
					response = requests.post(url, files=files)
					if response.status_code != 200:
						return
					link = 'https://telegra.ph' + response.json()[0]['src']
					await msg.edit(f"<b>Ссылка на фото: <code>{link}</code></b>", parse_mode='html')
				elif reply.media and reply.video:
					video = reply.video
					file_name = await reply.download_media(f"phots/")
					url = "https://telegra.ph/upload"
					files = {"file": ("video.mp4", open(file_name, 'rb'))}
					responce = requests.post(url, files=files)
					if responce.status_code != 200:
						return
					link = "https://telegra.ph" + responce.json()[0]['src']
					await msg.edit(
						f"<b>Ссылка на видео: <code>{link}</code></b>",
						parse_mode='html'
					)

				files = os.listdir("phots/")

				for file in files:
					file_path = os.path.join("phots/", file)
					if os.path.isfile(file_path):
						os.remove(file_path)
						print("файл {} успешно удален".format(file))

			except Exception as e:
				print(e)



		@self.client.on(events.NewMessage(pattern=r'\.boot'))
		async def download_shablons_handler(msg):
			reply: msg = await msg.get_reply_message()
			if not reply:
				return await msg.edit(
					"<b>Не вижу реплая</b>",
					parse_mode='html'
				)

			if reply:

				file_name = reply.file.name

				_M_text_document = await reply.download_media(f"{self.dir}{file_name}")
				with open(_M_text_document, 'rb') as _M_file:
					_M_raw_data = _M_file.read()
					_M_result = chardet.detect(_M_raw_data)


					if "UTF-8" not in _M_result['encoding']:
						await msg.edit(
							"<b>Шаблон</b> <code>{}</code> <b>имеет недопустимую кодировку</b> <code>{}</code>\n<b>Изменяю кодировку...</b>".format(file_name, _M_result['encoding']),
							parse_mode='html'
						)
						await asyncio.sleep(3)
					
						_M_result_data = _M_raw_data.decode(_M_result['encoding'], 'ignore')
						_M_write_data = _M_result_data.encode("utf-8")
						with open(_M_text_document, 'wb') as f:
							f.write(_M_write_data)
							f.close()

						await msg.edit(
							"<b>Файл</b> <code>{}</code> <b>успешно загружен\nПреобразован с</b> <code>{}</code> <b>в</b> <code>UTF-8</code>".format(file_name, _M_result['encoding']),
							parse_mode='html'
						)

					else:
						await msg.edit(
							"<b>Файл <code>{}</code> успешно загружен.</b>".format(file_name),
							parse_mode='html'
						)
					

		@self.client.on(events.NewMessage(pattern=r'\.infobot'))
		async def infobot_handler(msg):
			me = await self.client.get_me()
			if msg.sender_id == me.id:
				await msg.delete()
				ph: list = _choice(["https://i.pinimg.com/736x/eb/ee/e1/ebeee14f931bf6db91f3b0f698a67f2c.jpg", "https://i.pinimg.com/736x/3c/bc/e1/3cbce1738c3d5b789ffcba785495a7db.jpg"])
				owner = await self.client.get_entity(me.id)
				chat = await self.client.get_entity(msg.chat_id)
				entity = ''
				try:
					entity = chat.first_name
				except Exception:
					entity = chat.title
				pc_uptime: psutil = int(psutil.boot_time())

				uptime_datetime = datetime.fromtimestamp(pc_uptime)

				current_time = datetime.now()


				uptime_timedelta = current_time - uptime_datetime
				await msg.respond(
					f"**▲▼▲ThinkingFucker HelpInfo▼▲▼**\n\n**☆Owner: `{owner.first_name}`**\n**☆Chat: `{entity}` [`{msg.chat_id}`]**\n**☆Uptime: `{uptime_timedelta.days}` Days**\n\n**✵`.idfav` `×` __ch/msg id пересылает в избранное__**\n**✵`.ref` `×` __реплай ph/vd/gf для url ссылки, до 5мб__**\n**✵`.boot` `×`__ скачать шаблон__**\n**✵`.dict` `×` __директория шаблонов__**\n**✵`.oneoff` action + ch/us/msg id `×` __выключение команд__**\n\n**✵`.goall` time + .txt + url `×` автоответ на реплай вас__**\n**✵`.letsgo` time + user id + .txt + url `×` __автоответчик на юзера__**\n\n**✵`.spamone` time + chat id + user id + .txt + url + header `×` __спам с тегом на юзера__**\n**✵`.ran` .txt + attach + header `×` __спам раз в 25 минут__**\n**✵`.ges` time + chat id + message id + .txt + url + header `×` __спам с реплаем на сообщение__**\n\n**✵`.mediarun` time + chat id + count of attached media + .txt + header `×` __календарь с автопополнением, команда в избранных, отложенные сообщения__**\n**✵`.take` chat id `×` __удаление календаря__**\n\n**✵`!uptime` `×` __приписывает время работы в начало команды__**",
					file=ph
				)
		
				
				
 



		@self.client.on(events.NewMessage())
		async def watcher(msg):
			try:
				me = await self.client.get_me()
				if msg.chat_id == me.id:
					if msg.sender_id == me.id:
						if self.album["count_photos"] == 0:
							self.album["images"]: list = []
						if msg.media:
							self.album["count_photos"]+=1
							self.album["images"].append(msg.media)
							return
					


					

				if msg.sender_id in self.running_users:

					if self.users[msg.sender_id]["function"]:

						self.users[msg.sender_id]["function"].cancel()

					self.users[msg.sender_id]["function"] = asyncio.create_task(running_users_handler(msg, self.users[msg.sender_id]["time_sleep"], self.users[msg.sender_id]["file_name"], self.users[msg.sender_id]["photo"]))

				else:
					...

				if self.state == 1:
					reply: msg = await msg.get_reply_message()
					me = await self.client.get_me()

					if reply.sender_id == me.id:

						asyncio.create_task(rundomrun_users_handler(msg, self.rundom_file))
			except Exception as e:
				print(e)

	def start(self):
		self.client.run_until_disconnected()
		

if __name__ == "__main__":
	bot: TelegramAutoreplyBot = TelegramAutoreplyBot()
	bot.run()
	bot.start()

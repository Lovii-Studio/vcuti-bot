"""BOT VCUTI"""
"""CREATE BY - TheLovii"""
"""TEAM - HALCYON TEAM"""
"""GITHUB - github.com/TheLovii TEAM GITHUB - github.com/Halcyon-Team"""

"""IMPORTS"""
import typing
import vkcoin
import random
import sqlite3 as sql
import ast
import time
from vkbottle import Bot, Message, keyboard_gen
from vkbottle.branch import Branch, ExitBranch

"""SETTINGS"""
owner_vkid = 0 # Your VKID
merchant = vkcoin.VKCoin(user_id=owner_vkid, # Ваш ID на котором есть VKCoins
						 key='') # Ключ апи VKCoins

connection = sql.connect("vcuti_datab.db")
cc = connection.cursor()

"""KEYBOARDS"""
pvk_list = [[{'text': '100000', 'color': 'secondary'}, {'text': '500000', 'color': 'secondary'},
			 {'text': '1000000', 'color': 'secondary'}],
			[{'text': '2000000', 'color': 'primary'}, {'text': '5000000', 'color': 'primary'}],
			[{'text': '10000000', 'color': 'positive'}, {'text': '50000000', 'color': 'positive'}],
			[{'text': 'Назад', 'color': 'negative'}]]
pvk_kb = keyboard_gen(pvk_list, one_time=True)

nzd_list = [[{'text': 'Назад', 'color': 'negative'}]]
nzd_kb = keyboard_gen(nzd_list, one_time=True)

"""LONGPOLL"""
bot = Bot('',  # Твой токен group_id, НЕЗАБУДЬ включить Longpoll
		  group_id=,
		  debug=True)


@bot.on.pre_process()  # registration
async def autoreg(ans: Message):
	if ans.peer_id < 2e9:
		cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
		result = cc.fetchall()

		if len(result) >= 1:
			pass

		else:
			cc.execute(f"SELECT * FROM global")
			gresult = cc.fetchall()
			pid = gresult[0][0]
			pid += 1
			cc.execute("INSERT INTO users (vkid, pid, blnc, bant)"
					   f"VALUES ('{ans.from_id}', '{pid}', '100', '0')"
					   )
			cc.execute(f"UPDATE global SET allusers = {pid}")
			connection.commit()

			main_listb = [[{'text': f'Баланс: 100', 'color': 'secondary'}],
						  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
						   {'text': '⬆', 'color': 'primary'}],
						  [{'text': '🗄Резерв🗄', 'color': 'negative'}, {'text': '🆘Репорт🆘', 'color': 'negative'}]]

			main_kb = keyboard_gen(main_listb, one_time=False)
			await ans('Добро пожаловать в VCuti!\nЭто бот для игры в Nvuti на VKCoins💲\nОзнакомься с👇\n'
					  'Условия использования -  📃\n'
					  'Как пользоваться клавиатурой бота -  ℹ', keyboard=main_kb)

			with open("rlist.txt", "r", encoding="UTF-8") as f:
				peers = list(ast.literal_eval(f.read()))
			list.append(peers, ans.from_id)
			with open("rlist.txt", "w") as f:
				f.write(f"{peers}")



@bot.on.message(text=['Начать', 'Назад'], lower=True)
async def strt(ans: Message):
	cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
	blnc = cc.fetchall()[0][2]

	main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
				  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
				   {'text': '⬆', 'color': 'primary'}],
				  [{'text': '🗄Резерв🗄', 'color': 'negative'}, {'text': '🆘Репорт🆘', 'color': 'negative'}]]

	main_kb = keyboard_gen(main_listb, one_time=False)
	await ans('...', keyboard=main_kb)


@bot.on.message(text=['Играть▶', 'Играть'], lower=True)
async def play_inst(ans: Message):
	cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
	blnc = cc.fetchall()[0][2]

	main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
				  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
				   {'text': '⬆', 'color': 'primary'}],
				  [{'text': '🗄Резерв🗄', 'color': 'negative'}, {'text': '🆘Репорт🆘', 'color': 'negative'}]]

	main_kb = keyboard_gen(main_listb, one_time=False)
	await ans(
		'Чтобы играть используйте следующую команду👇🏻\nНвути процент меньше(1), больше(2) сумма ставки\n'
		'Пример: Нвути 70 1 100', keyboard=main_kb)


@bot.on.message(text=['⬇', 'Пополнить'], lower=True)
async def pblnc(ans: Message):
	cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
	blnc = cc.fetchall()[0][2]

	main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
				  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
				   {'text': '⬆', 'color': 'primary'}],
				  [{'text': '🗄Резерв🗄', 'color': 'negative'}, {'text': '🆘Репорт🆘', 'color': 'negative'}]]

	main_kb = keyboard_gen(main_listb, one_time=False)
	await ans('Для оплаты перейдите\n\nКоммисия 5%', keyboard=main_kb) # Укажите вашу ссылку для оплаты!!!


@bot.on.message(text='⬆')
@bot.on.message(text='Вывести')
@bot.on.message(text='вывести')
async def vblnc(ans: Message):
	await ans('Введите сумму для вывода\nКоммисия 5%', keyboard=pvk_kb)
	return Branch('vblnc')


@bot.branch.simple_branch('vblnc')
async def vbranch(ans: Message):
	cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
	blnc = cc.fetchall()[0][2]
	cc.execute(f"SELECT * FROM global")
	ccm = cc.fetchall()[0][1]
	if ans.text.lower() == 'Назад':
		main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
					  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
					   {'text': '⬆', 'color': 'primary'}],
					  [{'text': '🗄Резерв🗄', 'color': 'negative'}, {'text': '🆘Репорт🆘', 'color': 'negative'}]]

		main_kb = keyboard_gen(main_listb, one_time=False)
		await ans('...', keyboard=main_kb)
		return ExitBranch()

	else:

		try:
			sum = int(ans.text.lower())
			if sum <= blnc:
				ccm += sum * 0.05
				amount = sum - sum * 0.05
				amount *= 1000
				merchant.send_payment(ans.from_id, amount)
				blnc -= sum
				blnc = round(blnc, 2)
				cc.execute(f"UPDATE users SET blnc = {blnc} WHERE vkid = {ans.from_id}")
				cc.execute(f"UPDATE global SET comcoins = {ccm}")
				connection.commit()

				main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
							  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
							   {'text': '⬆', 'color': 'primary'}],
							  [{'text': '🗄Резерв🗄', 'color': 'negative'},
							   {'text': '🆘Репорт🆘', 'color': 'negative'}]]

				main_kb = keyboard_gen(main_listb, one_time=False)
				await ans('Готово✔️', keyboard=main_kb)
				return ExitBranch()

			else:
				main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
							  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
							   {'text': '⬆', 'color': 'primary'}],
							  {{'text': '🗄Резерв🗄', 'color': 'negative'},
							   {'text': '🆘Репорт🆘', 'color': 'negative'}}]

				main_kb = keyboard_gen(main_listb, one_time=False)
				await ans('Недостаточно средств на балансе❌', keyboard=main_kb)
				return ExitBranch()

		except Exception as e:
			print(f'{e}')
			main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
						  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
						   {'text': '⬆', 'color': 'primary'}
						   ],
						  [{'text': '🗄Резерв🗄', 'color': 'negative'}, {'text': '🆘Репорт🆘', 'color': 'negative'}]]
			main_kb = keyboard_gen(main_listb, one_time=False)
			await ans('...', keyboard=main_kb)
			return ExitBranch()


@bot.on.message(text='🗄Резерв🗄')
@bot.on.message(text='Резерв')
@bot.on.message(text='резерв')
async def mrezerv(ans: Message):
	cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
	blnc = cc.fetchall()[0][2]
	rzrv = merchant.get_balance(520369348, 520369348)
	rzrv = rzrv['520369348']
	rzrv /= 1000

	main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
				  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
				   {'text': '⬆', 'color': 'primary'}],
				  [{'text': '🗄Резерв🗄', 'color': 'negative'}, {'text': '🆘Репорт🆘', 'color': 'negative'}]]

	main_kb = keyboard_gen(main_listb, one_time=False)
	await ans(f'🗄Резерв бота - {rzrv}🗄', keyboard=main_kb)


@bot.on.message(text='🆘Репорт🆘')
@bot.on.message(text='Репорт')
@bot.on.message(text='репорт')
async def srepbrnch(ans: Message):
	cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
	rbs = cc.fetchall()[0][6]
	if rbs == 1.0:
		await ans('Для вас репорты ограничены администрацией⚠️')

	elif rbs >= 2.0:
		ntime = time.time()
		if ntime >= rbs:
			cc.execute(f"UPDATE users SET rban = '0' WHERE vkid = {ans.from_id}")
			connection.commit()
			await ans('Введите ваш вопрос\nЕсли у вас нет вопрос используйте команду "Назад"', keyboard=nzd_kb)
			return Branch('repbrnch')

		else:
			await ans('Для вас репорты временно ограничены администрацией⚠️')

	else:
		await ans('Введите ваш вопрос\nЕсли у вас нет вопрос используйте команду "Назад"', keyboard=nzd_kb)
		return Branch('repbrnch')


@bot.branch.simple_branch('repbrnch')
async def repbrnch(ans: Message):
	cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
	blnc = cc.fetchall()[0][2]
	if ans.text.lower() == 'Назад'\
			or ans.text.lower() == 'назад':

		main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
					  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
					   {'text': '⬆', 'color': 'primary'}],
					  [{'text': '🗄Резерв🗄', 'color': 'negative'}, {'text': '🆘Репорт🆘', 'color': 'negative'}]]

		main_kb = keyboard_gen(main_listb, one_time=False)
		await ans('...', keyboard=main_kb)
		return ExitBranch()

	else:

		main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
					  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
					   {'text': '⬆', 'color': 'primary'}],
					  [{'text': '🗄Резерв🗄', 'color': 'negative'}, {'text': '🆘Репорт🆘', 'color': 'negative'}]]

		main_kb = keyboard_gen(main_listb, one_time=False)
		await ans('Репорт отправлен!\nОжидайте ответа от саппартов', keyboard=main_kb)
		user = await bot.api.users.get(user_ids=ans.from_id)
		user_n = user[0].first_name
		user_name = f'@id{ans.from_id} ({user_n})'
		await bot.api.messages.send(peer_id=2000000001, random_id=0,
									message=f'🆘Report🆘\nОт {user_name}\nID VK: {ans.from_id}\nТекст репорта:\n{ans.text.lower()}'
									)
		return ExitBranch()


@bot.on.message(text='Нвути <prc:float> <b_or_m:int> <sst:float>', lower=True) # Здесь желательно ничего не трогать
async def play_nvuti(ans: Message, prc, b_or_m, sst):						   # При желании можно исправить на более сложный вариант с классами и т.д.
	cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
	result = cc.fetchall()
	blnc = result[0][2]
	aablnc = blnc + 1
	prcc = 10000
	prcc *= prc

	cc.execute("SELECT * FROM global")
	lpdk = cc.fetchall()[0][2]
	t1o4 = random.randint(1, lpdk)
	prc = round(prc, 2)
	sst = round(sst, 2)

	if prc <= 95.0:

		if prc >= 1.0:

			if sst >= float(aablnc):
				main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
							  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
							   {'text': '⬆', 'color': 'primary'}],
							  [{'text': '🗄Резерв🗄', 'color': 'negative'},
							   {'text': '🆘Репорт🆘', 'color': 'negative'}]]

				main_kb = keyboard_gen(main_listb, one_time=False)
				await ans('Недостаточно средств на балансе!', keyboard=main_kb)

			elif t1o4 == 1:  # подкрутка
				if b_or_m == 1:  # меньше подкрутка
					pcount = random.randint(prcc, 999999)
					blnc -= sst
					blnc = round(blnc, 2)
					cc.execute(f"UPDATE users SET blnc = {blnc} WHERE vkid = {ans.from_id}")
					connection.commit()

					nvuti_listb = [[{'text': f'Нвути {prc} {b_or_m} {sst}', 'color': 'negative'}],
								   [{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
								   [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
									{'text': '⬆', 'color': 'primary'}],
								   [{'text': '🗄Резерв🗄', 'color': 'negative'},
									{'text': '🆘Репорт🆘', 'color': 'negative'}]]

					nvuti_kb = keyboard_gen(nvuti_listb, one_time=False)
					await ans(f'Сожалею! Вы проиграли😭\nВаш баланс - {blnc}💰\nВыпало число - {pcount}🎲',
							  keyboard=nvuti_kb)

				elif b_or_m == 2:  # больше подкрутка
					pcount = random.randint(0, prcc)
					blnc -= sst
					blnc = round(blnc, 2)
					cc.execute(f"UPDATE users SET blnc = {blnc} WHERE vkid = {ans.from_id}")
					connection.commit()

					nvuti_listb = [[{'text': f'Нвути {prc} {b_or_m} {sst}', 'color': 'negative'}],
								   [{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
								   [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
									{'text': '⬆', 'color': 'primary'}],
								   [{'text': '🗄Резерв🗄', 'color': 'negative'},
									{'text': '🆘Репорт🆘', 'color': 'negative'}]]

					nvuti_kb = keyboard_gen(nvuti_listb, one_time=False)
					await ans(f'Сожалею! Вы проиграли😭\nВаш баланс - {blnc}💰\nВыпало число - {pcount}🎲',
							  keyboard=nvuti_kb)

				else:
					main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
								  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
								   {'text': '⬆', 'color': 'primary'}],
								  [{'text': '🗄Резерв🗄', 'color': 'negative'},
								   {'text': '🆘Репорт🆘', 'color': 'negative'}]]

					main_kb = keyboard_gen(main_listb, one_time=False)
					await ans('Ошибка!❌\nКажется вы неправильно установили значение меньше(1) или больше(2)❗',
							  keyboard=main_kb)
			else:  # неподкрутка
				pcount = random.randint(0, 999999)
				if b_or_m == 1:  # меньше

					if pcount <= prcc:
						osst = sst / prc
						osst *= 100
						osst -= sst
						blnc += osst
						blnc = round(blnc, 2)
						cc.execute(f"UPDATE users SET blnc = {blnc} WHERE vkid = {ans.from_id}")
						connection.commit()

						nvuti_listb = [[{'text': f'Нвути {prc} {b_or_m} {sst}', 'color': 'positive'}],
									   [{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
									   [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
										{'text': '⬆', 'color': 'primary'}],
									   [{'text': '🗄Резерв🗄', 'color': 'negative'},
										{'text': '🆘Репорт🆘', 'color': 'negative'}]]

						nvuti_kb = keyboard_gen(nvuti_listb, one_time=False)
						await ans(f'Поздравляю! Вы выиграли🎉\nВаш баланс - {blnc}💰\nВыпало число - {pcount}🎲',
								  keyboard=nvuti_kb)

					elif pcount >= prcc:
						blnc -= sst
						blnc = round(blnc, 2)
						cc.execute(f"UPDATE users SET blnc = {blnc} WHERE vkid = {ans.from_id}")
						connection.commit()

						nvuti_listb = [[{'text': f'Нвути {prc} {b_or_m} {sst}', 'color': 'negative'}],
									   [{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
									   [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
										{'text': '⬆', 'color': 'primary'}],
									   [{'text': '🗄Резерв🗄', 'color': 'negative'},
										{'text': '🆘Репорт🆘', 'color': 'negative'}]]

						nvuti_kb = keyboard_gen(nvuti_listb, one_time=False)
						await ans(f'Сожалею! Вы проиграли😭\nВаш баланс - {blnc}💰\nВыпало число - {pcount}🎲',
								  keyboard=nvuti_kb)

					else:
						main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
									  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
									   {'text': '⬆', 'color': 'primary'}],
									  [{'text': '🗄Резерв🗄', 'color': 'negative'},
									   {'text': '🆘Репорт🆘', 'color': 'negative'}]]
						main_kb = keyboard_gen(main_listb, one_time=False)
						await ans(
							'Техническая ошибка❌\nПожалуйста скопируйте это сообщение и отправьте в репорт с пометкой #баг\nКод ошибки: Число не совпадает с условиями',
							keyboard=main_kb)

				elif b_or_m == 2:
					prcc = 999999 - prcc
					if pcount >= prcc:
						osst = sst / prc
						osst *= 100
						osst -= sst
						blnc += osst
						blnc = round(blnc, 2)
						cc.execute(f"UPDATE users SET blnc = {blnc} WHERE vkid = {ans.from_id}")
						connection.commit()

						nvuti_listb = [[{'text': f'Нвути {prc} {b_or_m} {sst}', 'color': 'positive'}],
									   [{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
									   [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
										{'text': '⬆', 'color': 'primary'}],
									   [{'text': '🗄Резерв🗄', 'color': 'negative'},
										{'text': '🆘Репорт🆘', 'color': 'negative'}]]

						nvuti_kb = keyboard_gen(nvuti_listb, one_time=False)
						await ans(f'Поздравляю! Вы выиграли🎉\nВаш баланс - {blnc}💰\nВыпало число - {pcount}🎲',
								  keyboard=nvuti_kb)

					elif pcount <= prcc:
						blnc -= sst
						blnc = round(blnc, 2)
						cc.execute(f"UPDATE users SET blnc = {blnc} WHERE vkid = {ans.from_id}")
						connection.commit()

						nvuti_listb = [[{'text': f'Нвути {prc} {b_or_m} {sst}', 'color': 'negative'}],
									   [{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
									   [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
										{'text': '⬆', 'color': 'primary'}],
									   [{'text': '🗄Резерв🗄', 'color': 'negative'},
										{'text': '🆘Репорт🆘', 'color': 'negative'}]]

						nvuti_kb = keyboard_gen(nvuti_listb, one_time=False)
						await ans(f'Сожалею! Вы проиграли😭\nВаш баланс - {blnc}💰\nВыпало число - {pcount}🎲',
								  keyboard=nvuti_kb)

					else:
						await ans(
							'Техническая ошибка❌\nПожалуйста скопируйте это сообщение и отправьте в репорт с пометкой #баг\nКод ошибки: Число не совпадает с условиями')
				else:
					main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
								  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
								   {'text': '⬆', 'color': 'primary'}],
								  [{'text': '🗄Резерв🗄', 'color': 'negative'},
								   {'text': '🆘Репорт🆘', 'color': 'negative'}]]

					main_kb = keyboard_gen(main_listb, one_time=False)
					await ans('Ошибка!❌\nКажется вы неправильно установили значение меньше(1) или больше(2)❗',
							  keyboard=main_kb)
		else:
			main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
						  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
						   {'text': '⬆', 'color': 'primary'}],
						  [{'text': '🗄Резерв🗄', 'color': 'negative'},
						   {'text': '🆘Репорт🆘', 'color': 'negative'}]]
			main_kb = keyboard_gen(main_listb, one_time=False)
			await ans('Ошибка!❌\nКажется вы неправильно установили процент (от 1 до 95)❗', keyboard=main_kb)
	else:

		main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
					  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
					   {'text': '⬆', 'color': 'primary'}],
					  [{'text': '🗄Резерв🗄', 'color': 'negative'},
					   {'text': '🆘Репорт🆘', 'color': 'negative'}]]

		main_kb = keyboard_gen(main_listb, one_time=False)
		await ans('Ошибка!❌\nКажется вы неправильно установили процент (от 1 до 95)❗', keyboard=main_kb)


@bot.on.message(text='Баланс: <arg:float>')
async def dnb(ans: Message, arg):
	cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
	result = cc.fetchall()
	blnc = result[0][2]

	main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
				  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
				   {'text': '⬆', 'color': 'primary'}],
				  [{'text': '🗄Резерв🗄', 'color': 'negative'}, {'text': '🆘Репорт🆘', 'color': 'negative'}]]

	main_kb = keyboard_gen(main_listb, one_time=False)
	await ans(f'Это ваш баланс\nОн равен {arg}', keyboard=main_kb)


# =
@bot.on.message(text='!отписаться', lower=True) # Start mailing commands
async def unsubscribe_mailing(ans: Message):
	with open("rlist.txt", "r", encoding="UTF-8") as f:
		peers = list(ast.literal_eval(f.read()))

	if ans.from_id in peers:

		list.remove(peers, ans.from_id)
		with open("rlist.txt", "w") as f:
			f.write(f"{peers}")

		await ans('Вы успешно отписались на рассылки!\n'
				  'Чтобы подписаться используйте - !подписаться\n'
				  '[0] - Назад🔙', keyboard=on_kb)

	else:
		await ans('Вы уже отписаны на рассылки!\n'
				  'Чтобы подписаться используйте - !подписаться\n'
				  '[0] - Назад🔙', keyboard=on_kb)


@bot.on.message(text='!подписаться', lower=True)
async def subcribe_mailing(ans: Message):
	with open("rlist.txt", "r", encoding="UTF-8") as f:
		peers = list(ast.literal_eval(f.read()))

	if ans.from_id in peers:
		await ans('Вы уже подписаны на рассылку!\n'
				  'Чтобы отписаться используйте - !отписаться\n'
				  '[0] - Назад🔙', keyboard=on_kb)

	else:
		list.append(peers, ans.from_id)
		with open("rlist.txt", "w") as file:
			file.write(f"{peers}")

		await ans('Вы успешно подписались на рассылку!\n'
				  'Чтобы отписаться используйте - !отписаться\n'
				  '[0] - Назад🔙', keyboard=on_kb) # End mailing commands


@bot.on.message(text='admin commands', lower=True) # Start admin commands
async def admcom(ans: Message):
	cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
	adm = cc.fetchall()[0][5]

	if ans.from_id == owner_vkid:
		await ans('Админ команды📃:\n'
				  '1) set blnc <zn:int> <ida:int> - Устанавливает баланс, ida - Vkid\n'
				  '2)/id User - Узнать Vkid пользователя переслав сообщение\n'
				  '3) set pdkrtk zn - Установить значение подкрутки\n' # Чем меньше значение, тем больше подкрутка (от 1 до бесконечности)
				  '4) set adm zn ida - Назначить администратора\n'
				  '5) /delkeyboard - Удалить клавиатуру в беседе\n'
				  '6) set rban <zn:int> <ida:int> - Ограничить репорт zn - 1=навсегда, другие значения в минутах\n'
				  '7) mailing <text> - Рассылка'
				  )

	elif adm == 1:
		await ans('Админ команды📃:\n'
				  '1) set blnc <zn:int> <ida:int> - Устанавливает баланс, ida - Vkid\n'
				  '2)/id User - Узнать Vkid пользователя переслав сообщение\n'
				  '3) set rban <zn:int> <ida:int> - Ограничить репорт zn - 1=навсегда, другие значения в минутах'
				  )

	else:
		pass



@bot.on.message(text='set blnc <zn:int> <ida:int>', lower=True)
async def setbalance(ans: Message, zn, ida):
	cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
	adm = cc.fetchall()[0][5]
	if adm == 1:

		try:
			cc.execute(f"UPDATE users SET blnc = {zn} WHERE vkid = {ida}")
			connection.commit()
			await ans(f'Ready✅\nДанные:\nVkid - {ida}, zn - {zn}📃')

		except Exception as e:
			await ans('Ошибка❗\nИспользуйте set blnc vkid zn📃'
					  f'Код ошибки - {e}')

	else:
		pass


@bot.on.message(text='set pdkrtk <zn:int>', lower=True)
async def setpdkrtk(ans: Message, zn):
	if ans.from_id == owner_vkid:
		cc.execute(f"UPDATE global SET pdkrtk = {zn}")
		connection.commit()
		await ans(f'Ready✅\nДанные:\nzn - {zn}📃')


@bot.on.message(text='set adm <zn:int> <ida:int>', lower=True)
async def setadm(ans: Message, zn, ida):
	if ans.from_id == owner_vkid:

		try:

			if zn == 1:
				cc.execute(f"UPDATE users SET adm = '1' WHERE vkid = {ida}")
				connection.commit()
				await ans(f'Ready✅\nДанные:\n{ida} стал администратором')

			elif zn == 0:
				cc.execute(f"UPDATE users SET adm = '0' WHERE vkid = {ida}")
				connection.commit()
				await ans(f'Ready✅\nДанные:\n{ida} снят с поста администратора')

			else:
				await ans('Ошибка в первом значении❗\nИспользуйте либо 1(+ адм) либо 2(-адм)📃')


		except Exception as e:
			await ans('Ошибка❗\nИспользуйте set adm zn vkid📃\n'
					  f'Код ошибка - {e}')
	else:
		pass


@bot.on.chat_message(text='/id User', lower=True)
async def know_id(ans: Message):
	cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
	adm = cc.fetchall()[0][5]
	if adm == 1:
		cc.execute(f"SELECT * FROM users WHERE vkid = {ans.reply_message.from_id}")
		pid = cc.fetchall[0][1]

		await ans('ID This user in VK')
		await ans(f'{ans.reply_message.from_id}')
		await ans('PID') # Player ID
		await ans(f'{pid}')

	else:
		pass


@bot.on.message(text='otvet <ida:int> <arg>')
@bot.on.chat_message(text='/otvet <ida:int> <arg>')
async def ans_rep(ans: Message, ida, arg): # Answer on report
	cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
	adm = cc.fetchall()[0][5]
	if adm == 1:

		try:
			await ans(f'Ready✅\nОтвет отправлен\n ID VK = {ida}\n Text = {arg}')
			user = await bot.api.users.get(user_ids=ida)
			user_n = user[0].first_name
			user_name = f'@id{ans.from_id} ({user_n})'
			await bot.api.messages.send(peer_id={ida}, random_id=0,
										message=f'Здравствуйте {user_name}!\nНа ваш репорт поступил ответ: {arg}')

		except Exception as e:
			await ans(f'Форма команды: otvet <ida> <arg>')
			await ans(f'Код ошибки - {e}')

	else:
		pass

@bot.on.chat_message(text='/delkeyboard', lower=True)
async def dlkb(ans: Message):
	if ans.from_id == 267023627:
		await ans('ok', keyboard=nzd_kb)

	else:
		pass


@bot.on.message(text='set rban <zn:int> <ida:int>', lower=True)
async def setrban(ans: Message, zn, ida):
	cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
	adm = cc.fetchall()[0][5]
	if adm == 1:

		try:
			if zn == 1:
				cc.execute(f"UPDATE users SET rban = '1' WHERE vkid = {ida}")
				connection.commit()
				await ans(f'Ready✅\nДанные:\n{ida} получил бан репорта навсегда')

			elif zn == 0:
				cc.execute(f"UPDATE users SET rban = '0' WHERE vkid = {ida}")
				connection.commit()
				await ans(f'Ready✅\nДанные:\n{ida} теперь может писать в репорт')

			else:
				btime = time.time()
				btime += zn * 60
				cc.execute(f"UPDATE users SET rban = {btime} WHERE vkid = {ida}")
				connection.commit()
				await ans(f'Ready✅\nДанные:\n{ida} получил бан репорта на {zn} минут')

		except Exception as e:
			await ans('Ошибка❗\nИспользуйте set rban zn vkid📃\n'
					  f'Код ошибка - {e}')

	else:
		pass


@bot.on.message(text='mailing <text>', lower=True)
async def mailing(ans: Message, text):
	if ans.from_id == owner_vkid:
		await ans('Started...')
		with open("rlist.txt", "r", encoding="UTF-8") as f:
			peers = list(ast.literal_eval(f.read()))

		for peer in peers:

			try:
				await bot.api.messages.send(user_id=peer, random_id=0, message=f"📢Рассылочка:📢\n{text}\n"
																			   "Чтобы отписаться от рассылки используйте - !отписаться\n"
																			   "Чтобы подписаться на рассылку используйте - !подписаться\n")
			except Exception as e:
				await ans('Ошибка❗'
						  f'Код ошибка - {e}')

	else:
		pass # end admin commands


@bot.on.message(text='<arg>') # Not found handler
async def nfa(ans: Message, arg):
	cc.execute(f"SELECT * FROM users WHERE vkid = {ans.from_id}")
	result = cc.fetchall()
	blnc = result[0][2]

	main_listb = [[{'text': f'Баланс: {blnc}', 'color': 'secondary'}],
				  [{'text': '⬇', 'color': 'primary'}, {'text': 'Играть▶', 'color': 'negative'},
				   {'text': '⬆', 'color': 'primary'}],
				  [{'text': '🗄Резерв🗄', 'color': 'negative'}, {'text': '🆘Репорт🆘', 'color': 'negative'}]]

	main_kb = keyboard_gen(main_listb, one_time=False)
	await ans(f'"{arg}", что это такое?🧐 Не понимаю тебя!🙁\nИспользуй клавиатуру и вводи команды верно💭',
			  keyboard=main_kb)


bot.run_polling()

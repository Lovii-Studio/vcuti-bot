"""BOT VCUTI"""
"""CREATE BY - TheLovii"""
"""TEAM - HALCYON TEAM"""
"""GITHUB - github.com/TheLovii TEAM GITHUB - github.com/Halcyon-Team"""

import vkcoin
import termcolor
import sqlite3 as sql
import time

"""SETTINGS"""
connection = sql.connect("vcuti_datab.db")
cc = connection.cursor()

merchant = vkcoin.VKCoin(user_id=0, key='') # Твой ключ и user_id

"""POLLING"""
def logger(
	text: str, 
	color: str
	):
	print(
		'[' + termcolor.colored('VCuti Status', color=color) + '] ' + text
		)


logger('Прием платежей VKCoins начат!', 'green')


@merchant.payment_handler(handler_type='longpoll')
def webhook_ppl(
	data
	):
	try:
		fromid = int(data['from_id'])
		amount = int(data['amount'])
		amount /= 1000
		print(f'{amount}')
		cc.execute(f"SELECT * FROM users WHERE vkid = {fromid}")
		result = cc.fetchall()
		cc.execute(f"SELECT * FROM global")
		gresult = cc.fetchall()
		comc = gresult[0][1]

		if len(result) == 0:
			logger('Новый платеж, но владелец не найден :/', 'green')
			comc += amount
			cc.execute(f"UPDATE global SET comcoins = {comc}")
			connection.commit()

		else:
			blnc = result[0][2]
			blnc += amount - amount * 0.05
			comc += amount * 0.05
			cc.execute(f"UPDATE users SET blnc = {blnc} WHERE vkid = {fromid}")
			cc.execute(f"UPDATE global SET comcoins = {comc}")
			connection.commit()
			logger('Новый платеж!', 'green')

	except Exception as e:
		logger(f'Big Error! {e}', 'red')


merchant.run_longpoll(tx=[1], interval=0.25)
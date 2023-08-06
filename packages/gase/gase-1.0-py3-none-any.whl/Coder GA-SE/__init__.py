class SymbolNotFound(Exception):
	pass

dictonaryDECODE = {"а": "2", "б": "3", "в": "4", "г": "5", "д": "6", "е": "7", "ё": "8", "ж": "9", "з": "20", "и": "22", "й": "23", "к": "24", "л": "25", "м": "26", "н": "27", "о": "28", "п": "29", "р": "30", "с": "32", "т": "33", "у": "34", "ф": "35", "х": "36", "ц": "37", "ч": "38", "ш": "39", "щ": "40", "ъ": "42", "ы": "43", "ь": "44", "э": "45", "ю": "46", "я": "47", "!": "48", "?": "49", ".": "50"}
dictonaryENCODE = {'2': 'а', '3': 'б', '4': 'в', '5': 'г', '6': 'д', '7': 'е', '8': 'ё', '9': 'ж', '20': 'з', '22': 'и', '23': 'й', '24': 'к', '25': 'л', '26': 'м', '27': 'н', '28': 'о', '29': 'п', '30': 'р', '32': 'с', '33': 'т', '34': 'у', '35': 'ф', '36': 'х', '37': 'ц', '38': 'ч', '39': 'ш', '40': 'щ', '42': 'ъ', '43': 'ы', '44': 'ь', '45': 'э', '46': 'ю', '47': 'я', '48': '!', '49': '?', '50': '.'}
res = ""

def help():
	print("decode(text) - Закодировать; encode(text) - разкодировать")

def decode(text):
	global res
	for x in text:
		try:
			res += dictonaryDECODE[x]
		except Exception as _ex:
			raise SymbolNotFound
		res += "1"
	return res

def encode(text):
	text = str(text)
	symbol = ""
	result_symbols = ""

	for x in text:
		if x == "1":
			try:
				result_symbols += dictonaryENCODE[symbol]
			except Exception as _ex:
				raise SymbolNotFound
			symbol = ""
		else:
			symbol += x

	return result_symbols
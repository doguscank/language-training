import googletrans

def translate(_dict):
	f = open(f"translate/{_dict}.txt", "r", encoding = "utf8")
	words = f.readlines()
	for i in range(len(words)):
		words[i] = words[i][:len(words[i]) - 1:]
	f.close()		
	fwr = open(f"translate/{_dict}_translated.txt", "a", encoding = "utf8")
	for word in words:
		translated = googletrans.Translator().translate(text = word, dest = "zh-cn", src = "en")
		fwr.write(f"{translated.text} ({translated.pronunciation})\n")
	fwr.close()

def write_to_txt(from_dict_name, to_dict_name, from_dict, to_dict):
	path = f"translate/{from_dict}2{to_dict}_new.txt"
	fw = open(path, "a", encoding = "utf8")
	ffd_path = f"translate/{from_dict_name}.txt"
	ftd_path = f"translate/{to_dict_name}.txt"
	ffd = open(ffd_path, "r", encoding = "utf8")
	from_words = ffd.readlines()
	ffd.close()
	ftd = open(ftd_path, "r", encoding = "utf8")
	to_words = ftd.readlines()
	ftd.close()
	for i in range(len(from_words)):
		new_line = f"{from_words[i][:len(from_words[i]) - 1:].capitalize()},{to_words[i][:len(to_words[i]) - 1:]}\n"
		fw.write(new_line)
	fw.close()

#translate("Eng2Cinfrom")
#write_to_txt("Eng2Cinfrom", "Eng2Cinfrom_translated", "Eng", "Cin")
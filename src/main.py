import tkinter as tk
import random

all_dictionaries = []
language_options = ["Tur", "Cin", "Eng", "Ger", "Fra", "Jpn"]

def add_word(from_word, to_word, _dict, label):
	if from_word == "Word to be translated..." or to_word == "Translation..." or from_word == "" or to_word == "":
		print("Invalid input!")
	else:
		from_words, to_words = get_dictionary_words(_dict)
		if from_word not in from_words:
			path = f"dict/{_dict}.txt"
			faw = open(path, "a", encoding="utf8")
			faw.write(f"{from_word},{to_word}\n")
			faw.close()
			label.config(text = (f"{from_word} -> {to_word} is added to {_dict} dictionary!"))
		else:
			label.config(text = (f"{from_word} -> {to_word} is already added to {_dict} dictionary!"))

def remove_word(from_word, _dict, label):
	from_words, to_words = get_dictionary_words(_dict)
	if from_word == "Word to be translated..." or from_word == "Translation...":
		print("Invalid input!")
	elif from_word in from_words:
		index = from_words.index(from_word)
		from_words.remove(from_word)
		to_words.pop(index)
		new_dict = []
		for i in range(len(from_words)):
			new_dict.append(f"{from_words[i]},{to_words[i]}\n")
		path = f"dict/{_dict}.txt"
		frw = open(path, "w", encoding="utf8").close()
		frw = open(path, "a", encoding="utf8")
		for i in range(len(from_words)):
			frw.write(f"{from_words[i]},{to_words[i]}\n")
		frw.close()
		label.config(text = (f"{from_word} is removed from dictionary!"))
	else:
		label.config(text = (f"{from_word} is not in dictionary!"))

def get_word(entry):
	word = entry.get()
	return str(word)

def put_placeholder(entry, placeholder):
	if entry.get() == None or entry.get() == "":
		entry.insert(0, placeholder)

def remove_placeholder(event):
	if event.widget.get() == "Word to be translated..." or event.widget.get() == "Translation..." or event.widget.get() == "From..." or event.widget.get() == "To..." or event.widget.get() == "Click to search...":
		event.widget.delete(0, "end")

def get_dictionary_names():
	path = "dict/dictionaries.txt"
	f = open(path, "r", encoding="utf8")
	dictionaries = f.readlines()
	for i in range(len(dictionaries)):
		dictionaries[i] = dictionaries[i][0:(len(dictionaries[i]) - 1)]
	return dictionaries

def create_dictionary_name(_from, _to):
	return f"{_from}2{_to}\n"

def save_dictionary(dictionary_name):
	global all_dictionaries
	if not dictionary_name[0:(len(dictionary_name) - 1)] in all_dictionaries:
		save_path = "dict/dictionaries.txt"
		fs = open(save_path, "a", encoding="utf8")
		if dictionary_name != "2\n" and dictionary_name != "From...2To...\n" and dictionary_name != "2To...\n" and dictionary_name != "From...2\n":
			fs.write(dictionary_name)
			dict_path = f"dict/{dictionary_name[0:(len(dictionary_name) - 1)]}.txt"
			fd = open(dict_path, "a", encoding="utf8").close()
		fs.close()
	else:
		print(f"{dictionary_name[0:(len(dictionary_name) - 1)]} dictionary already exists!")

def clear_frame(frame):
	for w in frame.winfo_children():
		w.destroy()

def create_dictionary():
	global language_options
	create_dictionary_window = tk.Toplevel()
	create_dictionary_window.title("Create New Dictionary")
	languages = tuple(language_options)
	main_frame = tk.Frame(create_dictionary_window)
	main_frame.grid(column = 0, columnspan = 4, row = 0, rowspan = 4, pady = 40, padx = 40)	
	translate_from_str = tk.StringVar()
	translate_from_str.set(language_options[0])
	translate_from = tk.OptionMenu(main_frame, translate_from_str, *languages).grid(column = 0, columnspan = 4, row = 0, rowspan = 1, pady = 10)	
	translate_to_str = tk.StringVar()
	translate_to_str.set(language_options[1])
	translate_to = tk.OptionMenu(main_frame, translate_to_str, *languages).grid(column = 0, columnspan = 4, row = 1, rowspan = 1, pady = 10)
	save_button = tk.Button(main_frame, text = "Add Dictionary", command = lambda: save_dictionary(create_dictionary_name(str(translate_from_str.get()), str(translate_to_str.get())))).grid(column = 0, columnspan = 4, row = 2, rowspan = 1, pady = 10)
	print(get_dictionary_names())

def get_dictionary_words(_dict):
	path = f"dict/{_dict}.txt"
	f = open(path, "r", encoding="utf8")
	words = f.readlines()
	from_words = []
	to_words = []
	for i in range(len(words)):
		words[i] = words[i][0:(len(words[i]) - 1)]
		comma_pos = words[i].index(",")
		from_words.append(words[i][0:comma_pos])
		to_words.append(words[i][comma_pos + 1:len(words[i])])
	return from_words, to_words

def update_dictionary(from_listbox, to_listbox, _dict = "", from_list = "", to_list = ""):
	from_listbox.delete(0, "end")
	to_listbox.delete(0, "end")
	if not _dict == "":
		from_words, to_words = get_dictionary_words(_dict)
	else:
		from_words, to_words = from_list, to_list
	for word in from_words:
		from_listbox.insert("end", word)
	for word in to_words:
		to_listbox.insert("end", word)

def search(left_menu, right_menu, word, _dict):
	left_menu_words, right_menu_words = get_dictionary_words(_dict)
	new_left_list = []
	new_right_list = []
	if not word == "":
		for menu_word in left_menu_words:
			if word.casefold() in menu_word.casefold():
				new_left_list.append(menu_word)
				new_right_list.append(right_menu_words[left_menu_words.index(menu_word)])
		for menu_word in right_menu_words:
			if word.casefold() in menu_word.casefold():
				new_right_list.append(menu_word)
				new_left_list.append(left_menu_words[right_menu_words.index(menu_word)])
		update_dictionary(left_menu, right_menu, from_list = new_left_list, to_list = new_right_list)
	else:
		update_dictionary(left_menu, right_menu, from_list = left_menu_words, to_list = right_menu_words)

def show_dictionary():
	dictionary_window = tk.Toplevel()
	dictionary_window.title("Dictionary")
	main_frame = tk.Frame(dictionary_window)
	main_frame.grid(column = 0, columnspan = 6, row = 0, rowspan = 8, pady = 20, padx = 40)
	search_string = tk.StringVar()
	search_area = tk.Entry(main_frame, textvariable = search_string)
	put_placeholder(search_area, "Click to search...")
	search_area.bind("<Button-1>", remove_placeholder)
	search_area.grid(column = 0, columnspan = 3, row = 0, rowspan = 1)
	dict_names = tuple(get_dictionary_names())
	dict_select = tk.StringVar()
	dict_select.set(dict_names[0])
	dict_selector = tk.OptionMenu(main_frame, dict_select, *dict_names)
	dict_selector.grid(column = 3, columnspan = 3, row = 0, rowspan = 1, pady = 10)
	from_word_list = tk.Listbox(main_frame)	
	to_word_list = tk.Listbox(main_frame)
	dict_select.trace_variable("w", lambda _, __, ___: update_dictionary(from_word_list, to_word_list, _dict = str(dict_select.get())))
	update_dictionary(from_word_list, to_word_list, _dict = str(dict_select.get()))
	from_word_list.grid(column = 1, columnspan = 2, row = 1, rowspan = 7, padx = 10)	
	to_word_list.grid(column = 3, columnspan = 2, row = 1, rowspan = 7, padx = 10)
	search_string.trace_variable("w", lambda _, __, ___: search(from_word_list, to_word_list, str(search_string.get()), str(dict_select.get())))

def open_new_words_window():
	input_window = tk.Toplevel()
	input_window.title("Add New Words")
	main_frame = tk.Frame(input_window)
	main_frame.grid(column = 0, columnspan = 6, row = 0, rowspan = 6, pady = 40, padx = 40)
	translate_from = tk.Entry(main_frame)
	translate_from.grid(column = 0, columnspan = 6, row = 1, rowspan = 1, pady = 10)
	translate_to = tk.Entry(main_frame)
	translate_to.grid(column = 0, columnspan = 6, row = 2, rowspan = 1, pady = 10)
	put_placeholder(translate_from, "Word to be translated...")
	put_placeholder(translate_to, "Translation...")
	translate_from.bind("<Button-1>", remove_placeholder)
	translate_to.bind("<Button-1>", remove_placeholder)
	dictionary_list = tuple(get_dictionary_names())
	dict_name = tk.StringVar()
	dict_name.set(get_dictionary_names()[0])
	dictionary_selector = tk.OptionMenu(main_frame, dict_name, *dictionary_list).grid(column = 0, columnspan = 6, row = 0, rowspan = 1)
	status_label = tk.Label(main_frame)
	status_label.grid(column = 0, columnspan = 6, row = 3, rowspan = 1)
	add_new_word_button = tk.Button(main_frame, text = "Add To Dictionary", command = lambda: add_word(get_word(translate_from), get_word(translate_to), str(dict_name.get()), status_label)).grid(column = 0, columnspan = 6, row = 4, rowspan = 1, pady = 10)
	remove_word_button = tk.Button(main_frame, text = "Remove From Dictionary", command = lambda: remove_word(get_word(translate_from), str(dict_name.get()), status_label)).grid(column = 0, columnspan = 6, row = 5, rowspan = 1, pady = 10)
	
def show_word(from_label, to_label, _dict, mode):
	from_words, to_words = get_dictionary_words(_dict)
	if mode == -1:
		length = len(from_words)
		index = from_words.index(from_label.cget("text"))
		if (index - 1) < 0:
			index = length - 2
		else:
			index = index - 1
		from_label.config(text = from_words[index])
		to_label.config(text = to_words[index])
	elif mode == 0:
		from_label.config(text = from_words[0])
		to_label.config(text = to_words[0])
	elif mode == 1:
		length = len(from_words)
		index = from_words.index(from_label.cget("text"))
		if (index + 1) > length - 1:
			index = 0
		else:
			index = index + 1
		from_label.config(text = from_words[index])
		to_label.config(text = to_words[index])

def word_shower(main_frame):
	clear_frame(main_frame)
	dictionary_list = tuple(get_dictionary_names())
	dict_name = tk.StringVar()
	dict_name.set(dictionary_list[0])	
	from_word_label = tk.Label(main_frame, text = "Show text here...", height = 10, width = 25, relief = "sunken", font = ("Times New Roman", 35))
	from_word_label.grid(column = 0, columnspan = 4, row = 0, rowspan = 4, sticky = "W", padx = 5, pady = 5)
	to_word_label = tk.Label(main_frame, text = "Show text here...", height = 10, width = 25, relief = "sunken", font = ("Times New Roman", 35))
	to_word_label.grid(column = 5, columnspan = 4, row = 0, rowspan = 4, sticky = "W", padx = 5, pady = 5)
	next_word_button = tk.Button(main_frame, text = "Next Word", command = lambda: show_word(from_word_label, to_word_label, str(dict_name.get()), 1), width = 20, height = 3, font = ("Times New Roman", 20))
	next_word_button.grid(column = 5, columnspan = 4, row = 4, rowspan = 1, pady = 10)
	prev_word_button = tk.Button(main_frame, text = "Previous Word", command = lambda: show_word(from_word_label, to_word_label, str(dict_name.get()), -1), width = 20, height = 3, font = ("Times New Roman", 20))
	prev_word_button.grid(column = 0, columnspan = 4, row = 4, rowspan = 1, pady = 10)
	dict_name.trace_variable("w", lambda _, __, ___: show_word(from_word_label, to_word_label, str(dict_name.get()), 0))
	dict_selector = tk.OptionMenu(main_frame, dict_name, *dictionary_list).grid(column = 4, columnspan = 1, row = 0, rowspan = 1)
	show_word(from_word_label, to_word_label, str(dict_name.get()), 0)

def generate_random(min, max):
	return random.randint(min, max)

def show_random_word(show_label, _dict, btnA, btnB, btnC, btnD):
	from_words, to_words = get_dictionary_words(_dict)
	rnd = generate_random(0, len(from_words) - 1)
	rnd_btn = generate_random(0, 3)
	show_label.config(text = from_words[rnd])
	buttons = [btnA, btnB, btnC, btnD]
	randoms = []
	for i in range(20):
		new_rnd = generate_random(0, len(from_words) - 1)
		if not new_rnd == rnd:
			if not new_rnd in randoms:
				randoms.append(new_rnd)
				if len(randoms) == 4:
					break
	for i in range(len(buttons)):
		buttons[i].config(background = show_label.cget("background"))
		if not i == rnd_btn:
			buttons[i].config(text = to_words[randoms[i]])
		else:
			buttons[i].config(text = to_words[rnd])
	
def check_choice(label_word, combo_label, button, _dict):
	from_words, to_words = get_dictionary_words(_dict)
	index = from_words.index(label_word)
	combo = combo_label.cget("text")[7:]
	if button.cget("text") == to_words[index]:
		print("true")
		button.config(background = "green")
		combo = int(combo) + 1
		combo_label.config(text = f"Combo: {combo}")
	else:
		print("false")
		button.config(background = "red")
		combo = 0		
		combo_label.config(text = f"Combo: {combo}")

def word_guess(main_frame):	
	clear_frame(main_frame)
	dictionary_list = tuple(get_dictionary_names())
	dict_name = tk.StringVar()
	dict_name.set(dictionary_list[0])
	from_words, to_words = get_dictionary_words(dict_name.get())
	dict_selector = tk.OptionMenu(main_frame, dict_name, *dictionary_list).grid(column = 4, columnspan = 1, row = 0, rowspan = 1)
	show_label = tk.Label(main_frame, height = 2, width = 20, relief = "sunken", font = ("Times New Roman", 40))
	show_label.grid(column = 0, columnspan = 9, row = 1, rowspan = 2, pady = 20, padx = 20)	
	combo_label = tk.Label(main_frame, text = "Combo: 0", font = ("Times New Roman", 20))
	combo_label.grid(column = 0, columnspan = 2, row = 6, rowspan = 1, pady = 10, padx = 20)
	btnA = tk.Button(main_frame, width = 15, height = 2, command = lambda: check_choice(show_label.cget("text"), combo_label, btnA, str(dict_name.get())), font = ("Times New Roman", 40))
	btnA.grid(column = 0, columnspan = 4, row = 3, rowspan = 1, pady = 10, padx = 20)
	btnB = tk.Button(main_frame, width = 15, height = 2, command = lambda: check_choice(show_label.cget("text"), combo_label, btnB, str(dict_name.get())), font = ("Times New Roman", 40))
	btnB.grid(column = 5, columnspan = 4, row = 3, rowspan = 1, pady = 10, padx = 20)
	btnC = tk.Button(main_frame, width = 15, height = 2, command = lambda: check_choice(show_label.cget("text"), combo_label, btnC, str(dict_name.get())), font = ("Times New Roman", 40))
	btnC.grid(column = 0, columnspan = 4, row = 5, rowspan = 1, pady = 10, padx = 20)
	btnD = tk.Button(main_frame, width = 15, height = 2, command = lambda: check_choice(show_label.cget("text"), combo_label, btnD, str(dict_name.get())), font = ("Times New Roman", 40))
	btnD.grid(column = 5, columnspan = 4, row = 5, rowspan = 1, pady = 10, padx = 20)
	nextBtn = tk.Button(main_frame, text = "Next Word", width = 10, height = 2, command = lambda: show_random_word(show_label, str(dict_name.get()), btnA, btnB, btnC, btnD), font = ("Times New Roman", 20))
	nextBtn.grid(column = 6, columnspan = 2, row = 6, rowspan = 1, pady = 10, padx = 20)
	show_random_word(show_label, str(dict_name.get()), btnA, btnB, btnC, btnD)

def write_words_to_file(_dict, from_or_to):
	from_words, to_words = get_dictionary_words(_dict)
	f = open(f"{_dict}{from_or_to}.txt", "w", encoding = "utf8").close()
	f = open(f"{_dict}{from_or_to}.txt", "a", encoding = "utf8")
	if from_or_to == "from":
		for word in from_words:
			f.write(f"{word}\n")
		f.close()
	elif from_or_to == "to":
		for word in to_words:
			f.write(f"{word}\n")
		f.close()
	else:
		print(f"Invalid argument {from_or_to} in write_words_to_file !")

def paint(event, color):
	x1, y1, x2, y2 = (event.x - 1), (event.y - 1), (event.x + 1), (event.y + 1)
	event.widget.create_oval(x1, y1, x2, y2, width = 5, fill = color, outline = color, tags = "drawing")

def reveal_word(event, reveal_id):
	event.widget.itemconfigure(reveal_id, text = event.widget.word_to_reveal)
	event.widget.itemconfigure(reveal_id, font = ("Times New Roman", 40))

def create_new_draw(from_words, to_words, from_word_canvas, to_word_canvas, reveal_id, draw_canvas_id):
	rnd = generate_random(0, len(from_words) - 1)
	word = from_words[rnd]
	from_word_canvas.delete("drawing")
	from_word_canvas.itemconfigure(draw_canvas_id, text = word)
	to_word_canvas.itemconfigure(reveal_id, text = "Click To Reveal The Answer")
	to_word_canvas.itemconfigure(reveal_id, font = ("Times New Roman", 20))
	to_word_canvas.word_to_reveal = to_words[rnd]

def writers_area(main_frame):
	clear_frame(main_frame)
	dictionary_list = tuple(get_dictionary_names())
	dict_name = tk.StringVar()
	dict_name.set(dictionary_list[0])
	from_words, to_words = get_dictionary_words(dict_name.get())
	dict_selector = tk.OptionMenu(main_frame, dict_name, *dictionary_list).grid(column = 4, columnspan = 1, row = 1, rowspan = 1)
	next_word_button = tk.Button(main_frame, text = "Next Word", command = lambda: create_new_draw(from_words, to_words, draw_canvas, reveal_canvas, reveal_id, draw_canvas_id)).grid(column = 4, columnspan = 1, row = 2, rowspan = 1)
	clear_button = tk.Button(main_frame, text = "Clear", command = lambda: draw_canvas.delete("drawing")).grid(column = 4, columnspan = 1, row = 3, rowspan = 1)
	draw_canvas = tk.Canvas(main_frame, width = 400, height = 400, bg = "white")
	draw_canvas.grid(column = 0, columnspan = 4, row = 1, rowspan = 7, padx = 20, pady = 20)
	draw_canvas.bind("<B1-Motion>", lambda event: paint(event, "black"))
	draw_canvas.bind("<B3-Motion>", lambda event: paint(event, "white"))
	reveal_canvas = tk.Canvas(main_frame, width = 400, height = 400, bg = "white")
	reveal_canvas.grid(column = 5, columnspan = 4, row = 1, rowspan = 7, padx = 20, pady = 20)
	reveal_id = reveal_canvas.create_text(200, 200, text = "Click To Reveal The Answer", font = ("Times New Roman", 20))
	draw_canvas_id = draw_canvas.create_text(200, 385, text = "", font = ("Times New Roman", 15))
	reveal_canvas.bind("<Button-1>", lambda event: reveal_word(event, reveal_id))
	create_new_draw(from_words, to_words, draw_canvas, reveal_canvas, reveal_id, draw_canvas_id)
	
def main_menu(main_frame):
	clear_frame(main_frame)
	word_shower_button = tk.Button(main_frame, text = "Text Displayer", width = 32, height = 4, font = ("Times New Roman", 18), command = lambda: word_shower(main_frame), pady = 4, padx = 4).grid(column = 0, columnspan = 9, row = 1, rowspan = 3)
	word_guess_button = tk.Button(main_frame, text = "Word Guess Game", width = 32, height = 4, font = ("Times New Roman", 18), command = lambda: word_guess(main_frame), pady = 4, padx = 4).grid(column = 0, columnspan = 9, row = 4, rowspan = 3)
	writers_area_button = tk.Button(main_frame, text = "Writers' Area", width = 32, height = 4, font = ("Times New Roman", 18), command = lambda: writers_area(main_frame), pady = 4, padx = 4).grid(column = 0, columnspan = 9, row = 7, rowspan = 3)

def main_app():
	app = tk.Tk()
	app.title("Language Training")
	function_menu = tk.Menubutton(app, text = "Select Function")
	function_menu.menu = tk.Menu(function_menu, tearoff = 0)
	function_menu["menu"] = function_menu.menu
	function_menu.menu.add_command(label = "Add or Remove Words", command = open_new_words_window)
	function_menu.menu.add_command(label = "Open Dictionary", command = show_dictionary)
	function_menu.menu.add_command(label = "Create New Dictionary", command = create_dictionary)
	function_menu.grid(column = 0, columnspan = 1, row = 0, rowspan = 1, sticky = "w")
	main_frame = tk.Frame(app, width = 400, height = 400)
	main_frame.grid(column = 0, columnspan = 9, row = 1, rowspan = 9)
	main_menu(main_frame)
	app.bind("<Escape>", lambda event: main_menu(main_frame))
	app.mainloop()

main_app()
#write_words_to_file("Eng2Cin", "from")
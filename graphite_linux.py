from tkinter import *
from tinytag import TinyTag
import tkinter as tk
from tkinter import filedialog
from decimal import Decimal
from mutagen import File
from PIL import Image, ImageTk
from pathlib import Path
import time, pygame, os


artist_name = None
def write_to_file(var, var2, var3): #var3 to be displayed as artist, var 2 to be displayed as song, var to open song.txt
	if var3 != None:
		with open(var, 'w') as song_file:
			song_file.write(str(var3) + ' - ' + var2)
	else:
		with open(var, 'w') as song_file:
			song_file.write(var2)

pygame.init()
pygame.mixer.init()

home_path = Path.home()
app_path = home_path / '.config' / 'graphite-app'
song_path = home_path / 'song.txt'
config_path = app_path / 'graphite.conf'
req_path = app_path / 'requirements.txt'

def overwrite_settings():
	global app_path
	with open(config_path, 'w') as cfg:
		cfg.write('# Main settings\n')
		cfg.write('1 foreground:white\n')
		cfg.write('2 background:black\n')
		cfg.write('3 big font:DejaVu Sans\n')
		cfg.write('4 small font:DejaVu Sans\n')
		cfg.write('5 window width:480\n')
		cfg.write('6 window height:276\n')
		cfg.write('\n')	
		cfg.write('# Image settings\n')
		cfg.write('7 album cover x:350\n')
		cfg.write('8 album cover y:90\n')
		cfg.write('9 album cover width:100\n')
		cfg.write('10 album cover height:100\n')
		cfg.write('# Directory and file settings\n')
		cfg.write(f'11 directory to choose music from:{app_path}/\n')
		cfg.write(f'12 logo2 directory:{app_path}/graph_logo2.png\n')
		cfg.write(f'13 logo3 directory:{app_path}/graph_logo3.png\n')
		cfg.write('# ^^^ You can set your own logo\'s. Keep a reasonable size though.\n')
		cfg.write('# Misc settings\n')
		cfg.write('write to song.txt:0\n')
		cfg.write('# ^^^ Enable by turning it to 1\n')
		cfg.write('developermode:0\n')
		cfg.write('# ^^^ TURNING THIS TO ANYTHING ELSE THAN 0 WILL RETURN GRAPHITE.CONF TO IT\'S ORIGINAL STATE.\n')
		cfg.write('# ^^^ Helpful if you messed something up and want to fix it. Back up your settings in another .txt file first.\n')
		cfg.write('# ^^^ Please proceed with caution.\n')	
		cfg.write('# You can delete these comments, but keep everything else. ESPECIALLY developer mode.\n')

def app_dir_gph():
	global app_path, song_path, config_path, req_path

	if not app_path.exists():
		app_path.mkdir()
	if not song_path.exists():
		song_path.touch()
	if not config_path.exists():
		config_path.touch()
		overwrite_settings()
	if not req_path.exists():
		req_path.touch()
		with open(req_path, 'w') as f:
			f.write('pygame\n')
			f.write('mutagen\n')
			f.write('tinytag\n')
			f.write('pillow\n')
			f.write('pynput\n')	


	with open(config_path, 'r') as cfg:
		for line in cfg:
			if ':' not in line:
				continue
			key, value = line.split(':', 1)
			key = key.strip()
			value = value.strip()			

			if key == '1 foreground':
				_standardfg = str(value)
			elif key == '2 background':
				_standardbg = str(value)
			elif key == '3 big font':
				fonty = (str(value), 12)
			elif key == '4 small font':
				fonty2 = (str(value), 9)
			elif key == '5 window width':
				w_w = str(value)
			elif key == '6 window height':
				w_h = str(value)
			elif key == '7 album cover x':
				coverty_x = int(value)
			elif key == '8 album cover y':
				coverty_y = int(value)
			elif key == '9 album cover width':
				coverty_w = int(value)
			elif key == '10 album cover height':
				coverty_h = int(value)
			elif key == '11 directory to choose music from':
				_music_user_directory = str(value)
			elif key == '12 logo2 directory':
				_logo2_directory = str(value)
			elif key == '13 logo3 directory':
				_logo3_directory = str(value)
			elif key == 'write to song.txt':
				write_or_not = int(value)
			elif key  == 'developermode':
				developermode = int(value)
	start_geo = f"{w_w}x{w_h}"
	if developermode == 1:
		overwrite_settings()
	return _standardfg, _standardbg, fonty, fonty2, w_w, w_h, coverty_x, coverty_y, coverty_w, coverty_h, _music_user_directory, _logo2_directory, _logo3_directory, write_or_not, developermode, start_geo

_standardfg, _standardbg, fonty, fonty2, w_w, w_h, coverty_x, coverty_y, coverty_w, coverty_h, _music_user_directory, _logo2_directory, _logo3_directory, write_or_not, developermode, start_geo = app_dir_gph()

idle = 'idle'
if write_or_not == 1:
	write_to_file(song_path, idle, artist_name)

gver = 'graphite 0.2' #graphite version

global_volume = Decimal('1.00')
selected_song = None
paused = False
playing = False
hovering = False
file_extension = ''	#.flac .mp3 and everything else
song_raw_name = None	#previously 'test'
song_list = []		#0 will be the name of the first song, 1 the second, blah blah blah
current_index = 0	#the current song number
artist_name = None

window = Tk()		#sets window
window.geometry(str(start_geo))	#sets starting geometry
window.title('graphite')	#sets window title to graphite	
icon = PhotoImage(file=f'{_logo2_directory}')		#sets icon to graph_logo2.png from graphite-app folder. *NOW you can put your image here.	
window.iconphoto(True,icon)				#sets window logo to icon
window.config(background=_standardbg)			#sets window background to standard background, at the start it is 'white'
window.resizable(False,False)				#you cannot resize the window when this is uncommented.
play_inf = 'idle'

passed_label = Label(window,text='',fg=_standardfg,bg=_standardbg,font=fonty,cursor='hand2')
song_name = Label(window, text='', font=fonty, fg=_standardfg, bg=_standardbg)
file_extension_label = Label(window, text=str(file_extension), fg=_standardfg, font=fonty, bg=_standardbg)
coverty_label = Label(window,takefocus=0,bg=_standardbg)
song_name.place(x=5, y=28, anchor='w')
file_extension_label.place(x=475, y=28, anchor='e')
coverty_label.place(x=coverty_x,y=coverty_y)
passed_label.place(x=425,y=28,anchor='e')
graph_logo = f'{_logo2_directory}'
coverty = Image.open(graph_logo)
coverty = coverty.resize((coverty_w, coverty_h), Image.Resampling.LANCZOS)
coverty = ImageTk.PhotoImage(coverty)
coverty_label.config(image=coverty)
coverty_label.image = coverty

def song_time():
	global selected_song, playing
	if selected_song:
		audio = File(selected_song)

		ntime = pygame.mixer.music.get_pos() / 1000
		elapsed = time.strftime('%M:%S', time.gmtime(ntime))
		ail = audio.info.length
		naudio = time.strftime('%M:%S', time.gmtime(ail))
		to_print = (elapsed + '/' + naudio)
		passed_label.config(text=to_print)
	window.after(80,song_time)
song_time()

dir_label = Label(window,text='file',font=fonty,fg=_standardfg,cursor='hand2',bg=_standardbg)
play_button = Label(window,text='play/stop',font=fonty,fg=_standardfg,cursor='hand2',bg=_standardbg)
vol_button = Label(window,text=str(global_volume),font=fonty,fg=_standardfg,cursor='hand2',bg=_standardbg)
playing_info = Label(window,text=str(play_inf),font=fonty2,fg=_standardfg,bg=_standardbg)
skip_left = Label(window,text=' <- ',font=fonty2,fg=_standardfg,cursor='hand2',bg=_standardbg)
skip_right = Label(window,text=' -> ',font=fonty2,fg=_standardfg,cursor='hand2',bg=_standardbg)
play_button.place(x=432,y=218,anchor='n')
dir_label.place(x=48, y=218, anchor='n')
vol_button.place(x=240,y=218,anchor='n')
playing_info.place(x=240,y=242,anchor='n')
skip_left.place(x=48,y=242,anchor='n')
skip_right.place(x=432,y=242,anchor='n')

next_song1 = Label(window,text='',font=fonty2,fg=_standardfg,bg=_standardbg)
next_song2 = Label(window,text='',font=fonty2,fg=_standardfg,bg=_standardbg)
next_song3 = Label(window,text='',font=fonty2,fg=_standardfg,bg=_standardbg)
next_song4 = Label(window,text='',font=fonty2,fg=_standardfg,bg=_standardbg)
next_song5 = Label(window,text='',font=fonty2,fg=_standardfg,bg=_standardbg)
next_song1.place(x=5,y=100,anchor='w')
next_song2.place(x=5,y=120,anchor='w')
next_song3.place(x=5,y=140,anchor='w')
next_song4.place(x=5,y=160,anchor='w')
next_song5.place(x=5,y=180,anchor='w')

artist_label = Label(window,text='',font=fonty2,fg=_standardfg,bg=_standardbg)
artist_label.place(x=48,y=39.5,anchor='n')
ttag = None

def get_files_from_bar():
	global selected_song,song_list,current_index,hovering,paused,playing,artist_label,file_extension,song_raw_name,artist_name,song_path,app_path,coverty_w,coverty_h,_music_user_directory
	path = filedialog.askdirectory(initialdir=str({_music_user_directory}))	
	if path:
		files = sorted([f for f in os.listdir(path) if f.lower().endswith(('.mp3','.wav','.ogg','.flac','.aac','.m4a', '.alac'))])
		files_covert = sorted([f for f in os.listdir(path) if f.lower().endswith(('cover.jpg','cover.png'))])
		if files:
			song_list = [os.path.join(path, f) for f in files]
			current_index = 0

			selected_song = song_list[current_index]
			song_raw_name, file_extension = os.path.splitext(os.path.basename(selected_song))
			pygame.mixer.music.stop()
			hovering = False
			paused = False
			current_index = 0
		else:
			song_list = []
			selected_song = None
			song_name.config(text='no audio :^(')
		if files_covert:
			covert_file = os.path.join(path, files_covert[0])
			try:
				coverty = Image.open(covert_file)
				coverty = coverty.resize((coverty_w, coverty_h), Image.Resampling.LANCZOS)
				coverty = ImageTk.PhotoImage(coverty)

				coverty_label.config(image=coverty)
				coverty_label.image = coverty
			except Exception as e:
				pass
		else:
			coverty = Image.open(f'{_logo2_directory}')
			coverty = coverty.resize((coverty_w, coverty_h), Image.Resampling.LANCZOS)
			coverty = ImageTk.PhotoImage(coverty)

			coverty_label.config(image=coverty)
			coverty_label.image = coverty
	update_playing_info()

dir_label.bind('<Button-1>', lambda event: get_files_from_bar())
window.bind('<Tab>', lambda event: get_files_from_bar())
dir_label.bind('<Enter>', lambda event: dir_label.config(fg='grey'))
dir_label.bind('<Leave>', lambda event: dir_label.config(fg=_standardfg))







def play_this_song():
	global selected_song, paused, playing, current_index, file_extension, song_raw_name, song_path, write_or_not

	if selected_song:
		pygame.mixer.music.load(selected_song)
		pygame.mixer.music.set_volume(float(global_volume))
		pygame.mixer.music.play()
		paused = False
		playing = True
		song_raw_name, file_extension = os.path.splitext(str(os.path.basename(selected_song)))
	
		file_extension_label.config(text=file_extension.lstrip('.'))
		try:
			ttag = TinyTag.get(str(selected_song))
			artist_name = ttag.artist
			artist_label.config(text=artist_name)
		except Exception as e:
			artist_name = None
			artist_label.config(text='no artist')

	if write_or_not == 1:
		write_to_file(song_path, song_raw_name, artist_name)

def play_click(event=None):
	global selected_song, paused, playing, play_inf, artist_name, write_or_not

	if not selected_song:
		song_name.config(text='no audio selected :^(')
		if write_or_not == 1:
			write_to_file(song_path, 'idle', artist_name)
		return
	else:
		play_inf = 'playing'
		if write_or_not == 1:
			write_to_file(song_path, song_raw_name, artist_name)
		play_this_song()

def play_button_(event=None):
	global play_inf,song_name,paused,playing,artist_name
	if paused:
		play_inf = 'playing'
		write_to_file(song_path, song_raw_name, artist_name)
		pygame.mixer.music.unpause()
		play_button.config(fg=_standardfg)
		paused = False
		playing = True
	elif playing:
		play_inf = 'paused'
		write_to_file(song_path, 'paused', artist_name)
		pygame.mixer.music.pause()
		paused = True
		playing = False
	else:
		play_click()

play_button.bind('<Button-1>',play_button_)
play_button.bind('<Enter>',lambda event: play_button.config(fg='grey'))
play_button.bind('<Leave>',lambda event: play_button.config(fg=_standardfg))
window.bind('<space>', play_button_)

def vol_click(event):
	global global_volume,vol_button

	if global_volume < Decimal('1.00'):
		global_volume += Decimal('0.05')

		pygame.mixer.music.set_volume(float(global_volume))
		vol_button.config(text=str(global_volume))

def vol_dec(event):
	global global_volume,vol_button

	if global_volume > Decimal('0.00'):
		global_volume -= Decimal('0.05')
		pygame.mixer.music.set_volume(float(global_volume))
		vol_button.config(text=str(global_volume))

def vol_scroll(event):
	if event.delta > 0:
		vol_click(event)
	else:
		vol_dec(event)

vol_button.bind('<Button-4>', vol_click)
vol_button.bind('<Button-5>', vol_dec)
window.bind('<Up>', vol_click)
window.bind('<Down>', vol_dec)

vol_button.bind('<Enter>', lambda event: vol_button.config(fg='grey'))
vol_button.bind('<Leave>', lambda event: vol_button.config(fg=_standardfg))

def skip_left_click(event):
	global global_volume,skip_left,current_index,selected_song
	if current_index - 1 >= 0:
		current_index -= 1
		selected_song = song_list[current_index]
		play_this_song()

def skip_left_enter(event):
	global hovering
	hovering = True
	skip_left.config(fg='grey')
def skip_left_leave(event):
	global hovering
	hovering = False
	skip_left.config(fg=_standardfg)

window.bind('<Left>', skip_left_click)
skip_left.bind('<Button-1>', skip_left_click)
skip_left.bind('<Enter>', skip_left_enter)
skip_left.bind('<Leave>', skip_left_leave)

def skip_right_click(event):
	global global_volume,skip_right,current_index,selected_song

	if current_index + 1 < len(song_list):
		current_index += 1
		selected_song = song_list[current_index]
		play_this_song()

def skip_right_enter(event):
	global hovering
	hovering = True
	skip_right.config(fg='grey')
def skip_right_leave(event):
	global hovering
	hovering = False
	skip_right.config(fg=_standardfg)


window.bind('<Right>', skip_right_click)
skip_right.bind('<Button-1>',skip_right_click)
skip_right.bind('<Enter>', skip_right_enter)
skip_right.bind('<Leave>', skip_right_leave)

def update_playing_info():	# This is absolute chaos, good luck reading this.
	global playing, paused, selected_song, current_index, song_list, hovering, play_inf, next_song1, next_song2, next_song3, next_song4, next_song5, playing_info, artist_name

	if playing:
		if pygame.mixer.music.get_busy():
			play_inf = 'playing'
		elif not paused and not hovering:
			if current_index + 1 < len(song_list):
				current_index += 1
				selected_song = song_list[current_index]
				play_this_song()
			else:
				playing = False
				paused = False
				play_inf = 'idle'
	if current_index + 1 < len(song_list):
		next_song_path1 = song_list[current_index + 1]
		next_song_path2 = song_list[current_index + 2] if current_index + 2 < len(song_list) else None
		next_song_path3 = song_list[current_index + 3] if current_index + 3 < len(song_list) else None
		next_song_path4 = song_list[current_index + 4] if current_index + 4 < len(song_list) else None
		next_song_path5 = song_list[current_index + 5] if current_index + 5 < len(song_list) else None

		next_song_name1 = os.path.basename(next_song_path1)
		next_song_name2 = os.path.basename(next_song_path2) if next_song_path2 else '     -     '
		next_song_name3 = os.path.basename(next_song_path3) if next_song_path3 else '     -     '
		next_song_name4 = os.path.basename(next_song_path4) if next_song_path4 else '     -     '
		next_song_name5 = os.path.basename(next_song_path5) if next_song_path5 else '     -     '
	else:
		next_song_name1 = '     -     '
		next_song_name2 = '     -     '
		next_song_name3 = '     -     '
		next_song_name4 = '     -     '
		next_song_name5 = '     -     '

	next_song1.config(text=next_song_name1, anchor='w')
	next_song2.config(text=next_song_name2, anchor='w')
	next_song3.config(text=next_song_name3, anchor='w')
	next_song4.config(text=next_song_name4, anchor='w')
	next_song5.config(text=next_song_name5, anchor='w')

	
	song1_ext = os.path.splitext(os.path.basename(next_song_name1))
	song2_ext = os.path.splitext(os.path.basename(next_song_name2))
	song3_ext = os.path.splitext(os.path.basename(next_song_name3))
	song4_ext = os.path.splitext(os.path.basename(next_song_name4))
	song5_ext = os.path.splitext(os.path.basename(next_song_name5))

	if selected_song != None:
		song_name.config(text=song_raw_name)

	if next_song_name1 is not None:
		if len(song1_ext[0]) > 35:
			title = next_song_name1[:len(song1_ext[0]) // 3] + '..'
			next_song1.config(text=title, anchor='w')
		else:
			next_song1.config(text=song1_ext[0], anchor='w')

	if next_song_name2 is not None:
		if len(song2_ext[0]) > 35:
			title = next_song_name2[:len(song2_ext[0]) // 3] + '..'
			next_song2.config(text=title, anchor='w')
		else:
			next_song2.config(text=song2_ext[0], anchor='w')

	if next_song_name3 is not None:
		if len(song3_ext[0]) > 35:
			title = next_song_name3[:len(song3_ext[0]) // 3] + '..'
			next_song3.config(text=title, anchor='w')			
		else:
			next_song3.config(text=song3_ext[0], anchor='w')

	if next_song_name4 is not None:
		if len(song4_ext[0]) > 35:
			title = next_song_name4[:len(song4_ext[0]) // 3] + '..'
			next_song4.config(text=title, anchor='w')
		else:
			next_song4.config(text=song4_ext[0], anchor='w')
	
	if next_song_name5 is not None:
		if len(song5_ext[0]) > 35:
			title = next_song_name5[:len(song5_ext[0]) // 3] + '..'
			next_song5.config(text=title, anchor='w')
		else:
			next_song5.config(text=song5_ext[0], anchor='w')


	if playing == True:
		play_inf = 'playing'
		play_button.config(text='stop')
	elif paused == True:
		play_inf = 'paused'
		play_button.config(text='play')
	elif paused == False and playing == False:
		play_inf = 'idle'
		play_button.config(text='play')

	if artist_name != None:
		artist_label.place_configure(x=48)
		if len(artist_name) > 14:
			artist_label.config(text=artist_name[:len(artist_name) // 2] + '..')
	playing_info.config(text=str(play_inf))
	window.after(100, update_playing_info)
update_playing_info()
window.mainloop()

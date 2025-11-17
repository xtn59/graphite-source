from tkinter import *
from tinytag import TinyTag
import tkinter as tk
from tkinter import filedialog
from decimal import Decimal
from mutagen import File
import pygame
from PIL import Image, ImageTk
from mutagen import File
import time
from pynput import keyboard
from pynput.keyboard import Key
from pynput.keyboard import Listener
from pathlib import Path
import subprocess
import os

pygame.init()
pygame.mixer.init()
app_path = None

def app_dir_gph():
	global system, app_path

	local_appdata = os.getenv('LOCALAPPDATA')
	app_path = Path(local_appdata) / 'graphite-app'

	if not app_path.exists():
		app_path.mkdir(parents=True)

	return app_path

app_dir_gph()



gver = 'graphite alpha'		#graphite versiom

global_volume = Decimal('1.00')
selected_song = None
paused = False
playing = False
hovering = False
file_extension = ''		#mp3 flac etc.
song_raw_name = ''		#C:\something\Dandy Andy.mp3

song_list = []			#0 is the first song, 1 is the second, etc.
current_index = 0		
artist_name = None

_gpumode = "light"		#application theme
_standardfg = "black"		#standard foreground for the labels
_standardbg = "white"		#standard background for anything that has a declared background
_gpuflip = "dark"		#the next theme to cycle to

start_geo = '480x640'		#standard geometry of the app
graph_logo = app_path / 'graph_logo2.png'	#graphite logo destination

fonty = ('JetBrains Mono','12')	#JetBrains Mono font needed
fonty2 = ('JetBrains Mono','9')	#same here
window = Tk()			#declare the window or something
window.geometry(str(start_geo))	#set the geometry, 480 px width and 640 px height
icon = PhotoImage(file=graph_logo)	#set icon/logo
window.iconphoto(True,icon)		#actually set it this time
window.config(background=_standardbg)	#window background color
window.resizable(False,False)		#graphite not resizable if this is uncommented
window.title('graphite')		#set window title, straightforward

play_inf = 'idle'		#graphite is idle i guess
        


def update_label_colors(root):
	for w in root.winfo_children():
		if isinstance(w, Label):
			w.config(fg=_standardfg, bg=_standardbg)
		update_label_colors(w)
#^^^ this barely works


song_name = Label(window, text=selected_song, font=fonty, bg=_standardbg)
song_name.place(x=5, y=28, anchor='w')
file_extension_label = Label(window, text=str(file_extension), font=fonty, bg=_standardbg)
file_extension_label.place(x=475, y=28, anchor='e')

coverty_label = Label(window,takefocus=0)
coverty_label.place(x=165,y=400)

coverty = Image.open(graph_logo)
coverty = coverty.resize((150, 150), Image.Resampling.LANCZOS)
coverty = ImageTk.PhotoImage(coverty)

coverty_label.config(image=coverty)
coverty_label.image = coverty

graphite_ver = Label(window,text=str(gver),fg=_standardfg,bg=_standardbg,font=fonty2)
graphite_ver.place(x=720,y=588,anchor='n')

passed_label = Label(window,text='',fg=_standardfg,bg=_standardbg,font=fonty,cursor='hand2')
passed_label.place(x=425,y=28,anchor='e')
def song_time():
	global selected_song, playing
	if selected_song:
		audio = File(selected_song)

		ntime = pygame.mixer.music.get_pos() / 1000
		elapsed = time.strftime('%M:%S', time.gmtime(ntime))
		nig = audio.info.length
		naudio = time.strftime('%M:%S', time.gmtime(nig))
		to_print = (elapsed + '/' + naudio)
		passed_label.config(text=to_print)
	window.after(100,song_time)

#def rewind_forward():
#	global playing
#	if playing == True:
#		pos = pygame.mixer.music.get_pos() / 1000
#		seconds = 5000
#		pygame.mixer.music.set_pos(pos + seconds)
#passed_label.bind('<Button-4>',lambda event: rewind_forward())
#^^^ will be used to skip seconds in a song in the future
song_time()


dir_label = Label(window,text='file',font=fonty,fg=_standardfg,cursor='hand2',bg=_standardbg)
dir_label.place(x=48, y=588, anchor='n')
play_button = Label(window,text='play/stop',font=fonty,fg=_standardfg,cursor='hand2',bg=_standardbg)
play_button.place(x=432,y=588,anchor='n')
vol_button = Label(window,text='vol: ' + str(global_volume),font=fonty,fg=_standardfg,cursor='hand2',bg=_standardbg)
vol_button.place(x=240,y=588,anchor='n')
playing_info = Label(window,text=str(play_inf),font=fonty2,fg=_standardfg,bg=_standardbg)
playing_info.place(x=240,y=612,anchor='n')
skip_left = Label(window,text='<- skip',font=fonty2,fg=_standardfg,cursor='hand2',bg=_standardbg)
skip_left.place(x=48,y=612,anchor='n')
skip_right = Label(window,text='skip ->',font=fonty2,fg=_standardfg,cursor='hand2',bg=_standardbg)
skip_right.place(x=432,y=612,anchor='n')

next_song1 = Label(window,text='Rn nthmn',font=fonty2,fg=_standardfg,bg=_standardbg)
next_song1.place(x=5,y=100,anchor='w')
next_song2 = Label(window,text='Rn nthmn',font=fonty2,fg=_standardfg,bg=_standardbg)
next_song2.place(x=5,y=120,anchor='w')
next_song3 = Label(window,text='Rn nthmn',font=fonty2,fg=_standardfg,bg=_standardbg)
next_song3.place(x=5,y=140,anchor='w')
next_song4 = Label(window,text='Rn nthmn',font=fonty2,fg=_standardfg,bg=_standardbg)
next_song4.place(x=5,y=160,anchor='w')
next_song5 = Label(window,text='Rn nthmn',font=fonty2,fg=_standardfg,bg=_standardbg)
next_song5.place(x=5,y=180,anchor='w')

artist_label = Label(window,text='',font=fonty2,fg=_standardfg,bg=_standardbg)
artist_label.place(x=48,y=39.5,anchor='n')
ttag = None

def get_files_from_bar():
	global selected_song,song_list,current_index,hovering,paused,playing,artist_label,file_extension,song_raw_name,artist_name,graph_logo
	
	appdata = os.getenv('LOCALAPPDATA')
	gapp_path = Path(appdata) / 'graphite-app'
	path = filedialog.askdirectory(initialdir=str(gapp_path))
	
	
	if path:
		files = sorted([f for f in os.listdir(path) if f.lower().endswith(('.mp3','.wav','.ogg','.flac','.aac','.m4a', '.alac'))])
		files_covert = sorted([f for f in os.listdir(path) if f.lower().endswith(('cover.jpg','cover.png'))])
		if files:
			song_list = [os.path.join(path, f) for f in files]
			current_index = 0


			selected_song = song_list[current_index]
			song_raw_name, file_extension = os.path.splitext(os.path.basename(selected_song))
			song_name.config(text=song_raw_name)
			file_extension_label.config(text=file_extension.lstrip('.'))
			pygame.mixer.music.stop()
			hovering = False
			paused = False
			current_index = 0
		else:
			song_list = []
			selected_song = None
			song_name.config(text='graphite found no audio !')
		if files_covert:
			covert_file = os.path.join(path, files_covert[0])
			try:
				coverty = Image.open(covert_file)
				coverty = coverty.resize((150, 150), Image.Resampling.LANCZOS)
				coverty = ImageTk.PhotoImage(coverty)

				coverty_label.config(image=coverty)
				coverty_label.image = coverty
			except Exception as e:
				pass
		else:
			coverty = Image.open(graph_logo)
			coverty = coverty.resize((150, 150), Image.Resampling.LANCZOS)
			coverty = ImageTk.PhotoImage(coverty)

			coverty_label.config(image=coverty)
			coverty_label.image = cover
	update_playing_info()

dir_label.bind('<Button-1>', lambda event: get_files_from_bar())
dir_label.bind('<Enter>', lambda event: dir_label.config(fg='grey'))
dir_label.bind('<Leave>', lambda event: dir_label.config(fg=_standardfg))







def play_this_song():
	global selected_song, paused, playing, current_index, file_extension, song_raw_name

	if selected_song:
		if not selected_song.startswith('[autoskip]'):
			pygame.mixer.music.load(selected_song)
			pygame.mixer.music.set_volume(float(global_volume))
			pygame.mixer.music.play()
			paused = False
			playing = True
			song_raw_name, file_extension = os.path.splitext(os.path.basename(selected_song))
			song_name.config(text=song_raw_name)
			file_extension_label.config(text=file_extension.lstrip('.'))
			try:
				ttag = TinyTag.get(str(selected_song))
				artist_name = ttag.artist
				artist_label.config(text=artist_name)
			except Exception as e:
				artist_name = 'graphite'
				artist_label.config(text=artist_name)
		else:
			current_index += 1
			play_this_song()






def play_click(event=None):
	global selected_song, paused, playing, play_inf

	if not selected_song:
		song_name.config(text='No audio selected !')
		return
	else:
		play_inf = 'playing'
		play_this_song()

def play_button_(event=None):
	global play_inf,song_name,paused,playing
	if paused:
		play_inf = 'playing'
		pygame.mixer.music.unpause()
		play_button.config(fg=_standardfg)
		paused = False
		playing = True
	elif playing:
		play_inf = 'paused'
		pygame.mixer.music.pause()
		paused = True
		playing = False
	else:
		play_click()



play_button.bind('<Button-1>',play_button_)
play_button.bind('<Enter>',lambda event: play_button.config(fg='grey'))
play_button.bind('<Leave>',lambda event: play_button.config(fg=_standardfg))


window.bind('<space>', play_button_)


def on_press(key):
	if str(key) == 'Key.media_play_pause' or str(key) == 'XF86AudioPlay' or str(key) == 'XF64AudioPlay':
		play_button_()



def vol_click(event):
	global global_volume,vol_button

	if global_volume < Decimal('1.00'):
		global_volume += Decimal('0.05')

		pygame.mixer.music.set_volume(float(global_volume))
		vol_button.config(text='vol: ' + str(global_volume))

def vol_dec(event):
	global global_volume,vol_button

	if global_volume > Decimal('0.00'):
		global_volume -= Decimal('0.05')
		pygame.mixer.music.set_volume(float(global_volume))
		vol_button.config(text='vol: ' + str(global_volume))

def vol_scroll(event):
	if event.delta > 0:
		vol_click(event)
	else:
		vol_dec(event)

vol_button.bind('<MouseWheel>', vol_scroll)

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


skip_left.bind('<Button-1>',skip_left_click)
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


skip_right.bind('<Button-1>',skip_right_click)
skip_right.bind('<Enter>', skip_right_enter)
skip_right.bind('<Leave>', skip_right_leave)







def update_playing_info():	#Good luck reading this...
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


	if selected_song is not None:
		song_basename = os.path.basename(selected_song)
		if len(song_basename) > 35:
			basename = os.path.basename(selected_song)
			song_name.config(text=basename[:len(basename) // 2] + '..')


	if next_song_name1 is not None:
		if len(song1_ext[0]) > 45:
			title = next_song_name1[:len(song1_ext[0]) // 2] + '..'
			next_song1.config(text=title, anchor='w')
		else:
			next_song1.config(text=song1_ext[0], anchor='w')

	if next_song_name2 is not None:
		if len(song2_ext[0]) > 45:
			title = next_song_name2[:len(song2_ext[0]) // 2] + '..'
			next_song2.config(text=title, anchor='w')
		else:
			next_song2.config(text=song2_ext[0], anchor='w')

	if next_song_name3 is not None:
		if len(song3_ext[0]) > 45:
			title = next_song_name3[:len(song3_ext[0]) // 2] + '..'
			next_song3.config(text=title, anchor='w')			
		else:
			next_song3.config(text=song3_ext[0], anchor='w')

	if next_song_name4 is not None:
		if len(song4_ext[0]) > 45:
			title = next_song_name4[:len(song4_ext[0]) // 2] + '..'
			next_song4.config(text=title, anchor='w')
		else:
			next_song4.config(text=song4_ext[0], anchor='w')
	
	if next_song_name5 is not None:
		if len(song5_ext[0]) > 45:
			title = next_song_name5[:len(song5_ext[0]) // 2] + '..'
			next_song5.config(text=title, anchor='w')
		else:
			next_song5.config(text=song5_ext[0], anchor='w')


	if playing == True:
		play_inf = 'playing'
	elif paused == True:
		play_inf = 'paused'
	elif paused == False and playing == False:
		play_inf = 'idle'

	if artist_name != None:
		if len(artist_name) > 14:
			artist_label.place_configure(x=48)
			artist_label.config(text=artist_name[:len(artist_name) // 2] + '..')
		if artist_name == "graphite":
			artist_label.place_configure(x=48)    
	elif artist_name == None:
		artist_name = "graphite"



	playing_info.config(text=str(play_inf))
	window.after(50, update_playing_info)

def __updatebar():
	global start_geo, exten_geo

	if window.winfo_width() == 480:
		window.geometry(str(exten_geo))
	else:
		window.geometry(str(start_geo))
def __updategputex():
	global _gpuflip, _standardbg, _standardfg, _gpumode

	if _gpuflip == "dark":
		_standardbg = "white"
		_standardfg = "black"
		_gpuflip = "light"
		_gpumode = "dark"
		window.config(background=_standardbg)
	else:
		_standardbg = "black"
		_standardfg = "white"
		_gpuflip = "dark"
		_gpumode = "light"
		window.config(background=_standardbg)
	update_label_colors(window)
update_playing_info()
window.bind('<Escape>', lambda event: __updategputex())
#window.bind('<Tab>', lambda event: __updatebar())
window.mainloop()

#this is all, modify graphite however you want.
#xtn

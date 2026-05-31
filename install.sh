#!/bin/bash

issu=$(whoami)

clear

if [[ $issu == "root" ]]; then
	echo "You are either running this with sudo or you are root."
	echo "Please run the script as a normal user."
	echo "Otherwise, you'll install graphite to root."
fi

echo "installing dependencies with pip..."
pip install -r misc/requirements.txt --break-system-packages --no-input
pip uninstall tk pillow --break-system-packages --no-input

echo "making directories and copying files..."

mkdir -p ~/.config/graphite
mkdir -p ~/.config/graphite/playlists
touch ~/.config/graphite/graphite.conf
touch ~/.config/graphite/playlists/graphite.pl
cp -r logo/*.png ~/.config/graphite/
echo "you may be prompted with sudo. it only copies files, don't worry."
sudo cp -r graphite /bin/
sudo cp -r misc/6x13.otb $HOME/.local/share/fonts/

echo "
foreground = black;
background = white;
font = Misc Fixed;
font size = 10;

directory to choose music from = $HOME;
logo2 directory = $HOME/.config/graphite/logo2.png;
logo3 directory = $HOME/.config/graphite/logo3.png;
send notifs on song play = 0;

dir x = 0;
dir y = 215;
play x = 35;
play y = 215;
vol x = 105;
vol y = 215;
passed x = 230;
passed y = 222;
artist x = 0;
artist y = 13;
song x = 0;
song y = 0;
status x = 220;
status y = 0;
" > ~/.config/graphite/graphite.conf

clear
echo "you need to install - tk, python-pillow - manually, in your package manager."
echo "this is very important. please do so, otherwise graphite wont bother to start!!!!!!"

echo "finished"
exit


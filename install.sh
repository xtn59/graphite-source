#!/bin/bash

issu=$(whoami)

clear

if [[ $issu == "root" ]]; then
	echo "You are either running this with sudo or you are root."
	echo "Please run the script as a normal user."
	echo "Otherwise, you'll install graphite to root."
	exit
fi

echo "making directories and copying files..."

mkdir -p ~/.config/graphite
touch ~/.config/graphite/graphite.conf
cp -r *.png ~/.config/graphite/
echo "you may be prompted with sudo. it only copies files, don't worry."
sudo cp -r graphite /bin/
sudo cp -r 6x13.otb $HOME/.local/share/fonts/

echo "

foreground:black
background:white
font:Misc Fixed

# Path.home() is a function in python
directory to choose music from:f'{Path.home()}'
logo2 directory:$HOME/.config/graphite/logo2.png
logo3 directory:$HOME/.config/graphite/logo3.png

send notifs on song play:0

" > ~/.config/graphite/graphite.conf

echo "finished"
exit


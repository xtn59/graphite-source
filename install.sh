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
sudo cp -r graphite /bin/

echo "

foreground:black
background:white
big font: DejaVu sans
small font: DejaVu Sans
window width:480
window height:276

album cover x:350
album cover y:90
album cover width:100
album cover height:100

# Path.home() is a function in python
directory to choose music from:f'{Path.home()}'
logo2 directory:/home/bdr/.config/graphite/logo2.png
logo3 directory:/home/bdr/.config/graphite/logo3.png

send notifs on song play:0
developermode:0

" > ~/.config/graphite/graphite.conf

echo "finished"
exit


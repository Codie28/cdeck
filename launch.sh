dir=`dirname $0`

if ! pacman -Qs python-elgato-streamdeck; then
  echo Streamdeck python api is not installed, installing
  yay -S python-elgato-streamdeck
  sudo pacman -S python-setproctitle hidapi
fi

mkdir $dir/assets/plart
/usr/bin/python $dir/cdeck.py

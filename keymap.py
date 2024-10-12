import os
import subprocess
import urllib.request
from PIL import Image, ImageDraw

FONT =  "MesloLGSNerdFont-Bold.ttf"
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

prev_player = "os"
download_plart = True

oriant = 3

def get_key_style(deck, index, pushed):
    global oriant
    match index:
        # TODO change based on the current theme
        case index if ( oriant == 0 and index == 2 ) or ( oriant == 3 and index == 0 ) :
            name   = "funt"
            icon   = "mode.png"
            font   = FONT
            label  = "uwu"
            action = ""
        case index if ( oriant == 0 and index == 3 ) or ( oriant == 3 and index == 1 ) :
            name   = "funt"
            icon   = "mode.png"
            font   = FONT
            label  = "test"
            action = ""
        case index if index >= 5 and index <= 7:
            players = subprocess.run(['playerctl', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('UTF-8')
            players = players.split("\n")
            players = players[:-1]
            name   = "pldisp"
            icon   = "mode.png"
            font   = FONT
            if len(players) > index - 5:
                label = players[index-5]
            else:
                label = "nome" 
            action = ""

        case index if index > 9 and index < 15:
            try:
                return get_player_style(index)
            except:
                return { "name": "error" }
        case index if ( index >= oriant + 0 and index < oriant + 2 ) or ( index >= oriant + 5 and index < oriant + 7 ):
            if pushed:
                oriant = 0 if oriant == 3 else 3
            try:
                return get_player_art(index - oriant)
            except:
                return { "name": "error"}
        case _:
            name   = "empty"
            icon   = ""
            font   = "" 
            label  = ""
            action = ""

    return {
        "name":   name,
        "icon":   os.path.join(ASSETS_PATH, icon),
        "font":   os.path.join(ASSETS_PATH, font),
        "label":  label,
        "action": action 
    }

def get_player_style(index):
    current_player = get_best_player()
    status  = subprocess.run(['playerctl', '-p', current_player, 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('UTF-8')
    # talk about wierd logic
    play_pause = "pause" if status == "Playing\n" else "play"
    index -= 10
    icon_list = ['minus', 'prev', play_pause, 'next', 'plus']
    action = ""

    if current_player == "os":
        action_list = ['amixer -q sset Master 4%-', 'previous', 'play-pause', 'next', 'amixer -q sset Master 4%+']
        action = action_list[index]
    else:
        action_list = ['volume 0.05-', 'previous', 'play-pause', 'next', 'volume 0.05+']
        action = f'playerctl -p {current_player} {action_list[index]}'

    if str(index) in '04':
        try:
            volume  = subprocess.run(['playerctl', '-p', current_player, 'volume'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('UTF-8').split('\n')[0]
            label = f'{round(float(volume) * 100)}%'
        except:
            label = ''

    else:
        label = ''

    return {
        "name":   f"player-{index}",
        "icon":   os.path.join(ASSETS_PATH, f'{icon_list[index]}.png'),
        "font":   os.path.join(ASSETS_PATH, FONT),
        "label":  label,
        "action": action,
        "player": current_player
    }

def get_best_player():
    global prev_player

    status  = subprocess.run(['playerctl', '-a', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('UTF-8')
    players = subprocess.run(['playerctl', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('UTF-8')
    if len(players) > 0:
        try:
            playing_index = (status.split('\n').index('Playing'))
            current_player = players.split('\n')[playing_index]
        except:
            if prev_player == "os":
                prev_player = players.split('\n')[0]
            current_player = prev_player

        prev_player = current_player
        return current_player
    else:
        return "os"

def get_player_art(index):
    if str(index) not in "0156":
        return { "name": "error" }
    current_player = get_best_player()
    if current_player.startswith('firefox'):
        return { "name": "error" }

    art_url  = subprocess.run(['playerctl', '-p', current_player, 'metadata', 'mpris:artUrl'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('UTF-8')

    plart_path = os.path.join(ASSETS_PATH, f'plart/')

    urllib.request.urlretrieve(art_url, plart_path + '/plart.png')
    base_img = Image.open(plart_path + 'plart.png')

    base_img = base_img.resize((144 * 2, 144 * 2))

    corner_3 = base_img.copy()
    corner_3.crop((144 * 0, 144 * 0, 144 * 1, 144 * 1)).save(plart_path + '/corner0.png')

    corner_4 = base_img.copy()
    corner_4.crop((144 * 1, 144 * 0, 144 * 2, 144 * 1)).save(plart_path + '/corner1.png')

    corner_3 = base_img.copy()
    corner_3.crop((144 * 0, 144 * 1, 144 * 1, 144 * 2)).save(plart_path + '/corner5.png')

    corner_4 = base_img.copy()
    corner_4.crop((144 * 1, 144 * 1, 144 * 2, 144 * 2)).save(plart_path + '/corner6.png')

    return {
        "name":   f"plart-{index}",
        "icon":   f'{plart_path}/corner{index}.png',
        "font":   os.path.join(ASSETS_PATH, FONT),
        "label":  '',
        "action": '',
        "player": current_player
    }

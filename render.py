import os
from PIL import Image, ImageDraw, ImageFont
from StreamDeck.ImageHelpers import PILHelper
from catppuccin import PALETTE

from keymap import get_key_style

# This whole funcion is a mess but `don fix that ain't broke`.
def render_key_image(deck, key_style, pushed=False):
    bg_color = get_background_color()
    pl_color = get_playerbg_color()

    if key_style["name"] == "empty":
        image = Image.new(mode='RGBA', size=(145, 144), color=bg_color)
    elif key_style["name"] == 'error':
        image = Image.new(mode='RGBA', size=(144, 144), color=get_error_color())
    else:
        image = 1
        if key_style["name"].startswith('player'):
            icon = Image.open(key_style["icon"])
            icon = icon.convert('RGBA')
            # player-2 is the play-pause button
            if key_style["name"] == "player-2":
                image = Image.new(mode='RGBA', size=(144, 144), color=get_playerfg_color(key_style["player"]))
            else:
                image = Image.new(mode='RGBA', size=(144, 144), color=pl_color)
                bg_draw = ImageDraw.Draw(image)
                bg_draw.rounded_rectangle([(16, 16), (144-16, 144-16)], radius=32, fill=get_playerfg_color(key_style["player"]))
            icon = icon.resize((144, 144))
            image = Image.alpha_composite(image, icon)
        elif key_style["name"] == 'plicon':
            image = Image.new(mode='RGBA', size=(144, 144), color=get_playerfg_color(key_style["player"]))
        else:
            icon = Image.open(key_style["icon"])
            icon = icon.convert('RGBA')
            icon = icon.resize((144, 144))
            background = Image.new(mode='RGBA', size=(144, 144), color=bg_color)
            image = Image.alpha_composite(background, icon)

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(key_style["font"], 14 * 2 )
        draw.text((image.width / 2, image.height - 5), text=key_style["label"], font=font, anchor="ms", fill=get_font_color())

    image = PILHelper.create_scaled_key_image(deck, image, margins=[0, 0, 0, 0])
    return PILHelper.to_native_key_format(deck, image)

def update_key_image(deck, key, pushed):
    key_style = get_key_style(deck, key, pushed)
    image = render_key_image(deck, key_style)

    with deck:
        deck.set_key_image(key, image)

def get_background_color():
    prefix = os.environ['QTILE_THEME_HOME']
    with open(os.path.expanduser(f'{prefix}/catscheme')) as f:
        file = f.read().split('\n')
        # TODO: make it work with more then two themes
        return PALETTE.frappe.colors.surface2.hex if file[0] == 'frappe' else PALETTE.latte.colors.overlay0.hex

def get_playerbg_color():
    prefix = os.environ['QTILE_THEME_HOME']
    with open(os.path.expanduser(f'{prefix}/catscheme')) as f:
        file = f.read().split('\n')
        # TODO: make it work with more then two themes
        return PALETTE.frappe.colors.surface0.hex if file[0] == 'frappe' else PALETTE.latte.colors.surface0.hex

def get_playerfg_color(player_name):
    palatte = 1
    prefix = os.environ['QTILE_THEME_HOME']
    with open(os.path.expanduser(f'{prefix}/catscheme')) as f:
        file = f.read().split('\n')
        palatte = PALETTE.frappe.colors if file[0] == 'frappe' else PALETTE.latte.colors

    # god damn it firefox
    if player_name.startswith('firefox'):
        return palatte.yellow.hex
    else:
        pl_colors = {
            "spotify": palatte.green.hex,
            "os":    palatte.base.hex,
        }
        return pl_colors[player_name] or "#ffccff"

def get_font_color():
    prefix = os.environ['QTILE_THEME_HOME']
    with open(os.path.expanduser(f'{prefix}/catscheme')) as f:
        file = f.read().split('\n')
        # TODO: make it work with more then two themes
        return PALETTE.frappe.colors.crust.hex if file[0] == 'frappe' else PALETTE.latte.colors.text.hex

def get_error_color():
    prefix = os.environ['QTILE_THEME_HOME']
    with open(os.path.expanduser(f'{prefix}/catscheme')) as f:
        file = f.read().split('\n')
        # TODO: make it work with more then two themes
        return PALETTE.frappe.colors.red.hex if file[0] == 'frappe' else PALETTE.latte.colors.red.hex

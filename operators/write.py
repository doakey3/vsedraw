import bpy
import os
from .utils import make_glyph_strip

def get_glyph_width(vert_collection):
    verts = []
    for group in vert_collection:
        verts.extend(group)
    return max(verts, key=lambda v: v[0])[0]


def get_m_width():
    letter_folder = os.path.join(os.path.dirname(__file__), 'letters')
    glyph_name = get_char_name('M') + '.glyph'
    path = os.path.join(letter_folder, glyph_name)

    with open(os.path.join(letter_folder, glyph_name)) as f:
        char_text = f.read().strip()
    lines = char_text.split('\n')

    verts = []
    for line in lines:
        curve_verts = eval(line)
        for vert in curve_verts:
            verts.append(vert)
    max_x = max(verts, key=lambda v: v[0])[0]
    return max_x


def get_char_name(char):
    character_dict = {
        "!": "exclamation",
        "#": "pound",
        "$": "dollar",
        "%": "percentage",
        "&": "ampersand",
        "'": "quotesingle",
        "(": "parenthesisleft",
        ")": "parenthesisright",
        "*": "asterisk",
        "+": "plus",
        ",": "comma",
        "-": "minus",
        ".": "period",
        "/": "slash",
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        ":": "colon",
        ";": "semicolon",
        "<": "lessthan",
        "=": "equal",
        ">": "greaterthan",
        "?": "question",
        "@": "at",
        "A": "a-uppercase",
        "B": "b-uppercase",
        "C": "c-uppercase",
        "D": "d-uppercase",
        "E": "e-uppercase",
        "F": "f-uppercase",
        "G": "g-uppercase",
        "H": "h-uppercase",
        "I": "i-uppercase",
        "J": "j-uppercase",
        "K": "k-uppercase",
        "L": "l-uppercase",
        "M": "m-uppercase",
        "N": "n-uppercase",
        "O": "o-uppercase",
        "P": "p-uppercase",
        "Q": "q-uppercase",
        "R": "r-uppercase",
        "S": "s-uppercase",
        "T": "t-uppercase",
        "U": "u-uppercase",
        "V": "v-uppercase",
        "W": "w-uppercase",
        "X": "x-uppercase",
        "Y": "y-uppercase",
        "Z": "z-uppercase",
        "[": "bracketleft",
        "\\": "backslash",
        "]": "bracketright",
        "^": "caret",
        "_": "underscore",
        "`": "grave",
        "a": "a-lowercase",
        "b": "b-lowercase",
        "c": "c-lowercase",
        "d": "d-lowercase",
        "e": "e-lowercase",
        "f": "f-lowercase",
        "g": "g-lowercase",
        "h": "h-lowercase",
        "i": "i-lowercase",
        "j": "j-lowercase",
        "k": "k-lowercase",
        "l": "l-lowercase",
        "m": "m-lowercase",
        "n": "n-lowercase",
        "o": "o-lowercase",
        "p": "p-lowercase",
        "q": "q-lowercase",
        "r": "r-lowercase",
        "s": "s-lowercase",
        "t": "t-lowercase",
        "u": "u-lowercase",
        "v": "v-lowercase",
        "w": "w-lowercase",
        "x": "x-lowercase",
        "y": "y-lowercase",
        "z": "z-lowercase",
        "{": "curlyleft",
        "|": "verticalbar",
        "}": "curlyright",
        "~": "tilde",
        "Δ": "delta",
        "←": "arrowleft",
        "↑": "arrowup",
        "→": "arrowright",
        "↓": "arrowdown",
        "☐": "box",
        "♀": "female",
        "♂": "male",
        '"': "quotedouble",
    }
    try:
        return character_dict[char]
    except KeyError:
        return character_dict['☐']


class Write(bpy.types.Operator):
    bl_label = "Write"
    bl_idname = "vsedraw.write"
    bl_description = "Write the text"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        text = scene.vsedraw.text
        if text == "":
            return {"FINISHED"}
        letter_folder = os.path.join(os.path.dirname(__file__), 'letters')

        m_width = get_m_width()

        curve_verts = []

        current_x = 0

        for char in text:
            if char == " ":
                current_x += m_width
            else:
                glyph_name = get_char_name(char) + ".glyph"
                with open(os.path.join(letter_folder, glyph_name)) as f:
                    char_text = f.read().strip()
                lines = char_text.split('\n')

                for line in lines:
                    verts = eval(line)
                    for vert in verts:
                        vert[0] += current_x
                    curve_verts.append(verts)

                current_x = get_glyph_width(curve_verts) + m_width / 2

        new_scene = bpy.data.scenes.new(text)
        new_scene.render.fps = scene.render.fps
        new_scene.render.fps_base = scene.render.fps_base
        context.screen.scene= new_scene
        make_glyph_strip(scene, new_scene, curve_verts)

        return {"FINISHED"}

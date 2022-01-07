from enum import Enum
def get_letters(file_name: str) -> list:
    with open(file_name, 'r') as f:
        notes = f.readlines()
        return list(map(lambda x: x.replace('\n', ''), notes))

def MARK(note:str) -> str:
    return f"({note})"
STRING_SEPARATOR = "\n"
FRET_SEPARATOR = "|"
FRET_MARGIN = "-"
FRET_SIZE = 7


class Note:
    margin = ""
    marker = ""
    def __init__(self, marker, margin):
        self.marker = marker
        self.margin = margin

class NoteKind(Enum):
    PRIME = Note(lambda x: f"=({x})=", "=")
    THIRD = Note(lambda x: f"=={x}==", "-")
    FIFTH = Note(lambda x: f"={x}=", "-")
    OTHER = Note(lambda x: f"+{x}+", "-")
    REGULAR = Note(lambda x: x, "-")


notes = get_letters('notes.txt')
sel_notes = list(map(MARK, notes))


def order_notes(first_one: str, notes: list) -> list:
    idx = notes.index(first_one)
    size = len(notes)
    result = list([notes[(x + idx) % size] for x in range(size)])
    last_one = first_one
    try:
        last_one = str(int(notes[-1]) + 1)
    except:
        last_one = first_one
    result.append(last_one)
    return result


def print_fret_with_note(note: str, n: Note) -> str:
    size = FRET_SIZE
    margin = "-"
    note_size = len(note)
    margin_right = (size - note_size) // 2
    margin_left = size - note_size - margin_right
    
    return margin_left * n.margin + note + margin_right * n.margin

def get_note_def(note: str, notes: list):
    try:
        idx = notes.index(note)

        if idx == 0:
            return NoteKind.PRIME
        elif idx == 1:
            return NoteKind.THIRD
        elif idx == 2: 
            return NoteKind.FIFTH
        else:
            return NoteKind.OTHER
    except:
        return NoteKind.REGULAR

def print_fret(note: str, notes: list, mark_function) -> str:
    n = get_note_def(note, notes).value
    return print_fret_with_note(n.marker(note) if note in notes else note, n) 

def print_string(starting_note: str, notes: list, base_notes: list, mark_function) -> str: 
    ordered_notes = order_notes(starting_note, base_notes) 
    string_notes = [print_fret(x, notes, mark_function) for x in ordered_notes]
    return FRET_SEPARATOR.join(string_notes)

def customize_string(string: str) -> str:
    return string[0:FRET_SIZE] + "[" + string[FRET_SIZE:] + "]"

def print_fretboard(notes: list, base_notes: list, mark_function)->str:
    starting_notes = ["E", "A", "D", "G", "H", "E"][::-1]
    strings = [print_string(x, notes, base_notes, mark_function) for x in starting_notes]
    strings.insert(0, print_string("0", [], list(map(str, range(12))),lambda x: x))
    pretty_strings = map(customize_string, strings)
    fretboard = STRING_SEPARATOR.join(pretty_strings)
    return fretboard

print("==== A dur ====")
print(print_fretboard(["A", "C'", "E"], notes, MARK))
print("\n\n")
print("==== B dur ====")
print(print_fretboard(["B", "D", "F", "D'"], notes, MARK))




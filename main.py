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

class NoteDecorator:
    def __init__(self, f, margin):
        self.f = f
        self.margin = margin

class NoteKind(Enum):
    PRYMA = NoteDecorator(lambda x: f"=({x})=", "=")
    TERCJA = NoteDecorator(lambda x: f"=={x}==", "-")
    KWINTA = NoteDecorator(lambda x: f"={x}=", "-")
    DODATKOWA = NoteDecorator(lambda x: f"+{x}+", "-")
    ZWYKLA = NoteDecorator(lambda x: x.lower(), "-")

class Note:
    def __init__(self, name: str, kind: NoteKind):
        self.name = name
        self.kind = kind

    def decorated(self):
        return self.kind.value.f(self.name)
    
    def get_margin(self):
        return self.kind.value.margin



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


def print_fret_with_note(n: Note) -> str:
    size = FRET_SIZE
    note_size = len(n.decorated())
    margin_right = (size - note_size) // 2
    margin_left = size - note_size - margin_right
    
    return margin_left * n.get_margin() + n.decorated() + margin_right * n.get_margin()

def get_note_def(note: str, notes: list):
    try:
        idx = notes.index(note)

        if idx == 0:
            return NoteKind.PRYMA
        elif idx == 1:
            return NoteKind.TERCJA
        elif idx == 2: 
            return NoteKind.KWINTA
        else:
            return NoteKind.DODATKOWA
    except:
        return NoteKind.ZWYKLA

def print_fret(note: str, notes: list) -> str:
    # n = get_note_def(note, notes).value
    for n in notes:
       if n.name == note:
           return print_fret_with_note(n)
    return print_fret_with_note(Note(note, NoteKind.ZWYKLA)) 

def print_string(starting_note: str, notes: list, base_notes: list) -> str: 
    ordered_notes = order_notes(starting_note, base_notes) 
    string_notes = [print_fret(x, notes) for x in ordered_notes]
    return FRET_SEPARATOR.join(string_notes)

def customize_string(string: str) -> str:
    return string[0:FRET_SIZE] + "[" + string[FRET_SIZE:] + "]"

def print_fretboard(notes: list, base_notes: list)->str:
    starting_notes = ["E", "A", "D", "G", "H", "E"][::-1]
    strings = [print_string(x, notes, base_notes) for x in starting_notes]
    strings.insert(0, print_string("0", [], list(map(str, range(12)))).replace("-", " "))
    pretty_strings = map(customize_string, strings)
    fretboard = STRING_SEPARATOR.join(pretty_strings)
    return fretboard

def get_minor_game_notes(prime: str, notes: list) -> list:
    ordered_notes = order_notes(prime, notes)
    return [
        Note(prime, NoteKind.PRYMA),
        Note(ordered_notes[2], NoteKind.DODATKOWA),
        Note(ordered_notes[3], NoteKind.DODATKOWA),
        Note(ordered_notes[5], NoteKind.DODATKOWA),
        Note(ordered_notes[7], NoteKind.DODATKOWA),
        Note(ordered_notes[8], NoteKind.DODATKOWA),
        Note(ordered_notes[10], NoteKind.DODATKOWA),

    ]

def get_major_game_notes(prime: str, notes: list) -> list:
    ordered_notes = order_notes(prime, notes)
    return [
        Note(prime, NoteKind.PRYMA),
        Note(ordered_notes[2], NoteKind.DODATKOWA),
        Note(ordered_notes[4], NoteKind.DODATKOWA),
        Note(ordered_notes[5], NoteKind.DODATKOWA),
        Note(ordered_notes[7], NoteKind.DODATKOWA),
        Note(ordered_notes[9], NoteKind.DODATKOWA),
        Note(ordered_notes[11], NoteKind.DODATKOWA),

    ]

def get_minor_pentatonic_notes(prime: str, notes: list) -> list:
    ordered_notes = order_notes(prime, notes)
    return [
        Note(prime, NoteKind.PRYMA),
        Note(ordered_notes[3], NoteKind.DODATKOWA),
        Note(ordered_notes[5], NoteKind.DODATKOWA),
        Note(ordered_notes[7], NoteKind.DODATKOWA),
        Note(ordered_notes[10], NoteKind.DODATKOWA),

    ]

def get_major_pentatonic_notes(prime: str, notes: list) -> list:
    ordered_notes = order_notes(prime, notes)
    return [
        Note(prime, NoteKind.PRYMA),
        Note(ordered_notes[2], NoteKind.DODATKOWA),
        Note(ordered_notes[4], NoteKind.DODATKOWA),
        Note(ordered_notes[7], NoteKind.DODATKOWA),
        Note(ordered_notes[9], NoteKind.DODATKOWA),

    ]


def get_minor_chord_notes(prime: str, notes: list) -> list:
    ordered_notes = order_notes(prime, notes)
    return [
        Note(prime, NoteKind.PRYMA),
        Note(ordered_notes[3], NoteKind.TERCJA),
        Note(ordered_notes[7], NoteKind.KWINTA)
    ]
def get_major_chord_notes(prime: str, notes: list) -> list:
    ordered_notes = order_notes(prime, notes)
    return [
        Note(prime, NoteKind.PRYMA),
        Note(ordered_notes[4], NoteKind.TERCJA),
        Note(ordered_notes[7], NoteKind.KWINTA)
    ]

def print_fretboard_with_selected_notes(title: str, sel_notes:list, notes: list):
    print(f"==== {title} ====")
    print(print_fretboard(sel_notes, notes))
    # print("\n")
    print("")

def print_fretboard_with_major_chord(prime: str, notes: list):
    sel_notes = get_major_chord_notes(prime, notes)
    print_fretboard_with_selected_notes(f"Akord {prime} dur", sel_notes, notes)

def print_fretboard_with_minor_chord(prime: str, notes: list):
    sel_notes = get_minor_chord_notes(prime, notes)
    print_fretboard_with_selected_notes(f"Akord {prime.lower()} moll", sel_notes, notes)

def print_fretboard_with_major_pentatonic(prime: str, notes: list):
    sel_notes = get_major_pentatonic_notes(prime, notes)
    print_fretboard_with_selected_notes(f"Pentatonika {prime} dur", sel_notes, notes)

def print_fretboard_with_minor_pentatonic(prime: str, notes: list):
    sel_notes = get_minor_pentatonic_notes(prime, notes)
    print_fretboard_with_selected_notes(f"Pentatonika {prime.lower()} moll", sel_notes, notes)

def print_fretboard_with_major_game(prime: str, notes: list):
    sel_notes = get_major_game_notes(prime, notes)
    print_fretboard_with_selected_notes(f"Gama {prime} dur", sel_notes, notes)

def print_fretboard_with_minor_game(prime: str, notes: list):
    sel_notes = get_minor_game_notes(prime, notes)
    print_fretboard_with_selected_notes(f"Gama {prime.lower()} moll", sel_notes, notes)

def print_legend():
    print("  |  ".join([f"{v.name} : {v.value.f('A')}" for v in NoteKind]))
    print("\n")

def print_both_chords(primes:list, notes:list):
    for prime in primes:
        print_fretboard_with_major_chord(prime, notes)
        print_fretboard_with_minor_chord(prime, notes)
        
def print_both_pentatonics(primes:list, notes:list):
    for prime in primes:
        print_fretboard_with_major_pentatonic(prime, notes)
        print_fretboard_with_minor_pentatonic(prime, notes)

def print_both_games(primes:list, notes:list):
    for prime in primes:
        print_fretboard_with_major_game(prime, notes)
        print_fretboard_with_minor_game(prime, notes)


primes = "CDEFGABH"
notes = get_letters('notes.txt')
sel_notes = list(map(MARK, notes))

# arr = [Note("A", NoteKind.PRIME), Note("C'", NoteKind.THIRD), Note("E", NoteKind.FIFTH)]
# print_fretboard_with_selected_notes("A dur", arr, notes)
print_legend()
# print_fretboard_with_major_chord("A", notes)
# print_fretboard_with_minor_chord("A", notes)
# print_both_chords(primes, notes)
print_both_pentatonics(primes, notes)
# print_both_games(primes, notes)
# print_fretboard_with_selected_notes("Gryf pusty", [], notes)
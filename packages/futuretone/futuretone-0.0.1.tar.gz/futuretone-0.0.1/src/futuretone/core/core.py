import enum
import random
import struct


class NoteType(enum.Enum):
    Triangle = 0
    Circle = 1
    Cross = 2
    Square = 3
    TriangleHold = 4
    CircleHold = 5
    CrossHold = 6
    SquareHold = 7
    # Invalid = 8
    # Invalid2 = 9
    # Invalid3 = 10
    SlideL = 12
    SlideR = 13
    SlideLPart = 15
    SlideRPart = 16


class Note(object):
    def __init__(self, button=None, pos=None, start=None, wobble=None, *reserved):
        super(Note, self).__init__()
        self.button = button or NoteType.Triangle
        self.pos = pos or (0, 0)
        self.start = start or (0, 0)
        self.wobble = wobble or 0.5
        self.reserved = reserved or [0, 0, 0]

    @classmethod
    def random(cls):
        max_width = 480
        max_height = 272

        button = random.choice(list(NoteType))
        position_x = float(random.randint(0, max_width))
        position_y = float(random.randint(0, max_height))
        start_x = float(random.randint(-100, max_width + 100))
        start_y = float(random.randint(-100, max_height + 100))
        wobble = random.random()
        return Note(button, (position_x, position_y), (start_x, start_y), wobble)

    def __str__(self):
        return self.button.name

    def __repr__(self):
        return f'{self.button!r} @ {self.pos} from {self.start}'


class NoteDef(object):
    def __init__(self, *notes):
        super(NoteDef, self).__init__()
        self.notes = notes
        assert 0 < len(self.notes) <= 4
        self.__struct = struct.Struct('<I144x28x')
        self.__struct_note = struct.Struct('<I5fiII')
        assert self.__struct.size == 0xB0
        assert self.__struct_note.size == 0x24

    def to_bytes(self):
        count = len(self.notes)
        buffer = bytearray(self.__struct.size)
        self.__struct.pack_into(buffer, 0, count)

        for i, note in enumerate(self.notes):
            self.__struct_note.pack_into(buffer, 4 + i * self.__struct_note.size,
                                         note.button.value,
                                         *note.pos,
                                         *note.start,
                                         note.wobble,
                                         *note.reserved)

        return buffer

    @staticmethod
    def from_bytes(bytearray_):
        count = int.from_bytes(bytearray_[:4], 'little')

        struct_note = struct.Struct('<I5fiII')
        assert struct_note.size == 0x24
        notes = []

        for i in range(count):
            data = struct_note.unpack_from(bytearray_, 4 + struct_note.size * i)
            button, pos_x, pos_y, start_x, start_y, wobble, *res = data

            button = next((e for e in NoteType if button == e.value), NoteType.Triangle)
            notes.append(Note(button, (pos_x, pos_y), (start_x, start_y), wobble, *res))

        return NoteDef(*notes)

    @classmethod
    def random(cls):
        buttons = random.randint(1, 4)
        notes = [Note.random() for _ in range(buttons)]
        return NoteDef(*notes)

    def __str__(self):
        return '+'.join([str(note) for note in self.notes])

    def __repr__(self):
        return '+'.join([repr(note) for note in self.notes])

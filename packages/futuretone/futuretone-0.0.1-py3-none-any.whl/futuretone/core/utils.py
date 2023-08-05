from ps4debug import PS4Debug
from .core import NoteDef


def spawn_note(debugger: PS4Debug, pid: int, *notes: NoteDef, **kwargs) -> int | None:
    executable_base = kwargs.get('base_address') or \
                      next(m[1] for m in debugger.get_process_maps(pid) if m[0] == 'executable')
    chart_base = debugger.read_uint64(pid, executable_base + 0xC687708 + 0x2C600)

    # No chart loaded, spawning a note would crash the game
    if chart_base == 0:
        return

    game_target = int.to_bytes(executable_base + 0x08B34000 + 0x3B81E78, 4, 'little')
    call_target = int.to_bytes(executable_base + 0x734E30, 8, 'little')

    memory_size = 4096
    note_spawner = (b'\x48\x8B\xF7\x48\x8B\xDF\x48\x31\xFF\xBF' + game_target +
                    b'\x31\xDB\x49\xBF' + call_target + b'\x41\xFF\xD7\xC3')
    rpc_stub = kwargs.get('rpc_stub') or debugger.install_rpc(pid)

    with debugger.memory(pid, memory_size) as memory:
        debugger.write_memory(pid, memory, note_spawner)

        note_base = memory + len(note_spawner)
        notes_max = (memory_size - len(note_spawner)) // 0xB0

        # Ensure the note data fits in memory
        assert len(notes) <= notes_max

        # Send notes to game
        for i, note in enumerate(notes):
            note_bytes = note.to_bytes()
            debugger.write_memory(pid, note_base + i * len(note_bytes), note_bytes)

        # Spawn the note
        rax = debugger.call(pid, memory, note_base, rpc_stub=rpc_stub)
        return rax[0]

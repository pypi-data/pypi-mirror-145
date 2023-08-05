import typer
from .ps4debug import PS4Debug
from .core import spawn_note, NoteDef, Note, NoteType

app = typer.Typer()


@app.command()
def test_spawn():
    with PS4Debug() as ps4:
        typer.echo(f'Connected to {typer.style(ps4.endpoint[0], fg="green")}')

        processes = ps4.get_processes()
        typer.echo(f'Retrieved {typer.style(len(processes), fg="green")} processes')

        pid = next(p.pid for p in processes if p.name == 'eboot.bin')
        if not pid:
            raise Exception('No eboot.bin loaded')
        typer.echo(f'eboot.bin found ({typer.style(pid, fg="green")})')

        maps = ps4.get_process_maps(pid)
        base_address = next(map_.start for map_ in maps if map_.name == 'executable')
        typer.echo(f'Retrieved base address: {typer.style(hex(base_address), fg="green")}')

        rpc_stub = ps4.install_rpc(pid)
        typer.echo(f'Successfully injected RPC stub at {typer.style(hex(rpc_stub), fg="green")}')

        while typer.confirm('Press enter to spawn a random note', default=True):
            note = NoteDef.random()
            rax = spawn_note(
                ps4, pid, note,
                base_address=base_address,
                rpc_stub=rpc_stub)

            typer.echo(f'Spawned note {typer.style(note, fg="green")} (rax = {typer.style(rax, fg="yellow")})')


if __name__ == '__main__':
    app()

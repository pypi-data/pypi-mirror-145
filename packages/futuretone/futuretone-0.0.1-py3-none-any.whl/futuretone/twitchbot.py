from twitchio.ext import commands, pubsub
import random
import asyncio
import typer

from .core import Note, NoteDef, NoteType, spawn_note
from ps4debug import PS4Debug


class FutureToneIntegrationBot(commands.Bot):
    def __init__(self, **settings):
        channel_name = settings.get('twitch_channel')
        bot_token = settings.get('bot_token')
        user_token = settings.get('access_token') or bot_token
        ps4_ip = settings.get('ps4_ip')
        title_id = settings.get('title_id')

        if not channel_name:
            raise Exception('No channel name provided!')

        if not bot_token:
            raise Exception('No bot token provided!')

        assert title_id == 'CUSA06211'

        super(FutureToneIntegrationBot, self).__init__(
            token=bot_token,
            initial_channels=[channel_name],
            prefix='!'
        )

        self.title_id = title_id
        self.pubsub = pubsub.PubSubPool(self)
        self.channel_name = channel_name
        self.user_token = user_token
        self.ps4debug = PS4Debug(ps4_ip)

    def __enter__(self):
        self.ps4debug.__enter__()

        typer.echo(f'Connected to {typer.style(self.ps4debug.endpoint[0], fg="green")}')

        processes = self.ps4debug.get_processes()
        typer.echo(f'Retrieved {typer.style(len(processes), fg="green")} processes')

        pid = next(p.pid for p in processes if p.name == 'eboot.bin')
        if not pid:
            raise Exception('No eboot.bin loaded')
        typer.echo(f'eboot.bin found ({typer.style(pid, fg="green")})')

        process_info = self.ps4debug.get_process_info(pid)
        if process_info.title_id != self.title_id:
            raise Exception(f'Wrong game running. Expected: {self.title_id}, got: {process_info.title_id}')
        typer.echo(f'Game found [{typer.style(self.title_id, fg="green")}]')

        maps = self.ps4debug.get_process_maps(pid)
        base_address = next(map_.start for map_ in maps if map_.name == 'executable')
        typer.echo(f'Retrieved base address: {typer.style(hex(base_address), fg="green")}')

        rpc_stub = self.ps4debug.install_rpc(pid)
        typer.echo(f'Successfully injected RPC stub at {typer.style(hex(rpc_stub), fg="green")}')

        self.pid = pid
        self.base_address = base_address
        self.rpc_stub = rpc_stub
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ps4debug.__exit__(exc_type, exc_val, exc_tb)
        self.ps4debug = None
        self.pid = None
        self.base_address = None
        self.rpc_stub = None

    async def event_ready(self):
        typer.echo(f'Logged in as | {typer.style(self.nick, fg="green")}')
        typer.echo(f'User id is | {typer.style(self.user_id, fg="green")}')

        channel = await self.fetch_channel(self.channel_name)
        await self.subscribe_to_topics(
            pubsub.channel_points(self.user_token)[channel.user.id],
        )

    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage):
        if event.status != 'UNFULFILLED' or event.reward.paused or event.reward.title != 'Spawn random note':
            return

        text = event.input
        user_name = event.user.name
        notes = [NoteDef.random()]

        typer.echo(f'{typer.style(user_name, fg="green")} redeemed a random note: "{typer.style(text, fg="green")}"')
        typer.echo(f'  Generated note: {typer.style(notes[0], fg="green")}')
        if text:
            self.ps4debug.notify(f'{user_name}: {text}')

        rax = spawn_note(
            self.ps4debug, self.pid, *notes,
            base_address=self.base_address,
            rpc_stub=self.rpc_stub)

        delay_min, delay_max = 3, 10
        while rax is None:
            delay = random.randint(delay_min, delay_max)
            delay_min += 1
            delay_max += 2
            print(f'Could not spawn {typer.style(notes[0], fg="green")}.'
                  f'No song playing? Retrying in {delay} seconds...')
            await asyncio.sleep(delay)

            rax = spawn_note(
                self.ps4debug, self.pid, *notes,
                base_address=self.base_address,
                rpc_stub=self.rpc_stub)
        else:
            typer.echo(f'Spawned note {typer.style(notes[0], fg="green")} (rax = {typer.style(rax, fg="yellow")})')

    async def subscribe_to_topics(self, *topics):
        await self.pubsub.subscribe_topics(topics)

    @commands.command()
    async def help(self, ctx: commands.Context):
        if ctx.author.is_mod:
            await ctx.send(f'You don\'t need help stoichSlow')

    @commands.command()
    async def quit(self, ctx: commands.Context):
        if ctx.author.is_mod:
            typer.echo(f'Bot disconnected by {typer.style(ctx.author.name, fg="green")}')
            await ctx.send('Bye!')
            await self.close()

    @commands.command()
    async def showcommands(self, ctx: commands.Context):
        if ctx.author.is_mod:
            await ctx.send(', '.join([f'!{k}' for k in self.commands]))

    @commands.command()
    async def test(self, ctx: commands.Context):
        if ctx.author.is_mod:
            note = NoteDef.random()
            rax = spawn_note(
                self.ps4debug, self.pid, note,
                base_address=self.base_address,
                rpc_stub=self.rpc_stub)

            typer.echo(f'Spawned note {typer.style(note, fg="green")} (rax = {typer.style(rax, fg="yellow")})')

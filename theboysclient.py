import discord

class TheBoysClient(discord.Client):
    admin = None
    admindm = None

    async def on_ready(self):
        print(f"{self.user} connected to server ")
        self.admin = self.get_user(618798266284507157)

    async def on_member_join(self, member):
        print(f"{member.name} has joined")
        if not self.admindm:
            self.admindm = await self.admin.create_dm()
        await self.admindm.send(f"{member.name} joined the server.\nID:{member.id}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        print(message.author)
        if not self.admindm:
            self.admindm = await self.admin.create_dm()
        await self.admindm.send(f"A crow from {message.author} ID:{message.author.id} of the north milord. It reads:\n {message.content}")

        if "pineapple" == message.content and not isinstance(message.channel, discord.DMChannel):
            await message.channel.send("The safeword has been uttered. Winter is coming, and there be dragons.")


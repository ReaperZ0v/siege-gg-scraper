from matches import SiegeMatch
import discord 


class ReplyClient(discord.Client):
    async def on_ready(self):
        print("ready...")

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return "NOT PERMITTED"

        if message.content.startswith('!show-match-log'):
            sg_match_object = SiegeMatch("6124-japan-league-apac-sengoku-vs-guts-gaming")
            await message.reply(sg_match_object, mention_author=True)

if __name__ == "__main__":
    client = ReplyClient()
    client.run('')
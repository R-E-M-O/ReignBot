from datetime import datetime, timedelta
from discord.ext import commands, tasks
import pytz



class ReignBot(commands.Bot):
    eastern = pytz.timezone('US/Eastern')
    now = datetime.now(eastern)
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    def __init__(self, command_prefix, intents):
        #subclass init of commands.Bot
        super().__init__(command_prefix=command_prefix, intents= intents)

        self.guild_raid_announcement_complete: bool = False
        self.guild_siege_announcement_complete: bool = False
        self.guild_infiniteraid_announcement_complete: bool = False

    @tasks.loop(seconds=5)  # Check every minute
    async def announcement_loop(self):
        current_weekday = self.now.weekday()

        if (current_weekday == self.THURSDAY) and not self.guild_raid_announcement_complete:
            self.guild_raid_announcement_complete = await self.check_announce_guildRaid()

        if (current_weekday == self.MONDAY) and (not self.guild_siege_announcement_complete):
            self.guild_siege_announcement_complete = await self.check_announce_guildSiege()

        if (current_weekday == self.SATURDAY) and not self.guild_infiniteraid_announcement_complete:
            self.guild_infiniteraid_announcement_complete = await self.check_announce_guildInfiniteRaid()

        if current_weekday == self.FRIDAY:
            self.guild_raid_announcement_complete = False

        if current_weekday == self.SATURDAY:
            self.guild_siege_announcement_complete = False

        if current_weekday == self.SUNDAY:
            self.guild_infiniteraid_announcement_complete = False

    
    async def check_announce_guildRaid(self) -> bool:
        raid_time = self.eastern.localize(datetime.strptime('09:00 PM', '%I:%M %p'))  # Set your raid time here
        announce_time = (datetime.combine(self.now, raid_time.time()) - timedelta(hours=9)).time()  # 9 hours before raid
        announce_complete = False

        if self.now.time() >= announce_time:
            channel_id = 1157848530388529243
            channel = self.get_channel(channel_id)

            # check channel is valid
            if channel:
                # Get the hour as an integer to remove leading zero
                hour = int(raid_time.strftime('%I'))
                # Get the minute
                minute = raid_time.strftime('%M')
                # Get AM/PM
                am_pm = raid_time.strftime('%p')

                # Send the announcement
                announcement = f"@everyone Guild Raid will take place at {hour}:{minute} {am_pm}. Get your attacks in ASAP if you cannot make it then!"
                await channel.send(announcement)
                announce_complete = True
            
        return announce_complete
        

    async def check_announce_guildSiege(self) -> bool:
        siege_time = self.eastern.localize(datetime.strptime('12:00 PM', '%I:%M %p'))
        announce_time = (datetime.combine(self.now, siege_time.time()) - timedelta(hours=2)).time()  # 2 hours before siege battle
        announce_complete = False

        if self.now.time() >= announce_time:
            channel_id = 1157848530388529243
            channel = self.get_channel(channel_id)

            # check channel is valid
            if channel:
                # Get the hour as an integer to remove leading zero
                hour = int(siege_time.strftime('%I'))
                # Get the minute
                minute = siege_time.strftime('%M')
                # Get AM/PM
                am_pm = siege_time.strftime('%p')

                # Send the announcement
                announcement = f"@everyone Guild Siege starts at {hour}:{minute} {am_pm}. ATTACK ONLY THE MARKED BASES!"
                await channel.send(announcement)
                announce_complete = True

        return announce_complete


    async def check_announce_guildInfiniteRaid(self) -> bool:
        announce_infiniteraid_time = self.eastern.localize(datetime.strptime('12:00 PM', '%I:%M %p'))
        announce_complete = False

        if self.now.time() >= announce_infiniteraid_time:
            channel_id = 1157848530388529243
            channel = self.get_channel(channel_id)

            # check channel is valid
            if channel:
                # Send the announcement
                announcement = f"@everyone Make sure you get your Infinite Raid attacks in before the weekend ends!"
                await channel.send(announcement)
                announce_complete = True
            
        return announce_complete


    async def on_ready(self):
        if not self.announcement_loop.is_running():
            self.announcement_loop.start()
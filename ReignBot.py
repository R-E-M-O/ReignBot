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

    @tasks.loop(seconds=5)  # Check every minute
    async def announcement_loop(self):
        guild_raid_announcement_complete: bool = False
        guild_siege_announcement_complete: bool = False
        guild_infiniteraid_announcement_complete: bool = False
        current_weekday = self.now.weekday()

        if (current_weekday == self.THURSDAY) and not guild_raid_announcement_complete:
            guild_raid_announcement_complete = await self.check_announce_guildRaid()

        if (current_weekday == self.MONDAY or self.THURSDAY) and not guild_siege_announcement_complete:
            guild_siege_announcement_complete = await self.check_announce_guildSiege(current_weekday)

        if (current_weekday == self.SATURDAY) and not guild_infiniteraid_announcement_complete:
            guild_infiniteraid_announcement_complete = await self.check_announce_guildInfiniteRaid()


        if current_weekday == self.FRIDAY:
            guild_raid_announcement_complete = False

        if current_weekday == self.SATURDAY:
            guild_siege_announcement_complete = False

        if current_weekday == self.SUNDAY:
            guild_infiniteraid_announcement_complete = False

    
    async def check_announce_guildRaid(self) -> bool:
        raid_time = self.eastern.localize(datetime.strptime('09:00 PM', '%I:%M %p'))  # Set your raid time here
        announce_time = (datetime.combine(self.now, raid_time.time()) - timedelta(hours=9)).time()  # 9 hours before raid

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
            else:
                # get_channel fail
                return False
            # announcement complete
            return True
        else:
            # not time to announce
            return False
        

    async def check_announce_guildSiege(self, DAY) -> bool:
        siege_time = self.eastern.localize(datetime.strptime('12:00 PM', '%I:%M %p'))
        announce_time = (datetime.combine(self.now, siege_time.time()) - timedelta(hours=3)).time()  # 9 hours before raid

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
                announcement = f"@everyone Guild Siege happening at {hour}:{minute} {am_pm}. ATTACK ONLY THE MARKED BASES!"
                await channel.send(announcement)
            else:
                # get_channel fail
                return False
            # announcement complete
            return True
        else:
            # not time to announce
            return False


    async def check_announce_guildInfiniteRaid(self) -> bool:
        announce_infiniteraid_time = self.eastern.localize(datetime.strptime('12:00 PM', '%I:%M %p'))

        if self.now.time() >= announce_infiniteraid_time:
            channel_id = 1157848530388529243
            channel = self.get_channel(channel_id)

            # check channel is valid
            if channel:
                # Send the announcement
                announcement = f"@everyone Make sure you get your Infinite Raid attacks in before the weekend ends!"
                await channel.send(announcement)
            else:
                # get_channel fail
                return False
            # announcement complete
            return True
        else:
            # not time to announce
            return False



        

        


    async def on_ready(self):
        self.announcement_loop.start()
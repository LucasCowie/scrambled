'use strict'

import 'dotenv/config'
import { Client, Events, ChannelType, GuildMemberManager } from 'discord.js'
import { calendar } from '../helpers/import-calendar.js'
import { checkExisitingForumEvents } from '../helpers/thread-manager.js'
import startCalendarMonitor from '../daemons/calendar-monitor.js'

export default {
  name: Events.ClientReady,
  once: true,
  execute: async (client) => {
    try {
      
      // get our guild (the server)
      const guild = await client.guilds.cache.get(process.env.WUMPUS_GUILD)
      console.log(`[discord] logged into "${guild.name}" [${guild.id}] as "${client.user.username}#${client.user.discriminator}"`)
      
      console.log(`[discord] checking calendar data`)
      const courseCalendar = await calendar()
      
      // check ...
      await checkExisitingForumEvents(
        process.env.NETW,
        courseCalendar.courses,
        process.env.PROG_WUMPUS_FORUM_CHANNEL,
        ChannelType,
        client
      )

      // Start the calendar monitoring daemon
      await startCalendarMonitor(client)

      return true
    } catch (ex) {
      console.error(`[discord] bot unable to start`, ex)
    }
  },
}

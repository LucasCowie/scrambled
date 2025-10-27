import 'dotenv/config'
import ical from 'node-ical'
import { resolve } from 'path'
import { existsSync } from 'fs'
import { readFile, writeFile } from 'fs/promises'

// importing and caching cal data ...

const cache = {
  courses: {
    prog: { key: 'prog', location: process.env.PROG, events: [], tagId: '' },
    webd: { key: 'webd', location: process.env.WEBD, events: [], tagId: '' },
    netw: { key: 'netw', location: process.env.NETW, events: [], tagId: '1432035950397096087' },
    osys: { key: 'osys', location: process.env.OSYS, events: [], tagId: ''},
    dbas: { key: 'dbas', location: process.env.DBAS, events: [], tagId: ''},
  },
  write: async function (path, data) {
    try {
      await writeFile(path, JSON.stringify(data, null, 2), 'utf8')
    } catch (err) {
      console.error('[discord] error writing json', err)
      throw err
    }
  },
  read: async function (path) {
    try {
      const content = await readFile(path, 'utf8')
      return JSON.parse(content)
    } catch (err) {
      if (err.code === 'ENOENT') {
        // File doesn’t exist — return null or a default
        return null
      }
      console.error('Error reading cache file:', err)
      throw err
    }
  },
}

export async function calendar() {
  // -. define the path to the cache file, and determine if file exists already
  const cachePath = resolve(process.env.BRIGHTSPACE_CACHE_PATH)
  const preExisting = existsSync(cachePath, (err) => {
    return err ? false : true
  })

  // 1-a. fetch the calendar .ics file from remote source, (converts to json)
  // 1-b. use local (expected) json file
  const address = process.env.BRIGHTSPACE_CALENDAR_URL + process.env.BRIGHTSPACE_TOKEN
  const events = !preExisting ? await ical.async.fromURL(address) : await cache.read(cachePath)

  if (events && !preExisting) {
    console.log(`[discord] successfully wrote cache file`)
    await cache.write(cachePath, events)
  }

  // 2. map courses to events
  for (const [courseKey, course] of Object.entries(cache.courses)) {
    for (const [eventKey, event] of Object.entries(events)) {
      if (event.location === course.location) {
        cache.courses[courseKey].events.push(event)
      }
    }
  }

  console.log(`[discord] successful`)
  // console.log(`[disocrd] cache preview`, cache)
  return cache
}

/**
 * Get upcoming assignments from all courses
 * @param {number} daysAhead - Number of days to look ahead (default: 30)
 * @returns {Promise<Array>} - Array of assignment objects with course info
 */
export async function getUpcomingAssignments(daysAhead = 30) {
  const calendarData = await calendar()
  const now = new Date()
  const futureDate = new Date()
  futureDate.setDate(futureDate.getDate() + daysAhead)

  const assignments = []

  for (const [courseKey, course] of Object.entries(calendarData.courses)) {
    for (const event of course.events) {
      // Only include events with a start date in the future
      if (event.start && event.type === 'VEVENT') {
        const eventDate = new Date(event.start)
        if (eventDate >= now && eventDate <= futureDate) {
          assignments.push({
            ...event,
            courseKey,
            tagId: course.tagId,
          })
        }
      }
    }
  }

  // Sort by due date
  assignments.sort((a, b) => new Date(a.start) - new Date(b.start))

  return assignments
}

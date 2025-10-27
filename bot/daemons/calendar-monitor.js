import 'dotenv/config'
import cron from 'node-cron'
import mongoose from 'mongoose'
import { getUpcomingAssignments } from '../helpers/import-calendar.js'
import { postAssignment } from '../helpers/post-assignment.js'

/**
 * Calendar monitoring daemon
 * Checks for new assignments and posts them to Discord forum
 * @param {Object} client - Discord client instance
 */
export async function startCalendarMonitor(client) {
  console.log('[calendar-daemon] Starting calendar monitor...')

  // Connect to MongoDB if not already connected
  if (mongoose.connection.readyState === 0) {
    await mongoose.connect(process.env.DB_URI)
    console.log('[calendar-daemon] Connected to MongoDB')
  }

  // Function to check and post assignments
  const checkAssignments = async () => {
    try {
      console.log('[calendar-daemon] Checking for new assignments...')
      
      // Get assignments for the next 30 days
      const assignments = await getUpcomingAssignments(30)
      
      console.log(`[calendar-daemon] Found ${assignments.length} upcoming assignments`)

      // Post each assignment
      for (const assignment of assignments) {
        await postAssignment(
          client,
          assignment,
          assignment.courseKey,
          assignment.tagId
        )
      }

      console.log('[calendar-daemon] Assignment check complete')
    } catch (error) {
      console.error('[calendar-daemon] Error checking assignments:', error)
    }
  }

  // Run immediately on startup
  await checkAssignments()

  // Schedule to run every 6 hours
  // Cron format: minute hour day month weekday
  // '0 */6 * * *' = every 6 hours at minute 0
  cron.schedule('0 */6 * * *', checkAssignments)

  console.log('[calendar-daemon] Calendar monitor started - checking every 6 hours')
}

export default startCalendarMonitor

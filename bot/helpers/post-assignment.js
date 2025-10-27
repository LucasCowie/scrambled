import 'dotenv/config'
import { ChannelType } from 'discord.js'
import Assignment from '../../server/models/Assignments.js'

/**
 * Posts an assignment to the Discord forum channel
 * @param {Object} client - Discord client instance
 * @param {Object} assignment - Assignment object with uid, summary, start, end, description
 * @param {string} courseKey - Course key (prog, webd, netw, osys, dbas)
 * @param {string} tagId - Discord forum tag ID for the course
 * @returns {Promise<Object>} - Created thread object
 */
export async function postAssignment(client, assignment, courseKey, tagId) {
  try {
    // Check if assignment already posted
    const existing = await Assignment.findOne({ uid: assignment.uid })
    if (existing) {
      console.log(`[calendar-daemon] Assignment already posted: ${assignment.summary}`)
      return null
    }

    // Get forum channel
    const forumChannelId = process.env.WUMPUS_FORUM_CHANNEL
    const forum = client.channels.cache.get(forumChannelId)

    if (!forum || forum.type !== ChannelType.GuildForum) {
      console.error('[calendar-daemon] Forum channel not found or invalid')
      return null
    }

    // Format the assignment content
    const dueDate = new Date(assignment.start)
    const formattedDate = dueDate.toLocaleString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })

    const content = [
      `**Due Date:** ${formattedDate}`,
      `**Course:** ${courseKey.toUpperCase()}`,
      assignment.description ? `\n**Description:**\n${assignment.description}` : '',
      assignment.url ? `\n**Link:** ${assignment.url}` : '',
    ]
      .filter(Boolean)
      .join('\n')

    // Create forum post with tag
    const threadOptions = {
      name: assignment.summary || 'New Assignment',
      message: { content },
    }

    // Add tag if provided
    if (tagId) {
      threadOptions.appliedTags = [tagId]
    }

    const thread = await forum.threads.create(threadOptions)

    // Save to database
    await Assignment.create({
      uid: assignment.uid,
      courseKey,
      title: assignment.summary,
      dueDate: dueDate,
      threadId: thread.id,
    })

    console.log(`[calendar-daemon] Posted assignment: ${assignment.summary} in course ${courseKey}`)
    return thread
  } catch (error) {
    console.error('[calendar-daemon] Error posting assignment:', error)
    throw error
  }
}

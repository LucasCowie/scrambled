# Calendar Automation Setup

This bot automatically monitors your school's Brightspace calendar and creates Discord forum posts for new assignments.

## Features

- 🔄 **Automatic monitoring**: Checks calendar every 6 hours
- 📝 **Smart posting**: Creates formatted forum posts with assignment details
- 🏷️ **Course tagging**: Automatically tags posts with the correct course tag
- 🚫 **Duplicate prevention**: Tracks posted assignments in MongoDB to avoid duplicates
- 📅 **30-day lookahead**: Monitors assignments due in the next 30 days

## Setup

### 1. Environment Variables

Make sure your `.env` file includes:

```bash
# Discord
WUMPUS_TOKEN=your_bot_token
WUMPUS_CLIENT=your_client_id
WUMPUS_GUILD=your_guild_id
WUMPUS_FORUM_CHANNEL=your_forum_channel_id

# Brightspace Calendar
BRIGHTSPACE_TOKEN=your_brightspace_token
BRIGHTSPACE_CALENDAR_URL=https://your-school.brightspace.com/d2l/le/calendar/feed/user/feed.ics?token=
BRIGHTSPACE_CACHE_PATH=./bot/_tmp/calendar-cache.json

# Courses (these are the "location" values from your calendar)
PROG=Programming_Course_Location
NETW=Networking_Course_Location
DBAS=Database_Course_Location
WEBD=Web_Dev_Course_Location
OSYS=Operating_Systems_Course_Location

# Database
DB_URI=mongodb://localhost:27017/scrambled
# or MongoDB Atlas:
# DB_URI=mongodb+srv://username:password@cluster.mongodb.net/scrambled
```

### 2. Discord Forum Tags

To enable course tagging, you need to add the tag IDs to `bot/helpers/import-calendar.js`:

```javascript
const cache = {
  courses: {
    prog: { key: 'prog', location: process.env.PROG, events: [], tagId: 'YOUR_TAG_ID' },
    webd: { key: 'webd', location: process.env.WEBD, events: [], tagId: 'YOUR_TAG_ID' },
    netw: { key: 'netw', location: process.env.NETW, events: [], tagId: '1432035950397096087' },
    osys: { key: 'osys', location: process.env.OSYS, events: [], tagId: 'YOUR_TAG_ID'},
    dbas: { key: 'dbas', location: process.env.DBAS, events: [], tagId: 'YOUR_TAG_ID'},
  },
  // ...
}
```

**To find your tag IDs:**
1. Right-click on Discord and enable Developer Mode (User Settings > Advanced > Developer Mode)
2. Go to your forum channel settings > Tags
3. Right-click on a tag and copy its ID

### 3. Database Setup

The bot requires MongoDB to track posted assignments:

**Option A: Local MongoDB**
```bash
# Install MongoDB locally
# Windows: https://www.mongodb.com/try/download/community
# Then run:
mongod
```

**Option B: MongoDB Atlas (Cloud)**
1. Create a free cluster at https://www.mongodb.com/atlas
2. Get your connection string
3. Add it to `.env` as `DB_URI`

### 4. Run the Bot

```bash
npm run dev:bot
```

The calendar daemon will:
1. Start immediately and check for new assignments
2. Continue checking every 6 hours automatically
3. Post new assignments to your forum channel with formatted details

## How It Works

1. **Calendar Import** (`bot/helpers/import-calendar.js`)
   - Fetches your Brightspace calendar via ICS URL
   - Caches it locally for performance
   - Maps events to courses based on location

2. **Assignment Tracking** (`server/models/Assignments.js`)
   - Stores posted assignments in MongoDB
   - Prevents duplicate posts using the assignment UID

3. **Posting Logic** (`bot/helpers/post-assignment.js`)
   - Formats assignment details (due date, course, description, link)
   - Creates forum thread with appropriate course tag
   - Saves to database after successful post

4. **Monitoring Daemon** (`bot/daemons/calendar-monitor.js`)
   - Runs on bot startup
   - Scheduled via cron to check every 6 hours
   - Processes all upcoming assignments (next 30 days)

## Customization

### Change Check Frequency

Edit `bot/daemons/calendar-monitor.js`:

```javascript
// Current: every 6 hours
cron.schedule('0 */6 * * *', checkAssignments)

// Examples:
// Every hour: '0 * * * *'
// Every 12 hours: '0 */12 * * *'
// Daily at 8am: '0 8 * * *'
```

### Change Lookahead Window

Edit `bot/daemons/calendar-monitor.js`:

```javascript
// Current: 30 days
const assignments = await getUpcomingAssignments(30)

// Change to 14 days:
const assignments = await getUpcomingAssignments(14)
```

## Troubleshooting

**Bot doesn't post assignments:**
- Check MongoDB connection in logs
- Verify `WUMPUS_FORUM_CHANNEL` is correct
- Ensure bot has permissions to create threads in forum
- Check course location values match your calendar

**Duplicate posts:**
- Clear the Assignments collection in MongoDB
- Check that assignment UIDs are unique

**Calendar not loading:**
- Verify `BRIGHTSPACE_TOKEN` is valid
- Check `BRIGHTSPACE_CALENDAR_URL` format
- Delete cache file and let it refetch

## Manual Testing

You can manually trigger the calendar check by restarting the bot, or create a test command.

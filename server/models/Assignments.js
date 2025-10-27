import { Schema, model } from 'mongoose'

const assignmentSchema = new Schema(
  {
    uid: {
      type: String,
      required: true,
      unique: true,
      index: true,
    },
    courseKey: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    dueDate: {
      type: Date,
      required: true,
    },
    threadId: {
      type: String,
      required: true,
    },
    postedAt: {
      type: Date,
      default: Date.now,
    },
  },
  {
    timestamps: true,
  }
)

export default model('Assignment', assignmentSchema)

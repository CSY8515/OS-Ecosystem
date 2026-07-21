# Reminder Guide

Smart Reminder accepts ISO 8601 due times for schedules, routines, deadlines, expirations, maintenance, learning, and work. It labels entries `DUE` or `OVERDUE`, calculates minutes until due, and sorts by due time. The caller owns recurring-rule expansion and durable reminder storage.

Notification Manager accepts a `dedupe_key` and suppresses repeats during the service session.

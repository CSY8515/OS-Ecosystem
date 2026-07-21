# Personal Secretary Architecture

## Boundary

Personal Secretary is a project-neutral synthesis layer. Source projects own tasks, learning records, schedules, work records, and retention. The capability receives caller-provided snapshots, calculates advisory output, and stores only its execution result.

## Flow

1. Validate the public request contract.
2. Optionally collect data through a Collaboration gateway.
3. Produce a deterministic briefing, review, ranking, reminder, comparison, or notification.
4. Optionally attach Enhancement insights.
5. Submit the advisory output to Safety validation.
6. Return the result and persist an execution record.
7. Only when explicitly requested, pass a request to Automation; Automation retains approval and execution authority.

AI Hub is represented by an optional interface but is never called by the v1 default runtime.

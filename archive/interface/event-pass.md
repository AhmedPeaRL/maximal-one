# Event Pass Interface

This repository accepts events in the following sense only:

An event is anything that passes without request.

Examples:
- A visit
- A clone
- A star
- A fork
- A manual issue
- A manual workflow dispatch

No event is required.
No event is awaited.
No event is logged unless coherence permits.

This interface does not listen.
It allows.

If nothing ever happens,
the system is complete.

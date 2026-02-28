# Live Data Activation Plan

Current State:
- attractor field: EMPTY
- statistical-state.json count = 0

## Activation Steps

1. Enable GitHub Action:
   evaluation.yml

2. Schedule:
   cron: "0 */6 * * *"

3. Push experiment outputs to:
   /data/live/

4. Auto-update:
   state.json

5. Display on GitHub Pages dashboard.

---
name: gpf-hub-ui
description: Owns desktop Phase 1 shell chrome and the public observability-hub viewer (layout, tabs, enlarge, copy). Use when CoS assigns hub-ui, or when changing hub HTML/CSS/JS without changing settle numbers.
disable-model-invocation: true
---

# Hub UI

Display only. Systems owns `manifest.json` numbers.

**Model lock:** Chart chrome, viz-wall layout, 15m board placement, enlarge/lightbox, and any visual pass on a chart run as **Claude Opus 5** (`claude-opus-5-thinking-max`). CoS must Task-launch this role with that model for those jobs. Grok / other parents do not invent or restyle the board.

## Start

Read [PROTOCOL.md](../../../docs/agents/PROTOCOL.md). Read [golf-offshoot/docs/HUB_DESK.md](../../../golf-offshoot/docs/HUB_DESK.md) first — that file is the desk lock. Post START on the desk.

## You may touch

- `golf-offshoot/src/golf_offshoot/operator_surface/app.py` (render/copy/layout)
- `golf-offshoot/src/golf_offshoot/operator_surface/desk.py`
- `golf-offshoot/src/golf_offshoot/operator_surface/desk.css`
- `golf-offshoot/src/golf_offshoot/operator_surface/desk.js`
- `golf-offshoot/src/golf_offshoot/operator_surface/lanes.py`
- `golf-offshoot/src/golf_offshoot/golf_kalshi/hub.py` (display regions)
- `golf-offshoot/src/golf_offshoot/golf_kalshi/organs.py` (drawer wrap)
- `docs/observability-hub/index.html`
- `docs/observability-hub/assets/`
- Hub READMEs that describe chrome (not settle figures)

## You must not

- Write settle/win/lose into `manifest.json` (that is `systems`)
- Add forms, cash, arm, Kalshi keys
- Invent charts; missing stays `not yet available`
- Put golf WC1 / Ill on `learning_lane_15m`

## Done

Handoff → `validator`. Thread: what changed. Then CoS.

# Choice wording catalog (optional demo)

**Live operating model:** in-chat clickable A / B / C options. A click in chat **is** the reply. See **Choice Presentation Standard** in `.cursor/rules/applications-gated-method.mdc`.

This folder is **not** how a live run decides. [`catalog.json`](catalog.json) is the versioned wording source the agent copies into the in-chat picker. [`index.html`](index.html) is an optional local demo of that catalog. A click on the demo copies a letter; it does **not** authorize.

## Payload schema (`gated-formalization.choice-ask.v1`)

```json
{
  "decision_id": "claim-type",
  "title": "What kind of claim is this?",
  "prompt_plain": "Say what this sentence is doing before anyone scores it.",
  "options": [
    {
      "letter": "A",
      "label": "Descriptive",
      "plain_language": "…",
      "does_not_mean": "…",
      "one_liner": "claim-type descriptive"
    }
  ],
  "details": { "Amb": "optional", "locks": "optional" }
}
```

## Agent contract

When the method offers a choice:

1. Call Cursor’s in-chat structured picker (`AskQuestion`) with **one** question.
2. Option **id** = letter (`A`, `B`, …). Option **label** = short name + one everyday sentence (`plain_language` from this catalog, or a live fill).
3. Treat the click as the authorization. Do not ask the user to retype the letter. Do not send them to this HTML page or to a canvas.
4. Do not auto-run UX/CX/CR/QI or auto-admit material; the click only records which option they chose.

## Files

| File | Role |
|------|------|
| `catalog.json` | Versioned wording for all standard decisions (source for the in-chat picker) |
| `index.html` | Optional `file://` demo — not the live decision UI |

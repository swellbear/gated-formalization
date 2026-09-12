# Five product ideas the method could attach to

**Written:** 2026-09-07 · **Status: proposed only.** Nothing in this file is admitted, and nothing here is shown to be useful yet. Each idea is a candidate waiting on a decision, and each one carries a time budget that is set **here, now** — if the budget runs out without the named result, the idea gets parked and we stop proposing follow-ons for it.

**How to read this.** These are five products the method's habits could sit underneath: read the real source first, propose only after reading, tell admitted apart from proposed on the face of the thing, name the holes instead of filling them with confident copy, and quit on a clock you set before you started. Marketing, ads, coverage, and sales talk are never treated as settled fact in any of the five. None of them tells you what to buy, what a thing is worth, or how something will turn out.

**Not clones.** None of these is a courtroom-transcript map, a patent-adjacent hardware study, or a crew of agents dressed up as a workshop. Four are things an ordinary person opens on purpose; one is a tool an engineer opens every day.

**Extra review seat:** still held. None of the five needs it, so it stays parked.

---

## TLDR — pressure-test these two first

1. **Fogline** (idea 1). It can be tested on bug histories we already have, the answer exists outside the tool (the cause that actually turned out to be the cause), and it fails loudly and cheaply. It also tests the part of the method most likely to be worthless in a product: whether writing the missing piece down beats just chasing it.
2. **Manual First** (idea 3). Same reason, sharper: the manufacturer's own manual is the outside answer, so the tool cannot grade its own homework. A wrong part number for a model year is either there or it isn't.

The other three are worth building an opinion about, but not first. **Frozen Clock** (idea 5) is the most fun and the worst first test — it cannot say anything for ninety days by construction. **Two Records** (idea 2) and **Written Scope** (idea 4) both need other people's material before they can be judged, so they are slower to kill.

---

## 1. Fogline — a bug notebook that makes you name the missing piece

**Pitch.** When you start chasing a bug you write one line before you touch anything: what you actually cannot see, what result would knock the idea out, what result would make it stronger, and how long you'll spend. The clock starts when you write the line and does not get extended later. Every check you run ends with one word — killed, hardened, wrong piece, or same as before — and you cannot open the next check until you've picked one. Two "same as before" in a row and the thread pauses: you either name a different missing piece or you stop. What you're left with at the end of the day is a short honest record of what you learned, instead of forty tabs and a feeling.

**How the method powers it.** The whole thing is the method's habit of naming one hole at a time, with a knock-it-out-or-make-it-stronger condition attached, and a scoreboard where "that was the wrong piece" counts as progress instead of failure. Restating the same foggy result twice pauses the thread. You can't propose a fix before reading the real thing — the actual log, the actual stack, the actual spec — so a forum answer or a model's guess enters as proposed, never as the cause. And once a thread is parked, the tool stops offering you new ideas about it.

**Complementary app.** *Fogline* — a small command-line and desktop companion that opens a gap line, wraps the checks you run (`fogline run pytest -k …`) and stamps their wall time against the budget you set at the start, refuses to open a new check until the last one has an outcome word, locks the thread after two "same as before" results, and exports a paste-ready "what this taught" note for the pull request or the issue.

**Exit test.** Six bugs with known causes from a real project history, one engineer, **twenty minutes each, budget set now**. It works if, on at least four of six, the cause that actually turned out to be the cause appears in the first two gap lines, and the log ends in killed or hardened rather than a restate — and if the notebook path takes no more than 1.5× the time of the same engineer working the same bug class without it. Short of that, parked, and no second debugging tool gets proposed on this thread.

**Hard NOs.** No crew of agents. No suggested fix presented as the cause. No developer scoring, streaks, or productivity charts. No treating a green test as proof the cause was found. No telling anyone the bug is fixed. No auto-closing anything.

---

## 2. Two Records — a family tree that shows what rests on hints

**Pitch.** Family trees today grow on hints and other people's unsourced trees, and after a few clicks nobody can tell which parts came from a document. Two Records is a tree where every link — this person is that person's child — wears its status on its face: admitted when you have read an actual record that says so, proposed when it's your reasoning and here's the reasoning, parked when the trail runs out. You cannot hang a proposed parent on a person until you've logged one real record for the person you're standing on, so name-matching alone doesn't grow the tree. Each dead end gets one line: what document would settle it, where that document would live, and how long you'll spend looking. When the register is gone or the courthouse burned, the line is parked and the app stops suggesting speculative parents for it.

**How the method powers it.** Two real sources before anything is admitted, and a hint is not a source. Three online trees agreeing with each other is copies agreeing, not a record — that never gets promoted. Every open dead end is one line on a running list with a settle-it condition, and looking that stops moving gets parked instead of quietly continuing. Narrowing an ancestor down to two candidates is not proving which one.

**Complementary app.** *Two Records* — import a GEDCOM and get the tree recolored by status, plus a "proposed only" view that shows plainly how much of your tree rests on hints, research cards for each dead end with a time budget on them, and an export that will not publish proposed links as facts — they leave the app labeled proposed, with the reasoning attached.

**Exit test.** Three published, properly cited genealogies used as the answer key, plus one tree containing a well-known bad merge. **Forty minutes per tree, budget set now.** It works if hint-only links land as proposed at least nine times in ten, no documented link is wrongly parked, and the bad merge is flagged as proposed rather than carried as admitted. Short of that, parked.

**Hard NOs.** No reading a DNA match as proof of a specific parent. No famous-ancestor suggestions. No auto-merge. No confidence percentages. No treating agreement among online trees as a record. No claiming a line is established because it is popular.

---

## 3. Manual First — what the video says versus what the manual says

**Pitch.** You search a fault code and get a video telling you to pull the drain pump, a forum thread telling you to replace the control board, and a sponsored part at the top of the page. Manual First takes the video's own words and the thread, pulls out the checkable bits — part numbers, torque figures, what the code means, the order of steps — and stands them next to the manufacturer's service manual and parts diagram for your exact model. What the manual backs up shows as admitted. What only the video says shows as proposed. What the manual doesn't cover gets named as a hole, in your own words, so you know what you're guessing about before you order a part. It does not tell you the machine will be fixed.

**How the method powers it.** The service manual and the parts diagram are the real source; the video, the thread, the top-voted answer, and the sponsored part are claims about it, and none of them ever gets promoted to fact — not by view count, not by upvotes, not by being repeated on four channels. The per-model list of what's admitted grows over time and stays separate from what's merely claimed. When there's no manual for a model, that's a named hole and the thread parks rather than filling the gap with confident copy.

**Complementary app.** *Manual First* — paste a video link or a thread plus your model number, get a three-column sheet (in the manual / only claimed / not covered), a part-number check against the diagram for that model year, and a printable "before you order" hole list. The per-model sheet is kept and improves as manuals are added.

**Exit test.** Twelve popular repair videos across four models where the manual is available. A human reads the manuals first and writes the mismatch list, sealed, before the tool runs. **Fifteen minutes per video, budget set now.** It works if the tool catches at least eight of the sealed mismatches — wrong part number for the model year, a figure quoted from a different model, a step order the manual forbids — with no more than two false alarms. Short of that, parked, and no second version gets proposed.

**Hard NOs.** No "safe to do yourself" verdicts. No gas, mains, or brake work guidance. No affiliate or sponsored parts anywhere in the product — that's the thing we're supposed to be discounting. No treating popularity as evidence. No promising a fix works. No inventing a manual that doesn't exist for the model.

---

## 4. Written Scope — what your quote actually says, and what was only said

**Pitch.** You have three quotes for the same job — a roof, a transmission, a solar install, a treatment plan — plus brochures and whatever the salesperson told you on the doorstep. Written Scope pulls each quote apart into what is actually written down (line items, quantities, brand and model, warranty wording, what happens if they open it up and find rot) and lines the three up next to each other. Anything that exists only in the brochure or only in conversation goes in its own column, marked as said, not written. The gaps come back as questions you can send, worded so they can be answered in writing. It does not tell you which quote to take, and it does not tell you whether the price is fair. It tells you what your paperwork doesn't say.

**How the method powers it.** Sales talk and brochures are claims, and they stay in the claimed column no matter how confident they were. Every gap is a named hole with a way to close it — get it in writing, and the line moves from proposed to admitted on the next pass. Recommending a bid, or a fair price, is exactly the kind of call the method refuses to dress up as a finding, so the product refuses it too. And there's a clock: if a real user can't get useful questions out of it inside the budget, the idea parks rather than getting a nicer interface.

**Complementary app.** *Written Scope* — photograph or upload the quotes, get the side-by-side line-item table, the "said but not written" column, and a question list you can send as-is. When a revised quote comes back, run it again and see which questions actually turned into written line items or written exclusions. No score, no badge, no best-value pick.

**Exit test.** Ten real multi-quote jobs from real people. **Twenty-five minutes per job, budget set now.** It works if, on at least seven of ten, the user sends the questions and at least two per job come back as new written line items or written exclusions that weren't in the first quote. If fewer come back, or users say the questions were the obvious ones they'd already have asked, it's parked.

**Hard NOs.** No fair-price estimate. No recommended bid. No negotiation script framed as what you ought to pay. No lead generation and no referral fees. No legal, medical, or dental advice. No promising a contractor will honor anything. No lifting brochure language into the written column.

---

## 5. Frozen Clock — a scoreboard of who keeps dates

**Pitch.** Organizations promise dates: a studio's roadmap, a city's bridge, a vendor's third-quarter feature, an agency's opening day. Frozen Clock records the promise the moment it's made, with the date frozen exactly as it was first stated and a snapshot of where it was said — the roadmap page, the council minutes, the release notes, not the article about them. Then it waits. When the frozen date passes, the promise gets one plain outcome: shipped, moved, restated with nothing new, or gone. Two restatements with nothing new and the thread pauses, because a promise that keeps getting repeated without a date isn't news. The result is a boring, honest record of who keeps dates, which nobody currently keeps because everyone re-anchors to the latest date instead of the first one.

**How the method powers it.** The frozen clock *is* the product: the date is set when the promise is born and nobody gets to move it afterwards, which is the one discipline that makes this kind of tracking mean anything. The promise of record is the organization's own words, never the coverage of them or an analyst's note. Restated-with-nothing-new pauses the thread, which is what keeps it from turning into an outrage feed. And a missed date stays a missed date — it does not become a prediction about the next one, or a view on the stock.

**Complementary app.** *Frozen Clock* — watch a roadmap, changelog, or minutes feed; capture each dated promise with a snapshot of the source as it read that day; publish a per-organization page of promises, frozen dates, outcomes, and paused threads. Follow one organization and get one note when a frozen date passes. Not a daily feed.

**Exit test.** Five organizations with public dated roadmaps, twenty promises captured. **First verdict window is ninety days from capture, and the window does not move.** It works if at least sixteen of twenty promises get an outcome that two independent readers agree on from the snapshots alone, and at least three threads reach paused under the two-restatement rule — if nothing ever pauses, the rule is decoration. Short of that, parked.

**Hard NOs.** No price targets and no buy, sell, or hold. No calling anyone a liar; a moved date is a moved date. No scraping behind logins. No coverage or analyst note as the promise of record. No leaderboard ranked on feel. No guessing whether the next date holds.

---

## What this file does not do

It does not show that any of the five is useful — that stays unproven until one of the exit tests above runs and passes on its own frozen clock. It does not authorize a build. It does not price anything, recommend anything, or promise an outcome for any user of any of the five. Two of the five (**Fogline**, **Manual First**) are put forward as the ones to test first; the other three are held. The extra review seat stays parked.

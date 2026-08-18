---
marp: true
theme: default
paginate: true
style: |
  section {
    font-size: 28px;
  }
  section.lead {
    background: #310066;
    color: #ffffff;
  }
  section.lead h1, section.lead h2 {
    color: #ffffff;
  }
  section.standout {
    background: #beaefc;
    color: #310066;
    text-align: center;
    font-size: 36px;
  }
  h1, h2 {
    color: #310066;
  }
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }
---

<!-- _class: lead -->

# The Web Layer: Testing Types Become Mechanical Gates

**Agentic Software Engineering — Lecture 11**
Week 6 · Meeting 1 of 2 · launches **Stage C** · **PKB checkpoint 1 due**

---

## The one idea

A test type is a **claim type** — and a green unit suite and a working application are **different claims**.

Gates are the taxonomy, given teeth.

---

## Green suite, broken app

From the case study's smoke-gate rationale:

> *"supertest never starts bin/www, so unit tests **cannot catch a broken boot**. A clean clone has no .env... so smoke-test from a fresh checkout, not from a warm working tree."*

Two lessons in one row:
1. The HTTP test suite never boots the real server
2. Even the real server proves the wrong thing from a **warm tree**

(You met this Tuesday as the fresh-clone gate. Same argument. It is always the same argument.)

<!-- 0-10 min. -->

---

## The claim hierarchy, on your stack

| Type | In Stage C | The claim |
|---|---|---|
| Unit | Engine suite — untouched | The rules are correctly implemented |
| Integration | Flask test-client + DB | The web layer drives engine and DB correctly |
| Smoke | Fresh clone → boots → renders | The application actually starts, from nothing |
| End-to-end | *deferred to Project 2* | A user can do the thing |

No quantity of one substitutes for another. **Different sentences.**

---

## Worked example: both paths for one route

```python
def test_legal_move_advances_board(client):
    resp = client.post("/move", data={"row": 3, "col": 4})
    assert resp.status_code == 200

def test_occupied_cell_rejected(client):
    client.post("/move", data={"row": 3, "col": 4})
    resp = client.post("/move", data={"row": 3, "col": 4})
    assert resp.status_code == 400
    # board unchanged; SAME player's turn  (SPEC S-3.3!)
```

The failure path is where agent-written code quietly "simplifies."

Clause S-3.3 now has a **second interface** enforcing it. (Week 7: a second *language*.)

<!-- 10-26 min. -->

---

## The gate table (the real one)

Lint · Tests · Smoke · Both-paths · Contract · Coverage · Review · Live-app

Two ideas to steal:

1. **Gates activate progressively** — each row has an *active-from* milestone. Too early = noise (teaches everyone to ignore red). Too late = the work is already built wrong
2. **Red is mechanical** — *"a red gate returns the work to in-progress — it does not advance."* No judgment call

Your Stage C table: three rows (lint, tests, smoke) + the coverage law you've had since Stage A.

<!-- 26-40 min. -->

---

<!-- _class: standout -->

## Demo: running the gates — and one red

GATES.md → all green → a "simplified" rejection path → **red** → the work goes *back*

<!-- 40-54 min. The red-gate beat is the memory they keep. Pass-4's lesson in procedure form. -->

---

## What the 90 seconds buys

From Stage C on: gates run before **every commit**, visible in history.

Every commit on main now carries the same three claims, mechanically checked —

which is what lets *future you*, then teammates, then **autonomous agents** trust the branch without re-deriving trust by hand.

Project 2's entire autonomy story stands on gates you learn to run this week.

---

## Flask, sized for this project

- Routes → handlers → `render_template` (Jinja) → HTML
- **App factory** (`create_app()`) — what makes test-client isolation clean (same shape as Tuesday's DB fixture)
- "Light JS" = a click posts a move; the server re-renders. No framework, no build step

**The layering rule, third enforcement:** the web layer is a *caller*, like the CLI.

```
git diff stage-b..HEAD -- game.py     # prints NOTHING
```

An entire interface appears; the engine never notices.

<!-- 54-64 min. -->

---

## Stage C checklist (from the brief)

- [ ] Play + leaderboard pages, fresh-clone-workable
- [ ] **Empty `game.py` diff**
- [ ] `GATES.md` + visible gate runs in history
- [ ] Both-paths test-client tests
- [ ] Per-directory `web/CLAUDE.md` (layering rule + layer commands)
- [ ] Cost hook — assigned Thursday

**PKB checkpoint 1 collected today.**

---

## Questions to think about

1. Complete "this test claims that..." for each of your tests — then find the claim *none* of them makes.
2. Price the rejection-path bug at each discovery point: gate-before-commit, grader, week-7 port.
3. Write the one `web/CLAUDE.md` sentence that lets an agent *check* the layering rule, not just admire it.

---

## Before Thursday

- [required] Claude Code docs: Hooks; Memory
- [recommended] `student-materials/hooks/log-cost-on-end.ps1` — read it **as a spec**

**Thursday: the environment starts doing things without being asked.**

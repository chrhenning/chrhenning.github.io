---
layout: distill
title: "Before the Breakthrough: Why Research and Engineering Need Different Cultures"
date: 2026-05-10 10:00:00
description: "Research is not slow engineering. Why companies that want breakthroughs need to cherish two cultures, not collapse them into one."
tags: research engineering
categories: leadership
giscus_comments: true
related_posts: true
related_publications: false
citation: false
bibliography: 2026-05-10-before-the-breakthrough-research-engineering-cultures.bib

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: The Year Before the Breakthrough
  - name: Two Kinds of Work
  - name: When Incentives Don't Match the Work
  - name: Cherishing Both Cultures
  - name: The Interface Between the Two Cultures
  - name: From Vision to Breakthrough
---

Research and engineering are equally demanding disciplines when done right. They are simply different kinds of work, with different rhythms, different success criteria, and different definitions of progress. Companies that want to produce breakthroughs need to recognize that distinction and cherish both cultures on their own terms.

The reason this matters is structural. When the two are conflated, when researchers sit inside engineering teams and are reviewed against engineering deliverables, the incentive structure quietly favors short-term, visible delivery over long-term, compounding progress. This post is an argument for why that conflation costs companies their breakthroughs, and what it takes to host both cultures under one roof.

## The Year Before the Breakthrough

Academic science moves paper by paper, and the cadence rewards small, defensible contributions: a dataset extended, a method refined, a benchmark nudged forward. Breakthroughs happen, but the unit of progress is the publication, and progress is visible because progress is _defined_ to be visible.

Industrial research is different. When a company asks a team to make a new technology actually work for a real use case, the goal stops looking incremental from the outside and becomes binary. Inside the team the work is still incremental, but the rest of the company sees only one signal. **It doesn't work until it does.** The classic example is training a [foundation model](https://en.wikipedia.org/wiki/Foundation_model). The year before it works looks like nothing from the outside: curated datasets, dataloader plumbing, a long string of failed architectures, hypotheses ruled out. None of it ships. None of it shows up in a release note. None of it can be demoed. Then a threshold is crossed, and only in retrospect does the prior year look like progress.

Research progress in this regime is non-linear and compounding. Failed experiments are not wasted effort; they are the substrate the breakthrough is built on. But during the compounding period the work is genuinely invisible. Not because researchers are hiding it, but because the units of progress (a ruled-out hypothesis, a cleaner dataset, a slightly better internal benchmark) don't render in the language product and engineering use to track delivery.

## Two Kinds of Work

The distinction is simple to state.

- **Engineering** is reliable delivery against known specifications. The work rewards predictability. Success looks like shipped features, system uptime, customer outcomes, velocity. The right question to ask an engineer is: _"when can we have this?"_
- **Research** is the reduction of uncertainty on hard problems. The work rewards being right about hard things, not fast about easy ones. Success looks like insight, killed hypotheses, validated prototypes, decisions changed. The right question to ask a researcher is: _"what did you learn, and what should we do differently?"_

This is not a hierarchy. Both kinds of work demand deep expertise: engineers who ship reliably at scale and researchers who frame the right experiment and read its result correctly are doing equally non-trivial work. The difference is in shape, not in difficulty.

The framing closest to industrial research at its best is what Donald Stokes called [Pasteur's Quadrant](https://en.wikipedia.org/wiki/Pasteur%27s_quadrant): research that is both fundamentally novel _and_ aimed at a concrete real-world problem. It is also the kind of work that fits least comfortably into a sprint cadence.

## When Incentives Don't Match the Work

Whether researchers and engineers sit on the same team, share standups, or report to the same person matters less than people think. The argument is not about silos or org charts. What matters is the **incentive structure**: what counts as "having delivered", what gets rewarded at review time, what the team celebrates as success.

If researchers and engineers are reviewed against the same scoreboard, the comparison is structurally unfair. Not because anyone is being lazy, but because the units of progress don't compare. The engineer can show shipped tickets. The researcher can show a notebook full of negative results. Side by side, the engineer always wins.

The consequence is predictable. Researchers don't stop being researchers by decision; they stop by gradient, one sprint at a time. The hard, uncertain, possibly-zero-payoff bets get deprioritized in favor of the predictable wins. **Researchers measured by engineering yardsticks start working like engineers.** What's left is a team of engineers working on safe problems, which is precisely what you didn't fund a research function for.

This also affects who stays. The people most willing to do uncertain work, the ones who would have produced the breakthroughs, are the first to leave when the system tells them their work doesn't count.

What remains is a company that claims an R&D function while running an engineering one. The label persists; the conditions for breakthrough research do not.

## Cherishing Both Cultures

Some argue the cultural tension is so difficult to manage that startups should avoid dedicated research functions altogether <d-cite key="molander2021startup"></d-cite>. That may be the right call when research is peripheral to the business model. But for companies whose edge depends on solving problems that don't yet have solutions, avoiding the problem doesn't make it disappear. It only defers the question of how to build the conditions in which that research can succeed.

Fixing this is a leadership responsibility. Researchers can't change the incentive structure they're embedded in, and engineers can't be blamed for responding rationally to the one they have. The job is to design the conditions in which both kinds of work can succeed, not to force one to look like the other.

In practice, that means a set of cultural commitments:

- Treat **"what did you learn"** as a first-class deliverable, not a consolation prize.
- **Defend research time** at the leadership level, rather than negotiating it away sprint by sprint.
- Make **research progress legible** on its own terms: regular forums, written artifacts, decisions changed because of a research result.
- Use **different review rubrics** for research and engineering work, even when the two roles sit at the same pay grade.
- Acknowledge out loud that **some research returns nothing usable**, and that this is the cost of working on hard problems, not a sign of failure.

Each of these is easy to say and hard to hold. Under customer pressure, the gradient always points back toward predictable delivery. Holding the line is what creates the conditions for the breakthroughs.

Cherishing research is not the same as exempting it from accountability. Drift is a real failure mode, and protected research time only matters if that time is being spent well. Healthy research teams hold themselves to specific kinds of rigor: explicit hypotheses, written technical bets, kill criteria for experiments, and regular strategic review of which directions are still worth pursuing. The aim is not to make research look like engineering, but to keep exploration directed and the difference between learning and drifting legible to leadership.

History supports this. Bell Labs produced the transistor, information theory, and Unix not because researchers were also engineers, but because the institution treated research as a distinct, valued discipline with its own success criteria, embedded in a company that knew how to commercialize the result <d-cite key="gertner2012idea"></d-cite><d-cite key="potter2024belllabs"></d-cite>. And the pattern is not unique to Bell Labs: the industrial research divisions that left a lasting mark on technology, including IBM Research and Xerox PARC, all gave research its own discipline and criteria rather than collapsing it into engineering <d-cite key="lecun2025research"></d-cite>. PARC's legacy carries both lessons. Protecting research is necessary but not sufficient: the foundational technologies it produced were turned into products by other companies, a reminder that breakthroughs also need a credible path from result to product <d-cite key="hiltzik1999dealers"></d-cite>.

## The Interface Between the Two Cultures

Keeping research and engineering distinct is not the same as keeping them apart. Both need to be grounded in the same customer problems, not because one team owns that signal, but because shared grounding is what keeps research from drifting into abstraction and engineering from solving the wrong things efficiently.

In practice the interface is about legibility in both directions. Research makes its findings visible: what was learned, what was ruled out, what changed, and what the company should do differently. Engineering makes its constraints visible: what is deployable, what breaks at scale, what customers can't work with. In machine learning, for instance, the model is a research artifact, owned and iterated by the research team, while engineering owns the serving infrastructure, latency budgets, and the cost envelope the model must fit into. Neither side hands a finished artifact across a wall. The work is continuous: shared context, regular conversation, and decisions made together about when a research result is ready to shape what gets built next.

## From Vision to Breakthrough

Research is most useful in companies that have a **long-term vision**: a clear sense of where they want to be in three or five years, and an honest assessment of the technical gaps between today and that future. Without a vision, research becomes hard to direct and easy to underfund. With a vision, researchers can lay the foundation for it by tackling the high-uncertainty problems that engineering can't yet specify, instead of being squeezed into highly-specified short-term deliverables that only an engineer can satisfy.

This is also the connection to what I've previously called [Technology Readiness Debt](/blog/2025/technology-readiness-debt/). When a company builds before the underlying technology is fully ready, research is the mechanism that pays off that debt on the company's own timeline, rather than waiting for the world to do it instead.

The companies that build defensible technical IP are the ones that figured out how to host two different shapes of work under the same roof, without forcing one to look like the other. **Research is not slow engineering.** The distinction is not a tension to resolve; it is a feature of how breakthroughs actually happen.

In the end, don't get caught up in the terminology. Whether you call the work research, R&D, or advanced engineering, leadership's job is to ensure that both short-term delivery and long-term progress are rewarded on their own terms. Cherish both cultures, or you will quietly lose the conditions for either to do its best work.

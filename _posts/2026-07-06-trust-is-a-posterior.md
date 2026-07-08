---
layout: distill
title: "Trust Is a Posterior: Why Good Work Can Only Be Appreciated Statistically"
date: 2026-07-06 08:00:00
description: A shipped feature reveals almost nothing about how well it was built, because from the outside the quality of engineering work is a credence good. Trust accumulated across many projects is the only statistically valid way to price it.
og_image: https://chrhenning.com/assets/img/posts/trust-is-a-posterior/illustration.jpg
tags: engineering technical-debt
categories: leadership
giscus_comments: true
related_posts: true
related_publications: false
citation: false
bibliography: 2026-07-06-trust-is-a-posterior.bib

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: Quality Is a Credence Good
  - name: One Quiet Project Is Almost No Evidence
  - name: Trust Is a Posterior
  - name: The Lag That Outlives the Credit Window
  - name: Auditing Your Own Judgment
  - name: Appreciated Statistically
---

Picture two engineers shipping the identical feature. One cuts every corner to hit the date. The other takes the extra time to handle the edge cases that production will eventually find. I have argued before that this kind of care, not the corner-cutting, is what keeps teams fast in the long run ([Scrappiness Incentivizes Sloppiness](/blog/2025/scrappiness-incentivizes-sloppiness/)). Yet when credit is handed out, nothing in the record tells the two apart: the feature works, and that is all the record says. This post asks why the person supplying the care is so rarely credited for it. The usual explanation blames the evaluators, their inattention, their bias toward whatever demos well. The explanation here is more mechanical: a delivered project, seen from the outside, carries almost no information about craftsmanship. What looks like ingratitude is, at bottom, a statistics problem.

**The quality of engineering work is a [credence good](https://en.wikipedia.org/wiki/Credence_good): something an evaluator cannot assess even after using it. Since the work itself cannot be judged, we judge the worker: trust, built by watching the same person across many projects, is not a consolation prize for that limitation. It is the only statistically valid way to price it.**

<div class="row mt-3 justify-content-center">
    <div class="col-md-10 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/trust-is-a-posterior/illustration.jpg" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <b>Indistinguishable today, unmistakable later.</b> The same shipped feature looks the same from either engineer on day one. Only with time does careless work surround itself with alerts and incidents, and careful work earn a seat among the people who trust it. Image generated with Google Gemini.
</div>

## Quality Is a Credence Good

Economists [sort goods](https://en.wikipedia.org/wiki/SEC_classification_of_goods_and_services) by when their quality becomes knowable. You can judge a shirt before buying it and a restaurant meal after eating it. But you cannot judge a car repair even after driving home, because the judgment would take the same expertise that did the repair. That third kind is a credence good, and the standard survey of the field (see <d-cite key="dulleck2006credence"></d-cite>) names computer specialists alongside doctors and mechanics in its very title.

A shipped feature is the repaired car. The manager, like the customer at the garage, sees that it runs. Whether it runs because the code is clean and the edge cases are handled, or because nobody has hit the bad path yet, is exactly the information a credence good withholds. Not every quality is hidden; a reviewer can judge readability at a glance. But the qualities that separate the two engineers from the opening are the **credence kind: robustness, restraint, anticipation of the change that has not arrived yet**.

The same literature names the two ways an expert can fail you: doing less than the problem needs, and doing more <d-cite key="dulleck2006credence"></d-cite>. Engineering has both, as sloppiness and over-engineering, and the outcome reveals neither.<d-footnote>The incentives do not transfer one to one. A mechanic who overtreats is usually padding the bill. An engineer who over-engineers is more often indulging taste, caution, or ambition. What transfers is the observability problem: whatever the motive, the customer cannot tell too much from just right.</d-footnote> From outside, "built it properly" and "gold-plated it" are observationally identical: nothing happens.<d-footnote>Code review blunts this only partially. A reviewer can assess much of the quality directly, but not the counterfactual: complexity whose payoff lies in a future the reviewer cannot inspect reads as over-engineering until justified. And the reviewer is rarely the one assigning credit.</d-footnote>

## One Quiet Project Is Almost No Evidence

An observation only moves your beliefs if it is more likely under one explanation than another. That is where a quiet project fails you. Shipping without incident is what careful work produces, but it is what careless work produces too, most of the time: shortcuts rarely fail on the first day, or the tenth. **No fire is not evidence of no fire hazard, because fire hazards rarely produce fires.** The signal lives almost entirely in the rare, lagged failure: the incident, the regression that traces back to a shortcut.

Put illustrative numbers on it, with a quarter of operation as the unit of observation. Suppose properly built systems get through a quarter fire-free 98% of the time, and carelessly built ones 90% of the time. A quiet quarter is then almost equally likely either way, so seeing one multiplies the odds on "properly built" by 0.98/0.90, about 1.1, close enough to nothing. A fire, at 10% versus 2%, is five times likelier under "carelessly built," so it multiplies the odds the other way by 5.<d-footnote>Evidence compounds multiplicatively across independent observations. One quiet quarter multiplies the odds by 0.98/0.90, which is about 1.09; after ten quiet quarters the odds have moved by 1.09 to the tenth power, about 2.3, and after twenty-five, about 8. Because a single fire (factor 5) is so much more diagnostic than a single quiet quarter (factor 1.09), it takes roughly nineteen consecutive quiet quarters to offset the evidentiary weight of one fire: 1.09 to the nineteenth power is about 5. Quiet stretches are cheap to produce and expensive to accumulate.</d-footnote> With these rates, one incident erases roughly nineteen quiet quarters of accumulated evidence.

This is not a claim about inattentive managers; it is a claim about information. A single quiet project is close to zero evidence about the quality behind it, for anyone who sees only the outcome. Quality becomes legible only in aggregate: either the rare fire eventually breaks out, or the quiet stretch grows long enough to mean something.

## Trust Is a Posterior

That aggregate has a familiar name. Tobi Lütke describes the trust between colleagues as a battery: it starts about half charged when you join a team, and every interaction charges or discharges it <d-cite key="lutke2018trustbattery"></d-cite>. Strip the metaphor and a Bayesian object appears. The half charge is a prior, each interaction is an update, and the battery's level is a posterior probability over what kind of engineer you are. This is not loose talk: game theory models reputation in repeated games as exactly this posterior over an unobserved type <d-cite key="kreps1982reputation"></d-cite>, and online reputation systems compute it literally.<d-footnote>The beta reputation system scores marketplace counterparties by Bayesian updating over a beta distribution, incremented with every good or bad interaction <d-cite key="josang2002beta"></d-cite>.</d-footnote> The battery gets the behavior right; the posterior explains why trust that tracks evidence has to behave this way. Three corollaries follow.

Trust builds slowly because the evidence arrives slowly. Each quiet quarter is worth a factor of 1.1, so the posterior moves in small steps no matter how patient or generous the observer is. Nobody can earn trust faster than the information comes in.<d-footnote>Only the work-quality part of the battery charges this slowly. Interpersonal signals such as warmth or arrogance arrive with every interaction, so the impression of who you are settles long before the evidence about your work has begun to accumulate. And that impression carries weight: people prefer working with a likable colleague of middling competence over a competent one they dislike <d-cite key="casciaro2005jerks"></d-cite>.</d-footnote>

Trust is asymmetric because failure is more diagnostic than success. One fire outweighs nineteen quiet quarters, so trust erodes faster than it accrues. Human judgment tracks that arithmetic: the [negativity bias](https://en.wikipedia.org/wiki/Negativity_bias) in how we form impressions of each other exists, on the standard account, precisely because negative information is more diagnostic <d-cite key="skowronski1989negativity"></d-cite>.

And trust does not transfer, because the posterior lives in the head of whoever did the observing. Change teams or companies and you reset close to the prior, not because the new observer is unfair, but because they have not run the updates yet. References and titles soften the reset, but they only raise the starting prior: they certify what you delivered, not how. Most of your credit stays behind.

## The Lag That Outlives the Credit Window

Sloppy work is not invisible forever. Left long enough, it produces the incident, the rewrite, the system nobody wants to touch. Strictly speaking that makes quality an experience good on a very long delay, but the refinement rescues nothing, because the delay routinely outlasts the window in which anyone assigns credit: a performance cycle, sometimes an entire tenure. The evidence arrives eventually, but it lands on somebody else, long after anyone remembers who built what.

The extreme case is prevention, where the entire value of the work is a disaster that never happens, so no delay, however long, ever surfaces the evidence. A shipped feature is only the ordinary case: part visible output, part invisible quality, and the invisible part obeys the same statistics. I wrote about the extreme case in [Your Best Work Leaves No Trace](/blog/2026/we-reward-the-fix-not-the-prevention/), which closed on a promise it did not explain: that prevention earns trust, on a slower ledger. The posterior is that ledger.

Can you close the gap by explaining your reasoning? To a listener with the expertise and time to probe, yes: sound reasoning is hard to fake, and imitation tends to crumble under follow-up questions. But that is the close-up channel, and it does not travel. At a distance, where nobody is probing, the careless can claim craftsmanship just as fluently, and a claim stays credible only if faking it would be costly <d-cite key="spence1973signaling"></d-cite>. The costly signal is the track record itself: a long fire-free stretch is the one thing careless work cannot cheaply produce. Narration does not replace the record; it makes the record legible sooner.

## Auditing Your Own Judgment

The scarcity of evidence is not only your evaluators' problem. I have often asked myself whether my own instinct to build things properly sometimes tips into over-engineering, and the same statistics apply: one outcome is barely informative about the instinct that produced it. Introspection is no better an instrument, because conviction is not evidence, whichever direction it points.

Experience alone will not settle it. Intuition becomes trustworthy under two conditions: an environment regular enough to have learnable patterns, and enough feedback to learn them <d-cite key="kahneman2009intuitive"></d-cite>. Foresight fails the feedback condition badly. The payoff of an investment in structure arrives late, rarely, and confounded with everything else that happened in between, so even a payoff you do see is hard to trace back to the decision that produced it.

So build the feedback loop deliberately. Peter Drucker's "feedback analysis" is the practice: whenever you make a consequential call, write down what you expect to happen, then check the record against the outcome later <d-cite key="drucker1999managing"></d-cite>.<d-footnote>The same practice reached investing as the "decision journal," which Michael Mauboussin traces to advice he received directly from Daniel Kahneman: buy a notebook and log your reasoning before you know how a decision turns out <d-cite key="mauboussin_decisionjournal"></d-cite>.</d-footnote>

Engineering offers an unusually auditable version of that log. In [The Two Cuts of an MVP](/blog/2026/mvp-two-cuts/) I argued that vision is what places your seams, the deliberate boundaries you pay for so the system can change where you expect it to. That post left a question open: how do you ever find out whether your vision is sound? The seam log is the answer. Write down, at the time, which seam you are paying for and what you expect it to buy. Later, check which ones actually got exercised. A seam you deliberately paid for is checkable after the fact in a way a general sense of "being careful" is not.

Two caveats keep the audit honest. First, weigh by what an exercised seam saved, not by how often seams get exercised. A cheap seam that heads off one catastrophic rewrite has paid for itself even if it is the only one out of ten that ever gets used: a low exercise rate does not mean the seam was unnecessary. Second, the log has to be written before the outcome is known, or [hindsight bias](https://en.wikipedia.org/wiki/Hindsight_bias) quietly rewrites the reasoning for you: knowing how something turned out makes people misremember how predictable it felt in advance <d-cite key="fischhoff1975hindsight"></d-cite>.

Kept honestly over enough decisions, the log begins to answer what no single project ever could: whether the instinct is calibrated.

## Appreciated Statistically

Two implications follow, one for each side of the evaluation.

If you are the one doing the work, slow credit is not the same as no credit. It means the unit that gets evaluated, including by yourself, is not the project but the portfolio. Stay in front of the same observers long enough for one to accumulate, rather than resetting the posterior at every move.

If you are the one doing the evaluating, staring harder at the deliverable in front of you will not help. That leaves two honest options. Get close to the work, or borrow the view of someone who already is: read the code, sit in the design reviews, ask the people who reviewed it. Where that does not scale, aggregate: judge incident frequency across a portfolio and a stretch of time.

Performance reviews make the sampling problem concrete. The projects that come to mind in the room are few and memorable ([availability heuristic](https://en.wikipedia.org/wiki/Availability_heuristic)), admitted as evidence because they are written down, while the quiet majority of the record never makes the packet. Your trust in the person's work is the summary that includes it. When the two disagree, that is not bias intruding on evidence; it is a larger sample disagreeing with a smaller one, and a reason to look at the whole record.

None of the pieces here are new. Credence goods, reputation as a posterior in a repeated game, the diagnosticity of bad news: each is textbook in its own field. This post only aims them at one ordinary question, asked from both sides of the table and never answerable on the spot: was the work you shipped this quarter good enough to build on, or just good enough to ship?

The two engineers from the opening still look identical on the day they ship. No sharper eye will tell them apart; only accumulation will.

**Good work cannot be appreciated in the moment. It can only be appreciated statistically.**

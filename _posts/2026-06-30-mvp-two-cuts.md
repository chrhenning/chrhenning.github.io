---
layout: distill
title: The Two Cuts of an MVP – Why Iterating and Incrementing Both Come Down to Vision
date: 2026-06-30 08:00:00
description: Every “cut it for the MVP” is one of two moves. You either defer a feature or build a throwaway stand-in. Whether either becomes debt depends not on the cut but on the boundary you leave beneath it, and on a vision clear enough to place it.
og_image: https://chrhenning.com/assets/img/posts/mvp-two-cuts/overview.jpg
tags: mvp technical-debt
categories: product-management
giscus_comments: true
related_posts: true
related_publications: false
citation: false
bibliography: 2026-06-30-mvp-two-cuts.bib

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: The Two Cuts
  - name: The Two Cuts Already Have Names
  - name: The Decision Rule and the Seam
  - name: Vision Places the Seams
  - name: When the Seam Comes Due
  - name: Cutting With Vision
---

"Minimum viable product" is one of the most misread terms in product development. People hear _minimum_ and reach for permission to ship something rough. But an MVP is not a license to ship a sub-quality product. As I argued in [Scrappiness Incentivizes Sloppiness](/blog/2025/scrappiness-incentivizes-sloppiness/), sloppy execution feels fast and quietly costs you the sustained speed that actually matters. What an MVP minimizes is not quality. It is scope.

<div class="row mt-3 justify-content-center">
    <div class="col-md-12 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/mvp-two-cuts/overview.jpg" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
  Every MVP cut is one of two moves. <strong>Defer</strong>: leave a gap to fill in later. <strong>Substitute</strong>: drop in a deliberate stand-in, then swap it for the real thing later. Either way, what's already built stays untouched. Image generated with Google Gemini.
</div>

This is the third post in a series on the debts you take on while building a product. The first argued that [technical, strategic, and feature debt](/blog/2025/mvp-manage-debt-and-iterate-fast/) are tools, not sins, as long as you take them on consciously. The second covered the [technology readiness debt](/blog/2025/technology-readiness-debt/) you carry when the technology you need isn't ready yet. Both stayed fairly abstract. This one is concrete, about a decision you make dozens of times while scoping an MVP, often without noticing you've made it: **what to cut**.

"Let's just cut that for the MVP" gets said in a meeting, everyone nods, and the decision is made in three seconds. But cutting scope is not a single move. Every time you trim something from an MVP, you're doing one of two very different things, and most teams never notice which one they just made. Confusing them is how a lean product quietly turns brittle.

## The Two Cuts

The first cut is **deferral**: you leave a feature _out of scope_ and plan to build it later. The second is **substitution**: you build a deliberate stand-in, something you _intend_ to throw away and replace once you've learned what you need to build.

At first glance only one of them is debt. A clean deferral isn't debt, it's just scope: debt is something you borrow and have to pay back, and a feature you never built was never borrowed. Substitution is real debt, because you've put something into the product specifically so you can replace it, and that replacement is the repayment. The word doing the work there is _clean_: keeping a deferral clean turns out to be the whole game.

That has a flip side. If a deferred feature is _just scope_ and costs you nothing, then **whatever you do keep in scope has to be built cleanly.** If authentication is in scope, build proper, secure auth that will carry you forward for the foreseeable future without further thought. That isn't premature optimization; it's getting the in-scope requirements right so you can take them off your mind and focus fully on the next thing. Clean execution on what you commit to is what buys you _sustained_ speed.

So far this looks like a tidy binary: defer cleanly, or substitute deliberately. But there's a catch, and it's the same catch for both cuts. Whether either one stays safe depends on something underneath the visible choice, and that something, it turns out, is placed by your vision.

## The Two Cuts Already Have Names

Neither cut is new. The literature on [iterative and incremental development](https://en.wikipedia.org/wiki/Iterative_and_incremental_development) has a name for each, and it has spent decades pointing out that people conflate them.

Alistair Cockburn drew the line cleanly in _Using Both Incremental and Iterative Development_ <d-cite key="cockburn2008incremental"></d-cite>. **Incremental** development stages a system in parts that are built and integrated over time; you add pieces to something that stays. **Iterative** development builds a rough version and then reworks it, refining the same thing through repeated passes. Jeff Patton illustrated the difference memorably: painting the Mona Lisa _incrementally_ means finishing it corner by corner, while painting it _iteratively_ means sketching the whole canvas roughly and sharpening it pass after pass <d-cite key="patton2008iterating"></d-cite>.

Deferral is the incremental move; substitution is the iterative one. Fred Brooks supplies the cautionary arc for substitution. His famous advice, "plan to throw one away; you will, anyhow," was about building a deliberate throwaway to learn from. Two decades later he partly recanted, devoting a chapter of the anniversary edition of [_The Mythical Man-Month_](https://en.wikipedia.org/wiki/The_Mythical_Man-Month) to the argument that an incremental-build model beats building one to discard <d-cite key="brooks1995mythical"></d-cite>. The lesson isn't that one cut is right and the other wrong. It's Cockburn's: you need _both_, used deliberately.

A single MVP almost always mixes the two, which is why the unit you classify is the individual cut, not the whole product. That also corrects a quiet imprecision in the usual mantra. "Build an MVP and iterate" names only half the work: iterating reworks what's already there, but just as much of what follows an MVP is _incrementing_, adding the pieces you deliberately deferred. The fuller version is **"build an MVP, then iterate _and_ increment"**, and telling which of the two a given cut commits you to is the skill this post is about.

## The Decision Rule and the Seam

The practical test is one question, asked the moment you make a cut: **will I grow this, or throw it away?** If you'll grow it, you're deferring, and the job is to leave room for it. If you'll throw it away, you're substituting, and the job is to keep the throwaway from spreading. Either way, decide deliberately, not with the reflexive "we'll clean it up later" muttered under a deadline.

Here's the catch I promised: a deferral can _silently_ become a substitution. "Defer multi-tenancy" but build around single-organization assumptions, and you haven't deferred anything; you've baked a single-tenant architecture in, and retrofitting tenancy later is a rewrite. The absence became a stand-in you never chose.

What separates a clean deferral from that trap is whether you left a **seam**: in Michael Feathers' words, "a place where you can alter behavior in your program without editing in that place" <d-cite key="feathers2004legacy"></d-cite><d-cite key="fowler2024legacyseam"></d-cite>. A seam holds the place for something not yet built, or contains a throwaway so swapping it later has a small blast radius. It needn't be a literal interface. For access control, it's less a request choke point than a **data model that anticipates the partition**: design entities so they can later be split into groups or tenants, and adding role-based access control becomes _filling in_ a boundary that already exists rather than re-cutting the model.

Substitution works the same way. Say you need a machine-learning model you can't train well yet. Define the target interface now, a versioned [ONNX](https://onnx.ai/) contract, so today's weaker artifact merely satisfies it and can be swapped cleanly later; versioning the contract even lets the interface evolve as your vision sharpens, without breaking everything around it. The throwaway sits behind a clean boundary, so the rebuild is a swap, not a rewrite. This is exactly the seam the [skateboard-to-car analogy](/blog/2025/mvp-manage-debt-and-iterate-fast/) I criticized earlier lacked: a skateboard has no boundary to rebuild behind, so "upgrading" it into a car means starting over, whereas a contained throwaway lets you replace only the part that was always meant to go.<d-footnote>The generic version is any stand-in placed behind a stable interface: a manual or <a href="https://en.wikipedia.org/wiki/Wizard_of_Oz_experiment">"Wizard of Oz"</a> backend behind the API the real service will expose, or a payments interface wired to a test provider before the real integration exists. The point isn't to mock everything. Substitute only what has to be in the product from day one but can't be built properly yet; the stable interface is what lets the rest of the product increment around it.</d-footnote>

Which points at what the two cuts share. Every cut asks two questions, not one. The cut you chose sets _what the seam has to do_: hold an empty place you'll fill, or contain a throwaway you'll swap. The second question is independent, and it's the one that decides whether the cut is safe at all: does that seam exist?

<table>
  <thead>
    <tr>
      <th></th>
      <th><strong>Seam present</strong></th>
      <th><strong>No seam</strong></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Defer</strong></td>
      <td>clean scope: place held, fill later</td>
      <td>accidental substitution: backed into a rewrite</td>
    </tr>
    <tr>
      <td><strong>Substitute</strong></td>
      <td>honest throwaway: contained, swap later</td>
      <td>duct tape: stand-in smeared everywhere</td>
    </tr>
  </tbody>
</table>

Read down the columns, not across the rows: both cuts are safe _with_ a seam and dangerous _without_ one. A deferral with no seam isn't really a deferral, you baked the feature's absence in, so adding it later is a rewrite; a substitution with no seam can't be thrown away as planned, because the stand-in leaks into everything around it until pulling it out is a rewrite too. Not that every cut needs a seam: a cleanly additive feature can just be deferred with nothing held open for it. But where a cut would otherwise harden an assumption you'll later have to undo, leaving the seam out is exactly the sloppiness that scrappy teams mistake for speed.

## Vision Places the Seams

If the seam is what matters, the next question is where to put one, and you can't seam everything. Even a light seam costs foresight and indirection, and the heavy ones cost real engineering. Seaming everywhere is its own kind of debt: the speculative over-engineering that ["you aren't gonna need it"](https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it) warns against.

A seam is a bet about where the system will change, and **your vision is your best model of where it will change**. That is why vision tells you where the seams belong. The principle goes back to David Parnas's [information hiding](https://en.wikipedia.org/wiki/Information_hiding): hide the design decisions most likely to change behind a module boundary, so a change touches one place instead of many <d-cite key="parnas1972criteria"></d-cite>. The seam is that boundary. This is the resolution of the earlier catch, and the reason the right cut depends on your vision: vision operates one level _below_ the visible decision to cut. Two teams can make the identical surface call, "leave out access control," and one ends clean while the other ends rewritten, purely because one team's vision told it to anticipate the partition and the other's didn't.

This is also why the vision has to be **falsifiable**. A vision vague enough that it can never be wrong can't tell you anything about where change is coming, so it can't guide a single seam. A specific vision can be corrected by what you learn, and each correction re-points the seams.<d-footnote>Which is why a confident vision that is simply wrong can be worse than a vague one: it spends real effort seaming where change never comes while leaving the true fault lines bare. Falsifiability pays off only when feedback arrives fast enough to move a seam before the one you skipped has hardened into a rewrite.</d-footnote>

What you're really foreseeing is not a fixed roadmap but a set of _options_: a seam is a small premium you pay now to keep the right, but not the obligation, to change a component later. This is the options view of modularity that Baldwin and Clark formalized: a module boundary carries a real option to redesign what sits behind it, worth most exactly where the future is uncertain <d-cite key="baldwin2000designrules"></d-cite>. You buy options where the underlying is volatile, and vision is what tells you which volatility is worth insuring against.<d-footnote>Which makes foresight itself a form of prevention, and prevention's payoff is always an absence. A seam placed early averts a rewrite that then never happens, so the cost it saved leaves no trace and the work goes uncredited. It's the same asymmetry I explored in <a href="/blog/2026/we-reward-the-fix-not-the-prevention/">Your Best Work Leaves No Trace</a>: thinking ahead is chronically undervalued precisely because what it prevents can't be seen, even though it's exactly what buys the sustained iteration speed this whole series is about.</d-footnote>

## When the Seam Comes Due

A substitution doesn't come due on a schedule. It comes due when you expand into a new segment that makes the stand-in load-bearing. The hand-tuned rules engine that stood in for a model is fine until you sell to a customer whose cases it can't cover: that's the moment to spend the seam you left and swap in the real thing. The rebuild is _pulled_ by the market, not done speculatively.

That is why an MVP needs not just a minimal product but a **[minimum viable segment](https://underscore.vc/resources/minimum-viable-segment/)**: a single, well-defined slice of the market you serve fully today, before rolling into the next one.<d-footnote>The idea is well worn. In <a href="https://en.wikipedia.org/wiki/Crossing_the_Chasm"><i>Crossing the Chasm</i></a>, Geoffrey Moore called this narrow first segment a beachhead, his military metaphor: as in the D-Day landings, you seize one small, defensible stretch of a contested shore and secure it fully before pushing inland <d-cite key="moore1991chasm"></d-cite>. Bill Aulet later made choosing a beachhead one of the first steps of his 24-step method <d-cite key="aulet2013disciplined"></d-cite>. Scaling ahead of that segment has a name, premature scaling, and the Startup Genome project found it among the most common ways startups die; in their data, no prematurely scaled company passed a hundred thousand users <d-cite key="startupgenome2011premature"></d-cite>.</d-footnote>

So grow your scalability _together with_ your addressable market: each new segment both justifies the rework and tells you what it needs to do. This is no license to build cheap and unscalable: if the "right" scalable version costs little more than the stand-in, or the vision already makes it near-certain, just build it properly now. Deferral earns its keep only when doing it right would cost significantly more. The seams you left are what let you grow into a new segment without tearing the product apart, and the segment tells you which seam to spend next.

## Cutting With Vision

The "two cuts" is the part you can see: defer, or substitute. They are genuinely different moves, one adding, one replacing, with different work left to do. But what makes _either_ of them safe is the same thing: a **seam** under the cut, placed where your **vision** says change is coming. That is why the same shortcut can be smart scoping for one team and a future rewrite for another. Same cut, different vision, different seam.

That closes the loop on the trilogy. The first post argued debt is a tool you wield deliberately; the second, that technology readiness debt is what you carry when the technology isn't ready yet; and this one, that the everyday cuts of an MVP turn safe or dangerous on one hidden thing: whether a falsifiable vision left you the seams to grow some parts and replace others, paced by the market you actually serve.

So the next time someone says "let's just cut that for the MVP," ask the quiet follow-up: are we deferring this or replacing it, and either way, where's the seam?

**Cutting scope is how you move fast. Leaving seams is how you stay fast.**

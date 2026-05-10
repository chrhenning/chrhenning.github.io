---
layout: distill
title: Technology Readiness Debt – Building Before the Future Arrives
date: 2025-09-12 08:15:00
description: Technology Readiness Debt (TRD) is the gap between today's imperfect technology and tomorrow's vision — a strategic debt you carry to learn early, but one that only R&D can repay on your terms.
tags: technical-debt
categories: product-management
giscus_comments: true
related_posts: true
related_publications: false
citation: false

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: What Is Technology Readiness Debt?
  - name: The Payoff of Carrying TRD
  - name: When TRD Comes Due
  - name: Building Before the Future Arrives
---

In my [last blog post](/blog/2025/mvp-manage-debt-and-iterate-fast/), I explored the different forms of debt in product development — from technical to strategic to marketing — and argued that debt itself isn't bad, as long as you're conscious of the trade-offs and align them with your long-term vision.

This time, I want to introduce a type of debt I haven’t seen described before: **Technology Readiness Debt (TRD)**. Unlike technical debt, which is often the result of shortcuts, TRD comes from building in a world where the technology you really need isn't ready yet. You ship something that's "good enough" to deliver value and gather market insights, knowing you'll have to replace it once the underlying technology matures.

TRD is the reality of building ambitious products before the technology is fully ready. The real question isn't whether you carry it, but whether you manage it consciously and have the R&D muscle to pay it off before others do.

## What Is Technology Readiness Debt?

**Technology Readiness Debt (TRD)** arises when you build a product knowing that the underlying technology is not yet fully mature. You accept that your first solution will be imperfect — brittle, limited, or inefficient — but you move forward anyway to gain real-world experience, validate customer needs, and be ready when the technology catches up.<d-footnote>TRD is not to be confused with <a href="https://en.wikipedia.org/wiki/Technology_readiness_level">Technology Readiness Levels</a> (TRLs), a framework originally developed by NASA to measure how mature a technology is, ranging from basic principles (TRL 1) to fully operational systems (TRL 9). TRL measures the maturity of a technology; TRD describes the strategic choice to build before the necessary TRL has been reached.</d-footnote>

This makes TRD fundamentally different from [technical debt](https://en.wikipedia.org/wiki/Technical_debt). TRD comes from constraints: the "right" solution doesn't exist yet. You can either wait until it does, or build with what you have. Taking on TRD means choosing to start learning early, knowing you'll need to rebuild later.

Take **computer vision** (CV). A decade ago, deep learning was already showing enormous promise, but it wasn't yet straightforward to deploy in production. We're still far from a universal solution; most production CV still requires carefully engineered pipelines. But the point is: if you had waited for "deep learning to be ready", you would have lost years of market learning. Early, imperfect solutions bought valuable insights — at the cost of accumulating TRD.

The key is that TRD is not a mistake. It's a conscious trade-off: **you accept a temporary technological compromise** to validate a vision early, gain customers, and prepare for the moment when the tech finally catches up — **and position yourself to be the first to scale** when it does.

### TRD in the Innovator's Dilemma

In his classic book [The Innovator’s Dilemma](https://en.wikipedia.org/wiki/The_Innovator%27s_Dilemma), Clayton Christensen showed why established companies often fail when faced with disruptive technologies. The paradox is simple: incumbents listen to their best customers, who demand better performance on known metrics. As a result, they ignore new technologies that start off weaker, niche, or "not good enough" for their mainstream market.

That's exactly where Technology Readiness Debt (TRD) lives. Emerging technologies almost always start immature: unreliable, costly, or clunky. For an incumbent, adopting them early looks irrational — it would disappoint existing customers and cannibalize revenue.

Startups, on the other hand, have nothing to lose. By deliberately taking on TRD, they play in spaces incumbents can't. They validate early use cases, learn about customers who are underserved by the status quo, and position themselves for scale when the technology matures.

- **Blockbuster vs. Netflix.** Blockbuster ignored streaming because the infrastructure and customer base weren't ready. Netflix, meanwhile, carried TRD — first by operating in DVDs, then by pivoting fast as broadband spread. Their early learning and brand presence gave them a head start incumbents couldn't match.
- **Early electric cars.** Major automakers dismissed EVs because limited range and high costs alienated their core buyers. Startups (and later Tesla) leaned into those limitations, targeting enthusiasts and niche markets. By carrying TRD, they were ready when battery technology and infrastructure caught up.

The lesson: **TRD is the wedge that lets innovators survive the dilemma**. Incumbents are trapped by customer demands today; startups can embrace technology's immaturity to be ready for tomorrow.

## The Payoff of Carrying TRD

If TRD is about building with immature technology, the natural question is: why bother? Why not just wait until the technology is "ready"?

The answer is that **market timing rarely lines up with technology timing**. Visionary ideas almost always arrive before the technology is fully mature. If you wait for perfection, you miss the chance to:

- **Validate your vision early.** A long-term product vision is necessary, but reality rarely matches the founder's slide deck. TRD allows you to get a version into customers' hands early, so you learn where your assumptions are wrong before investing years of R&D.
- **Understand your customers deeply.** The danger of waiting is that by the time the technology is ready, you may have no idea what customers actually want. Carrying TRD forces you into the messy process of co-creation: testing, iterating, and adapting your vision in the real world.
- **Build brand and trust.** Even imperfect early solutions plant seeds of credibility. Customers remember who showed up first — especially if you're transparent about limitations and committed to improving over time.
- **Position for the inflection point.** By the time the technology matures, you've already paid the learning costs. Competitors who start then face both the technical gap and the market gap.

The critical nuance is this: **TRD only makes sense if you have a long-term vision.** Without a vision, TRD just looks like a bad product. But with a vision, the imperfect early product is a stepping stone — a vehicle for validated learning that ensures when the technology catches up, your business is not only ready but already trusted.

## When TRD Comes Due

Like any debt, TRD eventually comes due. You can't carry brittle and hacked-together solutions forever. At some point, the technology gap must be closed — or your competitors will close it for you.

There are two ways this "repayment" happens:

- **External progress.** Sometimes, the world solves your problem for you. Hardware costs drop, standards emerge, or new algorithms become commodity. If you timed it right, you can simply swap in the new tech when it matures. This is what happened with Netflix: once broadband became ubiquitous, streaming became inevitable.
- **Internal R&D.** More often, though, you can't just wait. The specific problems you face won't be solved "out there" — or at least not on your timeline. That's when you need focused research and development to actively close the gap between today's imperfect solution and your long-term vision.

In my experience building up R&D in a startup, I’ve seen how easy it is to underestimate this second path. It is tempting to treat R&D as optional — something you add later, when you’re already successful. In reality, R&D is the mechanism that lets you pay off TRD before someone else does. It not only closes the gap but also gives you the expertise to know when external progress is ready, the talent to keep pushing forward, and the differentiation to build a moat competitors can’t easily copy.

But there's a catch: TRD is not isolated from [technical debt](https://en.wikipedia.org/wiki/Technical_debt). When the time comes to replace your tech stack, you must also be in a position where accumulated shortcuts don't strangle the transition.

### R&D as the Bridge from Today to Tomorrow

As mentioned earlier, TRD only makes sense if you have a long-term vision. Without that vision, you're just shipping fragile products that will eventually break. But vision alone isn't enough — you need a way to bridge the gap between what's possible today and what's required tomorrow. That bridge is R&D.

R&D serves three critical roles in paying off TRD:

- **Closing the gap.** Internal research lets you attack the unsolved problems that stand between your MVP and your future product. Without it, you're waiting on external forces that may never align with your needs.
- **Shaping the direction of progress.** If you only adopt external advances, you're downstream of innovation. R&D moves you upstream: you're not just a consumer of technology, but a contributor, sometimes even setting the standards that others later follow.
- **Maintaining vision integrity.** TRD assumes that you will eventually converge on a stronger, more scalable solution. R&D is what keeps that convergence alive. Without it, the vision risks being eroded by short-term hacks until the original ambition disappears.

A strong R&D function is not a luxury to add once you've "made it" — it's the mechanism that ensures you ever get there. **It attracts the kind of people who want to solve hard problems, accelerates the repayment of TRD, and gives you the confidence to bet on ambitious futures without waiting for the world to hand them to you.**

The companies that win aren't the ones with no TRD. They're the ones with the discipline to carry it consciously and the R&D muscle to pay it off before anyone else can.

## Building Before the Future Arrives

As I argued in [my previous post](/blog/2025/mvp-manage-debt-and-iterate-fast/), smart debt management is not about avoiding debt, but about wielding it deliberately. Unlike feature, design, or technical debt, **technology readiness debt (TRD) is both unavoidable and strategic**. Bold visions often rely on technologies that aren't yet mature. The only way to make those visions real is to carry TRD consciously — validating customer needs early so that when the technology arrives, you’re ready. And because waiting for external progress is rarely enough, **R&D becomes the critical lever to pay off TRD on your terms, before others do it for you**.

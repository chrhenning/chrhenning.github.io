---
layout: distill
title: Scrappiness Incentivizes Sloppiness - Why Lean Thinking and Debt Management Build Better Products
date: 2025-10-31 19:15:00
description: Scrappiness is often mistaken for agility, but in practice it breeds unmanaged debt; a lean, debt-aware mindset achieves speed without sacrificing integrity.
tags: mvp
categories: product-management
giscus_comments: true
related_posts: true
related_publications: false
citation: false
bibliography: 2025-10-31-scrappiness-incentivizes-sloppiness.bib

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: Scrappiness and Technical Debt
  - name: The Empirical Case for Quality
  - name: Throwaway Code - The True Exception
  - name: Lean Thinking - The Sustainable Alternative
  - name: Conclusion — Speed Without Sacrifice
---

I often hear “scrappiness” praised as a virtue in modern software engineering — a call to move fast, improvise, and avoid perfectionism. There's truth in that; perfectionism can paralyze progress.

Yet "scrappiness" is a dangerously vague term. It's meant to signal agility and resourcefulness, but in practice, it often incentivizes **sloppiness**. When everything is excused as "scrappy", [technical debt](https://en.wikipedia.org/wiki/Technical_debt) becomes invisible — and invisible debt is the kind that never gets paid.

The irony is that what we celebrate as "speed" is often just **short-term acceleration** at the expense of sustainable long-term velocity and progress. Code quality, far from being a luxury, is what keeps teams fast once the first version ships. Research confirms this: poor-quality code leads to up to fifteen times more defects and more than double the development time <d-cite key="tornhill2022code"></d-cite>.

In this blog, I argue that scrappiness is a poor metaphor for effective engineering. A **lean, debt-aware** mindset achieves speed without sacrificing integrity, and ultimately, builds better products.

## Scrappiness and Technical Debt

When code is meant to last — to be extended, maintained, or shared — scrappiness becomes a **redundant concept**. Every shortcut taken in such a context already falls under a well-defined term: **technical debt**. The difference is that debt carries a built-in moral — it must be paid back. Scrappiness, in contrast, is often celebrated as if no repayment were needed.

Technical debt is not inherently bad; it’s a deliberate trade-off to gain short-term speed when learning or market feedback is paramount. But the key is awareness: you consciously take on debt with the intention to repay it later. Once that awareness fades, debt compounds. McKinsey calls this the vicious cycle of technical debt: the more you defer cleanup, the slower and riskier each subsequent change becomes <d-cite key="baig2023breakingtechnicaldebt"></d-cite>.

Scrappiness, as it's typically invoked in teams, drops that awareness. It's debt without bookkeeping — an emotional appeal to "just get it done". This mindset normalizes low-quality practices and weakens accountability. Developers no longer distinguish between lean trade-offs that enable learning and sloppy compromises that silently tax every future iteration.

This drive for initial speed sometimes aligns with the philosophy of ["Worse is Better"](https://en.wikipedia.org/wiki/Worse_is_better), a term often misunderstood. Its original intent is not to produce "bad" quality, but to favor simplicity and implementation speed over premature complexity and completeness, allowing for rapid adoption and essential feedback.<d-footnote>In the end, <a href="https://www.geeksforgeeks.org/software-engineering/premature-optimization/">premature optimization is known as the root of all evil</a>.</d-footnote> This approach is a form of strategic, conscious technical debt. However, if teams use this rationale to justify low-quality solutions that are not truly disposable or built upon simple, correct core behavior, they are simply trading temporary motion for lasting momentum.

## The Empirical Case for Quality

If "scrappiness" were truly the path to speed, messy codebases would outperform clean ones — but empirical data proves the opposite. Code quality is one of the strongest predictors of long-term development velocity.

Quantitative analysis consistently debunks the myth of a speed-versus-quality trade-off <d-cite key="tornhill2023codequality"></d-cite>. For instance, a study of 39 proprietary codebases found that low-quality systems take 124% longer to modify and suffer from drastically higher maintenance costs and defect rates <d-cite key="tornhill2022code"></d-cite>. Unmanaged debt doesn't just slow teams down—it **doubles the effort required to deliver value**.

Large organizations have learned this lesson the hard way. Meta's engineering culture, once defined by "move fast and break things", eventually shifted toward a more disciplined focus on stability and sustainable velocity <d-cite key="stokelwalker2024movefast"></d-cite>. As early as 2014, Facebook officially replaced its old motto with "move fast with stable infrastructure" <d-cite key="murphy2025stableinfra"></d-cite>. The company recognized that speed built on instability doesn't scale. Further, Mockus et al. (2025) detail how systematic code quality improvements became essential to maintaining productivity across their tens of thousands of engineers <d-cite key="mockus2025code"></d-cite>. Code quality is not an aesthetic concern — it's the primary engine of long-term performance and velocity.

## Throwaway Code: The True Exception

There is one domain where scrappiness can make sense: true throwaway prototypes.

When the sole purpose of a piece of code is to explore an idea, validate a hypothesis, or test a risky assumption, the goal is learning — not longevity. In such cases, debt is irrelevant because the system will never need to be maintained or extended. The code is disposable by design.

However, confusion begins when teams lack the discipline to actually throw prototypes away. What starts as an experiment quickly becomes the seed of a production system — and the shortcuts taken under "scrappy" conditions turn into liabilities.

Even for genuine prototypes, scrappiness shouldn't mean sloppiness. A prototype should be simple, transparent, and trustworthy enough to support the learning it's meant to produce. When the prototype itself becomes too messy to reason about, it defeats its own purpose, generating false signals rather than insight.

The distinction is crucial: the right mindset is not "move fast and hack things", but rather "build just enough to learn — and know when to throw it away".

## Lean Thinking: The Sustainable Alternative

If scrappiness is the illusion of speed, [lean thinking](https://en.wikipedia.org/wiki/Lean_thinking) is its sustainable form.

Lean development doesn't reject shortcuts — it manages them. It emphasizes clear priorities, continuous learning, and incremental improvement without glorifying chaos. Where scrappiness rewards improvisation for its own sake, lean thinking insists that every shortcut comes with an explicit plan for repayment.

This mindset aligns with what both empirical research and industry practice have converged on: quality is a driver of long-term speed, not a drag on it. Maintaining clean, modular codebases leads to shorter lead times resulting in competitive advantages <d-cite key="tornhill2023codequality"></d-cite>. Lean development is about moving deliberately: fast where you can, careful where you must. It values maintainability over complexity, speed with accountability, and debt with discipline.

## Conclusion — Speed Without Sacrifice

Scrappiness too often becomes a blanket excuse for poor quality and unmanaged shortcuts. Once "scrappy" work enters production, the hidden costs begin to surface: slower iteration, more bugs, and eroding trust in the system.

A more precise and constructive framing is debt management. Technical debt is a tool — one that lets teams balance exploration and execution, provided they track and repay it consciously. Where scrappiness ignores consequences, debt management acknowledges them. Where scrappiness rewards improvisation, lean thinking rewards learning.

The most effective teams don't move fast by cutting corners — they move fast because their systems allow them to. They treat quality as infrastructure, not ornamentation. In the end, **the choice isn't between speed and stability, but between temporary motion and lasting momentum**.

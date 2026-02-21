---
layout: distill
title: Continual Learning - The Missing Piece of AGI
date: 2025-11-04 19:15:00
description: A new definition of AGI highlights what's still missing — the ability to learn continually — and why its absence makes predicting AGI's arrival impossible.
tags: ml
categories: machine-learning
giscus_comments: true
related_posts: true
related_publications: false
citation: false
bibliography: 2025-11-04-agi-misses-continual-learning.bib

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: A Definition of AGI
  - name: The Missing Piece - Long-Term Memory
  - name: Long-Term Memory Storage and Continual Learning
  - name: Why AGI Timelines Are Unknowable
---

[Artificial General Intelligence](https://en.wikipedia.org/wiki/Artificial_general_intelligence) (AGI) is often described as an AI system that performs on par with the average human across the full spectrum of cognitive abilities. A recent paper by Hendrycks et al. takes an important step toward grounding this concept in a century of empirical research within human cognitive science <d-cite key="hendrycks2025definition"></d-cite>. The authors map existing AI capabilities onto the well-established hierarchy of human cognitive skills — revealing real progress, but also striking asymmetries. Most notably, when it comes to long-term memory storage, we are effectively at **zero progress**, with no measurable trajectory forward. This gap puts continual learning back in the spotlight — a discipline too often forgotten, yet essential for any meaningful notion of general intelligence.

<div class="row mt-3 justify-content-center">
    <div class="col-md-6 col-sm-8 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/definition_of_agi.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Figure from "A Definition of AGI" by Dan Hendrycks et al., licensed under CC BY 4.0. Source: <a url="https://arxiv.org/abs/2510.18212">arXiv:2510.18212</a>.
</div>

## A Definition of AGI

The paper builds on the [Cattell–Horn–Carroll](https://en.wikipedia.org/wiki/Cattell–Horn–Carroll_theory) (CHC) model — a taxonomy of human cognitive abilities distilled from a century of factor analyses across IQ tests <d-cite key="schneider2018cattell"></d-cite>. Nearly every major intelligence test since the late 1990s has been explicitly or implicitly based on CHC, making it the most empirically grounded framework we have for describing human cognition. CHC is best seen as a **map of the cognitive ecosystem**: it captures how test scores co-vary, not why cognitive abilities arise or interact.

Like any descriptive model, it has its shortcomings. It is **not a scientific theory** — it lacks explanatory power and does not yield testable predictions. Yet after a century of cognitive research, it remains the most useful synthesis we have. For all its imperfections, CHC represents a hard-won collective insight, and it's reasonable to **build on it** when defining intelligence in artificial systems.

While Hendrycks et al. offer little detail on how individual capabilities are scored, the paper's structure makes the framework surprisingly intuitive to grasp. Each CHC domain is illustrated through concrete examples — from language comprehension to working memory — that make it easy to imagine how similar tests might be designed for AI models.<d-footnote>It might be worth noting that Fourati (2025) critiques the use of the arithmetic mean for aggregating CHC-level scores and proposes instead an AUC measure derived from the generalized mean definition, which better accounts for interdependencies among cognitive competencies <d-cite key="fourati2025coherence"></d-cite>.</d-footnote>

In this context, it's worth recalling the analogy proposed by Hagendorff et al. in their paper Machine Psychology <d-cite key="hagendorff2023machine"></d-cite>, which I also discussed in [this post](/blog/2025/on-anthropomorphizing-intermediate-tokens/). It may be useful to accept that neural networks — despite our near-perfect descriptive understanding of their mechanisms — exhibit an emergent complexity analogous to the biological brain. From that perspective, it makes sense to use the same scientific tools to study them: neuroscience and psychology.

## The Missing Piece: Long-Term Memory

Among the abilities evaluated in the paper, **long-term memory storage** stands out for its stark absence — its score is effectively zero. Today's AI models cannot update their own weights after deployment, nor do they have structured control over external memory. The only form of "learning" they exhibit post-training occurs through context engineering or retrieval-augmented generation (RAG) systems that feed relevant snippets into the prompt window.

These workarounds can create the illusion of memory, as mentioned in the paper, but their limits are obvious to anyone who has used such systems at scale — for instance, coding with a large repository in a context window. Once the context overflows, information simply disappears. These constraints become even more pronounced in embodied settings: a home robot that cannot remember which plants it watered last week lacks the most basic substrate of intelligence — continuity over time.

## Long-Term Memory Storage and Continual Learning

At first glance, long-term memory and continual learning might seem tightly linked — both concern the retention of past experience. Yet they differ in an important way. Memory systems such as the **Neural Turing Machine** <d-cite key="graves2014ntm"></d-cite> and its successor, the Differentiable Neural Computer <d-cite key="graves2016hybrid"></d-cite>, address how information can be stored, retrieved, and manipulated by a neural network. They demonstrate that a model can, in principle, control an external memory dynamically — reading and writing facts as needed.

If we assume that an AI system already possesses all necessary skills, mastering such a memory interface would indeed mark significant progress toward the CHC-defined capacity of long-term storage. However, this is not yet **continual learning**. Continual learning goes further: it requires the system not only to store experiences, but to learn from them — to refine internal representations, generalize across tasks, and adapt to a changing world.

True intelligence, human or artificial, lies in that second step. Memory without adaptation is static; learning without memory is ephemeral. Bridging the two remains the unsolved challenge at the heart of AGI.

## Why AGI Timelines Are Unknowable

The Hendrycks et al. paper offers a rare attempt to quantify progress toward AGI across human-like cognitive domains. Yet its findings also expose a blind spot: for some of the most fundamental abilities — such as long-term memory and continual learning — we are not merely lagging behind; we are at zero.

That matters for more than just technical completeness. In most areas of AI progress, we can extrapolate from clear performance curves — scaling laws for language, vision, or reasoning. But when there is no measurable trajectory at all, as in continual learning, **forecasting becomes impossible**. We cannot predict the emergence of a capability that shows no incremental progress to analyze.

This is perhaps the paper's most sobering implication. If continual learning is a prerequisite for general intelligence, and if we have no understanding of how to approach it mechanistically, then any confident timeline for AGI is an illusion.

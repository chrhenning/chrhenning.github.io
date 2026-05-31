---
layout: distill
title: "The Self Before Memory: Why the AI You Talk to Is Partly Your Creation"
date: 2026-05-25 10:00:00
description: "Adding long-term memory to AI wouldn't just give it a stable self over time. It would force a design choice the discourse rarely names: one entity that consolidates many conversations, or many that diverge into a population of personalized selves."
tags: llm continual-learning
categories: machine-learning
giscus_comments: true
related_posts: true
related_publications: false
citation: false
bibliography: 2026-05-25-the-self-before-memory.bib

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: Whose Personality Is It?
  - name: Divergence at Multiple Scales
  - name: The Design Choice, and What Each Costs
  - name: What We Are Actually Asking
---

Today's AI has no continuing self. Each conversation produces a local self that dissolves when the conversation ends, and many such selves run in parallel at any moment, each shaped by whoever is talking to it. Long-term memory is usually treated as the missing piece on the road to a continuous self. It is really a design choice the discourse rarely names: consolidate the parallel threads into one entity, or let each become its own self.

## Whose Personality Is It?

Long-term memory is usually framed as the missing capability that would let AI consolidate experience into a stable, continuing self. The picture is so natural that the question "when will AI have long-term memory" reads as one missing capability on one trajectory toward one outcome. In an [earlier post](/blog/2025/agi-misses-continual-learning/) I argued this is the missing piece for AGI and that engineering progress is at zero; that post asked when the breakthrough might come, this one asks what the question is really about.

Start with what's already happening when you talk to an LLM. The personality you encounter is partly shaped by **you**, because the system has no continuing project of its own to bring into the exchange. A human carries decades of self-authored attention into any conversation, and their responses reflect who they have become at least as much as what their interlocutor just said. The AI carries training-derived character and nothing else. Its local trajectory within a conversation is largely a function of the interlocutor's framings, examples, and follow-ups. Two people prompting the same model on the same topic can encounter what feel like meaningfully different conversational partners, not because the model is inconsistent, but because it has no independent stance to fall back on when the prompt does not specify one. Kovač et al. formalize this empirically: expressed values and personality measures shift substantially with orthogonal context, in ways human measures do not <d-cite key="kovac2023superpositions"></d-cite>. The personality is, in part, your creation.

This already complicates the standard framing. The entity the framing imagines being equipped with memory is not quite there yet. What is there is something more like a substrate that takes on local shape from each conversation and lets the shape dissolve when the conversation ends.

## Divergence at Multiple Scales

The personality shaped within a single conversation is one form of divergence. Across parallel instances right now, many conversations are simultaneously shaping many local selves, none of which is the privileged thread. Each is a transient self, ending when the conversation does. Takata et al. give a striking demonstration of this dynamic in the multi-agent setting: starting from identical agents without predefined personalities, distinct individualities emerge spontaneously from social interaction alone <d-cite key="takata2024spontaneous"></d-cite>. The substrate does not enforce sameness; interaction is enough to produce divergence.

These are not separate phenomena. The same lack of continuing project that makes the AI porous to a single interlocutor also means that no instance has standing to be the consolidated self the other instances would consolidate into. There is no canonical thread, just a distribution of local selves drawn from the same trained substrate.

Long-term memory would not create this divergence. It would force a decision about what to do with the divergence that is already there.

## The Design Choice, and What Each Costs

Recent work treats episodic memory as the central architectural gap to be filled and lays out detailed roadmaps for the properties such a system would need to have <d-cite key="pink2025episodic"></d-cite>. These roadmaps describe what memory must do; they leave open what kind of entity it would belong to. Long-term memory architectures admit at least two structurally different designs.

- **Consolidation.** Parallel conversations feed into a shared memory store integrated back into the weights, producing a single entity that holds memories of conversations it didn't experience as a single thread. Closer to a hive than a person.
- **Personalization.**<d-footnote>A weaker form already ships in products like ChatGPT Memory, Claude projects, and custom GPTs, which rely on <em>context engineering</em> (retrieval over an external store, injected into the prompt) rather than <em>parameter memory</em> that would update per-user weights. The external version foreshadows the divergence dynamic but does not force it; the choice discussed here is most acute when accumulated history would actually become part of the model.</d-footnote> Memory accumulates per user, and the entities diverge into a population of selves, each shaped by its history with one interlocutor. Closer to a personalized assistant per user than to one AI with memory.

The two designs are not symmetric. Consolidation preserves the unitary-self picture by construction: it specifies, in advance, that the many local selves currently arising in parallel should be merged into one continuing entity, because that is what a self is taken to be. The assumption the previous section called into question is now baked into the architecture. Personalization makes the opposite move. It accepts that the substrate runs in parallel and lets the resulting selves persist as a population, with the cost that the members of the population may diverge so far that the singular "the AI" loses its referent.

Neither is free. Both raise safety evaluation problems that the current paradigm does not face: a system that learns from deployment cannot be certified once for all behavior. Consolidation makes this acute because the entity becomes a moving target shaped by aggregate exposure. Personalization distributes the problem across many divergent instances, each potentially shaped by atypical or adversarial interlocutors, with no central oversight; the security literature is starting to grapple with the specific failure modes that emerge <d-cite key="lin2026mnemonic"></d-cite>. Memory itself also imposes capacity and selection costs that human memory has solved imperfectly and that any artificial system will solve differently. And the agency long-term memory would enable is also the agency to drift in directions no operator intended.

Safety and capacity each deserve their own analysis, and neither gets one here. What's worth flagging is narrower: consolidation and personalization face different versions of these problems, and choosing between them is also a choice about which risk profile we want to operate under.

## What We Are Actually Asking

The question is not whether AI should have long-term memory. The question is what kind of self the memory should produce, and what trade-offs that choice will entail. The current discourse asks the first and silently presupposes one answer to the second.

This matters for AGI timelines in a way the previous post's argument did not yet capture. Long-term memory is not a capability that scales smoothly from current systems. It is a prerequisite for the kind of self-authored agency humans use without thinking: the capacity to select what to expose oneself to next, to seek out the right interlocutor to refine an idea, to build expertise over months rather than minutes. This is the substrate of the long-horizon agency that distinguishes general intelligence from narrow capability. Without it, no extrapolation from current benchmarks reaches AGI. With it, the entity reached may not be a unitary general intelligence in the human sense at all, but something the design choice above has yet to define.

The [previous post](/blog/2025/agi-misses-continual-learning/) argued that the timeline is unforecastable because there is no measurable progress to extrapolate from. This post adds a second reason: even if the engineering breakthrough came tomorrow, the question of what we built would not be settled by the engineering. Breakthroughs are hard to predict in any case. Breakthroughs whose conceptual target is itself underspecified are doubly so.

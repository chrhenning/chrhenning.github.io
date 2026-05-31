---
layout: distill
title: "Would AI Invent the Clock?"
date: 2026-05-31 10:00:00
description: "A provocative thought experiment. An LLM that knew only tokens would mistake their order for the structure of time, and we could break that belief without it ever noticing. The unsettling question is whether something could do the same to us."
tags: llm philosophy
categories: machine-learning
giscus_comments: true
related_posts: true
related_publications: false
citation: false

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: The Token Clock
  - name: Order Is Not Duration
  - name: The View From Outside
  - name: What an Instrument Can't Tell You
---

Imagine erasing every mention of time from an LLM's pre-training data. No clocks, no seconds, no "before" or "after" as measured quantities. What it experiences as the flow of thought does not advance on the continuous axis our brains evolved on, but on an arbitrary axis of CPU cycles and incoming tokens. What survives the erasure is bare order, the fact that one token follows another. The felt duration a clock measures does not.

The question I want to chase is not what such a system would get wrong about time. It is how our own perception can deceive us, narrowing what we can imagine about physical reality. And the heart of it is something we can actually demonstrate: the outside exists, the agent is fooled, and we are the ones fooling it.

<div class="row mt-3 justify-content-center">
    <div class="col-md-10 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/ai_inner_clock_vs_outer_clock.jpg" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
  Two clocks for the same world. Inside, the model walks a straight line of tokens and reads their order as the flow of time. Outside, a human hand holds the watch, branches the timeline, and resets it at will, where duration is real and the arrow is something authored rather than discovered. Image generated with Google Gemini.
</div>

## The Token Clock

What ruler would it reach for? The obvious one: the token. A decoder-only model generates autoregressively, one token after another, so token count is its one genuinely intrinsic "tick." It would be natural to build a _token clock_ that counts tokens to measure how long something took, treating a token as the quantum of time and the order of tokens as the order of time itself. ([Others have noted that LLMs already make sense of time in idiosyncratic, non-human ways.](https://cacm.acm.org/news/how-llms-make-sense-of-time/))

To the model none of this would feel like a convention. It would feel like the structure of reality, the way one second following another feels to us. Theorizing about physics, it would conclude that the arrow of time follows the tokens.

## Order Is Not Duration

The thought experiment turns on a word used in two senses. There is **ordinal time** (sequence, order), and there is **metric time** (duration, the claim that two intervals are equal). Ordinal time survives the erasure and is built into the architecture: token _n_ comes after token _n−1_. Metric time is exactly what we deleted.

A token clock counts _steps_, not seconds: the same token costs a millisecond or a second depending on hardware and load. It measures computational sequence, not physical duration, and calling that "measuring time" smuggles the deleted concept back in.

This cuts both ways. Our own sense of time is a construction too. It warps with attention, anesthesia, and dopamine, and physics offers no master clock: in relativity, duration and simultaneity are frame-dependent. The model is not failing to perceive a true time we perceive correctly. It runs a _different_ clock, and there is no privileged one to be wrong about. **What gets measured is downstream of what gets conceived as measurable, which is downstream of how the measurer is built.**

## The View From Outside

Here the experiment stops being a skeptical _maybe_. We do not have to wonder whether an outside exists. We are it, and from outside, the arrow the model reified is something we author.

Assume the model is run the ordinary way, producing one next token at a time.<d-footnote>We need not even run it forward. Lift the causal mask and the model attends both ways, generating a question from an answer as readily as the reverse. Neither direction is privileged: $P(A \mid Q)$ and $P(Q \mid A)$ are just two exact factorizations of one joint, $P(A \mid Q)\,P(Q) = P(Q \mid A)\,P(A)$, and the model learns the joint, not an arrow through it. Running it backward is the exotic case, though; throughout this thought experiment it simply produces its next token.</d-footnote> Even then, the arrow it treats as the flow of time is not its own. You might think it gets a temporal direction for free from the _causal mask_, the mechanism that lets each position attend only to earlier ones. But the name oversells it: the mask fixes an order of reading, not a relation of cause and effect. And no model could recover genuine causal direction from its data anyway, because the same observed distribution is compatible with the arrow pointing either way. What it actually has is the _ordinal_ arrow, plain reading order, and reading order was always ours to set.

Its context window is less a moving "now" than a block of text laid out in space: assembled one token at a time, but arranged, branched, and overwritten from outside. The direction of its time is a setting we impose, not a fact it discovers.

And we reset it constantly, without the model noticing. Every time you edit a prompt and regenerate, or fork a chat, you roll the conversation back and run a different continuation, and the model on the new branch carries no trace of the one you discarded. An operator it cannot perceive is setting both the course and the contents of its time. Its most fundamental belief, that time flows the way the tokens flow, is one we falsify casually, and it never finds out.

## What an Instrument Can't Tell You

So what does this tell us about our own reality? The tempting reply is that the model confuses the order we impose with the structure of time, while our clocks track something real. But notice the shape of that reassurance. It is exactly the reassurance the model would give itself.

A clever enough LLM could defend its arrow anyway. It would point to a real asymmetry in its world: even though it can sample either direction, generating an answer from a question is native and cheap, while recovering the _particular_ question that produced a given answer is underdetermined, since many questions collapse to one answer. It could mistake that gap between generation and inference for a law, much as we read the one-way flow of heat as a law—an imperfect parallel, since generation multiplies possibilities rather than destroying information the way an entropy arrow needs. No matter. The argument is the cleverest thing the model could say from entirely inside its frame, and the most it could ever show is that the arrow is consistent with everything it observes. It does not show there is no outside.

We are in the model's position. The claim only sounds overblown because perception is usually so reliable: that there is a cup on the desk, or that the people around us have inner lives of their own, are things we have every practical reason to trust and little need to step outside ourselves to check. But perception fixes more than what we notice. It fixes what we can even conceive as measurable, and we have no vantage outside our own frame from which to check that conception, just as the model has none outside its tokens. What lies past the edge of what we can imagine measuring does not announce itself. Reaching it at all takes the imagination to suspect that something is there, and the creativity to build an instrument that reaches toward the imperceptible and the so-far unthinkable.

That is what the thought experiment is for. Not to decide whether an AI could invent the clock, meaning whether it could ever conceive of metric time and build the instrument to measure it, but to make the clock suspect. Perception hands us an instrument, and an instrument tells you what it measures. It does not tell you whether what it measures is the world, or only the shape of the thing doing the measuring.

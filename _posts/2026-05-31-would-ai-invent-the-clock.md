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
  - name: We Author Its Time
  - name: We Might Be in the Same Position
---

Everything we can imagine is assembled out of things we have already perceived. A color we have never seen, a sense we do not possess, a dimension we have no organ for: we can gesture at them, but we cannot actually picture them. This is easy enough to grant and strangely hard to feel the weight of, because the boundary it describes is invisible from the inside. We cannot inspect the edge of our own perception.

There is one place where that edge becomes visible: a mind we built ourselves. We can watch such a mind assemble its picture of reality and see, from the outside, exactly where the picture stops being about the world and starts being about the mind, because we are the ones who drew its boundary.

Take time. Of our four dimensions it is the odd one, the only one with an arrow, a direction you cannot walk back through. Whether that arrow is a feature of the world or a feature of the only instrument we have for noticing it is impossible to settle from the inside; there is no stepping outside yourself to check. But you can build something whose outside you _do_ occupy, and watch what it makes of time.

<div class="row mt-3 justify-content-center">
    <div class="col-md-10 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/ai_inner_clock_vs_outer_clock.jpg" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
  Two clocks for one world. Inside, the model walks a straight line of tokens and reads their order as the flow of time. Outside, a human hand holds the watch, branching the timeline and resetting it at will. Image generated with Google Gemini.
</div>

## The Token Clock

Imagine training a large language model on text with every trace of time removed. No clocks, no seconds, no "an hour later." What is left for it to experience as time?

An LLM generates one token after another. That sequence is the only thing in its world that reliably ticks, so it would be natural for the model to treat the token as its unit of time, to build a _token clock_ that counts tokens the way we count seconds. ([Others have noted that LLMs already make sense of time in their own non-human ways.](https://cacm.acm.org/news/how-llms-make-sense-of-time/)) Token _n_ comes after token _n−1_, and that "after" would feel, to the model, like the flow of time itself.

It would be wrong in a precise way. Counting tokens gives you the _order_ of things, never their _duration_: the same token might take a millisecond or a full second to produce, depending on the hardware underneath. The clock measures sequence, not time. But from the inside the model could not notice the difference. The order of its tokens would simply feel like the structure of reality, the way one second following another feels to us.

## We Author Its Time

Here is the unsettling part. We do not have to wonder whether there is a world outside the model's tokens. We _are_ that world, and from out here the arrow it treats as fundamental is ours to control.

Edit a prompt and regenerate, and you have rolled its time back and run a different continuation. Fork a chat and you have branched its timeline; the model on the new branch carries no trace of the one you discarded. You can stop it, restart it, and rearrange the text in its context window,<d-footnote>You might think the model at least gets its arrow for free from the so-called <em>causal mask</em>, the mechanism that lets each token attend only to earlier ones. But that name oversells it. The mask fixes an order of reading, not a relation of cause and effect; lift it and the model runs just as happily backwards, reconstructing a question from its answer. And it could never recover the true direction from its data in any case: the same text is equally consistent with the arrow pointing either way, since $P(\text{answer} \mid \text{question})\,P(\text{question})$ and $P(\text{question} \mid \text{answer})\,P(\text{answer})$ are two factorizations of one joint distribution. Training incentivizes a left-to-right reading order, but the distribution underneath is the same either way and carries no arrow of its own. The direction is a setting we choose, not a law the model discovers.</d-footnote> and it notices none of it. It cannot. The operator sets both the course and the contents of its time, and sits somewhere the model has no way to perceive.<d-footnote>None of this depends on the AI lacking a continuing self. Even one with long-term memory (continual learning, the subject of a <a href="/blog/2026/the-self-before-memory/">companion post</a>) would not run continuously the way a brain does. It is invoked rather than alive between calls; each step is triggered from outside. So its time stays ours to start, stop, and branch, no matter how much it carries across sessions.</d-footnote>

So its most basic belief, that time flows the way the tokens flow, is one we falsify constantly, casually, and it never finds out.

## We Might Be in the Same Position

So what does this say about us, and about that arrow we started with?

The comfortable reply is that the model mistakes an order we impose for the structure of time, while our clocks track something real. But that is exactly what the model would tell itself, and it could make a genuinely good case. From inside, it would point to what looks like a real asymmetry in its world: producing an answer from a question is cheap and natural, while recovering the _particular_ question behind a given answer is a guess among the many that could have led to it. It could read that one-way gap as a law, much the way we read the one-way flow of heat as the arrow of time.<d-footnote>The parallel is not exact, and the asymmetry is shakier than it looks. The thermodynamic arrow rests on information becoming inaccessible as entropy rises; the model's arrow runs the other way, with one answer fanning out into many possible questions. But generation fans out just as much, since one question admits many answers; the gap says more about how the model is used than about any law of its world. A mind reasoning from inside could be forgiven for missing both points and treating its asymmetry as the same kind of arrow.</d-footnote> The case would be clever, and it would fit everything the model can observe. It still would not show that there is no outside.

And our own clock is not the fixed thing it feels like. It stretches and compresses with attention, with dopamine, with anesthesia that can swallow an hour into a blink. Physics hands us no shared master clock to correct it against: in relativity, how long something takes and whether two events count as simultaneous both depend on who is asking. We are not perceiving a true time correctly while the model perceives a false one. There may simply be no outside reference that makes one reading the right one and the other the mistake.

We have no vantage outside our own perception either. And perception does not just decide what we notice; it decides what we can even conceive of measuring. **What we can measure is downstream of what we can imagine measuring, and that is downstream of how we are built.** The arrow of time may be a real feature of the world. Or it may be the shape of the instrument we look through, the way the token clock is the shape of the model, not the world. There is no settling that, and that is the point. An instrument tells you what it measures. It does not tell you whether what it measures is the world, or only the outline of the thing doing the measuring.

What lingers is how hard the cage is to escape. To reach past your own perception you must first imagine that there is something out there to reach, something you have no sensation of, no word for, no example of. That takes a rarer kind of creativity than solving a problem you can see: it means suspecting one you cannot. Our imagination is, by default, a prisoner of our perception. The clock may be one of the bars.

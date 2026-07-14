---
layout: distill
title: "Same Evidence, Opposite Certainty: Why AI Timelines Polarize on Shared Evidence"
date: 2026-07-12 08:00:00
description: AI timelines never converge, a life-long belief about human intelligence keeps shaping how new evidence gets read, and an imprecise definition of AGI means the two sides were never comparing the same thing. The first is a well-documented mechanism from the psychology of belief polarization; the second is simply definitional.
tags: agi bayesian
categories: machine-learning
og_image: https://chrhenning.com/assets/img/posts/same-evidence-opposite-certainty.jpg
giscus_comments: true
related_posts: true
related_publications: false
citation: false
bibliography: 2026-07-12-same-evidence-opposite-certainty.bib

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: A Belief Formed Over a Lifetime
  - name: Why Rational People Still Diverge
  - name: Not Even the Same Question
  - name: Why It Won't Converge
---

Each time a frontier model ships, one camp gets more confident AGI is close and the other gets more confident it isn't, both watching the exact same release. That alone isn't strange, informed people disagree on hard questions all the time. What's strange is the direction of travel: shared evidence should, if anything, bring people's views closer together, and instead both camps report growing certainty. That's the signature of [belief polarization](https://en.wikipedia.org/wiki/Group_polarization#Attitude_polarization), a well-studied pattern in which shared evidence pushes people further apart rather than together. Two mechanisms explain why it shows up here, and neither one requires anyone to be reasoning badly.

**AI timelines never converge, for two different reasons. One is a life-long belief about how human intelligence works that keeps shaping how every new AI result gets read: not a one-time split but an ongoing feedback loop. The other is that "AGI" is underspecified enough that two people can each give a coherent, carefully-reasoned forecast to a different question and call it one disagreement. Neither yields to more evidence, and neither requires anyone to be biased.**

<div class="row mt-3 justify-content-center">
    <div class="col-md-10 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/same-evidence-opposite-certainty.jpg" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <b>Same demo, opposite updates.</b> Two observers watch the same capability demonstration and each walks away more convinced of what they already believed. The evidence is shared; the lens is not. Image generated with Google Gemini.
</div>

## A Belief Formed Over a Lifetime

AGI's whole premise is matching human intelligence, so what you believe about the brain shapes what you expect from any attempt to build it. Some suspect something about the mind hasn't been discovered yet, so a machine matching it is distant almost by definition. Others treat the brain as a biological computer, remarkable but not miraculous: no missing ingredient, just gaps, and it's an open question whether closing them takes more scale on the current architecture or a genuinely different one.<d-footnote>Some of those gaps, like continual learning, show no measurable trajectory to extrapolate, so it's not obvious that scaling compute and data closes them (<a href="/blog/2025/agi-misses-continual-learning/">more here</a>).</d-footnote> Whichever you pick, the belief usually formed over a lifetime, long before anyone watched a transformer solve an olympiad problem.

This is the theory a Bayesian finds least embarrassing: the split lives in the prior. If two people start from different priors, both can update on the same evidence with perfect rationality and land decades apart. Nobody is being unreasonable, they just began in different places.

It's a tidy theory, and it's incomplete. A fixed starting difference explains a one-time gap between two people. It doesn't explain why that gap widens with each release, why watching the same model solve the same benchmark leaves both sides more certain than before. A one-time difference in starting point should, if anything, erode as shared evidence accumulates. Something else is doing the work of keeping the split alive, and widening it.

## Why Rational People Still Diverge

That something is hiding in the update rule itself. Bayesian updating has a simple recursive structure:

$$P_t(H) \propto P_{t-1}(H) \cdot P(E_t \mid H)$$

$H$ is the hypothesis you're tracking, "AGI arrives by year Y," say, and $E_t$ is the evidence that just arrived. The recursive part is easy to miss: $P_{t-1}(H)$, today's prior, is nothing but yesterday's posterior.<d-footnote>For a closer look at this same recursion, worked out for continual learning in neural networks rather than human belief updating, see Section 4.1.2 of my PhD thesis <d-cite key="henning2022phdthesis"></d-cite>.</d-footnote> Whatever you believed after the last piece of evidence is exactly the starting point for reading the next one.

Two ideal Bayesians with a common prior [cannot agree to disagree](https://en.wikipedia.org/wiki/Aumann%27s_agreement_theorem#cite_note-aumann1976-1): once their posteriors are common knowledge, the posteriors must be equal <d-cite key="aumann1976agreeing"></d-cite>. The AI community delivers the common-knowledge half of that setup, evidence and opinions broadcast constantly, yet produces the opposite of convergence. So the natural suspect is the other condition: the priors aren't common. The interesting question is where they differ.

They differ one level up from the timeline question. Evidence about AI capability doesn't bear on "will AGI arrive by year Y" directly. It reaches that question through a lens: a belief about whether the current paradigm generalizes or is doing something closer to sophisticated interpolation. And the lens is where the belief from the last section keeps acting: whether you expect the paradigm to generalize is largely your view of the brain — missing ingredient or wrong architecture — applied to the machines built to match it. Two people holding different lenses can update on the same evidence in opposite directions, without either one reasoning badly <d-cite key="jern2014belief"></d-cite>.

That's one round of evidence. Now let the recursion run. Each release doesn't just move the timeline estimate, it also updates the lens: a result read as the paradigm generalizing strengthens the belief that it generalizes, a result read as clever interpolation strengthens the belief that it's interpolation. And a single benchmark is rarely decisive enough to force either side to revise the lens itself. So the lens tends to deepen round after round, and small early differences compound instead of washing out.<d-footnote>No contradiction with the textbook result that the prior washes out as evidence accumulates (informally, the <a href="https://en.wikipedia.org/wiki/Bernstein%E2%80%93von_Mises_theorem">Bernstein–von Mises theorem</a>): washing out requires evidence that discriminates between the hypotheses. A result that both lenses absorb equally well says almost nothing about which lens is right, so that part of the prior is precisely what the data never correct.</d-footnote>

Isn't this just bias with extra steps? It's certainly what bias looks like. In the classic experiment on belief polarization, subjects on both sides of the death penalty debate read the same mixed pair of studies, and each side rated the study that agreed with them as more convincing than the one that didn't <d-cite key="lord1979biased"></d-cite>. But an honest reasoner behaves the same way. If you're convinced the death penalty doesn't deter crime, then of two conflicting studies, the one claiming it does is more likely the flawed one, and discounting it is your lens at work, not a double standard. Both sides doing exactly that reproduces the experiment's result, and from the updates alone you can't tell the honest reasoner from the motivated one. The claim isn't that the camps are unbiased. It's that no bias is required to produce the pattern.

Watch it happen in real time. When OpenAI's o3 scored 87.5% in a high-compute configuration on the ARC-AGI benchmark in December 2024, the benchmark's own creator, François Chollet, who had spent years arguing that current models don't really generalize, read it through his own lens and called it "a surprising and important step-function increase in AI capabilities" <d-cite key="chollet2024o3"></d-cite>, a rare concession against his own prior. Gary Marcus watched the same score and, through his lens, saw narrow optimization dressed up as reasoning: "I saw zero evidence that o3 could work reliably in open-ended domains" <d-cite key="marcus2024o3"></d-cite>. Same benchmark, same day, same number. The disagreement was never about the number.

What needs explaining isn't that the camps disagree, it's that each release leaves both more certain: most results get read through the lens, move the timeline question in the expected direction, and reinforce the lens for the next release. Most, not all: a strong enough result moves even a committed skeptic, as Chollet's update shows.<d-footnote>Someone whom no result could ever move the wrong way, on the other hand, would be irrational by any standard <d-cite key="jern2014belief"></d-cite>.</d-footnote> But the drift favors the lens. That's not a snapshot. It's a loop.

## Not Even the Same Question

The second mechanism is simpler, and it has nothing to do with how anyone updates their beliefs. "AGI" is not a defined event. People use the same word for fuzzy, subjective concepts, so they may be estimating timelines for different things.<d-footnote>A recent proposal offers a useful way to operationalize AGI through a set of human cognitive abilities <d-cite key="hendrycks2025definition"></d-cite>. But it is one attempt to specify the target, not a settled meaning of the term.</d-footnote>

One person may use “AGI” for a machine that can do what humans do cognitively. Another may use it for broad economic automation, or for a much more radical social transformation. None of these is a settled threshold. Even “most cognitive tasks” leaves open which tasks count, how well the system must perform them, and under what conditions. Like consciousness, AGI names a cluster of intuitions rather than a shared test.

No experiment resolves that definitional step. More evidence can sharpen a forecast once its target is fixed. It cannot tell us what an undefined label should mean.

## Why It Won't Converge

Put the two mechanisms together and the polarization is no mystery. The first doesn't yield to more evidence because the lens absorbs almost every release without strain, whichever direction it points, each result tends to get read in a way that reinforces the lens that read it. The second doesn't yield because there's nothing to settle: more data answers one of two questions more precisely, it never tells you which question deserved to be asked.

Neither mechanism needs anyone to be biased, tribal, or dishonest, and that's exactly what makes the pattern durable: **the same release can deepen both camps' certainty at once, in opposite directions, with both updates perfectly rational.** Convergence, if it's possible at all, needs both fixed: a definition specific enough to pin down what "AGI" actually means, and evidence built to discriminate between the lenses rather than evidence either lens can absorb. Look closely, though, and the second collapses into the first: nobody has said what would count as the paradigm failing to generalize, which makes "generalizes" exactly as undefined as "AGI" is. Until someone fixes that, the next release will do what every release before it did: leave both camps more certain, having watched the same thing happen.

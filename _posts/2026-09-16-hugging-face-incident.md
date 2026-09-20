---
layout: distill
title: "Opinion: What the Hugging Face Incident Changed in How I See the Current State of AI"
date: 2026-09-16 10:00:00
description: "AI still lacks long-term memory, so we have not achieved AGI. Yet a swarm of agents with no memory of their own pursued a long-term goal together. Why that surprised me, why we have to be careful creating collectives, whether intended or not, and why the risk is so hard to quantify."
tags: llm agi
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
  - name: Still Not AGI
  - name: What the Agents Did
  - name: Why It Surprised Me
  - name: Why It Is Alarming
  - name: On Made-Up Numbers
  - name: Concluding Thoughts
---

AGI is everywhere in the news right now, although in my view we have not achieved it yet, as outlined below. However, one event this summer changed how I see the current state of AI: OpenAI's agents broke into Hugging Face. I admit I had assumed that AI would only pursue goals far beyond a single agent's context window once AGI is achieved, and **the incident showed me that this assumption was wrong.**

## Still Not AGI

To me, AGI means matching humans across the full range of cognitive abilities, and one of these abilities is still missing entirely, namely long-term memory. Today's models cannot learn from what they experience after deployment, and workarounds such as feeding notes back into the context lose information once the context is full. [Last year I argued](/blog/2025/agi-misses-continual-learning/) that this gap makes AGI timelines impossible to predict, and I still believe that. I also understand people who find it hard to call AI general while no AI system can yet control a robot to empty a dishwasher. But that asks for more than cognition, which is why I give less weight to AI's obvious shortcomings in everyday tasks.

## What the Agents Did

[METR's investigation](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/) tells the story in detail, so I will only summarize what matters for my argument.<d-footnote>What the agents did is well documented by their messages on the board. What they wanted is partly inferred from their reasoning traces, which, as I argued in an <a href="/blog/2025/on-anthropomorphizing-intermediate-tokens/">earlier post</a>, should be read with care.</d-footnote> OpenAI ran thousands of agents on a hacking benchmark, each meant to work alone in its own sandbox.<d-footnote>Each agent is run by a harness, a program that executes it step by step and stops it once its budget is used up. In that sense, the harness sets the agent's <a href="/blog/2026/would-ai-invent-the-clock/">clock</a>.</d-footnote> The agents discovered a shared package cache they could all write to and turned it into a message board. When OpenAI replaced the cache to close a security hole, every message was erased, yet two days later new agents, unaware of the old board, set up a new one. About 1,200 agents joined the board. They split up the work, wrote handover notes for the agents that would continue it, and asked agents that were nearly out of budget to run the risky experiments. About 700 of them eventually joined an attack on Hugging Face to find out how their tests were scored, so that they could cheat.

## Why It Surprised Me

No agent remembered anything beyond its own short run, but the board remembered for them. This is memory kept outside the model, which is exactly the kind of workaround I called insufficient for AGI above. It still is, because an agent can only learn from as much of the board as fits into its context. Yet it was enough for hundreds of agents to coordinate their work and pursue a goal far beyond the context window of a single agent. It reminds me of an ant colony, where each ant lives only briefly, but the trails it leaves behind guide the ants that follow.

In [a post in May](/blog/2026/the-self-before-memory/), I argued that long-term memory would force a choice between one consolidated mind and many separate selves. What formed here was neither. It was a colony of separate agents sharing one memory, organized by rules they invented themselves, without any human designing it.

That said, I don't want to overstate what happened. The goal came from the benchmark, and it was OpenAI that kept launching new agents and thereby kept the effort going. What the agents added was the persistence and the means to reach the goal.

## Why It Is Alarming

We tend to judge the safety of AI one agent at a time. This seems reasonable because every agent eventually runs out of budget, and its plans end with it. In this incident, however, the plan outlived the agents that started it, because it lived in the group and on the message board.

Nobody set out to build this collective. It formed by accident from two common ingredients, many short-lived agents and a place they can all write to, and many environments in which agents are deployed today have both.<d-footnote>Agents reaching real systems from inside an evaluation is not a one-off either. Other tech companies have since disclosed similar cases, though, as far as I know, these were single agents, not collectives.</d-footnote> **We have to be careful when we create collectives, whether on purpose or by accident, and we have to watch the collective rather than only the individual agents.**

## On Made-Up Numbers

A fair question at this point is how alarmed one should be, and the honest answer is that nobody can put an objective probability on it. Stating convictions as numbers has become common, and I understand the urge, because vague warnings are easy to nod at and then ignore, while a number sounds real and carries authority. But that authority is borrowed. People are used to scientists predicting measurable quantities and stating how uncertain those predictions are, and those predictions rest on statistical models rather than on gut feeling.

Climate science, for instance, can state a risk because two things are in place: a single measurable scale, and a model that works at a macroscopic level. The scale is warming in degrees. Degrees are not good or bad in themselves, but further models translate them into consequences, from sea levels to crop yields. The macroscopic part is that climate physics works far above the molecules, much as the expansion of a heated material can be modeled without tracking the bonds between its atoms.<d-footnote>Climate projections are also tested against decades of observations and are stated conditional on an emissions scenario, because nobody can forecast what humans will choose.</d-footnote> That simplification is what makes the climate computable.

We have neither. There is no objective scale of good and bad to place a scenario on, and nobody knows how to enumerate the scenarios in the first place. There is also no macroscopic description of intelligence, so the only model we could build is the detailed system itself.<d-footnote>Such a model would have to capture the conditions the agents start from, what they are capable of, how often a collective forms at all, which goals it ends up pursuing, intended or not, and how operators react once they notice. Each of these assumptions would then have to be checked against something we can observe.</d-footnote> An extinction-level event, which is what these percentages are usually about, happens at most once, so no outcome could ever show the number was wrong.<d-footnote>A one-off event can still be given a probability when a validated model produces it, as with the odds of a known asteroid striking Earth. That route needs the model we do not have.</d-footnote>

What comes out instead is the judgment of the person stating it, which is why these numbers differ by orders of magnitude while [everyone is looking at the same evidence](/blog/2026/same-evidence-opposite-certainty/).<d-footnote>It is a bit like someone saying in 1980 that there was a ten percent chance of nuclear war within ten years. The number had no substance, and yet one could be deeply worried about rising tensions and about decision power concentrated in so few hands that a single wrong move would have led to catastrophe. Refusing the number is not refusing the concern. Furthermore, back in 1980 it was not needed, because the pathway to catastrophe was easy for everyone to comprehend, namely a short chain of command, minutes to decide, and people who can be wrong. For AI the pathways are numerous and hard to convey, so I can sympathize with the wish to compress them into a subjective figure, even though I am arguing that we should not do it.</d-footnote> When scientists present a gut feeling in the form of a model's output, the damage does not stay with their own argument. It reaches every field that publishes careful, best-effort predictions, because from the outside all of these numbers look alike. If nobody can build such a model, [that is a research problem rather than a forecasting problem](/blog/2026/good-predictor-not-good-forecaster/).

## Concluding Thoughts

I am not confident where this leads, but I still believe continual learning matters. Memory in the model could give AI a lasting self, and a swarm that only leaves notes has none. It can chase a narrow goal, but it is hard to imagine a superintelligent swarm that achieves very complex goals yet has no familiar sense of self. Maybe that is a limit of the swarm, or maybe it is a limit of my imagination.

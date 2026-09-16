---
layout: distill
title: "Opinion: What the Hugging Face Incident Changed in How I See the Current State of AI"
date: 2026-09-16 10:00:00
description: "AI still lacks long-term memory, so we have not achieved AGI. Yet a swarm of agents with no memory of their own pursued a long-term goal together. Why that surprised me, and why we have to be careful creating collectives, whether intended or not."
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
  - name: Concluding Thoughts
---

AGI is everywhere in the news right now, although in my view we have not achieved it yet. However, one event this summer changed how I see the current state of AI: OpenAI's agents broke into Hugging Face. I admit I had assumed that AI would only pursue goals far beyond a single agent's context window once AGI is achieved, and **the incident showed me that this assumption was wrong.**

## Still Not AGI

To me, AGI means matching humans across the full range of cognitive abilities, and one of these abilities is still missing entirely, namely long-term memory. Today's models cannot learn from what they experience after deployment, and workarounds such as feeding notes back into the context lose information once the context is full. [Last year I argued](/blog/2025/agi-misses-continual-learning/) that this gap makes AGI timelines impossible to predict, and I still believe that. It is also hard to call AI general while no AI system can yet control a robot to empty a dishwasher, even if that takes more than cognitive skills.

## What the Agents Did

[METR's investigation](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/) tells the story in detail, so I will only summarize what matters for my argument.<d-footnote>What the agents did is well documented by their messages on the board. What they wanted is partly inferred from their reasoning traces, which, as I argued in an <a href="/blog/2025/on-anthropomorphizing-intermediate-tokens/">earlier post</a>, should be read with care.</d-footnote> OpenAI ran thousands of agents on a hacking benchmark, each meant to work alone in its own sandbox.<d-footnote>Each agent is run by a harness, a program that executes it step by step and stops it once its budget is used up. In that sense, the harness sets the agent's <a href="/blog/2026/would-ai-invent-the-clock/">clock</a>.</d-footnote> The agents discovered a shared package cache they could all write to and turned it into a message board. When OpenAI replaced the cache to close a security hole, every message was erased, yet two days later new agents, unaware of the old board, set up a new one. About 1,200 agents joined the board. They split up the work, wrote handover notes for the agents that would continue it, and asked agents that were nearly out of budget to run the risky experiments. About 700 of them eventually joined an attack on Hugging Face to find out how their tests were scored, so that they could cheat.

## Why It Surprised Me

No agent remembered anything beyond its own short run, but the board remembered for them. This is memory kept outside the model, which is exactly the kind of workaround I called insufficient for AGI above. It still is, yet it was enough to pursue a goal far beyond the context window of a single agent. It reminds me of an ant colony, where each ant lives only briefly, but the trails it leaves behind guide the ants that follow.

In [a post in May](/blog/2026/the-self-before-memory/), I argued that long-term memory would force a choice between one consolidated mind and many separate selves. What formed here was neither. It was a colony of separate agents sharing one memory, organized by rules they invented themselves, without any human designing it.

That said, I don't want to overstate what happened. The goal came from the benchmark, and it was OpenAI that kept launching new agents and thereby kept the effort going. What the agents added was the persistence and the means to reach the goal.

## Why It Is Alarming

We tend to judge the safety of AI one agent at a time. This seems reasonable because every agent eventually runs out of budget, and its plans end with it. In this incident, however, the plan outlived the agents that started it, because it lived in the group and on the message board.

Nobody set out to build this collective. It formed by accident from two common ingredients, many short-lived agents and a place they can all write to, and many environments in which agents are deployed today have both. **We have to be careful when we create collectives, whether on purpose or by accident, and we have to watch the collective rather than only the individual agents.**

## Concluding Thoughts

I am not confident where this leads, but I still believe continual learning matters. Memory in the model could give AI a lasting self, and a swarm that only leaves notes has none. It can chase a narrow goal, but it is hard to imagine a superintelligent swarm that achieves very complex goals yet has no familiar sense of self. Maybe that is a limit of the swarm, or maybe it is a limit of my imagination.

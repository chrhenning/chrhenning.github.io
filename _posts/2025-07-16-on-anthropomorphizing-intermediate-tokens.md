---
layout: distill
title: On Anthropomorphizing Token Traces
date: 2025-07-16 21:12:00
description: My thoughts on the paper 'Stop Anthropomorphizing Intermediate Tokens as Reasoning/Thinking Traces!'
tags: ml
categories: machine-learning
giscus_comments: true
related_posts: false
related_publications: false
citation: false
bibliography: 2025-07-16-anthropomorphizing.bib
featured: true

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: Defining 'Reasoning' and 'Thinking'
  - name: The Limits of Human Introspection
  - name: Machine Psychology - An Alternative View
  - name: Alignment, Interpretability, and Misleading Signals
  - name: A Call for Scientific Rigor
  - name: Concluding Thoughts
---

In this post, I discuss a recent paper, <d-cite key="kambhampati2025stop"></d-cite>, which challenges the habit of **anthropomorphizing intermediate token traces** in large reasoning models (LRMs) — often misleadingly described as "reasoning" or "thinking" traces.

My goal here is not to summarize the paper (it’s worth reading in full), but to **highlight the aspects that resonated most with me** and to **add my own perspective**, particularly my view that **looking inside the cognitive processes of LLMs may be a fundamentally unachievable goal**, and what this means for how we approach **AI interpretability and alignment**.

## Terminology: Reasoning and Thinking

Debates about anthropomorphic terms like _“reasoning”_ or _“consciousness”_ are futile without clear definitions — these words are subjective, overloaded, and often understood differently by each participant. I’ve been part of countless unproductive discussions that boiled down to mismatched interpretations of these terms.

Standard definitions of [thinking](https://en.wikipedia.org/wiki/Thought) and [reasoning](https://en.wikipedia.org/wiki/Reason) remain vague. Broadly speaking, thinking is considered an umbrella concept encompassing both intuitive and deliberate mental processes, whereas reasoning refers more narrowly to structured, logical inference.

The paper briefly references Daniel Kahneman’s book [Thinking, Fast and Slow](https://en.wikipedia.org/wiki/Thinking,_Fast_and_Slow), which distinguishes between _System 1_ (fast, automatic, heuristic-driven) and _System 2_ (slow, effortful, and logical) thinking.

To my knowledge, cognitive science and psychology offer no universally accepted definitions of these concepts. I therefore adopt the System 1 vs. System 2 framework as an intuitive guide, assuming that LLMs already excel at System 1-like capabilities (fast pattern-matching and intuition), whereas LRMs aim to extend them with System 2-style reasoning abilities.

Unlike System 1-like pattern recognition, System 2-style reasoning requires structured planning, multi-step inference, and symbolic abstraction. **The problem: current attempts to achieve System 2 capabilities often focus on distilling human-like thought processes into LLMs via reasoning chains encoded in natural language.**

## Can We Express Thoughts in Natural Language?

This raises an immediate question: how can we reliably retrieve reasoning chains from humans themselves? To do so, we would need humans to recall and verbalize their thought processes in natural language. However, as noted by Kambhampati et al., the well-known paper _"Telling More Than We Can Know: Verbal Reports on Mental Processes"_ <d-cite key="nisbett1977telling"></d-cite> challenges the belief that humans can accurately do this.

The term [introspection illusion](https://en.wikipedia.org/wiki/Introspection_illusion) refers to the _"cognitive bias in which people wrongly think they have direct insight into the origins of their mental states"_. Because we often lack conscious access to higher-order mental processes, our explanations for why we think or act in certain ways are frequently constructed post hoc — relying on confabulated causal theories rather than genuine insight.

In short, **when people explain their own thoughts, they are often confabulating — constructing plausible narratives rather than reporting true internal processes.**

This raises two fundamental concerns. First, how realistic is it to expect that we can endow LLMs with System 2-like reasoning simply by distilling human-generated reasoning traces? Second, if humans themselves struggle to reliably articulate their own thought processes, how meaningful is it to treat LLM-generated reasoning traces, expressed in natural language, as evidence of any true cognition within this black box?

## Machine Psychology: Looking Inside a Model's Cognition

In my view, Kambhampati et al. highlight two **key fallacies** (cf. Sec. 3 in the paper):

1. **The drive to make reasoning traces interpretable**<d-footnote>The paper gives the example of DeepSeek’s transition from R1-Zero to R1 <d-cite key="guo2025deepseek"></d-cite>, where the push for improved language consistency actually harmed final model performance.</d-footnote>.
2. **The implicit assumption that these reasoning traces are causally connected to the model’s final output**.

Both fallacies stem from a persistent desire to "look inside" a model’s internal cognition, i.e., to treat its outputs as windows into an internal thought process. In this context, I find the analogy proposed by Hagendorff et al. in the paper _"Machine Psychology"_<d-cite key="hagendorff2023machine"></d-cite> especially powerful.

Most people easily recognize the abstract analogy that connects biological and artificial neural networks. But Hagendorff et al. argue that this analogy also applies to how these systems are studied.

Historically, human cognition has been studied along two orthogonal lines: neuroscience, which aims to understand the biological mechanisms, and psychology, which focuses on external behavior. The paper argues for a similar split when studying artificial systems:

- _Neuroscience &harr; Mechanistic Interpretability_ (dissecting the network’s structure and activations)
- _Psychology &harr; Machine Psychology_ (observing the model’s behavior through experiments).

The analogy to machine psychology highlights why looking into a model’s "mind" is both difficult — and perhaps fundamentally misguided.

**Machine psychology suggests we treat LLMs as opaque but testable subjects — design experiments, observe behaviors, and infer capabilities, rather than pretending we can read their minds through token streams.**

As noted in the previous section, human introspective reports are often post hoc narratives, constructed after the fact. LLMs trained to produce reasoning traces do the same. They learn how to talk about reasoning, not how to reason.

Mistaking surface-level explanations for true cognition risks giving us a false sense of alignment.

## Implications for Alignment and Interpretability

The paper by Kambhampati et al. helped shape my view that chain-of-thoughts (CoTs), while human-readable, should not be treated as reliable explanations of how a model arrives at its outputs. This implies they cannot be relied upon for (1) behavior auditing or (2) ensuring model honesty.

**CoTs are not ground-truth indicators of a model’s internal cognition.**

Yet, these illusions are easy to fall for, even within the scientific community, and they have implications for both AI alignment research and public discourse.

For example, a recent paper by Apollo Research on scheming <d-cite key="apolloresearch2024frontier"></d-cite> treats CoT content as primary evidence of deceptive behavior. But if CoTs are not causally tied to a model’s underlying "intent" (if such a concept even applies), the conclusions of such studies may be overreaching.

If even AI researchers and practitioners fall into this trap, how can we expect public figures or media outlets to avoid it?

The historian and writer Yuval Noah Harari, in a [recent discussion](https://www.youtube.com/watch?v=0BnZMeFtoAM&t=262s), remarked when speaking about CoTs: "we can see how the sentences and stories are formed in \[the AI's minds\]".
This phrasing — while understandable — reinforces the notion that we can see the actual thought process happening inside the language models.

This confusion over CoTs risks derailing conversations about alignment and interpretability, as it risks diverting attention toward misleading signals rather than genuine indicators of model behavior.

## A Call for Scientific Rigour and Integrity

This paper can also be seen as a reminder that **scientific rigour and intellectual integrity are essential for genuine progress**. This doesn’t imply that researchers are consciously deceiving anyone — but rather that it’s easy to mislead ourselves when dealing with vague concepts and opaque systems. I admit the fallacies highlighted in the paper were not obvious to me before I read it. Yet without critical reflection, we risk unintentionally heading in the wrong direction.

This tendency is not new in the field of AI. As Kambhampati et al. note, McDermott (1976)<d-cite key="mcdermott1976artificial"></d-cite> argued nearly fifty years ago that AI researchers often delude themselves and others by using on misleading language, poorly defined abstractions, and wishful thinking instead of rigorous analysis and empirical clarity.<d-footnote>It is amusing to note that McDermott’s paper ends with the line: "I have criticized AI researchers very harshly. &#91;...&#93; However, to say anything good about anyone is beyond the scope of this paper."</d-footnote>

The authors also reference Richard Feynman’s famous notion of “Cargo Cult Science,” from his [1974 commencement address at Caltech](https://calteches.library.caltech.edu/51/2/CargoCult.htm). Feynman’s warning about adopting the rituals of science without its spirit of honesty and self-skepticism feels particularly relevant today. When our models grow increasingly complex and their inner workings opaque, it is all too easy to substitute the appearance of understanding for actual insight.

To avoid repeating past mistakes, we need to adopt Feynman’s kind of honesty: a willingness to state clearly what we don’t know, to avoid anthropomorphic shortcuts, and to test claims empirically rather than leaning on appealing narratives.

## Concluding Thoughts

One important fact is that **CoTs do improve performance on certain tasks**. However, as Kambhampati et al. argue (and as several studies cited in the paper suggest), it is **far more plausible that this improvement is simply a side effect of the additional computation afforded by longer prompts**, rather than evidence that human-like thought processes have been "distilled" into the model.

Section 6 of the paper offers two insights worth highlighting. First, CoTs are just one form of **prompt augmentation** — essentially, a way of extending the prompt to give the model more "compute in time."
Second, drawing on Marvin Minsky’s observation that "intelligence is shifting the test part of generate-test into generation", the paper frames LLMs as generators of candidate solutions that are then evaluated by a verifier. The naive (and brute-force) strategy is to produce many solutions and let the verifier do all the work. A more intelligent approach, however, would be for the LLM itself to generate a much narrower, high-quality set of candidate solutions. Achieving this shift is a central motivation behind the development of large reasoning models (LRMs).

Looking ahead, there are many promising directions for future work. Personally, I find approaches like Chain of Continuous Thought <d-cite key="hao2024training"></d-cite> particularly compelling. This line of research avoids the deceptive desire for anthropomorphic "insights" and instead focuses on equipping LLMs with mechanisms to transfer dense, structured information via tokens — something that seems difficult, if not impossible, to achieve with plain language tokens sampled from the vocabulary.<d-footnote>It is, however, interesting to note that this referenced approach currently seems to heavily rely on a curriculum to move from human-generated CoTs to continuous CoTs.</d-footnote>

Ultimately, the value of CoTs may lie less in what they reveal about "how models think", and more in how they can be leveraged as tools to shape and constrain behavior — while keeping our expectations grounded in scientific rigor rather than anthropomorphic metaphors.

\*_This post has also been published on [Medium](https://medium.com/@chrhenning91/on-anthropomorphizing-token-traces-3e60026c41c4)._

---
layout: distill
title: The Bayesian Story Behind Prior-Fitted Networks
date: 2026-03-22 20:15:00
description: PFNs are often described as Bayesian predictors, but their training objective and inference mechanism suggest a more nuanced interpretation.
tags: ml
categories: machine-learning
giscus_comments: true
related_posts: true
related_publications: false
citation: false
bibliography: 2026-03-22-the-bayesian-story-of-pfns.bib

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: Introduction
  - name: Prior-Fitted Networks
  - name: The Bayesian Interpretation
  - name: How Bayesian Is It?
  - name: A Simple Illustration
  - name: Learning, Compression, and the Bayesian Brain
  - name: Concluding Remarks
---

## Introduction

Bayesian inference provides one of the most principled approaches to learning from data. By maintaining a distribution over plausible hypotheses and updating this distribution as evidence accumulates, Bayesian methods naturally capture **epistemic uncertainty** arising from limited data. Predictions are obtained by averaging over hypotheses according to their posterior probability.

In practice, however, exact Bayesian inference is often computationally expensive. This challenge has motivated a range of approximate methods, from variational inference to Monte Carlo techniques. A particularly intriguing recent idea is that **inference itself can be learned**. Rather than performing Bayesian inference for every new dataset, one can train a neural network to approximate the resulting predictions directly.

This idea is realised by **prior-fitted networks (PFNs)** <d-cite key="muller2021transformers"></d-cite>. These models achieve remarkable performance on small-data tasks and can produce well-calibrated predictive distributions with a single forward pass. At the same time, their success raises interesting conceptual questions about what exactly remains of the Bayesian framework once inference has been amortised.

## Prior-Fitted Networks

The starting point of Bayesian prediction is a **hypothesis space** $\mathcal{H}$ together with a prior distribution $p(h)$ over hypotheses $h \in \mathcal{H}$. Given a dataset $d$, Bayesian inference produces the posterior distribution

$$
p(h \mid d).
$$

Predictions for a new input $x$ are obtained through **Bayesian model averaging**

$$
p(y \mid d,x)
=
\mathbb{E}_{h \sim p(h \mid d)}
\big[
p(y \mid h,x)
\big].
$$

Computing this posterior predictive distribution typically requires integrating over the hypothesis space, which can be challenging in complex models.

Prior-fitted networks take a different approach. Instead of performing inference at test time, they **learn to approximate the posterior predictive distribution directly**.

Training proceeds by sampling synthetic tasks from the assumed prior. Concretely, a hypothesis $h \sim p(h)$ is first drawn from the prior. Inputs $x$ are then sampled from a predefined input domain, and the corresponding outputs $y$ are generated according to the predictive model $p(y \mid h,x)$. Repeating this process yields many datasets $d$ together with query inputs $x$ and targets $y$.

The network is trained to predict these targets from the observed dataset and query input, thereby learning a mapping

$$
f_\theta(d,x) \approx p(y \mid d,x).
$$

A key theoretical result of <d-cite key="muller2021transformers"></d-cite> (Corollary 1.1) shows that this training procedure minimises the expected KL divergence

$$
\mathbb{E}_{d,x}
\left[
\mathrm{KL}
\big(
p(\cdot \mid d,x)
\;\|\;
q_\theta(\cdot \mid d,x)
\big)
\right],
$$

where the expectation is taken over datasets $d$ generated from the prior. In other words, the network is trained to approximate the **posterior predictive distribution** on the distribution of datasets induced by the prior.

This idea is both elegant and powerful. Once trained, a PFN can produce predictions for a new dataset with a single forward pass, effectively amortising the cost of inference across many tasks. In practice, this approach has shown impressive performance on small-to-medium tabular datasets, as demonstrated by **TabPFN** <d-cite key="hollmann2025accurate"></d-cite>.

## The Bayesian Interpretation

Because PFNs are trained to approximate the posterior predictive distribution, they are sometimes described as **Bayesian predictors**. This description captures an important aspect of the method: the training objective explicitly encourages the network to reproduce Bayesian predictions.

However, it is important to distinguish between **approximating Bayesian predictions** and **performing Bayesian inference**.

In a classical Bayesian model, predictions arise from explicitly averaging over hypotheses

$$
p(y \mid d,x)
=
\int_{\mathcal{H}}
p(y \mid h,x)\, p(h \mid d)\, dh.
$$

The posterior distribution $p(h \mid d)$ is central to this process. It allows us to sample hypotheses and interpret predictive uncertainty in terms of disagreement between plausible explanations of the observed data.

A prior-fitted network, in contrast, does not maintain such a distribution. Instead, predictions are produced by a deterministic function

$$
f_\theta(d,x).
$$

The Bayesian model average is therefore no longer part of the inference procedure itself; it has effectively been **compiled into the network parameters** during training.

From this perspective, PFNs can be viewed as performing **supervised learning on a meta-learning objective**. The training data consists of many synthetic datasets generated from the prior, and the network learns to predict the corresponding targets. Maximum likelihood estimation can in turn be interpreted as minimising the KL divergence between the model's predictive distribution and the ground-truth conditional distribution. I discuss this connection in more detail in [a recent blog post](/blog/2025/when-mse-loss-leads-to-mis-steering/).

The impressive empirical performance of PFNs therefore reflects the ability of neural networks to generalise across tasks drawn from the prior distribution.

## How Bayesian Is It?

The previous section made a structural point: PFNs reproduce Bayesian predictions on average across tasks, but the inference itself is compiled into the network parameters rather than performed explicitly. This leaves open a sharper question. In what sense does the procedure that the network actually implements deserve the Bayesian label? It helps to separate three senses of the word: _reproducing_ Bayesian predictions, _implementing_ Bayesian inference as an explicit procedure, and _admitting_ a Bayesian interpretation at the level of behaviour. The previous section established that PFNs do the first but not the second. It is the third sense that the rest of this section probes, and several distinct issues make it hard to settle.

### The Bernstein–von Mises limit

The first complication is asymptotic. Under regularity conditions, the **Bernstein–von Mises theorem** states that, as the dataset grows, the posterior $p(h \mid d)$ becomes approximately Gaussian and concentrates around the maximum likelihood estimate. In this regime, Bayesian model averaging collapses toward a point estimate, predictive uncertainty is governed by the local curvature of the likelihood, and the influence of the prior on predictions fades.

Methodologically, this is convenient. Interpretively, it is somewhat uncomfortable: a wide range of procedures, Bayesian and non-Bayesian alike, become indistinguishable in their predictions. Calling any one of them "Bayesian" tells us little about the underlying mechanism.

PFNs are evaluated in _small-data_ settings, where this asymptotic equivalence has not yet kicked in. That is the regime in which the Bayesian label is most informative, and also the regime in which it is hardest to verify.

### Outside that limit, behaviour is shaped by prior and likelihood

Once we leave the asymptotic regime, Bayesian predictions become visibly sensitive to the chosen prior and likelihood. I discussed this in detail in [an earlier post](/blog/2026/uncertainty-decomposition/): epistemic uncertainty is only meaningful relative to a prior, and likelihood misspecification can silently corrupt the posterior.

In the classical Bayesian setup, the prior $p(h)$ is explicit and feeds directly into the posterior. A PFN sees no such prior. The network is exposed only to datasets sampled from the marginal data distribution induced by the prior and the predictive model. Different combinations of prior and likelihood can induce indistinguishable distributions over observed datasets; the network, in turn, is free to learn any mapping that reproduces the induced input-output statistics.

The learned object is therefore a conditional distribution over outputs given a dataset, not a posterior over hypotheses. Calling it Bayesian relies on knowing which prior generated the training data: that connection is supplied by the modeller, not enforced by the training procedure.

### Bayesian guarantees on in-context learning assume exact inference

A different angle on the question comes from recent work analysing in-context learning through Bayesian formalism <d-cite key="falck2024bayesian"></d-cite><d-cite key="muller2025position"></d-cite>. Two properties of true Bayesian predictors feature centrally in this line of work. First, predictions form a **martingale** as data accumulates: the current prediction is the conditional expectation of all future ones, so they fluctuate around it without systematic directional drift. Second, under exchangeability of the data, the order in which observations arrive does not affect the limiting prediction.

These results are best read as _characterisations_. They describe what an exact Bayesian system must look like, not whether a given learned model in fact behaves that way. The training objective of a PFN is multi-task supervised learning; nothing in it enforces these properties.

The continual learning literature offers a concrete illustration of how easily such properties can break.

<div class="row mt-3 justify-content-center">
    <div class="col-md-4 col-sm-4 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/prior-fitted/pfcl_ordering1.png" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-md-4 col-sm-4 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/prior-fitted/pfcl_ordering2.png" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-md-4 col-sm-4 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/prior-fitted/pfcl_ordering3.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
  Adapted from Fig. 4.3 in <d-cite key="henning2022phdthesis"></d-cite>. Two tasks (orange and green) are learned sequentially with a prior-focused continual learning method, in which the approximate posterior obtained after the first task plays the role of the prior for the second. <b>Left:</b> The orange task is observed first; the approximate posterior $q_{\theta^{(1)}}$ concentrates on a region that is also compatible with the green task. <b>Middle:</b> Continuing with the green task yields a joint approximate posterior $q_{\theta^{(1:2)}}$ that solves both tasks. <b>Right:</b> Reversing the order, green first, leads to an approximate posterior $q_{\theta^{(1)}}$ located in a region that has no overlap with the orange task. Along this trajectory, the orange task becomes unreachable. The order of observations changes the admissible solution set, illustrating how path-independence can fail once Bayesian inference is only approximated.
</div>

PFNs, in turn, are not explicitly Bayesian by construction. It is therefore not obvious that they should satisfy properties that even careful Bayesian approximations fail to satisfy.

## A Simple Illustration

The distinction becomes visible when comparing PFN predictions to the true posterior predictive distribution outside the training regime.

The figure below shows the result of a simple experiment based on a Gaussian process prior. A PFN is trained on datasets sampled from this prior and then compared to the analytic posterior predictive distribution.

<div class="row mt-3 justify-content-center">
    <div class="col-md-10 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/prior-fitted/pfn_gp_experiment.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
  Comparison between the posterior predictive distribution of a Gaussian process and the predictions of a prior-fitted network trained on datasets sampled from the same prior. In the region where training data typically occur, both models agree closely. Outside this region, the predictive distributions begin to diverge.
</div>

Within the training regime the PFN closely matches the Bayesian posterior predictive. Outside it, the two diverge: the Gaussian process posterior continues to reflect the prior and kernel assumptions, whereas the PFN falls back on the inductive biases of its architecture. This is expected: during training, inputs are drawn only from a specific domain, so the network never receives direct signal about prior-induced behaviour beyond it.

## Learning, Compression, and the Bayesian Brain

The PFN is trained to minimise the cross-entropy between its predictions and targets drawn from the prior-induced data distribution. Cross-entropy is expected code length, so the same objective can equally be read as compression: the network is pressured to compress many inference problems into a single forward pass. Its optimum is already known. The result quoted earlier (Corollary 1.1) says the objective is minimised exactly when the network reproduces the Bayesian posterior predictive. On the training distribution, then, compressing the data well and matching the Bayesian posterior predictive are the same thing.

Crucially, this is a statement about outputs, not about mechanism. The objective scores only what the network predicts, so any internal procedure producing those predictions is equally optimal under it. Compression pressure forces the network to settle on _some_ algorithm for turning a dataset into predictions, but cannot single out which one. That algorithm might be a form of approximate Bayesian inference, or something else entirely; from the predictions alone we can neither tell which, nor recover the prior and likelihood it would correspond to. This is structurally the same situation as the long-standing **Bayesian brain hypothesis** debate <d-cite key="knill2004bayesian"></d-cite>: cortical computation is often modelled as approximate Bayesian inference, yet whether the brain actually implements anything that deserves the description remains actively contested <d-cite key="bowers2012bayesian"></d-cite><d-cite key="jones2011bayesian"></d-cite>.

## Concluding Remarks

Prior-fitted networks provide a fascinating example of how **inference itself can be learned**. By training on large numbers of synthetic datasets, they effectively amortise Bayesian prediction and enable fast, single-pass inference on new problems.

The training objective encourages the network to reproduce Bayesian predictions on average across tasks, but it does not enforce the properties (exact posterior averaging, path-independence, prior-driven extrapolation) we usually associate with the Bayesian label. Whether the learned procedure is well described in Bayesian terms depends on the regime in which we evaluate it, and matters most precisely where PFNs are most useful: in the small-data regimes where the prior would otherwise dominate.

PFNs are perhaps best understood as **amortised approximations of Bayesian predictors**. Their behaviour can closely resemble Bayesian inference within the training distribution, but the strength of this resemblance ultimately depends on how well the learned mapping generalises beyond the tasks seen during training.

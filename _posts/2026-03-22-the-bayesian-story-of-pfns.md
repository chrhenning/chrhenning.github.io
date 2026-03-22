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
  - name: A Simple Illustration
  - name: Concluding Remarks
---

## Introduction

Bayesian inference provides one of the most principled approaches to learning from data. By maintaining a distribution over plausible hypotheses and updating this distribution as evidence accumulates, Bayesian methods naturally capture **epistemic uncertainty** arising from limited data. Predictions are obtained by averaging over hypotheses according to their posterior probability.

In practice, however, exact Bayesian inference is often computationally expensive. This challenge has motivated a range of approximate methods, from variational inference to Monte Carlo techniques. A particularly intriguing recent idea is that **inference itself can be learned**. Rather than performing Bayesian inference for every new dataset, one can train a neural network to approximate the resulting predictions directly.

This idea is realized by **prior-fitted networks (PFNs)** <d-cite key="muller2021transformers"></d-cite>. These models achieve remarkable performance on small-data tasks and can produce well-calibrated predictive distributions with a single forward pass. At the same time, their success raises interesting conceptual questions about what exactly remains of the Bayesian framework once inference has been amortised.

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

A key theoretical result of <d-cite key="muller2021transformers"></d-cite> (Corollary 1.1) shows that this training procedure minimizes the expected KL divergence

$$
\mathbb{E}_{d,x}
\left[
\mathrm{KL}
\big(
p(\cdot \mid x,d)
\;\|\;
q_\theta(\cdot \mid x,d)
\big)
\right],
$$

where the expectation is taken over datasets $d$ generated from the prior. In other words, the network is trained to approximate the **posterior predictive distribution** on the distribution of datasets induced by the prior.

This idea is both elegant and powerful. Once trained, a PFN can produce predictions for a new dataset with a single forward pass, effectively amortising the cost of inference across many tasks. In practice, this approach has shown impressive performance on small tabular datasets, as demonstrated by **TabPFN** <d-cite key="hollmann2025accurate"></d-cite>.

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

From this perspective, PFNs can be viewed as performing **supervised learning on a meta-learning objective**. The training data consists of many synthetic datasets generated from the prior, and the network learns to predict the corresponding targets. This objective closely resembles standard supervised learning. In particular, maximum likelihood estimation can be interpreted as minimizing the KL divergence between the model's predictive distribution and the ground-truth conditional distribution. I discuss this connection in more detail in [a recent blog post](/blog/2025/when-mse-loss-leads-to-mis-steering/).

The impressive empirical performance of PFNs therefore reflects the ability of neural networks to generalize across tasks drawn from the prior distribution.

## A Simple Illustration

The distinction becomes visible when comparing PFN predictions to the true posterior predictive distribution outside the training regime.

The figure below shows the result of a simple experiment based on a Gaussian process prior. A PFN is trained on datasets sampled from this prior and then compared to the analytic posterior predictive distribution.

<div class="row mt-3 justify-content-center">
    <div class="col-md-10 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/pfn_gp_experiment.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
  Comparison between the posterior predictive distribution of a Gaussian process and the predictions of a prior-fitted network trained on datasets sampled from the same prior. In the region where training data typically occur, both models agree closely. Outside this region, the predictive distributions begin to diverge.
</div>

Within the training regime the PFN closely matches the Bayesian posterior predictive. Outside it, the two diverge: the Gaussian process posterior continues to reflect the prior and kernel assumptions, whereas the PFN falls back on the inductive biases of its architecture. This is expected - during training, inputs are drawn only from a specific domain, so the network never receives direct signal about prior-induced behaviour beyond it.

## Concluding Remarks

Prior-fitted networks provide a fascinating example of how **inference itself can be learned**. By training on large numbers of synthetic datasets, they effectively amortise Bayesian prediction and enable fast, single-pass inference on new problems.

At the same time, it is worth keeping in mind what exactly the network has learned. A PFN does not perform Bayesian inference in the classical sense; instead, it approximates the outcome of Bayesian prediction through supervised learning across tasks.

In that sense, PFNs are best understood as **amortized approximations of Bayesian predictors**. Their behaviour can closely resemble Bayesian inference within the training distribution, but this resemblance ultimately depends on how well the learned mapping generalizes beyond the tasks seen during training.

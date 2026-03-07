---
layout: distill
title: Why Uncertainty in Machine Learning Is Conceptually Broken
date: 2026-03-07 11:15:00
description: A critique of why modern ML uncertainty estimates lack clear semantics, reliable evaluation, and meaningful use cases.
tags: ml
categories: machine-learning
giscus_comments: true
related_posts: true
related_publications: false
citation: false
bibliography: 2026-03-07-uncertainty-decomposition.bib

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog
---

Uncertainty estimation is often framed as the key to building reliable machine learning systems. Central to this narrative is the distinction between **aleatoric** and **epistemic** uncertainty. In this post, I argue that the commonly used **information-theoretic decomposition of predictive uncertainty does not generally correspond to these concepts** and often reflects modelling assumptions rather than properties of the data-generating process.

## Introduction

Uncertainty estimation has become one of the central themes in modern machine learning. The promise is appealing: if models can quantify what they know and what they do not know, we should be able to build systems that behave safely in the presence of noise, detect unfamiliar inputs, and actively acquire new knowledge.

The conceptual foundation of this promise is the widely used distinction between [aleatoric and epistemic uncertainty](https://en.wikipedia.org/wiki/Uncertainty_quantification#Aleatoric_and_epistemic). Aleatoric uncertainty is typically described as the irreducible randomness of the data-generating process, while epistemic uncertainty reflects gaps in the model's knowledge that could in principle be reduced with more data. In theory, separating these two sources of uncertainty would allow us to reason about noisy environments and model ignorance in a principled way.

In practice, however, the situation is far less clear. Most uncertainty measures used in machine learning are derived from properties of a specific probabilistic model rather than from the true data-generating process. As a result, quantities that are often interpreted as intrinsic properties of the world are in fact shaped by modelling assumptions such as the chosen likelihood function, hypothesis class, and prior. This mismatch becomes particularly visible when we attempt to evaluate uncertainty estimates: instead of directly measuring their quality, we typically rely on complex surrogate tasks such as [active learning](<https://en.wikipedia.org/wiki/Active_learning_(machine_learning)>) or out-of-distribution detection. But these tasks depend on many factors beyond uncertainty itself, making them unreliable indicators of whether our uncertainty estimates are actually meaningful. As discussed in my earlier work on OOD detection <d-cite key="dangelo:henning:2021:uncertainty:based:ood"></d-cite>, the connection between uncertainty estimates and downstream tasks is subtle and often misunderstood.

This conceptual ambiguity becomes especially problematic when considering one of the most popular tools in the uncertainty literature: the information-theoretic decomposition of predictive uncertainty into aleatoric and epistemic components. While this decomposition is frequently interpreted as revealing two fundamental sources of uncertainty in the data, it is in fact derived entirely from the structure of the model. Consequently, it does not generally provide a clean separation between intrinsic data noise and model ignorance.

In this post, I argue that this distinction — though intuitively appealing — is often misinterpreted in modern machine learning. By examining how uncertainty estimates depend on modelling assumptions, we will see why the commonly used decomposition can be misleading, why epistemic uncertainty is fundamentally tied to the choice of prior, and why extracting meaningful uncertainty becomes particularly difficult in amortised inference systems such as modern neural networks.

## Decomposing Predictive Uncertainty

> For a proper introduction to Bayesian statistics in the context of machine learning, see Chapters 2 and 3 of my thesis: <d-cite key="henning2022phdthesis"></d-cite>.

Consider a probabilistic model parameterized by $\theta$ that maps inputs $x$ to outputs $y$. We denote a dataset of input–output pairs by $d$. In a Bayesian setting, the model parameters are treated as random variables and updated after observing data. Accordingly, we consider the random variables $D$, $Y$, and $\Theta$ corresponding to the dataset, predictions, and model parameters.

Given an observed dataset $d$, the **posterior predictive distribution** is defined as

$$
\begin{equation}
p(y \mid d,x) = \mathbb{E}_{\theta \sim p(\theta \mid d)}
\left[
p(y \mid \theta,x)
\right]
\end{equation}
$$

where $p(\theta \mid d)$ denotes the posterior distribution over model parameters.

{% details Mutual information as reduction in predictive entropy %}
[Mutual information](https://en.wikipedia.org/wiki/Mutual_information) measures the statistical dependence between two random variables. It can be expressed in terms of entropies as

$$
\begin{align}
I(Y;\Theta)
&= \mathrm{KL}\!\left(
p(y,\theta)\;\middle\|\; p(y)\,p(\theta)
\right) \\
&= -H(Y \mid \Theta) + H(Y).
\end{align}
$$

Intuitively, mutual information quantifies how much knowing one variable reduces the uncertainty about the other.
{% enddetails %}

It is useful to consider the **mutual information** between predictions $Y$ and parameters $\Theta$ given the observed dataset $d$ and input $x$. This quantity can be written as

$$
\begin{align}
I(Y;\Theta \mid d,x)
&= \mathrm{KL}\!\left(
p(\theta \mid d)\, p(y \mid \theta,x)
\;\middle\|\;
p(\theta \mid d)\, p(y \mid d,x)
\right) \\
&= \mathbb{E}_{\theta \sim p(\theta \mid d)}
\left[
\mathrm{KL}\!\left(
p(y \mid \theta,x)
\;\middle\|\;
p(y \mid d,x)
\right)
\right].
\end{align}
$$

This expression shows that the mutual information can be interpreted as the **expected divergence between the predictive distribution of an individual hypothesis and the posterior predictive distribution**. In other words, it measures how much individual models sampled from the posterior disagree with the overall predictive distribution. For this reason, it is often used as a quantitative measure of epistemic uncertainty (see Section 3.4 of my PhD thesis <d-cite key="henning2022phdthesis"></d-cite>).

Using standard identities from information theory, we can derive a decomposition of the predictive entropy that relates it to this mutual information term. A decomposition of this form was promoted, for instance, by <d-cite key="depeweg2018decomposition"></d-cite>.

Under the assumed generative model, the prediction $Y$ is conditionally independent of the dataset $D$ given the model parameters $\Theta$. Therefore,

$$
\begin{align}
H(Y \mid \Theta, D=d, x) &=
- \mathbb{E}_{\theta, y \sim p(\theta \mid d)\, p(y \mid \theta,x)} \big[ \log \frac{p(\theta \mid d)\, p(y \mid \theta,x)}{p(\theta \mid d)} \big] \\
&= \mathbb{E}_{\theta \sim p(\theta \mid d)} \big[ H(Y \mid \theta,x) \big].
\end{align}
$$

Using the standard identity

$$
\begin{align}
H(Y \mid D=d,x)
&= H(Y \mid \Theta, D=d,x)
  + I(Y;\Theta \mid D=d,x),
\end{align}
$$

we obtain the following decomposition of the predictive entropy:

$$
\begin{align}
\underbrace{
H(Y \mid D=d,x)
}_{\text{entropy of predictive posterior}}
&=
\underbrace{
\mathbb{E}_{\theta \sim p(\theta \mid d)}
\big[ H(Y \mid \theta,x) \big]
}_{\text{often claimed to be aleatoric uncertainty}}
+
\underbrace{
I(Y;\Theta \mid D=d,x)
}_{\text{epistemic uncertainty}}.
\end{align}
$$

This identity is frequently interpreted as decomposing predictive uncertainty into aleatoric and epistemic components. In the next section, we will examine this interpretation more carefully and argue that the first term does not generally correspond to true aleatoric uncertainty.

## Why the Expected Entropy Is Not Aleatoric Uncertainty

The decomposition above is mathematically correct. However, interpreting the first term as **aleatoric uncertainty** is generally problematic.<d-footnote>This issue has been discussed previously, e.g., by <d-cite key="wimmer2023quantifying"></d-cite>.</d-footnote>

To see why, recall that aleatoric uncertainty is a property of the **data-generating process**, i.e., the entropy of the true conditional distribution ($p^*(y \mid x)$). In contrast, the quantity

$$
\begin{equation}
\mathbb{E}_{\theta \sim p(\theta \mid d)}
\big[ H(Y \mid \theta,x) \big]
\end{equation}
$$

depends entirely on the predictive distributions produced by the model. It therefore reflects how uncertain **individual hypotheses** are under the current posterior, rather than a property of the underlying data distribution.

In a very specific limit, the two can coincide. If the model is correctly specified and the amount of data grows without bound, the posterior ($p(\theta \mid d)$) collapses onto the true parameters. In this case the predictive model recovers the true data-generating distribution, and the expected entropy indeed corresponds to the aleatoric uncertainty.

In practice, however, we rarely operate in this limit. Models are almost always **misspecified**, meaning that no parameter setting exactly represents the true data-generating process. In such cases, the uncertainty produced by the likelihood model reflects modelling choices rather than intrinsic noise in the data (see also my earlier discussion of this issue in the context of regression losses [my recent blog post](/blog/2025/when-mse-loss-leads-to-mis-steering/)). As a result, the expected entropy term cannot generally be interpreted as a measure of aleatoric uncertainty.

The decomposition therefore separates **disagreement between models** from **uncertainty within individual models**, but this should not be mistaken for a clean decomposition of predictive uncertainty into epistemic and aleatoric components of the data-generating process.

## Concluding Remarks

The decomposition of predictive entropy into expected entropy and mutual information is a valid information-theoretic identity. However, interpreting this identity as a principled decomposition of predictive uncertainty into **aleatoric** and **epistemic** components is generally misleading. The quantities involved are defined purely in terms of the model's predictive distributions and therefore do not directly correspond to properties of the underlying data-generating process.

Conceptually, it is helpful to keep in mind that **aleatoric uncertainty is a property of the data**, while **epistemic uncertainty reflects limitations of our knowledge and modelling assumptions**. While certain limiting cases — such as correctly specified models with infinite data — can align these notions with the information-theoretic decomposition, such conditions rarely hold in practice.

I hope this short discussion helps create a bit of **conceptual clarity** around the interpretation of uncertainty decompositions in machine learning.

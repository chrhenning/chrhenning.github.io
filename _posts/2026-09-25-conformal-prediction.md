---
layout: distill
title: "Uncertainty Is Not Distribution-Free: Why Conformal Prediction Only Knows What Your Model Knows"
date: 2026-09-25 10:00:00
description: Conformal prediction guarantees coverage, but coverage can be exactly right and still uninformative, like accuracy on an imbalanced dataset. The sets only surface the uncertainty a model already has, so the real work is still in the model.
tags: uncertainty statistics
categories: machine-learning
og_image: https://chrhenning.com/assets/img/posts/conformal-prediction/misfit.png
giscus_comments: true
related_posts: true
related_publications: false
citation: false
bibliography: 2026-09-25-conformal-prediction.bib
thumbnail: assets/img/posts/conformal-prediction/lane-split-thumb.jpg

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: How Conformal Prediction Works
  - name: A Wrapper Cannot Fix the Model
  - name: Where It Goes Wrong
  - name: What It Is Good For
---

[Split conformal prediction](https://en.wikipedia.org/wiki/Conformal_prediction) has become a popular frequentist tool for putting uncertainty on a model's predictions. It needs no retraining and works with any model. Instead of a single answer, it returns a set of plausible answers, and a set with more than one answer signals uncertainty. These sets come with a guarantee: they contain the true answer, say, 90% of the time.

This ease of use hides what the sets reflect. They are the model's own confidence, cut off at a single threshold. If the model's confidence is not faithful, neither are the sets, yet the guarantee still holds.

A simple thought experiment shows how. Consider a method that ignores the input and returns the set of all labels with probability 90%, and an empty set otherwise. The true label is covered exactly 90% of the time, and the sets tell you nothing about any input. Coverage behaves like accuracy on an imbalanced dataset: the number can be correct and still say nothing about the cases you care about.<d-footnote>If only 0.1% of the people screened have cancer, a model that declares everyone healthy is 99.9% accurate and never finds a single case.</d-footnote>

**Conformal prediction adds one number, a global threshold. Everything that depends on the input was already in the model. It surfaces whatever uncertainty the model has but cannot make it faithful, so the real work is still in the model.**

This post is for practitioners who want to use conformal prediction and are unsure how to read its output. It is not a case against conformal prediction, which does what it promises. The point is to be clear about what it promises. For the deeper question of what uncertainty is in the first place, and why it is hard to model faithfully, see my [earlier post](/blog/2026/uncertainty-decomposition/).

## How Conformal Prediction Works

Split conformal prediction needs a trained model and a held-out calibration set. It also needs a score that measures how wrong the model is on an example, for instance $s(x,y) = 1 - \hat p(y \mid x)$ for a classifier or $s(x,y) = \lvert y - f(x) \rvert$ for a regressor.<d-footnote>Here $\hat p(y \mid x)$ is the model's predictive distribution, and $f(x)$ is the regressor's point prediction, the mean of its predictive distribution when it is trained with mean squared error.</d-footnote> It computes the score on every calibration example and takes the $1-\alpha$ quantile, $\hat q$, where $1-\alpha$ is the target coverage, say 90%.<d-footnote>Strictly, it takes a slightly higher quantile, at level $\lceil (n+1)(1-\alpha) \rceil / n$ for $n$ calibration examples, to account for the finite calibration set.</d-footnote> For a new input, the prediction set contains every answer whose score is at most $\hat q$. Angelopoulos and Bates <d-cite key="angelopoulos2023conformal"></d-cite> give an accessible introduction to the method and its variants.

The guarantee needs only one assumption. If calibration and test data are exchangeable, a condition weaker than i.i.d., the sets contain the true answer with probability at least $1-\alpha$, whatever the model and the data distribution. This is why conformal prediction is called distribution-free. But this probability is marginal, meaning averaged over all inputs. It says nothing about any particular input or group of inputs. This is easy to forget, because each set is built for one input and looks like an uncertainty estimate for it.

Whether the sets are useful for particular inputs depends on the model. I will call a model well-calibrated when its predictive distribution is close to the true one, $\hat p(y \mid x) \approx p^{\ast}(y \mid x)$, in expectation over inputs $x \sim p^{\ast}(x)$. Held-out negative log-likelihood measures this up to a constant. For a well-calibrated model, the sets contain the answers the data makes most likely at each input. In other words, they reflect the aleatoric uncertainty, which, as my [earlier post](/blog/2026/uncertainty-decomposition/) discusses in more detail, is a property of the data and not of the model.

## A Wrapper Cannot Fix the Model

The threshold $\hat q$ is computed once and does not depend on the input. For a classifier with the score $1 - \hat p(y \mid x)$, the prediction set is

$$
C(x) = \{y : \hat p(y \mid x) \ge 1 - \hat q\},
$$

which simply thresholds the model's predicted probabilities. What conformal prediction contributes is a principled threshold where one would otherwise pick an arbitrary one. That is worth something, but it does not produce uncertainty. Everything that varies from input to input comes from the model through its score. This is why the variants that make sets adapt to the input start with the model.<d-footnote>There are also conformal methods that calibrate a separate threshold for each group of inputs, known as Mondrian conformal prediction. They give coverage per group without touching the model, but within a group the threshold is again global. More refined methods exist, but they too rely on modelling choices.</d-footnote> An interval that widens where the data is noisy, for example, first needs a model that predicts the spread, and then a score that divides the error by it. That takes more modelling, not less.

<div class="row mt-3 justify-content-center">
    <div class="col-md-10 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/conformal-prediction/misfit.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <b>Conformal prediction fixes neither a misspecified model nor a poor fit.</b> Left: a model with a linear mean, which cannot represent data with a bump. Right: a model that can represent noise that changes with the input, but is fit poorly and expects the noise where the data is quiet rather than where it is noisy. The conformal set follows this wrong spread. Both sets cover 90% of the data overall, yet they are too wide where the model is fine and miss where it is wrong: on the bump and at the noisy end.
</div>

The left model is a classic regression model: a Gaussian with a constant variance and a mean that is linear in the input. Since the data has a bump, the model is misspecified. The right model is heteroscedastic: it also predicts the variance at each input. It could capture the noise, but it is fit poorly.

Both use a score that divides the error by the model's standard deviation $\sigma(x)$, so the conformal set is $f(x) \pm \hat q\,\sigma(x)$. The shape of the set comes from the model, and conformal prediction only scales it. Wherever the model is wrong, so is the set, even though it covers 90% overall.<d-footnote>A cleverer conformal method cannot fix this. For continuous inputs, no distribution-free method can guarantee coverage at each input, known as conditional coverage, unless its sets have infinite expected width <d-cite key="barber2021limits"></d-cite>. Coverage at each input needs assumptions about the data, and a model is where those assumptions live.</d-footnote>

## Where It Goes Wrong

Since the part that depends on the input comes from the model, the typical failures of conformal prediction are failures of the model.

**Confidence that does not flag errors.** What matters for conformal prediction is whether the model is less sure when it is wrong. If it is, its errors get larger sets. If it is equally sure either way, the set size no longer flags its errors.

<div class="row mt-3 justify-content-center">
    <div class="col-md-10 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="lazy" path="assets/img/posts/conformal-prediction/overconfidence.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <b>Set sizes flag errors only if the confidence does.</b> Both classifiers predict the same labels, and both sets reach 90% coverage. Left: a well-calibrated model is less sure when it is wrong, so its errors get larger sets. Right: a model that is equally sure when it is wrong, so its errors get the same sets as its correct answers.
</div>

Overconfidence is one way to make a model equally sure when it is wrong. A model is overconfident when its predictive distribution is sharper than the true one, $p^{\ast}(y \mid x)$. In the extreme, it puts all its probability on one label, whether it is right or wrong. If it is right more than 90% of the time, every set contains just the predicted label. The sets meet their coverage and are as small as possible, but they never flag an error.

A common application is large language models answering multiple-choice questions <d-cite key="kumar2023conformal"></d-cite>. Their probabilities are renormalized onto the answer tokens, so a model that puts little mass on any option can still look sure. Conformal prediction does not change this. The sets reflect uncertainty faithfully only if the model is well-calibrated over the answer options, which needs to be checked before wrapping it in conformal prediction.

**Wrong modelling choices.** In an [earlier post](/blog/2025/when-mse-loss-leads-to-mis-steering/), I looked at a common pitfall of misspecification. A powerful neural network learns to steer a car from human drivers and is trained with mean squared error. Where the road splits and both lanes are valid, it steers to the middle, straight into the divider.

<div class="row mt-3 justify-content-center">
    <div class="col-12 mt-3 mt-md-0">
        {% include figure.liquid loading="lazy" path="assets/img/posts/conformal-prediction/lane-split.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <b>Three choices of likelihood at the lane split.</b> Each panel shows, at an input where the road splits, the model's predictive distribution (blue) against the true one (grey), with the conformal set below. All three reach 90% coverage over all inputs. Left: a point regressor trained with mean squared error, drawn as the Gaussian with fixed variance that this loss implies. Middle: a Gaussian that also predicts its variance. Right: a categorical likelihood over buckets of the steering angle.
</div>

The standard recipe wraps the point regressor with the score $\lvert y - f(x) \rvert$ and returns the interval $[f(x) - \hat q, f(x) + \hat q]$, which has the same width at every input. It covers the true angle 90% of the time over all inputs, but the road rarely splits, so the width is set by the single lane. At the split, the interval misses both lanes and covers only the angles that lead to a crash.

A Gaussian that also predicts its variance does better. With the score $\lvert y - f(x) \rvert / \sigma(x)$, its interval widens at the split and reaches both lanes, so the set surfaces the uncertainty. But it still includes the divider. An interval assumes that the plausible answers lie next to each other. The assumption is never stated; it comes with the shape of the output.

A categorical likelihood over buckets of the steering angle does not make this assumption. With fine enough buckets, it represents both lanes, and conformal prediction returns both, with the gap between them. Of the three, it is the only likelihood that can faithfully capture the true distribution, but a full distribution is hard to act on. Conformal prediction turns it into two valid options, and the car can take either.

The score is a modelling choice too. The figure below wraps a model that matches the true distribution exactly. With a score built from its mean and standard deviation, it returns the same interval as the heteroscedastic Gaussian, because the score sees nothing else. With a score built from its density, it returns the two lanes. A set can only split into several options if the model represents them and the score makes use of them.

<div class="row mt-3 justify-content-center">
    <div class="col-md-10 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="lazy" path="assets/img/posts/conformal-prediction/lane-split-score.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <b>The score decides whether the set shows both lanes.</b> Both panels wrap the same model, which matches the true distribution exactly, and both reach 90% coverage over all inputs. Left: a score built from the model's mean and standard deviation returns one interval across the divider. Right: a score built from its density returns the two lanes.
</div>

**Outside the guarantee.** The guarantee needs exchangeability, and it degrades gracefully: if the data is close to exchangeable, coverage drops only a little <d-cite key="barber2023beyond"></d-cite>. But how close your data is to exchangeable is rarely known, and it matters most in a world that changes over time, as in [forecasting](/blog/2026/good-predictor-not-good-forecaster/).

Out of distribution, the guarantee does not apply at all, because the calibration set holds no such inputs. Noticing that an input is unfamiliar is a separate and hard problem, which I discuss in earlier posts on [uncertainty](/blog/2026/uncertainty-decomposition/) and [continual learning](/blog/2025/uncertainty-can-solve-continual-learning/).

## What It Is Good For

None of this makes conformal prediction useless. Even a well-calibrated model leaves you with a full distribution when you need a decision, such as whether to trust a prediction or hand it to a human. Conformal prediction turns that distribution into a decision with a principled threshold. The same works for a Bayesian model, where the sets are derived from the posterior predictive distribution and gain a frequentist guarantee, even if the prior or likelihood is misspecified. A set is also a more honest answer than a point estimate.

Uncertainty lives in the model's predictive distribution, and whether it means anything depends on the fit and the modelling choices behind it. Conformal prediction reads this distribution out as sets, with a guarantee that holds on average over inputs. Only for a well-calibrated model do the sets also reflect what the data allows at each input. The sets can only be as informative as the model behind them.

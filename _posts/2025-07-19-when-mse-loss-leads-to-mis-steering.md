---
layout: post
title: Why an MSE Loss Might Make Your Self-Driving Car Crash
date: 2025-07-19 09:56:00
description: This article explains why using MSE to train steering angle prediction can be a recipe for disaster.
tags: ml
categories: machine-learning
giscus_comments: true
related_posts: true
related_publications: true
---

Towards the end of my PhD, I co-authored a paper on model misspecification, see {% cite cervera:henning:2021:regression %}. The idea struck me while reviewing the self-driving car literature. I noticed that almost everyone was training steering angle predictors using the [mean squared error (MSE) loss](https://en.wikipedia.org/wiki/Mean_squared_error). It’s an understandable choice: MSE is the default loss for regression in machine learning.

Here's the catch: **using MSE for steering angle prediction is a bad idea because it trains your model to average over options rather than select one.**

Our paper explored this problem in depth, but the core insight — that MSE can cause a catastrophe — got buried under layers of cautious phrasing and technical detail. That’s how scientific writing works: every claim must be hedged, every conclusion defended. It’s the right approach for academics, but it often buries the simple, intuitive message.

A blog post is different. Here, I can say what I really think: **if you train a self-driving car with MSE, you’re optimizing for the wrong thing, and it might crash**.

In this post, I'll unpack that message. First, I'll explain the mathematical intuition behind MSE — it predicts the mean of the target predictive distribution. From there it's easy to see why even a model with near-zero MSE can still fail dramatically, and why this matters if you care about staying on the road (literally or metaphorically).

## The MSE Loss Forces the Model to Predict the Mean of a Gaussian

To understand why MSE behaves the way it does, we need to look at where it comes from.

> For a deeper dive into the origins of common loss functions, see chapter 2 of my thesis: {% cite henning2022phdthesis %}.

In practice, [maximum likelihood training](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation) essentially boils down to the minimization of a [Kullback–Leibler divergence](https://en.wikipedia.org/wiki/Kullback–Leibler_divergence) $$\text{KL}\left( p(y \mid x) ; q(y \mid w, x) \right)$$ of an assumed ground-truth distribution $$p(y \mid x)$$ from a parametrized model distribution $$q(y \mid x; w)$$.

In our case, $$x$$ is the image from the car's front camera and $$y \in \mathbb{R}$$ is the steering angle. In simple words, we assume that every image $$x$$ induces a distribution over steering angles $$p(y \mid x)$$. We also assume that human drivers sample from this distribution, generating data tuples $$(x,y)$$ - $$x$$ being the image the driver sees, and $$y$$ the steering angle they choose.

Now, since $$y$$ is continuous, we are dealing with a regression problem. Next, we need to choose a model $$q(y \mid w, x)$$ parametrized by $$w$$ that can faithfully resemble the unknown ground-truth data generating process $$p(y \mid x)$$. Unfortunately, continuous probability distributions are a bit cumbersome to work with, so the sake of simplicity we fall back onto a Gaussian approximation $$q(y \mid w, x) = \mathcal{N}(y; f(x; w), \sigma^2)$$, where $$f(x; w)$$ is (for us) a neural network with parameters $$w$$ that predicts the mean of the Gaussian.

Taking all of these assumptions together, we can arrive at a tractable loss function for our optimization problem:

$$
\min_w \mathbb{E}_{p(x)} \left[ \text{KL}\left( p(y \mid x) ; q(y \mid w, x) \right) \right] \Leftrightarrow \min_w - \mathbb{E}_{p(x,y)} \left[ \log q(y \mid w, x) \right] \Leftrightarrow \min_w \mathbb{E}_{p(x,y)} \left[ \left( y - f(x;w) \right)^2 \right]
$$

Taking a [Monte-Carlo estimate](https://en.wikipedia.org/wiki/Monte_Carlo_integration) of the last expected value yields the classical MSE loss used for regression.

## How the MSE Loss Can Make You Crash

Here's the core problem: MSE ignores safety and plausibility. It simply averages over all possible outcomes — and that average can be the worst choice.

The previous section highlighted that there are many assumptions going into the derivation of the MSE loss. One crucial assumption has been, that we directly predict a mean, which, at optimality, resembles the mean of the ground-truth $$p(y \mid x)$$ (cf. SM C in {% cite cervera:henning:2021:regression %}).

This is a problem, because we are not interested in the mean of $$p(y \mid x)$$, but the plausible choices it offers.

In the figure below, a highway lane splits into two: the driver can either turn left or right ($$p(y \mid x)$$ is bimodal). The mean of these choices points right in-between the two lanes.

<div class="row mt-3 justify-content-center">
    <div class="col-md-6 col-sm-8 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img//posts/steering_angle_illustration.pdf" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    This figure is taken directly from the paper (cf., Fig. 3 in {% cite cervera:henning:2021:regression %}). It shows a lane bifurcation where the driver has to decide to either go left or right. A possible ground-truth is shown in orange. An optimal model under these assumptions predicts the mean of plausible steering angles, which lies between the two valid choices — leading the car off the road.
</div>

## Beyond Cars: Why This Problem Matters

Any time you’re averaging over multiple plausible outcomes, MSE will happily produce a result that **doesn’t correspond to any real-world action**.

In self-driving, relying on a single steering-angle prediction would be unwise. Navigation goals, lane detection, and planning signals can all interact to mitigate risk. But these systems only reduce the chance of catastrophic failure — they don’t fix the **root cause: the wrong modelling choice**.

So here's my advice: **if you're working on regression, don't blindly pick MSE** just because textbooks treat it like the universal default. There are other alternatives — some of which we discuss in our paper.

If you’re curious, take a look! 😉

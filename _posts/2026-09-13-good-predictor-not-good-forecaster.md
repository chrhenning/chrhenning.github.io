---
layout: distill
title: "A Good Predictor Is Not Yet a Good Forecaster: Why Forecasting Needs Knowledge Beyond the Data"
date: 2026-09-13 10:00:00
description: A model that predicts well can still forecast badly, because the inputs it needs are not known yet and the future may not look like the past. Prior knowledge can reach beyond the data, and a causal picture shows where to attach it.
tags: forecasting causality statistics
categories: machine-learning
og_image: https://chrhenning.com/assets/img/posts/good-predictor-not-good-forecaster/only-weather-has-a-forecast.png
giscus_comments: true
related_posts: true
related_publications: false
citation: false
bibliography: 2026-09-13-good-predictor-not-good-forecaster.bib
thumbnail: assets/img/posts/good-predictor-not-good-forecaster/a-week-ahead-thumb.png

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: A Good Predictor That Cannot Forecast
  - name: Where Prior Knowledge Attaches
  - name: When the Causal Picture Is Not Obvious
---

Forecasting is usually treated as prediction with the target moved further out, which quietly assumes the future looks like the past.

But time has an arrow, and the world that generates our data keeps changing. How much this matters depends on the problem and its horizon, and judging that is the practitioner's job. For tomorrow's sea level it barely matters, because the tides repeat, but sea level at the end of the century depends on how much CO2 we will emit, which no tide gauge record can tell you.<d-footnote>Section 3.3 of my PhD thesis <d-cite key="henning2022phdthesis"></d-cite> discusses forecasting atmospheric CO2 with a Bayesian model. With a vague prior, the forecast becomes very uncertain right after the data ends. It stays confident for years only once a human encodes seasonality and a rising trend into the prior, knowledge that does not come from the data, and no past data can tell whether that knowledge will still hold.</d-footnote>

**Correlation is enough to predict well under the conditions a model was trained on. A forecast has to do without tomorrow's inputs, and tomorrow's conditions may differ from those in training. Only knowledge from outside the data can close that gap, and a causal picture shows where it comes in.**

<div class="row mt-3 justify-content-center">
    <div class="col-md-10 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/good-predictor-not-good-forecaster/only-weather-has-a-forecast.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <b>Only the weather has a forecast.</b> On past days, ice cream sales predict beach rescues at least as well as the weather does. For the coming days, only the weather has a forecast, so the rescue forecast is built on it and is only as certain as the weather forecast.
</div>

## A Good Predictor That Cannot Forecast

To plan lifeguard staffing, a coastal town wants a model of daily rescues. It records the weather, ice cream sales, parking receipts, and rescues, but not how many people are at the beach.

<div class="row mt-3 justify-content-center">
    <div class="col-md-8 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="lazy" path="assets/img/posts/good-predictor-not-good-forecaster/causal-picture.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <b>The causal picture of the beach.</b> All arrows act within a single day. The town records the solid boxes but not the dashed crowd. Rescues are the target.
</div>

I will call this a causal picture, an informal causal graph of which variable drives which. It says nothing about how things evolve from one day to the next.

Today's ice cream sales predict today's rescues very well, because both reflect the same hidden crowd. The correlation is spurious, since eating ice cream puts nobody in danger, but it is not weak. Sales track the crowd more closely than the weather does, so they are often the strongest signal in the data.

Now ask about next Thursday. The model first needs next Thursday's ice cream sales, which are no easier to know than the rescues. Ordinary prediction never has this problem, because its inputs are already measured.

The usual workaround is to predict next week's rescues from this week's records. But next Thursday's crowd depends on next Thursday's weather, which none of these records contain, so the model can do little better than guess from the season. The missing weather has to come from outside the data.

<div class="row mt-3 justify-content-center">
    <div class="col-md-10 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="lazy" path="assets/img/posts/good-predictor-not-good-forecaster/a-week-ahead.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <b>This week's records cannot forecast next week's rescues.</b> Ice cream sales from the same week track rescues closely. Shifted by a week, as the shaded band shows for sales, neither sales nor the weather tracks them.
</div>

There is a second problem. A learned relationship holds only as long as the world that produced it, and the world changes. If the most popular ice cream stand closes, a busy day sells like a quiet day used to, and any model built on ice cream sales staffs for a quiet beach. A model built on the weather is unaffected, because closing a stand changes neither the weather nor how many people it draws. Since a forecast lies beyond the data, no error on past data can reveal such a shift before it happens. This is the sense in which forecasting is often out-of-distribution.<d-footnote>Such shifts are ruled out only under stationarity, where the distribution of any stretch of the series does not depend on when it starts. Relationships learned from the past then keep holding, although the model still needs its future inputs.</d-footnote>

The model's uncertainty cannot be relied on to flag the shift either. As I argued in an [earlier post on uncertainty](/blog/2026/uncertainty-decomposition/), such estimates are only as sound as the model's assumptions.

## Where Prior Knowledge Attaches

Ask a lifeguard how busy next Thursday will be, and they will check the weather forecast. That forecast does not come from the town's weather records, which extrapolate no better than past sales, but from meteorology, built on physics, instruments, and satellites.<d-footnote>Since a weather forecast can be computed, a powerful enough model should be able to learn it, and machine learning models such as GraphCast <d-cite key="lam2023graphcast"></d-cite> now rival physics-based forecasts. But they learn from decades of temperature, wind, and humidity reconstructed at many heights across the whole globe, and each forecast starts from the current state of the atmosphere, estimated from satellites, weather balloons, and ground stations. A model trained on this week's records to predict next week's rescues sees none of this, so however powerful it is, it cannot learn the weather forecast along the way.</d-footnote> Ice cream sales have no such science behind them. Knowledge that reaches beyond the data comes from outside it, whether a physical model, a holiday calendar, or a festival booked for next Thursday.

Two pieces of knowledge are at work. By uncovering the structure behind the data, the causal picture guides you to the variable worth forecasting, the weather rather than ice cream sales. More generally, you follow the arrows back until you reach a variable whose future someone can actually forecast.<d-footnote>In symbols, with $r$ for rescues and $w$ for the weather, the rescue forecast is $p(r_{t+h} \mid \text{past}) = \int p(r_{t+h} \mid w_{t+h})\, p(w_{t+h} \mid \text{past})\, dw_{t+h}$. The first factor is learned from the town's records and the second comes from meteorology, so any uncertainty in the weather forecast carries into the rescue forecast.</d-footnote> A model of the weather's dynamics then carries it forward in time, the same kind of knowledge that lets astronomers forecast a comet's path years ahead without any machine learning.

When that knowledge runs out, the forecast should become vague rather than wrong. Beyond the reach of weather forecasts, the season still tells the town what an average August Thursday looks like, but not whether this one will be busy, so an honest forecast gives a wide range instead of a confident number.

Knowing where knowledge attaches matters even more now that pretrained forecasting foundation models are widely available, because using them well means understanding their limits. Chronos-2 <d-cite key="ansari2025chronos2"></d-cite>, for instance, accepts known future covariates, so it can use next Thursday's weather forecast if you supply one, but it cannot recreate meteorology from the town's history. Pretraining teaches generic patterns such as seasonality and trends, yet a model that sees only numbers does not know whether a series measures CO2 or ice cream sales, so it cannot tell where to look for knowledge about its future.<d-footnote>It would help if such models could also read what a series measures and where it comes from. Chronos-2 does not take such descriptions, although research on forecasting with textual context has begun.</d-footnote> Choosing which covariates to supply remains your job.

## When the Causal Picture Is Not Obvious

The beach example feels obvious only because everyone already carries its causal picture in their head, but real use cases rarely come with one.

Hand someone two hundred bioreactor sensor channels named by tag and ask for next week's yield, or a CRM export and ask which customers will leave next quarter. An ML engineer without domain knowledge cannot see which variable plays the role of the weather, or whether any does. So the target gets regressed on everything, the model scores well on past data, and it goes into use without anyone asking what drives the system.<d-footnote>You might wonder how this relates to root cause analysis. The two are closely related, because both rest on the same causal picture. Root cause analysis uses it to explain an outcome that already happened, and a forecast uses it to anticipate one.</d-footnote>

Before building a forecast, ask what drives the system and who already has a model of that driver, which usually means talking to a domain expert first. If the answer is a weather service, a production plan, or a physical model, attach it. If nobody has one and the past is no safe guide, you do not have a forecasting problem but a research problem.

Forecasting is not prediction moved further out. It starts where the data stops, and what carries it further is the knowledge you bring.

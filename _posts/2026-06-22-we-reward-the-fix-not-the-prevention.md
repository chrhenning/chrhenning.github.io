---
layout: distill
title: "Your Best Work Leaves No Trace: Why Engineering Teams Reward the Fix and Replace the Prevention"
date: 2026-06-22 09:00:00
description: From testing and reliability engineering to team culture, the hardest problems are prevented, not fixed. Yet we chronically undervalue prevention, and let visible process stand in for the invisible outcomes that actually matter.
og_image: https://chrhenning.com/assets/img/posts/we-reward-the-fix-not-the-prevention/the-fix-and-the-prevention.jpg
tags: engineering technical-debt
categories: leadership
giscus_comments: true
related_posts: true
related_publications: false
citation: false
bibliography: 2026-06-22-we-reward-the-fix-not-the-prevention.bib

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: An Old, Uncomfortable Asymmetry
  - name: Prevention Theater
  - name: The Same Trap, With People
  - name: The Same Failure, Different Clothes
  - name: Why the Trap Pays
  - name: Telling the Proxy From the Thing
  - name: Crediting What Never Happened
---

A production incident gets fixed under pressure late on a Friday, and by Monday the engineer who saved the day is the center of attention. Earlier that same quarter, a different engineer quietly did the work that kept a separate system stable: writing a test covering a rare edge case, fixing a backup routine, or tightening permissions before anyone could exploit them. None of that work earns a mention, because **the outage it prevented never happened**.

We celebrate the fix and barely perceive the prevention. That should bother us, because prevention is not heroics. It is simply the job done properly. The trouble is that doing the work well produces a set of absences: the outage that did not happen, the data that was not lost, and the breach that never occurred.

**Absences make terrible portfolio pieces.** You cannot easily point to a catastrophe that never came to pass, and you cannot provide visual proof of a smooth, quiet Friday night.

This asymmetry quietly shapes how engineering teams spend their attention. It is a dynamic that deeply resonates with my own experience, and even organizations that actively strive for balance struggle against the gravity of the visible crisis. The pressure is structural rather than personal. It explains a surprising amount: why testing, security, and backups perennially lose the prioritization fight, and why the most common organizational response backfires. Faced with prevention we cannot see, organizations reach for a visible proxy for it, and that proxy quietly crowds out the prevention it was meant to protect.

<div class="row mt-3 justify-content-center">
    <div class="col-md-10 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/we-reward-the-fix-not-the-prevention/the-fix-and-the-prevention.jpg" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
  The fix and the prevention. On the left, the crisis everyone sees: a person in the thick of it, surrounded by alarms and dashboards, the center of attention. On the right, the same storm faded to a ghost of what was averted, with the person who prevented it standing quietly, unthanked. Image generated with Google Gemini.
</div>

## An Old, Uncomfortable Asymmetry

The core observation here is neither mine nor is it new. It is one of the most rediscovered ideas in all of applied reasoning.

Back in 1850, Frédéric Bastiat told a simple story, now known as the [parable of the broken window](https://en.wikipedia.org/wiki/Parable_of_the_broken_window), about a boy who breaks a shop window <d-cite key="bastiat1850seen"></d-cite>. The neighbors try to cheer up the shopkeeper: look on the bright side, now the repairman gets paid, and that money flows on to others, so really everyone wins. Bastiat's point is that this misses what you cannot see. The money spent fixing the window is money the shopkeeper can no longer spend on shoes or books. The repair is visible, so we count it. The shoes that never got bought are invisible, so we forget them, even though they were just as real.

A century and a half later, Nassim Taleb gave the same idea its sharpest modern form, calling it the problem of silent evidence. He imagines a legislator who, at great political cost, forces every airline to install locked, reinforced cockpit doors, with the law taking effect on September 10, 2001 <d-cite key="taleb2007blackswan"></d-cite>. That person prevents the attacks of the next morning and is never thanked, never remembered, precisely because the catastrophe they averted never happened. Taleb's conclusion is blunt: everybody knows we need prevention more than treatment, but few reward acts of prevention, and history glorifies the names left in its books over the contributors it stays silent about.

The management literature has a name for the organizational version of this. Repenning and Sterman called their study of it, perfectly, "Nobody Ever Gets Credit for Fixing Problems that Never Happened" <d-cite key="repenning2001credit"></d-cite>. They describe the _capability trap_: under pressure, teams cut the invisible work (maintenance, improvement, prevention) to feed the visible work, which raises the firefighting load, which increases the pressure, which cuts the invisible work further.

So the diagnosis is settled and ancient. What I find more interesting, and less discussed, is what organizations actually _do_ in response to this asymmetry. Because they do not simply underfund prevention and leave it there. They reach for something that looks like prevention and is much easier to see.

## Prevention Theater

When real prevention earns no credit because it produces no signal, organizations look for a substitute. So we substitute a version of prevention that _does_ produce a signal: a gate, a checklist, a mandatory sign-off, a ceremony, a required reviewer, a manual QA pass on every change. These things generate artifacts. They populate a dashboard. They give a manager something to point at when someone asks what we are doing about quality. I'll call this **prevention theater**, with a deliberate nod to [Bruce Schneier's "security theater,"](https://en.wikipedia.org/wiki/Security_theater) the airport-style measures that make us feel safer without making us safer <d-cite key="schneier2003beyondfear"></d-cite>.

The trouble is not that gates are useless. A good gate verifies quality that is already there, and the best processes go further and build it in: a pilot's pre-flight checklist or a surgeon's pre-incision checklist makes the right step happen rather than merely recording that someone looked. Those earn their place, and the discipline is to keep asking which ones still do. The trouble is the other kind, the process bolted on to fight symptoms, standing in for quality the work does not have.<d-footnote>A gate is only as good as the thing it checks, and choosing that thing is most of the design. Test coverage is a weak choice: point an AI at the codebase and it will bulk-generate unit tests until the percentage clears the bar, yet those tests mostly assert that the code does whatever it already does. The gate fired and verified nothing.</d-footnote> It competes with the real thing for the same budget of attention and keeps winning, because it is _visible_ and the real work is not. We are optimizing for what we can see.

Quality control has known this for a long time. W. Edwards Deming, quoting Harold Dodge, put it in one line: **"You cannot inspect quality into a product."** <d-cite key="deming1986crisis"></d-cite> By the time the gate runs, the quality is already either built into the work or missing from it. The check does not add any; it only reveals what is there. A gate at the end of the line does not create quality; it just produces a record of having looked. Worse, it relocates responsibility. When there is a QA gate on every change, the author quietly stops owning whether the change is correct, because checking is now the gate's job. The bar drifts down to whatever the gate mechanically verifies, and everyone learns to write for the checklist rather than for the system.<d-footnote>Early coding agents made this concrete: pointed at a failing build, they would often rewrite the test rather than fix the root cause. <a href="https://metr.org/blog/2025-06-05-recent-reward-hacking/">METR found</a> that when the scoring code was visible to the model, it would routinely game the check rather than fix the code, and far less often when the scoring was hidden.</d-footnote>

I've argued before that scrappiness tends to launder unmanaged debt into a virtue (see [Scrappiness Incentivizes Sloppiness]({% post_url 2025-10-31-scrappiness-incentivizes-sloppiness %})), and that the speed-versus-quality trade-off is mostly a myth once you look at the data. Prevention theater is the mirror-image failure. Scrappiness skips the invisible work and admits it. Theater skips the invisible work while producing a convincing artifact that says otherwise, which is more dangerous, because it buys a false sense of safety. An ignored test suite, a rubber-stamped review, or a massive code diff nobody actually reads: each is a green light wired to nothing.

The tell, every time, is that the artifact has become the goal. This is [Goodhart's law](https://en.wikipedia.org/wiki/Goodhart%27s_law) in miniature: when a measure becomes a target, it stops being a good measure, because a proxy is always easier to optimize than the messy reality it stood for <d-cite key="goodhart1984monetary"></d-cite><d-cite key="strathern1997ratings"></d-cite>. The question shifts from "is this safe to ship?" to "did we complete the checklist?" Those are not the same question, and the gap between them is exactly the prevention we told ourselves we were buying.

## The Same Trap, With People

This identical pattern runs through the _human_ side of engineering, yet the technical and organizational versions of this failure are rarely treated as one.

A team's real standard is not what it writes in a values doc. It is the worst work it tolerates without comment. Lieutenant General David Morrison put it memorably (crediting the line to David Hurley): **"the standard you walk past is the standard you accept."** <d-cite key="morrison2013standard"></d-cite> Every time mediocre work ships without a conversation, the bar moves down a notch, and the move is small enough that no single instance feels wrong. Diane Vaughan studied the catastrophic version of this in her analysis of the Challenger launch and named it the [_normalization of deviance_](https://en.wikipedia.org/wiki/Normalization_of_deviance): the gradual process by which an unacceptable practice becomes acceptable, then expected, then invisible <d-cite key="vaughan1996challenger"></d-cite>. Dan Luu and Bruce Schneier have both pointed the same lens at software organizations <d-cite key="luu2015deviance"></d-cite><d-cite key="schneier2016deviance"></d-cite>.

The asymmetry repeats perfectly. The act that actually holds a standard is direct _engagement with sub-par work_. It requires pausing, having a slightly uncomfortable conversation, asking for rework, and coaching toward the bar. Because its entire payoff is an absence (the erosion of quality that did not set in), this work is quietly skipped, because shipping anyway always feels easier in the moment. And what do organizations reach for instead? A visible proxy. More process. A PR template, a mandatory second reviewer, a sign-off step, a heavier definition of done. This is the same prevention theater in a different costume: an artifact that says "we have standards" standing in for the invisible work of actually holding them.

The conversation is the prevention. The process is theater whenever it stands in for that conversation instead of provoking it. One produces a record; the other produces a culture, and only one of them is easy to point at in a performance review.

## The Same Failure, Different Clothes

Once you line the two up, the engineering version and the human version, it is hard to see them as separate problems. They are the same failure wearing different clothes.

In both cases, risk accumulates silently, with no signal, until it doesn't. James Reason called these _latent conditions_: weaknesses that sit dormant in a system, contributing nothing visible, until they line up with a triggering event <d-cite key="reason2000error"></d-cite>. In the image he later made famous, the holes in the Swiss cheese align. An untested code path and a tolerated lapse in standards are the same kind of object: a latent condition that produces no feedback while it is forming, and a great deal of feedback the day it finally matters.

<div class="row mt-3 justify-content-center">
    <div class="col-md-8 col-sm-12 mt-3 mt-md-0">
        <img src="{{ '/assets/img/posts/we-reward-the-fix-not-the-prevention/swiss-cheese-model.svg' | relative_url }}" class="img-fluid rounded z-depth-1" alt="Swiss cheese model of accident causation: several slices of cheese in a row, each with holes; a hazard passes through only when holes in successive slices line up." loading="lazy" />
    </div>
</div>
<div class="caption">
  James Reason's Swiss cheese model of accident causation: each defensive layer has holes, and harm passes through only in the rare moment they align. An untested code path and a tolerated lapse in standards are two such holes. Image by <a href="https://commons.wikimedia.org/wiki/User:BenAveling">Ben Aveling</a>, <a href="https://creativecommons.org/licenses/by-sa/4.0">CC BY-SA 4.0</a>, via <a href="https://commons.wikimedia.org/wiki/File:Swiss_cheese_model_textless.svg">Wikimedia Commons</a>.
</div>

And in both cases, the same manager makes the same trade for the same reason. The instinct that underfunds the test suite is the instinct that skips the standards conversation. The reflex that adds a QA gate is the reflex that adds a review template. It is not stupidity or laziness. It is a rational response to an incentive landscape where the visible is rewarded and the invisible is ignored. That incentive landscape is itself downstream of human cognition. Because we naturally register vivid events while remaining blind to non-events, an absence is not merely unrewarded; it is barely perceived. You cannot easily manage what produces no signal, so managers control the proxy that does.

Therefore, the fix is not to simply try harder to value invisible work. **Willpower loses to incentives every time.** This is Reason's point exactly: we cannot change the human condition, but we can change the conditions under which people work <d-cite key="reason2000error"></d-cite>. The fix is to change what the work produces.

## Why the Trap Pays

That fix is clear enough on paper, which raises the puzzle the literature tends to leave hanging: if the trap is this old, this documented, and this costly, why are so many companies that fall into it successful anyway? Because it is an equilibrium, not a mistake. Theater becomes the dominant organizational strategy because its cost is paid now and is entirely certain. Conversely, the payoff of real prevention is deferred and structurally unprovable. The engineer who prevents an outage holds only a counterfactual, with no proof that a disaster would have occurred or that they were the one who stopped it. The engineer who fixes an active outage holds concrete evidence: system logs, timestamps, incident reports, and a grateful customer. Even a firm that genuinely wants to reward prevention cannot easily price what its own people cannot prove, making the visible proxy the rational purchase.

And no single firm is uniquely punished for this choice, because its competitors all make the same move. You are graded against rivals who are equally afflicted rather than against perfection. This is the unobservable-quality problem that George Akerlof named in the [market for lemons](https://en.wikipedia.org/wiki/The_Market_for_Lemons), applied one level up. <d-cite key="akerlof1970lemons"></d-cite>

And the bill, when it comes due, hides on the same axis as the prevention. Latent conditions accumulate for years with no feedback, so a company can run on borrowed reliability and tolerated lapses long enough to get acquired, pivot, or ride a market wave before the holes line up. The successful-yet-afflicted firms we point to are partly just the ones where the cheese has not aligned yet; the ones it sank are the silent evidence we never see <d-cite key="taleb2007blackswan"></d-cite>.

But survivorship is only half of why the giants get away with it. The other half is that revenue is not a referendum on prevention. The largest firms win on entrenched advantages, on network effects, distribution, and sheer scale, and the profit those throw off is wide enough to absorb mediocre engineering as drag rather than death. Insulated from fierce competitive pressure, a massive firm simply carries the organizational slack. Economists refer to this as [X-inefficiency](https://en.wikipedia.org/wiki/X-inefficiency), a phenomenon routinely found in companies that do not operate under strict survival pressures <d-cite key="leibenstein1966xefficiency"></d-cite>. A dominant firm can firefight for years and still print money because its bottom-line profit was never priced on the outage that did not happen. Firefighting genuinely delivers for a while too, which is what makes the capability trap a trap <d-cite key="repenning2001credit"></d-cite>. So success is no proof the trap is benign. You cannot read prevention quality off a balance sheet: it is the same invisibility one level up, a cost that produces no signal and so never forces the fix.

And even when it never blows up, the trap is not free. Firefighting is its own standing tax: a reactive, draining mode of work that quietly costs the engineers who stop trusting their own systems and take their ambition elsewhere.

## Telling the Proxy From the Thing

_Changing what the work produces_ has a catch: any signal you invent to make prevention visible is one short step from hardening into the next gate. So the whole game is one question you can apply anywhere:

**Does this measure the absence I actually care about, or does it just produce evidence that I did something?** The first is prevention. The second is theater.

The cleanest thing I know that passes is the SRE practice of error budgets and service level objectives <d-cite key="googlesre_errorbudget"></d-cite>. Reliability is a classic invisible asset because nobody notices it until it vanishes. An error budget makes that absence measurable. It turns a vague notion like "the system kept working" into a concrete metric that you can spend, defend, and reason about. This structural transparency allows reliability to win prioritization arguments it would otherwise lose silently. <d-footnote>This cuts both ways: a budget is there to be spent. Reliability past the bar you actually need is over-engineering, not virtue. Prevention means hitting that bar, not chasing zero risk at the expense of progress.</d-footnote> It measures the outcome (did we stay within budget?), not the activity (did we hold the meeting?).

The same test sorts real review from theater. A reviewer who only records that someone looked fails it; review that genuinely engages with the work passes. But review is not where quality comes from. Only the author can build quality in, because only the author shapes the work, so responsibility for the result stays with them whoever signs off. Good review does not relieve them of that; it is two people raising the bar together, iterating toward something better than either would ship alone. The alternative to a rubber stamp, then, is not a lower engineering bar but authors who own what they merge and reviewers who genuinely sharpen it. A gate absorbs that ownership; a real metric, and a real review, hand it back.

The test carries straight to the human layer, where it says protect the conversation, not the template. Engaging with sub-bar work, directly and early, is the high-leverage act, but it only has weight if the bar is real, which means the people who hold it have to visibly live it. A team whose leaders preach quality and ship slop on a deadline learns, accurately, that quality is a slogan. Keep consequences in reserve, too, as the rare backstop that keeps everyday coaching credible. The template proves a step happened; the conversation changes the work.

Because real prevention creates no incident logs on its own, you must build that narrative deliberately. When an automated test catches a critical regression before it ships, or when a difficult conversation pulls a design back up to the bar, _name that outcome out loud_. This is the only way invisible work wins the narrative credit that visible crises receive for free.

## Crediting What Never Happened

The asymmetry that opened this essay is old, and it is not going away. We are wired to commit the classic economic fallacy Frédéric Bastiat identified: focusing on the broken window while staying blind to the unseen value lost to pay for it <d-cite key="bastiat1850seen"></d-cite>. We thank the firefighter and forget the person who fireproofed the building.

We cannot undo that cognitive bias. But we usually pile a second, preventable mistake on top of it. Because we cannot see real prevention, we reach for an artifact we can observe: a gate, a checklist, a heavier process, a formal record. Anything that lets us feel covered. That substitute is never free. It crowds out real prevention, and the safety it promises is mostly an illusion.

Therefore, the discipline required of modern engineering organizations is threefold:

- **Normalize counterfactual credit:** Celebrate and protect the problems that never happened loudly enough that the people who prevent disasters can survive a performance review.
- **Audit your metrics:** Where you do build a tracking signal, keep it strictly tied to the operational outcome you care about, and constantly verify that it has not decayed into an empty checkbox.
- **Distrust structural shortcuts:** Reject anything that promises to make prevention cheap or mechanical. The durable asset was never the formal process, but the underlying engineering culture that builds quality in before any gate runs.

If you are the engineer doing this quiet work, do not draw the cynical conclusion that prevention is a dead end, that you should let things break to be seen fixing them. The reward exists; it just sits on a slower ledger. Heroics earn applause, but prevention earns trust: the autonomy and hard problems that compound into the engineer everyone wants on their team.

The mistake is not doing the invisible work; the mistake is doing it silently. Make the counterfactual legible: name the catch, and say what those quiet days bought the business. This is the [signal](https://en.wikipedia.org/wiki/Signalling_%28economics%29) that answers Akerlof's lemons problem from earlier, making quality visible when it would otherwise go unpriced <d-cite key="spence1973signaling"></d-cite>.

The moment you have any leverage over what an organization rewards, use it.<d-footnote>Designing that reward structure is a leadership responsibility I've argued before in the split between research and engineering: judge both against a single scoreboard and you quietly train researchers to stop taking risks (see <a href="{% post_url 2026-05-10-before-the-breakthrough-research-engineering-cultures %}">Before the Breakthrough</a>).</d-footnote> As Steven Kerr observed, the core organizational failure is the folly of rewarding one behavior while hoping for another <d-cite key="kerr1975folly"></d-cite>. A system that pays only for visible fixes gets exactly what it prices: visible crises. Left unchecked, it trains its best people to light the fires they get paid to put out.<d-footnote>Kerr first made this argument in 1975, and it has held up uncomfortably well. Two decades later, the journal reprinted the paper as an absolute classic and polled its executive panel on whether organizations had stopped rewarding the wrong things. Largely, they had not <d-cite key="kerr1995academy"></d-cite>.</d-footnote>

What is easy to measure is almost always the theater.

**What matters is almost always the problem you never had.**

---
layout: distill
title: "Ship the Upgrade Path First: Distribution as a Control Plane for Fast Iteration"
date: 2026-07-01 08:00:00
description: The fastest-moving products are not the ones with the cleverest features, but the ones that can change what is already deployed. For self-hosted software that means building distribution and self-upgrade first, because without them there is no iterate step, and every cut made for the MVP quietly becomes permanent.
og_image: https://chrhenning.com/assets/img/posts/ship-the-upgrade-path-first/dispatch-vs-checkin.jpg
tags: distribution technical-debt
categories: engineering
giscus_comments: true
related_posts: true
related_publications: false
citation: false
bibliography: 2026-07-01-ship-the-upgrade-path-first.bib

authors:
  - name: Christian Henning
    affiliations:
      name: Personal Blog

toc:
  - name: Where It Runs Is Not Who Controls It
  - name: A Problem Infrastructure Already Solved
  - name: A Distribution Channel That Keeps Control
  - name: What It Buys You
---

Peter Thiel's claim about distribution is usually read as a sales lesson. It is just as true, and just as ignored, in engineering: "superior sales and distribution by itself can create a monopoly, even with no product differentiation" <d-cite key="thiel2014zerotoone"></d-cite>. His diagnosis is blunt: most startups that fail didn't fail on product. They failed because they never got a single distribution channel working.

For software that has to run inside someone else's infrastructure, the distribution channel does not end at the sale. The product only actually reaches the customer once it is installed, running, and kept current on their machines, and that is a technical problem: how a new version gets from your build pipeline onto their infrastructure. Get that wrong and you have exactly the failure Thiel describes, a product nobody can reliably receive, no matter how good the sales motion that closed the deal.

There is a stronger claim hiding in this. [MVP and iterate](/blog/2025/mvp-manage-debt-and-iterate-fast/) is not just a development philosophy; it is a bet that you can reach what you already shipped. For software you do not control at runtime, that bet is not free: the reach has to be built, or there is no iterate step, only a sequence of disconnected v1s stuck wherever they landed. Distribution is not one feature among many. It is the one that makes every other deferral real.

Imagine shipping a browser that cannot render a single webpage. Useless as a product, but not necessarily as a foundation: if it installs in one command and updates itself silently after that, every feature it is missing (rendering, JavaScript, bookmarks) is not a gap; it is a queue. The same logic holds for self-hosted software: get distribution and self-upgrade right first, and every feature after that is an iteration, not a redeployment.

[A cut is only a real deferral, not an accidental commitment, if there is a seam to grow it into later](/blog/2026/mvp-two-cuts/), and distribution with self-upgrade is the most basic seam there is: without it, there is no channel to deliver the deferred work through, and every "cut for the MVP" quietly becomes permanent. It is also the one cut that cannot itself be deferred: a distribution channel cannot ship through itself, so retrofitting one later costs a hand-coordinated migration for every install already in the field, exactly the cost it exists to remove.<d-footnote>"First" constrains the order, not the investment. For a product still validating itself with a single design partner, the channel can itself be an MVP, a manifest endpoint and a minimal self-updating client, and grow through its own upgrade path.</d-footnote>

**The distribution mechanism decides who controls the state of every deployed instance, and that control is what determines whether the fleet stays simple enough to change quickly, or decays into something nobody can touch without a support call.**

<div class="row mt-3 justify-content-center">
    <div class="col-md-10 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/ship-the-upgrade-path-first/dispatch-vs-checkin.jpg" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <b>Send someone to fix it, or let it check in.</b> Without a distribution channel, every change is a house call, one drifting install at a time. With one, every install converges on the current release by itself. Image generated with Google Gemini.
</div>

What follows first shows the failure modes when that control is lost, then one concrete way to keep it: a distribution API paired with a thin CLI.

## Where It Runs Is Not Who Controls It

Distribution usually gets discussed as a location question: SaaS or on-premises, hosted or self-hosted. That framing hides the variable that actually matters.

| Model                         | Where it runs           | Who controls deployed state | Iteration speed          |
| ----------------------------- | ----------------------- | --------------------------- | ------------------------ |
| SaaS, ad hoc                  | your infrastructure     | you, inconsistently         | medium, decays over time |
| SaaS, standardized (channel)  | your infrastructure     | you, via a control plane    | high                     |
| Raw-artifact self-hosted      | customer infrastructure | customer                    | low                      |
| Managed self-hosted (channel) | customer infrastructure | you, via a control plane    | high                     |

Iteration speed does not track where the software runs; it tracks whether a control plane keeps every instance converged. That is a design choice, separate from where the software executes, and it is the one that decides how fast you can move.

The self-hosted way of losing that control is worth making concrete: hand the customer a Docker Compose file (or a Helm chart, or an installer script) and a credential to pull your images. It is the fastest thing to build, and it is common enough that an entire commercial category, vendors like [Replicated](https://www.replicated.com/), exists to sell a better version of it to companies that got this far and hit a wall.

The crack in that wall is entropy. Once the deployment descriptor lives on the customer's machine, it is theirs to edit, and eventually they will: a tweaked port, a pinned old image, a config value nobody remembers setting. Multiply this across every customer and you no longer have one product running N times; you have N deployments in states nobody can fully describe. Every architectural change now needs to be coordinated by hand against those unknown states, so changes get deferred, workarounds accrete to avoid touching fragile installs, and [scrappiness quietly turns into unmanaged debt](/blog/2025/scrappiness-incentivizes-sloppiness/)<d-footnote>This is also a case where the damage is invisible until it isn't: a fleet that never drifted produces no incident to point to, so <a href="/blog/2026/we-reward-the-fix-not-the-prevention/">the discipline that prevented it rarely gets credited as the accomplishment it is</a>.</d-footnote>. [Deferring an architectural change under this kind of pressure is exactly how a deferral turns into an accidental, load-bearing commitment](/blog/2026/mvp-two-cuts/)<d-footnote>The credential handed out alongside the artifacts decays the same way and for the same reason: nobody is narrowing its scope or rotating it, so it stays broad and long-lived, exactly what security guidance recommends against <d-cite key="aws-iam-bestpractices"></d-cite>. A leaked key here is not a contained incident; it is a standing liability with no clean way to revoke just one customer's access.</d-footnote>.

This is not really about the artifacts themselves. Compose files and container images are fine. What is missing is an active party on the other end of the handoff, keeping state converged long after the install finished.

## A Problem Infrastructure Already Solved

Keeping many independently running copies of something converged on a known state is not a new problem, and cloud infrastructure has already spent a decade solving it.

A Kubernetes operator runs a reconciliation loop: it reads a declared desired state, compares it to what is actually running, and keeps nudging reality back toward the declaration <d-cite key="k8s-operator-pattern"></d-cite>. GitOps formalizes the same idea into four principles, one of them named outright: state must be _continuously reconciled_ <d-cite key="opengitops-principles"></d-cite><d-footnote>This post borrows the reconciliation part of that principle, not necessarily the continuity: the claim is that the update mechanism should be automated, not that it must run live or be vendor-triggered. A human can still decide when to run the CLI. Live, vendor-initiated reconciliation is a further, separate capability, one many regulated or customer-controlled environments do not permit at all.</d-footnote>, because agents that skip this step let the actual system drift out of line with the declared one, the same failure this post has been describing in customer fleets.

Distribution to customer environments is the same problem pointed outward. Instead of reconciling your own cluster against a declared state, you are reconciling every customer's install against a release you control. The fix is the same in spirit: do not hand over a static artifact and hope it stays correct. Build something that lets every deployment check in and stay converged. Build a **control plane**, not a one-time handoff.

## A Distribution Channel That Keeps Control

One way to build that control plane, abstracted from any specific implementation, splits cleanly into two pieces.

A **distribution API** is the only part that speaks business logic. A client authenticates to it<d-footnote>Reusing the customer's own identity provider to hand out short-lived tokens is a convenient way to do this without maintaining a separate credential store per customer.</d-footnote> and receives two things: a **release manifest**, a small piece of declarative data listing which container images and other artifacts make up the current release, and a **short-lived, scoped credential** for pulling exactly those images. Everything that might change, starting with what a release contains, lives server-side, where you can update it without touching a single deployed machine.

A **thin CLI** carries no business logic at all: it fetches the manifest, pulls the images and a channel-owned deployment descriptor (e.g., a Compose file or Helm chart)<d-footnote>The deployment descriptor is not itself a container image, but it does not need its own delivery path: it can ride along as an OCI artifact in the same registry, or live in a plain object store and be handed out as a pre-signed URL alongside the manifest. Either way, the same control-plane, data-plane split holds.</d-footnote>, manages a local configuration file that it owns, not one the customer hand-edits <d-cite key="twelvefactor-config"></d-cite>, and applies the descriptor to bring the release up. The client should be as replaceable and as boring as possible, because it is the one piece of code that has already left your control the moment it ships<d-footnote>Distributing the CLI itself can be much simpler than distributing the product: it carries no business logic and no secrets, so a public host like GitHub Releases can serve it directly, no distribution API or credential needed for that hop. A single static binary with no runtime to install is trivial to ship and self-update this way, common enough in the Go ecosystem to have dedicated tooling like <a href="https://goreleaser.com/">GoReleaser</a>. The release manifest can close the loop further, declaring the minimum CLI version a release requires so the client checks itself on every check-in.</d-footnote>.

An upgrade is nothing special in this design. The customer, or a scheduler they control, simply runs the same flow again, a **check-in**, and the install converges on whatever the manifest currently says.

**Thin client, fat server** is the principle underneath both choices, and it is the least obvious one worth naming directly: you cannot cheaply update code that runs where you do not control it, so the correct response is to minimize how much of it there is. Every unit of logic moved server-side is a unit of logic you can fix without a customer noticing.

<div class="row mt-3 justify-content-center">
    <div class="col-md-10 col-sm-12 mt-3 mt-md-0">
        {% include figure.liquid loading="eager" path="assets/img/posts/ship-the-upgrade-path-first/architecture.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <b>Control plane and data plane.</b> The thin CLI authenticates to the distribution API and receives a release manifest plus a short-lived, scoped credential. It then pulls images and the deployment descriptor directly from the registry, writes a local configuration file it owns, and brings the release up.
</div>

One detail explains a design choice that otherwise looks arbitrary: the API never serves the images itself. Large blobs belong in a **data plane** built for them, a registry <d-cite key="oci-distribution-spec"></d-cite> or an object store, while the API stays a **control plane** serving small, frequently changing metadata and handing out a credential scoped to exactly this pull <d-cite key="rfc8693"></d-cite>.

## What It Buys You

The payoff for engineering is the one this post has been arguing for throughout: a fleet that converges on every check-in is a fleet you can change.<d-footnote>A channel does not absolve releases from compatibility discipline; an upgrade still has to carry existing installs forward. What convergence changes is the scope of that discipline: each release migrates one known fleet state instead of N unknown ones.</d-footnote> Ship an architectural change once, to the manifest, and every install picks it up on its next check-in. No hand-coordinated rollout across N divergent configurations, no fleet nobody can touch without a support call.

The payoff for the business is the one Thiel's framing opened with. A working distribution channel is what lets self-hosted software stay **product-led** instead of quietly turning into a **services-led** business where every install needs a consultant. The distinction compounds: when upgrades are human work, every sale adds permanent operational load, and growth starts to scale with headcount instead of with software. Even SaaS only keeps that control by making the same design choice; running the servers yourself just makes drift easier to catch and correct. The harder, and more valuable, engineering problem is keeping control while the software runs on somebody else's infrastructure.

None of this is exotic. It recombines ideas infrastructure already trusts: reconciliation from Kubernetes, config-in-environment from twelve-factor apps, short-lived credentials from cloud security guidance, and manifest-plus-separate-artifacts from update frameworks like TUF <d-cite key="tuf-spec"></d-cite>. The only new part is pointing them outward, at infrastructure you do not own, instead of inward, at your own cluster.

I have built [a distribution channel along these lines](https://github.com/ethonAI/ethon-cli), in my case for the customer-installed edge components of a SaaS product, and it is a pattern others have landed on too<d-footnote>Siemens' Industrial Edge, for instance, lets you install and update its management platform on your own Kubernetes cluster through a single CLI, without ever touching a Helm chart directly <d-cite key="siemens-ieprovision"></d-cite>.</d-footnote>, one worth borrowing regardless of what you are shipping.

**Build the upgrade path first, and let it decide how much runway everything else gets.**

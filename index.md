---
layout: default
title: Home
description: A living record of our college dining research, decisions, and project work.
permalink: /
---

<section class="exhibit-hero" aria-labelledby="hero-title">
  <img class="exhibit-hero__image" src="{{ '/assets/images/campus-dining-work-session.jpg' | relative_url }}" alt="Meal containers, notebooks, and a campus map arranged on a dining table" width="1536" height="1024" fetchpriority="high">
  <div class="exhibit-hero__wash"></div>
  <div class="exhibit-hero__content">
    <p>CS 4390/5388 Software Project Management</p>
    <h1 id="hero-title">Meal plans that fit.</h1>
    <div class="exhibit-hero__actions"><a class="button button--orange" href="{{ '/sprints/sprint-1/' | relative_url }}">Explore the research</a><a class="button button--glass" href="{{ '/about/' | relative_url }}">Meet the team</a></div>
  </div>
</section>

<section class="signal-marquee" aria-label="Research areas">
  <div class="signal-marquee__track"><span>Menu accuracy</span><span>Dining hours</span><span>Sold-out items</span><span>Dietary information</span><span>Meal-plan value</span><span>Student workarounds</span><span aria-hidden="true">Menu accuracy</span><span aria-hidden="true">Dining hours</span><span aria-hidden="true">Sold-out items</span><span aria-hidden="true">Dietary information</span><span aria-hidden="true">Meal-plan value</span><span aria-hidden="true">Student workarounds</span></div>
</section>

<section class="sprint-accordion" aria-labelledby="sprint-heading">
  <header><h2 id="sprint-heading">Six sprints.<br>One evolving record.</h2><p>Select a sprint to see what the team has published so far.</p></header>
  <div class="sprint-accordion__items" data-sprint-accordion>
    <article class="sprint-slice is-open" data-sprint-slice>
      <button type="button" aria-expanded="true"><span>1</span><strong>Research foundation</strong><small>Current</small></button>
      <div class="sprint-slice__body"><h3>Research and project foundation</h3><p>Interview findings, the flexible meal-plan direction, business strategy, project charter, and retrospective.</p><ul><li>Market research</li><li>Top-pick deep dive</li><li>Business strategy</li><li>Project charter</li></ul><div class="sprint-slice__links"><a class="text-link" href="{{ '/sprints/sprint-1/' | relative_url }}">Open sprint 1</a><a class="text-link" href="{{ '/assets/pdfs/sprint-1-project-document.pdf' | relative_url }}" download>Download PDF</a></div></div>
    </article>
    {% for sprint in (2..6) %}<article class="sprint-slice" data-sprint-slice><button type="button" aria-expanded="false"><span>{{ sprint }}</span><strong>Sprint {{ sprint }}</strong><small>Planned</small></button><div class="sprint-slice__body"><h3>Sprint {{ sprint }}</h3><p>This record will be published after the sprint closes.</p><p class="empty-message">No project materials have been published for this sprint yet.</p></div></article>{% endfor %}
  </div>
</section>

<section class="research-intro">
  <p>Current research question</p>
  <h2>What happens when students cannot trust campus dining information?</h2>
  <div class="research-intro__visual"><img src="{{ '/assets/images/team-work-session.jpg' | relative_url }}" alt="Notebooks and laptops arranged for a campus dining research work session" width="1536" height="864" loading="lazy"></div>
  <div class="research-intro__copy"><p>The current phase broadens the investigation beyond price. The team is studying menu accuracy, unavailable food, location hours, allergies, dietary needs, and the workarounds students use when information fails.</p><div class="research-intro__links"><a class="text-link" href="#interview-method">See our interview method</a><a class="text-link" href="{{ '/assets/pdfs/sprint-1-project-document.pdf' | relative_url }}" download>Download Sprint 1 PDF</a></div></div>
</section>

<section id="interview-method" class="method-story">
  <div class="method-story__heading"><p>How we interview</p><h2>Ask about the last time, not the ideal future.</h2></div>
  <div class="method-stack">
    <article class="method-card"><span>Start with real behavior</span><h3>Talk about their life, not our idea.</h3><p>We do not pitch an app, website, meal plan, or proposed solution. We ask about a recent campus dining experience.</p></article>
    <article class="method-card"><span>Listen for evidence</span><h3>Concrete stories beat general opinions.</h3><p>Repeated problems, workarounds, consequences, and specific moments tell us more than compliments or hypothetical interest.</p></article>
    <article class="method-card"><span>Protect the research</span><h3>Record disconfirming evidence too.</h3><p>If someone has no problem, that belongs in the record. The conversation should never be forced toward the project idea.</p></article>
  </div>
</section>

<section class="team-roster" aria-labelledby="team-title">
  <header><h2 id="team-title">Four people share the work.</h2><p>Two profiles are confirmed in the current repository. Add the remaining names when the team is ready.</p></header>
  <div class="team-roster__grid">
    <article><div class="member-portrait"><span>ZC<br>Portrait pending</span></div><h3>Zachary Carrejo</h3><p>Market research, charter development, documentation, and Sprint 1 website content.</p></article>
    <article><div class="member-portrait"><span>SR<br>Portrait pending</span></div><h3>Salvador Rodarte</h3><p>Charter development, documentation, and development logging across sprints.</p></article>
    <article class="is-pending"><div class="member-portrait"><span>03<br>Portrait pending</span></div><h3>Team member</h3><p>Name, biography, role, and contribution statement to be added.</p></article>
    <article class="is-pending"><div class="member-portrait"><span>04<br>Portrait pending</span></div><h3>Team member</h3><p>Name, biography, role, and contribution statement to be added.</p></article>
  </div>
  <a class="text-link" href="{{ '/about/' | relative_url }}">View team profiles</a>
</section>

<section class="closing-action"><p>This page changes as the evidence changes.</p><h2>Follow the work, sprint by sprint.</h2><a class="button button--orange" href="{{ '/sprints/' | relative_url }}">Browse all sprints</a></section>

<aside class="disclosure"><strong>AI use disclosure</strong><p>AI tools support website design, development, and permitted grammar editing. The team authors the project research, analysis, and conclusions.</p></aside>

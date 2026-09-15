---
layout: default
title: Sprints
description: Browse each project sprint and its supporting documents.
permalink: /sprints/
---

<header class="page-intro"><p class="course-line">Project archive</p><h1>Six snapshots of a project in motion.</h1><p>Each sprint captures the team’s current evidence, decisions, deliverables, and reflection.</p></header>

<section class="sprint-index" aria-label="Sprint index"><a class="sprint-index__active" href="{{ '/sprints/sprint-1/' | relative_url }}"><span>Sprint 1</span><strong>Research and foundation</strong><small>Open sprint</small></a>{% for sprint in (2..6) %}<div class="sprint-index__planned"><span>Sprint {{ sprint }}</span><strong>Coming later</strong><small>Planned</small></div>{% endfor %}</section>

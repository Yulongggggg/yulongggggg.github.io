---
title: Yulong Liu
nav_title: About
nav: true
nav_order: 1
permalink: /
layout: page
hide_title: true
body_class: page-about
description: Cornell Ph.D. candidate working across computational geomechanics, poromechanics, reservoir simulation, and scientific machine learning.
---

<section class="home-hero">
  <div class="home-hero__copy">
    <h1 class="hero-name">Yulong<br>Liu</h1>
    <div class="intro-rule" aria-hidden="true"></div>
    <p class="hero-sub">Computational Geomechanics +<br>Scientific Machine Learning</p>
    <p class="hero-meta">Ph.D. candidate · Cornell University</p>
  </div>
  <img class="home-hero__mobile" src="{{ '/assets/img/cover-strata.png' | relative_url }}" alt="">
</section>

<section class="intro" aria-label="About">
  <div class="intro-main">
    <p class="intro-role">Earth and Atmospheric Sciences · Cornell University</p>
    <p class="intro-advisor">Minors in Computer Science and Scientific Computing · Advised by <a href="https://arsonlab.engineering.cornell.edu/" target="_blank" rel="noreferrer">Chloé Arson</a></p>
    <p class="intro-bio">
      I work at the intersection of computational geomechanics, poromechanics, reservoir simulation, and scientific machine learning. My research combines coupled multiphysics simulation of subsurface and reservoir systems with physics-informed neural networks, operator learning, and PDE-grounded verification of LLM-generated simulation code.
    </p>
    <p class="intro-links">
      <a href="mailto:yl3825@cornell.edu">Email</a>
      <a href="{{ '/assets/pdf/Yulong_Liu_CV.pdf' | relative_url }}?v={{ site.time | date: '%s' }}" target="_blank" rel="noreferrer">CV</a>
      <a href="https://scholar.google.com/citations?user=0CV0lsQAAAAJ&hl=en" target="_blank" rel="noreferrer">Google Scholar</a>
      <a href="https://github.com/Yulongggggg" target="_blank" rel="noreferrer">GitHub</a>
      <a href="https://www.linkedin.com/in/yulong-liu-19451a322/" target="_blank" rel="noreferrer">LinkedIn</a>
    </p>
  </div>
  <img class="intro-photo" src="{{ '/assets/img/yulong-liu-portrait.jpeg' | relative_url }}" alt="Portrait of Yulong Liu">
</section>

<section class="home-section" aria-label="Research interests">
  <div class="section-heading">
    <h2 class="section-title">Research interests</h2>
  </div>
  <div class="interest-grid">
    <div class="interest">
      <h3>Computational geomechanics</h3>
      <p>Coupled thermo-hydro-mechanical models of fractured rock, pressurized cavities, excavation, and reservoir systems using finite elements and MOOSE.</p>
    </div>
    <div class="interest">
      <h3>Scientific machine learning</h3>
      <p>Physics-informed neural networks, implicit neural representations, and operator learning for geometry-aware, physics-aware prediction.</p>
    </div>
    <div class="interest">
      <h3>Reservoirs &amp; porous media</h3>
      <p>Poromechanics, geothermal injection-production, fracture-controlled transport, and multiscale upscaling in porous subsurface media.</p>
    </div>
    <div class="interest">
      <h3>Reliable AI for simulation</h3>
      <p>PDE-grounded verification and LLM-based systems that reason about physical intent, not just syntactically valid simulation code.</p>
    </div>
  </div>
  <a class="text-route" href="{{ '/research/' | relative_url }}">Full research overview</a>
</section>

<section class="home-section" aria-label="Selected publications">
  <div class="section-heading">
    <h2 class="section-title">Selected publications</h2>
  </div>
  <ul class="home-pub-list">
    <li class="home-pub">
      <h3><a href="https://doi.org/10.1007/s00603-026-05882-5" target="_blank" rel="noreferrer">A Physics-Informed Neural Network for Pressurized Cavities of Arbitrary Shape in Heterogeneous Rock</a></h3>
      <p class="home-pub-authors"><strong>Yulong Liu</strong>, Chloé Arson</p>
      <p class="home-pub-venue">Rock Mechanics and Rock Engineering, 2026<span class="venue-tag venue-tag--journal">Journal</span></p>
    </li>
    <li class="home-pub">
      <h3><a href="https://arxiv.org/abs/2605.09360" target="_blank" rel="noreferrer">Your Simulation Runs but Solves the Wrong Physics: PDE-Grounded Intent Verification for LLM-Generated Multiphysics Simulation Code</a></h3>
      <p class="home-pub-authors"><strong>Yulong Liu</strong>, Zhenghan Song, et al.</p>
      <p class="home-pub-venue">arXiv preprint · under review at NeurIPS 2026<span class="venue-tag">Preprint</span></p>
    </li>
    <li class="home-pub">
      <h3><a href="{{ '/publications/' | relative_url }}">Operator Learning Surrogate Modeling of Hydraulically Fractured Geothermal Injection-Production Systems: A Cornell Case Study</a></h3>
      <p class="home-pub-authors"><strong>Yulong Liu</strong>, Jonah Botvinick-Greenhouse, Yunan Yang, Chloé Arson</p>
      <p class="home-pub-venue">ARMA 2026, Tucson<span class="venue-tag">Conference</span></p>
    </li>
  </ul>
  <a class="text-route" href="{{ '/publications/' | relative_url }}">All publications</a>
</section>

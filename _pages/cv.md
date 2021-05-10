---
layout: single
classes: wide
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
sidebar:
  - text: |
      ##### Download my CV here
      - [Français](/files/cv_une_page_fr.pdf)
      - [English](/files/CV_EN_single.pdf)
  # - title: "Degrees"
  # - text: |
  #     - PhD in Computer Science (*Informatique*), Université de Bordeaux, France, 2020
  #     - MSc in Electrical Engineering, Sub-field Computer Engineering, Unicamp, Brazil, 2016
  #     - BSc in Electrical Engineering, University of Campinas (Unicamp), Brazil, 2014
  #     - Diplôme d'ingenieur (~MEng), Télécom Paristech, France, 2013
  

---

<!-- {% include base_path %} -->

<!-- You can get one of my single-page CVs bellow:

* [CV en une page (en français)](/files/cv_une_page_fr.pdf)
* [One page CV (in english)](/files/CV_EN_single.pdf)

Or you can check my [linkedin profile](https://www.linkedin.com/in/{{site.author.linkedin }}). -->

<!-- Other than that, here goes a list of the activities I have registered here in this website. -->

## Degrees
* PhD in Computer Science (*Informatique*), Université de Bordeaux, France, 2020
* MSc in Electrical Engineering, Sub-field Computer Engineering, Unicamp, Brazil, 2016
* BSc in Electrical Engineering, University of Campinas (Unicamp), Brazil, 2014
* *Diplôme d'ingenieur* (~MEng), Télécom Paristech, France, 2013

## Employment
* Jan - Jun 2020: Temporary professor (ATER), Université de Bordeaux, France
* 2016 - 2020: Doctoral research contract, Mnemosyne Project-Team, Inria Bordeaux Sud-Ouest, France
* 2017 - 2019: Doctoral teaching assistant, Université de Bordeaux, France
* 2014 - 2016: Master's research contract, [FAPESP](https://fapesp.br/en/about) and University of Campinas, Brazil
* Aug 2012 - Jan 2013: Engineering Internship, [CEA LIST](http://www-list.cea.fr/en/discover-cea-list/qui-sommes-nous/overview), Gif-sur-Yvette, France

## Projects
  {% for post in site.projects reversed limit:3 %}
    {% include archive-single-cv.html %}
  {% endfor %}
  

[View more](/projects)

## Teaching
  {% for post in site.teaching reversed limit:3%}
    {% include archive-single-cv.html %}
  {% endfor %}


[View more](/teaching)

## Publications
  {% for post in site.publications reversed limit:3%}
    {% include archive-single-cv.html %}
  {% endfor %}


[View more](/publications)

## Talks
  {% for post in site.talks reversed limit:3%}
    {% include archive-single-cv.html %}
  {% endfor %}


[View more](/talks)

---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
excerpt: False
---


<!-- {% if author.googlescholar %} -->
<!-- {% endif %} -->

You can find my articles on <u><a href="https://scholar.google.com/citations?user=CKiUpv8AAAAJ">my Google Scholar profile</a>.</u>


{% include base_path %}

## Journal articles
{% for post in site.publications reversed %}
  {% if post.venuetype == 'journal' %}
    {% include archive-single.html %}
  {% endif%}
{% endfor %}

## Conference papers
{% for post in site.publications reversed %}
  {% if post.venuetype == 'proceeding' %}
    {% include archive-single.html %}
  {% endif%}
{% endfor %}

## Masters and PhD thesis
{% for post in site.publications reversed %}
  {% if post.venuetype == 'thesis' %}
    {% include archive-single.html %}
  {% endif%}
{% endfor %}

## Scientific and technical reports
{% for post in site.publications reversed %}
  {% if post.venuetype == 'repport' %}
    {% include archive-single.html %}
  {% endif%}
{% endfor %}

## Other publications
{% for post in site.publications reversed %}
  {% if post.venuetype == 'misc' %}
    {% include archive-single.html %}
  {% endif%}
{% endfor %}


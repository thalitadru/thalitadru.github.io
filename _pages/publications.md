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
{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}

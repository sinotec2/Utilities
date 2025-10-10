#!/bin/bash
for m in $(ls "*/*.md");do
  path=$(echo $m|cut -d'/' -f1)
  file=$(echo $m|cut -d'/' -f2)
  if [ $file == "_index.md"];then
    perma=/web_jokers/streamlit/develop/api-reference/$path
    sed -i 'd/
  fi
---
layout: default
title: API Reference
parent: Develop
grand_parent: streamlit
nav_order: 99
has_children: true
permalink: /web_jokers/streamlit/develop/api-reference
last_modified_date: 2025-01-15 08:09:26
tags: web
---


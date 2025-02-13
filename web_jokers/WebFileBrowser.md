---
layout: default
title: WebFileBrowser
parent: Web Jokers
nav_order: 99
last_modified_date: 2025-02-13 14:40:16
tags: web
---

#  Web File Browser
{: .no_toc }

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>
---

## 背景

## config init

### Synopsis

Initialize a new database to use with File Browser. All of this options can be changed in the future with the command 'filebrowser config set'. The user related flags apply to the defaults when creating new users and you don't override the options.

`filebrowser config init [flags]`

### Options

Name|Shorthand|Usage
-|:-:|-
addre|a|address to listen on
auth.header||HTTP header for auth.method=proxy
auth.method||authentication type
baseurl|b|base url
branding.disableExternal||disable external links such as GitHub links
branding.files||path to directory with images and custom styles
branding.name||replace 'File Browser' by this name
cert|t|tls certificate
commands||a list of the commands a user can execute
help|h|help for init
key|k|tls key
locale||locale for users
lockPassword||lock password
log|l|log output
perm.admin||admin perm for users
perm.create||create perm for users
perm.delete||delete perm for users
perm.download||download perm for users
perm.execute||execute perm for users
perm.modify||modify perm for users
perm.rename||rename perm for users
perm.share||share perm for users
port|p|port to listen on
recaptcha.host||use another host for ReCAPTCHA. recaptcha.net might be useful in China
recaptcha.key||ReCaptcha site key
recaptcha.secret||ReCaptcha secret
root|r|root to prepend to relative paths
scope||scope for users
shell||shell command to which other commands should be appended
signup|s|allow users to signup
sorting.asc||sorting by ascending order
sorting.by||sorting mode (name, size or modified)
viewMode||view mode for users

### Inherited

Name|Shorthand|Usage
-|:-:|-
config|c|config file path
database|d|database path


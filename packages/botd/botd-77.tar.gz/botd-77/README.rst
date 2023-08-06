README
######

**BOTD**

SYNOPSIS
========

botctl \<cmd\> \[key=value\] \[key==value\] 
    
DESCRIPTION
===========

**BOTD** is to achieve OS level integration of bot technology, a solid,
non hackable bot, that runs under systemd as a 24/7 background service.

INSTALL
=======

installation is through pypi or run python3 from the tarball (run
install_data as well).

::

 sudo pip3 install botd
 
CONFIGURATION
==============

to enable restarting of **BOTD** after reboot you need to enable it.

::

 sudo cp /usr/local/share/botd/botd.service /etc/systemd/system
 sudo systemctl enable botd --now

IRC
===

IRC configuration is done with the use of the botctl program, the cfg
command configures the IRC bot.

::

 sudo botctl cfg server=<server> channel=<channel> nick=<nick> 

default channel/server is #botd on localhost

SASL
====

some irc channels require SASL authorisation (freenode,libera,etc.) and
a nickserv user and password needs to be formed into a password. You can use
the pwd command for this

::

 sudo botctl pwd <nickservnick> <nickservpass>

after creating you sasl password add it to you configuration.

::

 sudo botctl cfg password=<outputfrompwd>

USERS
=====

if you want to restrict access to the bot (default is disabled), enable
users in the configuration and add userhosts of users to the database.

::

 sudo botctl cfg users=True
 sudo botctl met <userhost>

RSS
===

if you want rss feeds in your channel install feedparser.

::

 sudo apt install python3-feedparser

add a url to the bot and the feed fetcher will poll it every 5 minutes.

::

 sudo botctl rss <url>


COPYRIGHT
=========

**BOTD** is placed in the Public Domain, no Copyright, no LICENSE.

AUTHOR
======

Bart Thate

SEE ALSO
========

| https://pypi.org/project/botd

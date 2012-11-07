ok-qa - Open Knesset Question & Answers
======================================

This repository holds the code for `hasadna`_ project to support open Primary
election. The code contains a django project for a spcific party and allows
the party members to ask and upvote questions and for candidates to answer.

You are invited to fork the code, improve the design and send a pull request

.. _hasadna: http://hasadna.org.il

Quick Start
-----------

You can access the `live site`_ or if you're a Django developer, install
it on your local machine::

    $ mkvirtualenv --no-site-packages djangobench
    $ git clone https://github.com/hasadna/ok-qa.git
    $ cd ok-qa
    $ pip install -r requirements.txt
    $ python manage.py syncdb --migrate --noinput
    $ fab runserver

.. _live site: http://okqa.herokuapp.com

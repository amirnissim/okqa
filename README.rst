open-shot - Open Knesset Question & Answers
===========================================

This repository holds the code for `hasadna`_ project to support open Primary
election. The code contains a django project for a spcific party and allows
the party members to ask and upvote questions and for candidates to answer.

You are invited to fork the code, improve the design and send a pull request

.. _hasadna: http://hasadna.org.il

Quick Start
-----------

You can access the `dev site`_ or if you're a Django developer, install
it on your local machine::

    $ sudo pip install virtualenvwrapper
    $ mkvirtualenv oshot
    $ git clone https://github.com/hasadna/open-shot.git
    $ cd oshot
    $ pip install -r requirements.txt
    $ python manage.py syncdb --migrate --noinput
    $ python manage.py runserver

.. _dev site: http://oshot.hasadna.org.il

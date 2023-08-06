Slixmpp OMEMO plugin
####################

This library provides an interface to `python-omemo <https://github.com/syndace/python-omemo>`_.

License
-------

This plugin is licensed under GPLv3.

Note on the underlying OMEMO library
------------------------------------

As stated in `python-xeddsa's
README <https://github.com/Syndace/python-xeddsa/blob/136b9f12c8286b9463566308963e70f090b60e50/README.md>`_,
(dependency of python-omemo), this library has not undergone any
security audits. If you have the knowledge, any help is welcome.

Please take this into consideration when using this library.

Installation
------------

- ArchLinux (AUR):
   `python-slixmpp-omemo <https://aur.archlinux.org/packages/python-slixmpp-omemo>`_, or
   `python-slixmpp-omemo-git <https://aur.archlinux.org/packages/python-slixmpp-omemo-git>`_
- PIP: `slixmpp-omemo`
- Manual: `python3 setup.py install`

Examples
--------

The repository contains an example bot that contains many comments, and
can be used to test against other setups. To use it:

```
python examples/echo_bot.py --debug -j foo@bar -p passwd --data-dir /foo/bar
```

It also contains commands. Feel free to open merge requests or issues to
add new useful ones.

Credits
-------

For the help on OMEMO:

- Syndace
- Daniel Gultsch (`gultsch.de <https://gultsch.de/>`_)

And on Slixmpp:

- Mathieu Pasquet (`mathieui@mathieui.net <xmpp:mathieui@mathieui.net?message>`_)
- Emmanuel Gil Peyrot (`Link mauve <xmpp:linkmauve@linkmauve.fr?message>`_)

###################
CONFIGURATION
###################

Although `prefix` can be completely defined `on the fly` using ``**kwargs``,
frequently used prefixes should be declared in a configuration file located
at standard locations. Configuration file format may be

  - `yaml <https://yaml.org/spec/>`__
  - `toml <https://toml.io/en/>`__
  - `conf <https://docs.python.org/3/library/configparser.html>`__

********************************
Configuration Handling
********************************

Configuration is handled by `xdgpspconf <https://pradyparanjpe.gitlab.io/xdgpspconf/>`__


*********************
Configuration format
*********************

Sections:
==========

FLAGS
------

Following variables may be set as boolean values:

- ``short``: Information prefix is short (1 character).
- ``bland``: Information prefix lacks ansi style (color/gloss).
- ``iterate``: Resolve iterable object supplied as ``*args``.
- ``disabled``: Behave like python3 ``__builtins__.print``.
- ``pad``: Length of information prefix is fixed, padded with <*space*\ s> wherever necessary.
- ``flush``: This is passed to ``__builtins__.print``.

Following variables may be set to string values:

- ``pref_max``: Maximum length of prefix
- ``sep``: This is passed to ``__builtins__.print``.
- ``end``: This is passed to ``__builtins__.print``.
- ``file`` *Discouraged*: ``STDOUT`` gets appended to ``file``.

.. warning::

   Setting ``file`` in configuration may be risky as the file resource is opened out of context.

<``custom``>
-------------

The string ``custom`` (i.e. the name of section)
is used as prefix index while calling print function.

Following variables may be set as string names or integers
(ANSI Terminal colors) [black, red, g, 5, light blue]

- ``pref_color``: color of information prefix
- ``pref_bgcol``: background of information prefix
- ``text_color``: color of information text
- ``text_bgcol``: background of information text

Following variables may be set as strings or integers representing gloss
[dim, b, 2]

- ``pref_gloss``: brightness of information prefix
- ``text_gloss``: brightness of information text

Following variables may be set as str

- ``pref``: character long information prefix string (long form)
- ``pref_s``: 1 character information prefix (short form)

.. tip::

  *Remember to quote "" special characters* according to yaml/toml format specifications.

Example Configuration
------------------------

.. tabbed:: yaml

   .. code-block:: yaml
      :caption: style.yml or style.yaml or .psprintrc

      FLAGS:
        # short: False
        pad: True
        flush: True
        # sep:
        # end:
        pref_max: 7
        iterate: True

      help:
        pref: HELP
        pref_s: "?"
        pref_color: yellow
        pref_bgcol: black
        pref_style: normal
        text_color: white
        text_style: normal
        text_bgcol: black

.. tabbed:: toml

   .. code-block:: toml
      :caption: style.toml or .psprintrc

      [FLAGS]
      pad = true
      flush = true
      iterate = true

      [help]
      pref = "help"
      pref_s = "?"
      pref_color = "yellow"
      pref_bgcol = "terminal"
      pref_gloss = "dim"
      text_color = "terminal"
      text_gloss = "normal"
      text_bgcol = "terminal"

.. tabbed:: setup.cfg

   .. code-block:: ini
      :caption: style.conf or .psprintrc

      [FLAGS]
      pad = true
      flush = true
      iterate = true

      [help]
      pref = "help"
      pref_s = "?"
      pref_color = "yellow"
      pref_bgcol = "terminal"
      pref_gloss = "dim"
      text_color = "terminal"
      text_gloss = "normal"
      text_bgcol = "terminal"


.. tabbed:: pyproject.toml

   .. code-block:: toml
      :caption: pyproject.toml

      [psprint.FLAGS]
      pad = true
      flush = true
      iterate = true

      [psprint.help]
      pref = "help"
      pref_s = "?"
      pref_color = "yellow"
      pref_bgcol = "terminal"
      pref_gloss = "dim"
      text_color = "terminal"
      text_gloss = "normal"
      text_bgcol = "terminal"

.. tabbed:: setup.cfg

   .. code-block:: ini
      :caption: setup.cfg

      [psprint.FLAGS]
      pad = true
      flush = true
      iterate = true

      [psprint.help]
      pref = "help"
      pref_s = "?"
      pref_color = "yellow"
      pref_bgcol = "terminal"
      pref_gloss = "dim"
      text_color = "terminal"
      text_gloss = "normal"
      text_bgcol = "terminal"
      iterate = true

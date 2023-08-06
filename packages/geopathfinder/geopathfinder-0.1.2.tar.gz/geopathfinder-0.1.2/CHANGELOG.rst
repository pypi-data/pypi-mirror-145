=========
Changelog
=========

Version v0.1.2
==============

- logfiles are not anymore part of a yeoda_tree anymore, be default.
- reform on smart_tree.get_subtree_matching() and smart_tree.get_subtree_unique_rebased()

Version v0.1.1
==============

- fixed time retrieval bug in YeodaFilename

Version v0.1.0
==============

- yeoda_naming: logfiles folder is handled correctly


Version v0.0.7
==============

- introduces yeoda_naming
- allows flexible lenght filename parts
- fixes issued with python dependencies


Version v0.0.6
==============

- class restructuring to use the `from_filename` classmethod instead of always creating a new external parsing function
- minor restructuring of the existing file naming conventions
- added new file naming convention BMON
- minor bug removal

Version v0.0.5
==============

- new structure for 'naming_conventions' (implemented: SGRT, EODR)
- more options for en/decoding of filename fields.
- includes now file search and volume determination

Version v0.0.2
==============

- Switch to PyScaffold v2.5.11

Version v0.0.1
==============

- Add class SmartPath, SmartTree and SmartFilename
- Add class SgrtFilename and function yeoda_path
- Add unit tests

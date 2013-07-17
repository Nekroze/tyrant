Tyrant
------

A project manager that can handle automatic building, unit testing and
repository management in a simple CLI.

Tyrant is designed to be a one stop shop for setting up, managing, distributing
and generally developing (eventually) practically any programming project.

The first milestones/goals is to develop a configuration system for simple
informations on your project and a wrapper around git for managing the
repository.

In the future Tyrant will be able to manage any major DVCS repo and will have
an integrated way to build and or unittest each release with options to not
allow a new commit if a unit test fails or to report on the previous commits
unit test or build status for example.

The vision is for Tyrant to be a replacement for using many of the various
commands that comes with working on a modern project by wrapping them in a
single location. Once Tyrant is configured you can tell it to construct your
documentation, perform unit tests, build a release version and upload it along
with various other future features I have yet to even think of and of course
completely custom commands/features that anyone else can think of.

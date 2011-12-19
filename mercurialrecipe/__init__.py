"""
This recipe offers you an easy way to integration data from some Mercurial
repository into your buildout work-environment::

    [some_hg_dependency]
    recipe = mercurialrecipe
    repository = <REPOSITORY PATH/URL>

"""
import os
import shutil
import logging
from mercurial import commands, ui, hg


def get_repository(location):
    "Builds a Mercurial repository object out of the given location."
    return hg.repository(ui.ui(), location)


class Recipe(object):
    """
    This recipe supports following options:

    repository
        Path to the repository that should be cloned

    rev
        Revision that should be used. This is useful if you want to freeze
        the source at a given revision. If this is used, an update won't do
        all that much when executed.

    location
        optional, where it should clone the repo

    newest
        optional, if set than update is disabled
    """

    def __init__(self, buildout, name, options):#
        self.buildout, self.name, self.options = buildout, name, options
        self.options.setdefault('location',
            os.path.join(buildout.get('buildout') \
                .get('parts-directory'), name))
        self.rev = options.get('rev', None)
        self.source = self.options.get('repository')
        self.destination = self.options.get('location')
        self.newest = options.get('newest',
            buildout.get('buildout') \
                .get('newest', 'true')).lower() != 'false'
        self.as_egg = options.get('as_egg', 'false').lower() == 'true'
        self.log = logging.getLogger(name)

    def install(self):
        """
        Does the actual installation of this part.

        Be aware, that if the part was previously installed, it will
        get removed.
        """
        self.log.info("Cloning repository %s to %s" % (
            self.source, self.destination
        ))
        shutil.rmtree(self.destination, ignore_errors = True)
        commands.clone(ui.ui(), get_repository(self.source), self.destination)
        self.log.info("Updating to revision %s" % self.rev)
        if self.rev is not None:
            commands.update(ui.ui(), get_repository(self.destination), rev=self.rev)
            if self.as_egg:
                self._install_as_egg()
        return self.destination

    def update(self):
        """
        This method is run when a buildout environment should be updated. If
        the ``newest`` option is set, this will cause a pull from the upstream
        repository.
        """
        if self.rev is None and self.newest:
            self.log.info("Pulling repository %s and updating %s" % (
                self.source, self.destination
            ))
            commands.pull(ui.ui(), get_repository(self.destination),
                    self.source, update = True)
            if self.as_egg:
                self._install_as_egg()
        else:
            # "newest" is also automatically disabled if "offline"
            # is set.
            self.log.info("Pulling is disabled for this part")

    def _install_as_egg(self):
        """
        Install clone as development egg.
        """
        def _install(path, target):
            zc.buildout.easy_install.develop(path, target)

        target = self.buildout['buildout']['develop-eggs-directory']
        if self.paths:
            for path in self.paths.split():
                path = os.path.join(self.options['location'], path.strip())
                _install(path, target)
        else:
            _install(self.options['location'], target)

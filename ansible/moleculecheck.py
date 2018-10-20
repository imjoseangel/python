#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import imp
import os
import re
import subprocess
import sys

try:
    imp.find_module('git')
    import git
except ImportError as e:
    print("GitPython is not installed")
    sys.exit(1)


class moleculechecker():
    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.work_path = os.path.dirname(self.path)
        os.chdir(self.work_path)

    def dirpath(self):
        return (self.work_path)

    def __gitdownload(self):

        self.dirpath()
        repo = git.Repo()
        for item in repo.index.diff('origin/develop'):
            yield item.a_path

    def getroles(self):

        directories = list(self.__gitdownload())

        r = re.compile("roles/(.+?)/")
        newlist = set(list(filter(r.match, directories)))

        for item in newlist:
            roles = re.search(r"roles\/(.+?)\/", item)
            yield roles.group(1)


def main():
    getroles = moleculechecker()
    roles = (list(set(getroles.getroles())))
    work_path = getroles.dirpath()

    for role in roles:
        if os.path.exists(work_path + "/roles/%s/molecule" % role):
            os.chdir(work_path + "/roles/%s" % role)
            command = subprocess.call(['molecule', 'check'],
                                      stdin=None,
                                      stderr=subprocess.PIPE)
            if command != 0:
                sys.exit(1)
        else:
            pass


if __name__ == '__main__':
    main()

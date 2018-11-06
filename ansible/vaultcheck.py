#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)
import os
import sys
import re


class workpath():
    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.work_path = os.path.dirname(self.path)
        os.chdir(self.work_path)

    def dirpath(self):
        return (self.work_path)


def main():

    CRFAIL = "\033[91m"
    CEND = "\033[0m"

    # Sets default exit status code
    rc = 0

    myproject = workpath()
    work_path = myproject.dirpath()

    vaultpattern = re.compile(r"\$ANSIBLE_VAULT;\d\.\d;\w+")

    for dirpath, dirnames, filenames in os.walk(work_path):
        for filename in filenames:
            if filename.endswith('.vault'):
                vaultfile = open(os.path.join(dirpath, filename), 'r')
                vaulthead = vaultfile.readline()
                vaultfile.close()
                isvault = re.findall(vaultpattern, vaulthead)
                if not isvault:
                    print(CRFAIL +
                          "fail: [Unencrypted Vault] => (item=%s) \n" %
                          os.path.join(dirpath, filename) + CEND)
                    rc = 1

    sys.exit(rc)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# Copyright (c) 2018 The Unit-e developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import os
import re

"""A simple script that generates a TOC for all the ADRs"""


class HADRon:

    def __init__(self):
        pass

    def generate(self):

        toc_filename = "README.md"
        header = "| ADR | Title | Status | Created | Accepted |"
        sub_h = "|---|---|:---:|:---:|:---:|"

        lines = [header, sub_h]
        adrs = self.list_adrs()

        for adr in adrs:
            num = "[" + adr[:-3] + "](https://github.com/dtr-org/unit-e-docs/blob/master/adrs/" + adr + ")"
            with open(adr, "r") as file:
                title = ""
                status = ""
                created = ""
                accepted = ""
                complete = False
                for i in range(1, 10):
                    next_line = file.readline()

                    if not title and re.match("^# ADR-[0-9]*[: ].*$", next_line):
                        title = re.search("^# ADR-[0-9]*[: ](.*)$", next_line).group(1).strip()

                    if not status and re.match("^Status:.*$", next_line):
                        status = re.search("^Status:(.*)$", next_line).group(1).strip()

                    if not created and re.match("^Created:.*$", next_line):
                        created = re.search("^Created:(.*)$", next_line).group(1).strip()

                    if not accepted and re.match("^Accepted:.*$", next_line):
                        accepted = re.search("^Accepted:(.*)$", next_line).group(1).strip()
                        complete = True
                        break

                if not complete:
                    raise Exception("Cannot parse file: " + adr)

            new_entry = "|" + num + "|" + title + "|" + status + "|" + created + "|" + accepted + "|"
            lines.append(new_entry)

        with open(toc_filename, "w") as toc_file:
            for l in lines:
                toc_file.write(l + "\n")
            toc_file.close()

    def list_adrs(self):
        adrs = []
        for filename in os.listdir("."):
            if re.match("^ADR-[0-9]{4}\.md", filename):
                adrs.append(filename)

        adrs.sort(key=lambda a: int(re.search("^ADR-([0-9]{4})\.md", a).group(1)))
        return adrs


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    HADRon().generate()

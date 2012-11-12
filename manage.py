#!/usr/bin/env python
import os
import sys
from unipath import FSPath as Path

if __name__ == "__main__":

    sys.path.append(Path(__file__).absolute().ancestor(1).child('okqa'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "okqa.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

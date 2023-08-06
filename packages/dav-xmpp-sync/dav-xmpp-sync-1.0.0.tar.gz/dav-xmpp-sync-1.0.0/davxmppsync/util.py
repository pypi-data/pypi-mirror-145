#!/usr/bin/env python
# Written by Sumit Khanna
# License: AGPLv3
# https://battlepenguin.com
import re


def normalize_phone_numbers(number):
    return re.sub(r'[\s\(\)-]', '', number)

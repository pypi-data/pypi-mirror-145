# Written by Sumit Khanna
# License: AGPLv3
# https://battlepenguin.com

import requests
from requests.auth import HTTPBasicAuth
import sys
import re
from .__init__ import log
from .util import normalize_phone_numbers

DEFAULT_CATEGORY = 'Uncategorized'


def read_vcards(config):
    """Uses configuration to call vcard functions for retrival and decoding"""
    if 'vcards' in config and 'carddav' in config:
        log.error('You may specify either vcards or carddav, not both.')
        sys.exit(3)

    if 'carddav' in config:
        dav_config = config['carddav']
        default_category = dav_config.get('default_category')
        raw_cards = read_caldav(dav_config['url'], dav_config['username'], dav_config['password'])
    elif 'vcards' in config:
        file_config = config['vcards']
        raw_cards = read_vcardfile(file_config['file'])
        default_category = file_config.get('default_category')
    else:
        log.error('No contact retrieval defined in config. You must have a vcards or carddav section.')
        sys.exit(3)

    log.info(f"Default vCard category: {default_category}")
    card_split = split_all_vcards(raw_cards)
    # remove \r\n elements
    cards = [parsecard(c, default_category or DEFAULT_CATEGORY) for c in card_split]
    return cards


def read_caldav(url, username, password):
    """Step 1 called from read_vcards to read from CardDav server with authentication"""
    log.info(f'Requesting vCards From {url}')
    resp = requests.get(url, auth=HTTPBasicAuth(username, password))
    return resp.text


def read_vcardfile(file):
    """Step 1 called from read_vcards to read from file"""
    log.info(f'Loading vCards from {file}')
    with open(file, 'r') as fd:
        return fd.read()


def split_all_vcards(vcards):
    """Step 2: Split a long string from a file or HTTP request body into individual vcards"""
    if 'BEGIN:VCARD' not in vcards:
        log.error('No VCARDs found')
        log.debug(f'Document: {vcards}')
        sys.exit(2)
    else:
        raw_cards = re.split(r'END:VCARD(\r\n|\r|\n)BEGIN:VCARD', vcards)
        cards = []
        for c in raw_cards:
            ele = c.strip()
            if ele != '':
                cards.append(ele)
        return cards


def parsecard(card_string, default_category):
    """Step 3: Parse Individual Cards"""
    lines = card_string.splitlines()
    uid = [p for p in lines if p.startswith('UID')][0].split(':')[1]
    raw_numbers = [m for m in lines if m.startswith('TEL')]
    raw_cats = ([n for n in lines if n.startswith('CATEGORIES')] or [f':{default_category}'])[0].split(':')[1]
    cats = [c.strip() for c in raw_cats.split(',')]
    full_name = [o for o in lines if o.startswith('FN')][0].split(':')[1]
    numbers = {}
    for r in raw_numbers:
        num_type_match = re.search(r'TYPE=(.*?)[:;]', r)
        num_type = num_type_match.group(1) if num_type_match is not None else 'UNKNOWN'
        num = normalize_phone_numbers(r.split(':')[1])
        if num_type.lower() not in numbers:
            numbers[num_type.lower()] = []
        numbers[num_type.lower()].append(num)
    return {'uid': uid, 'numbers': numbers, 'full_name': full_name, 'tags': cats}


def filter_cards_with_numbers(all_cards, number_type):
    phone_cards = []
    for a in all_cards:
        if number_type not in a['numbers']:
            found_cats = list(a['numbers'].keys())
            if len(found_cats) > 0:
                log.warning(f"{a['full_name']} has no phone numbers of type {number_type}. Found: {list(a['numbers'].keys())}")
            else:
                log.warning(f"{a['full_name']} has no phone numbers")
        else:
            phone_cards.append(a)
    return phone_cards


def cards_by_category(cards):
    by_category = {}
    for c in cards:
        for t in c['tags']:
            if t not in by_category:
                by_category[t] = []
            by_category[t].append(c)
    return by_category


def cards_by_phone_number(cards, number_type_filter, number_prefix_filter):
    retval = {}
    for c in cards:
        if number_type_filter in c['numbers']:
            if number_prefix_filter is None or c['numbers'][number_type_filter][0].startswith(number_prefix_filter):
                retval[c['numbers'][number_type_filter][0]] = {'name': c['full_name'], 'groups': c['tags']}
    return retval

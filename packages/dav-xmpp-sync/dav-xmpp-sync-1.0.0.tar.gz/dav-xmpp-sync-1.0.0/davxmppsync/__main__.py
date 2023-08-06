#!/usr/bin/env python
# Written by Sumit Khanna
# https://battlepenguin.com/tech/moving-my-phone-number-from-google-hangouts-voice-to-an-sip-xmpp-service/
# License: AGPLv3
import yaml
import click
import logging
import sys
from rich.table import Table
from rich.console import Console
import time
from .__init__ import log
from .output import print_cards, print_cat_counts
from .xmpp import xmpp_client, update_roster
from .carddav import read_vcards, filter_cards_with_numbers, cards_by_phone_number, \
    cards_by_category
from .validator import validate_config


def load_config(config_file):
    with open(config_file, 'r') as fd:
        y_config = yaml.safe_load(fd)
    return y_config


@click.group()
@click.option('--config', default='config.yaml', help='Configuration YAML File')
@click.option('--dry-run', is_flag=True, default=False, help='Do not perform updates')
# Not yet implemented
# @click.option('--deletes', is_flag=True, default=False, help='Delete phone numbers in managed groups that are not in contacts')
@click.option('--verbose/--silent', default=False, help='Additional diagnostics and logging')
@click.pass_context
def main(ctx, config, dry_run, verbose):
    ctx.ensure_object(dict)
    ctx.obj['config'] = load_config(config)
    if not validate_config(ctx.obj['config']):
        sys.exit(2)
    ctx.obj['dry_run'] = dry_run

    if verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)


@main.command()
@click.pass_context
def sync(ctx):
    """Syncs CardDav contacts to XMPP server once and exits"""
    syn_config = ctx.obj['config']['sync']
    x_config = ctx.obj['config']['xmpp']

    all_cards = read_vcards(ctx.obj['config'])
    with_number = filter_cards_with_numbers(all_cards, syn_config['number_type'])
    by_phone_number = cards_by_phone_number(with_number, syn_config['number_type'], syn_config.get('number_prefix', None))

    managed_categories = list(cards_by_category(all_cards).keys())
    log.info(f'Managed Groups {managed_categories}')

    con = xmpp_client(x_config)
    update_roster(ctx.obj['dry_run'], con, by_phone_number, syn_config['gateway_domain'], managed_categories)


@main.command()
@click.option('--interval', envvar='INTERVAL', default=900, help='Interval between syncing in seconds')
@click.pass_context
def service(ctx, interval):
    """Syncs contacts continually at the configured interval"""
    while True:
        ctx.invoke(sync)
        log.info(f'Waiting {interval} seconds')
        time.sleep(interval)


@main.command()
@click.pass_context
def contacts(ctx):
    all_cards = read_vcards(ctx.obj['config'])
    print_cards(all_cards)


@main.command()
@click.pass_context
def categories(ctx):
    all_cards = read_vcards(ctx.obj['config'])
    card_cats = cards_by_category(all_cards)
    print_cat_counts(card_cats)


@main.command()
@click.pass_context
def roster(ctx):
    x_config = ctx.obj['config']['xmpp']
    syn_config = ctx.obj['config']['sync']
    con = xmpp_client(x_config)
    roster_obj = con.getRoster()
    raw_roster = roster_obj.getRawRoster()

    table = Table(title='XMPP Roster')
    table.add_column('Name')
    table.add_column('Numbers')
    table.add_column('Subscription')
    table.add_column('Groups')

    for num, data in raw_roster.items():

        g = data['groups'] if data['groups'] else []

        # Show the gateway domain transport account
        if num.endswith(syn_config['gateway_domain']) and num != syn_config['gateway_domain']:
            n = num.rstrip(f"@{syn_config['gateway_domain']}")
        else:
            n = num

        if data['subscription'] == 'both':
            sub = '[green]both[/green]'
        elif data['subscription'] == 'none':
            sub = '[red]none[/red]'
        else:
            sub = data['subscription']

        table.add_row(data['name'], n, sub, ','.join(g))
    console = Console()
    console.print(table)


if __name__ == '__main__':
    main()

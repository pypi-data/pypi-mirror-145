from .__init__ import log
import xmpp


def new_groups(dav_groups, xmpp_groups, managed_groups):
    """Resolves CardDav groups with those that are managed.
       We want to managed adding and deleting from categories defined in CardDav,
       but not remove people from XMPP groups, such as if someone creates a group
       such as "Recent" or "Favourites," to be managed outside their contacts.
    """
    unmanaged = [x for x in xmpp_groups if x not in managed_groups]
    return dav_groups + unmanaged


def update_roster(dry_run, xmpp_conn, cards_by_number, gateway_domain, managed_groups):

    at_gw_domain = f'@{gateway_domain}'
    dry_msg = '(DRYRUN) ' if dry_run else ''

    roster_obj = xmpp_conn.getRoster()
    raw_roster = roster_obj.getRawRoster()
    filtered_roster = {k: v for k, v in raw_roster.items() if k.endswith(gateway_domain)}

    for number, info in cards_by_number.items():
        new_jid = f'{number}{at_gw_domain}'
        if new_jid not in filtered_roster:
            log.info(f"{dry_msg}Adding {info['name']} ({number})")
            if not dry_run:
                roster_obj.Subscribe(new_jid)
                roster_obj.Authorize(new_jid)
        else:
            log.debug(f"Contact {info['name']} ({number}) exists on XMPP Server")

    for num, data in filtered_roster.items():
        if data['subscription'] != 'both':
            log.info(f"{dry_msg}Subscribing {num}")
            if not dry_run:
                roster_obj.Subscribe(num)
                roster_obj.Authorize(num)

    for jid, data in filtered_roster.items():
        if jid.endswith(at_gw_domain):
            phone = jid.rstrip(at_gw_domain)
            if phone not in cards_by_number:
                log.info(f'{phone} Not Found in Address Book')
            else:
                cur_card = cards_by_number[phone]
                updated_name = cur_card['name']
                update_groups = new_groups(cur_card['groups'], data['groups'], managed_groups)
                do_update = False
                if cards_by_number[phone]['name'] != data['name']:
                    log.info(f'{dry_msg}Updating {phone}. Setting name to {updated_name}')
                    do_update = True
                if not set(update_groups) == set(data['groups']):
                    log.info(f"{dry_msg}Updating groups for {cur_card['name']} to {update_groups}")
                    do_update = True
                if do_update and not dry_run:
                    roster_obj.setItem(jid, name=updated_name, groups=update_groups)


def xmpp_client(x_config):
    jid = xmpp.protocol.JID(x_config['jid'])
    con = xmpp.Client(server=jid.getDomain(), debug=[])
    con.connect()
    con.auth(jid.getNode(), x_config['password'])
    return con

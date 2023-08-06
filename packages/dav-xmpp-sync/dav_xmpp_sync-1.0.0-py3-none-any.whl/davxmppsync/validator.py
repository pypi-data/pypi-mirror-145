from .__init__ import log
from urllib.parse import urlparse


def uri_validator(x):
    """Validate URLs. See: https://stackoverflow.com/a/38020041/696836"""
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def require_all(section, lst, config):
    errors = ""
    if section not in config:
        errors.append(f'{section}: section required')
    else:
        for li in lst:
            if li not in lst:
                errors.append(f"{section}:{lst} required")
    return errors


def validate_config(config):
    errors = []
    if 'carddav' in config and 'vcards' in config:
        errors.append('You must specify carddav or vcards, not both.')
    if 'carddav' in config:
        errors += require_all('carddav', ['username', 'password', 'url'], config)

    errors += require_all('xmpp', ['jid', 'password'], config)
    errors += require_all('sync', ['number_type', 'number_prefix', 'gateway_domain'], config)

    if 'carddav' in config:
        carddav = config['carddav']
        if not uri_validator(carddav['url']):
            errors.append(f"Invalid carddav URL {carddav['url']}")

    if 'debug' in config['xmpp']:
        if type(config['xmpp']['debug']) != bool:
            errors.append('xmpp:debug must be True or False')

    if len(errors) > 0:
        for error in errors:
            log.fatal(error)
        return False
    else:
        return True

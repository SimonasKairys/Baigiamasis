import logging, httpagentparser
from datetime import datetime

logger = logging.getLogger(__name__)


def add_ip_and_browser(request):
    browser_info = request.META['HTTP_USER_AGENT']
    ip_address = get_client_ip(request)
    return {'browser_info': browser_info, 'ip_address': ip_address}


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_ip_and_browser(request):
    user_agent = request.META['HTTP_USER_AGENT']
    parsed_ua = httpagentparser.simple_detect(user_agent)
    ip_address = get_client_ip(request)

    logger.info(f'Timestamp: {datetime.now()} - IP Address: {ip_address} - Browser Info: {parsed_ua}')

    return {'browser_info': parsed_ua, 'ip_address': ip_address}

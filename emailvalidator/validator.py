"""
Initialize the emailvalidator django application, and configure
"""
import re
from .models import EmailRegExValidator, EmailDomainGroup


def is_email_valid(email):
    """
    Determines if the provided email is valid based on the regular expressions
    stored in the database.
    """
    validators = EmailRegExValidator.objects.all()
    regexes = [re.compile(r.regex) for r in validators]
    return any(regex.match(email) for regex in regexes)


def get_email_groups(email):
    """
    Returns an array of groups the provided email address matches.
    """
    validators = EmailRegExValidator.objects.all()
    group_regexes = [(re.compile(r.regex), r.group) for r in validators]
    return [group for regex, group in group_regexes if regex.match(email)]


def is_email_in_group(email, group):
    """
    Returns true if the specified email address successfully passes validation
    for the named group.
    """
    try:
        domain_group = EmailDomainGroup.objects.get(name=group)
        validators = EmailRegExValidator.objects.filter(group=domain_group)
        regexes = [re.compile(r.regex) for r in validators]
        return any(regex.match(email) for regex in regexes)
    except EmailDomainGroup.DoesNotExist:
        return False


AUTH_LDAP_SERVER_URI = 'ldap://ldapmas.fh-weingarten.de'

AUTH_LDAP_USER_DN_TEMPLATE = 'uid=%(user)s,ou=People,dc=fh-weingarten,dc=de'
AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
}

AUTH_LDAP_GROUP_SEARCH = LDAPSearch('ou=Group,dc=fh-weingarten,dc=de',
    ldap.SCOPE_SUBTREE, '(objectClass=posixGroup)')
AUTH_LDAP_GROUP_TYPE = PosixGroupType()
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CACHE_GROUPS = True

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

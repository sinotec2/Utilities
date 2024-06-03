
# settings.py
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

AUTH_LDAP_SERVER_URI = "ldap://your-ldap-server.com"
AUTH_LDAP_BIND_DN = "cn=admin,dc=example,dc=com"
AUTH_LDAP_BIND_PASSWORD = "yourpassword"
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    "ou=users,dc=example,dc=com",
    ldap.SCOPE_SUBTREE,
    "(uid=%(user)s)",
)

# Optionally configure group search and member membership
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    "ou=groups,dc=example,dc=com",
    ldap.SCOPE_SUBTREE,
    "(objectClass=groupOfNames)"
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()
AUTH_LDAP_REQUIRE_GROUP = "cn=required_group,ou=groups,dc=example,dc=com"
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=active_group,ou=groups,dc=example,dc=com",
    "is_staff": "cn=staff_group,ou=groups,dc=example,dc=com",
    "is_superuser": "cn=superuser_group,ou=groups,dc=example,dc=com",
}


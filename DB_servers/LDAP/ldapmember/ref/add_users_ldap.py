import ldap
import os, sys, subprocess

def add_user_ldap(lst):
    username, password, department=lst[:]
    # LDAP 伺服器設定
    domain='sinotech-eng'
    ext='com'
    base="dc="+domain+',dc='+ext
    ldap_server = "ldap://node03."+domain+'.'+ext":389"
    bind_dn = "cn=admin,"+base
    bind_password = "sino2024"
    dpt_gid={"y"+str(i):[str(500+i).encode('utf-8')] for i in range(1,7)}

    cmd_base='ldapsearch -x -H ' + ldap_server + ' -D "' + bind_dn + '" -w "' + bind_password + '" -b "' + base
    cmd=cmd_base + '" -LLL "(objectClass=posixAccount)" uid|grep uid|~/bin/awkk 2'
    users=subprocess.check_output(cmd,shell=True).decode('utf8').strip('\n').split()
    cmd=cmd_base + '" -LLL "(objectClass=posixAccount)" uidNumber|grep uidNumber|~/bin/awkk 2'
    unumb=subprocess.check_output(cmd,shell=True).decode('utf8').strip('\n').split()
    cmd=cmd_base + '" -LLL "(objectClass=posixAccount)" gidNumber|grep gidNumber|~/bin/awkk 2'
    gnumb=subprocess.check_output(cmd,shell=True).decode('utf8').strip('\n').split()
    usr_uid={i:j for i,j in zip(users,unumb)}
    usr_gid={i:j for i,j in zip(users,gnumb)}

    user_dn = "uid={},cn=users,cn=accounts,dc=example,dc=com".format(username)
    user_attrs = [('userPassword', [password.encode('utf-8')])]
    if username in users:
        if department[-1:]!=usr_gid[username][-1:]: 
            user_attrs += [('gidNumber', dpt_gid[department])]
    else:
        # 新使用者的 DN
    # 使用者屬性，這裡假設使用 'ou' 作為部門的屬性
        mx_uid=max([int(i) for i in unumb])
        user_attrs = [
        ('objectClass', [b'inetOrgPerson', b'posixAccount']),
        ('uid', [username.encode('utf-8')]),
        ('uidNumber', [str(mx_uid+1).encode('utf-8')]),
        ('gidNumber', dpt_gid[department]),
        ('cn', [username.encode('utf-8')]),
        ('sn', [username.encode('utf-8')]),
        ('userPassword', [password.encode('utf-8')]),
        ('ou', [b'People']),  # 部門屬性
        ('homeDirectory', [b'/home/{}'.format(username).encode('utf-8')]),  # homeDirectory 屬性
        # 其他屬性可根據需要添加
    ]

    try:
        # 連接 LDAP 伺服器
        ldap_conn = ldap.initialize(ldap_server)
        ldap_conn.simple_bind_s(bind_dn, bind_password)

        # 新增使用者
        ldap_conn.add_s(user_dn, user_attrs)
        print(f"User {username} added successfully.")

    except ldap.LDAPError as e:
        print(f"LDAP Error: {e}")

    finally:
        ldap_conn.unbind()

# 新增使用者到 'Sales' 部門
#add_user_ldap("newuser", "newpassword", "Sales")
add_user_ldap(sys.argv[1:])

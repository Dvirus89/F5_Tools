#!/bin/bash

# DO installation commands from udf-quick-start
curl -L -o /var/config/rest/downloads/f5-declarative-onboarding-1.47.0-14.noarch.rpm https://github.com/F5Networks/f5-declarative-onboarding/releases/download/v1.47.0/f5-declarative-onboarding-1.47.0-14.noarch.rpm
FN=f5-declarative-onboarding-1.47.0-14.noarch.rpm
CREDS=admin:ilovesleep
IP=127.0.0.1
DATA="{\"operation\":\"INSTALL\",\"packageFilePath\":\"/var/config/rest/downloads/$FN\"}"
curl -kvu $CREDS "https://$IP/mgmt/shared/iapp/package-management-tasks" -H "Origin: https://$IP" -H 'Content-Type: application/json;charset=UTF-8' --data $DATA

# Ask for license key
read -p "Please enter the license key for BIGIP 2: " LICENSE_KEY < /dev/tty

# Wait for DO to be ready
echo "Waiting for DO to be ready..."
sleep 10

# Create do.json for BIGIP 2
cat <<EOF > do.json
{
    "schemaVersion": "1.0.0",
    "class": "Device",
    "async": true,
    "label": "my BIG-IP declaration for declarative onboarding",

    "Common": {
        "class": "Tenant",

        "mySystem": {
            "class": "System",
            "hostname": "bigip2.example.com",
            "cliInactivityTimeout": 12000,
            "consoleInactivityTimeout": 12000,
            "autoPhonehome": false
        },
        "myLicense": {
            "class": "License",
            "licenseType": "regKey",
            "regKey": "$LICENSE_KEY"
        },
        "myDns": {
            "class": "DNS",
            "nameServers": ["8.8.8.8"],
            "search": ["f5.com"]
        },

        "myNtp": {
            "class": "NTP",
            "servers": [
                "0.pool.ntp.org",
                "1.pool.ntp.org",
                "2.pool.ntp.org"
            ],
            "timezone": "UTC"
        },

        "guestUser": {
            "class": "User",
            "userType": "regular",
            "password": "guestNewPass1",
            "partitionAccess": {
                "Common": {
                    "role": "guest"
                }
            }
        },

        "admin": {
            "class": "User",
            "userType": "regular",
            "password": "ilovesleep",
            "shell": "bash"
        },

        "myProvisioning": {
            "class": "Provision",
            "ltm": "nominal",
            "gtm": "nominal"
        },

        "internal": {
            "class": "VLAN",
            "tag": 4093,
            "mtu": 1500,
            "interfaces": [
                { "name": "1.1", "tagged": false }
            ]
        },

        "internal-self": {
            "class": "SelfIp",
            "address": "10.1.10.102/24",
            "vlan": "internal",
            "allowService": "default",
            "trafficGroup": "traffic-group-local-only"
        },

        "internal-floating": {
            "class": "SelfIp",
            "address": "10.1.10.100/24",
            "vlan": "internal",
            "allowService": "default",
            "trafficGroup": "traffic-group-1"
        },

        "external": {
            "class": "VLAN",
            "tag": 4094,
            "mtu": 1500,
            "interfaces": [
                { "name": "1.2", "tagged": false }
            ]
        },

        "external-self": {
            "class": "SelfIp",
            "address": "10.1.20.102/24",
            "vlan": "external",
            "allowService": "none",
            "trafficGroup": "traffic-group-local-only"
        },

        "external-floating": {
            "class": "SelfIp",
            "address": "10.1.20.100/24",
            "vlan": "external",
            "allowService": "default",
            "trafficGroup": "traffic-group-1"
        },

        "default": {
            "class": "Route",
            "gw": "10.1.10.1",
            "network": "default",
            "mtu": 1500
        },

        "managementRoute": {
            "class": "ManagementRoute",
            "gw": "192.0.2.4",
            "network": "192.0.2.1",
            "mtu": 1500
        },

        "dbvars": {
            "class": "DbVariables",
            "ui.advisory.enabled": true,
            "ui.advisory.color": "green",
            "ui.advisory.text": "bigip2"
        },

        "configsync": {
            "class": "ConfigSync",
            "configsyncIp": "/Common/internal-self/address"
        },

        "failoverAddress": {
            "class": "FailoverUnicast",
            "address": "/Common/internal-self/address"
        },

        "failoverGroup": {
            "class": "DeviceGroup",
            "type": "sync-failover",
            "members": [
                "bigip1.example.com",
                "bigip2.example.com"
            ],
            "owner": "/Common/failoverGroup/members/0",
            "autoSync": true,
            "saveOnAutoSync": false,
            "networkFailover": true,
            "fullLoadOnSync": false,
            "asmSync": false
        },

        "trust": {
            "class": "DeviceTrust",
            "localUsername": "admin",
            "localPassword": "ilovesleep",
            "remoteHost": "10.1.10.101",
            "remoteUsername": "admin",
            "remotePassword": "ilovesleep"
        }
    }
}
EOF

# DO Post with curl
curl http://127.0.0.1/mgmt/shared/declarative-onboarding --basic -u "admin:ilovesleep" -X POST -d @do.json

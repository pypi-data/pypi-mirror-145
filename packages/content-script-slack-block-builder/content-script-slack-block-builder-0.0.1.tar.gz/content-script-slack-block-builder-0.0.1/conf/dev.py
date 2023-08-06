#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
# @Filename : dev
# @Date : 2021-12-17-21-21
# @Project: content-service-chat-assistant

ENV = "dev"
MONGODB = {
    "host": "phll41000026d.amer.global.corp.sap",
    "port": "27017",
}

MONGODB_SOURCE = {
    "CUSTOMER": {
        "type": "api",
        "url": "https://iops.azure-api.net/cis-prod/cosmos/CCv2DB"
    }
}

VAULT = {
    "host": "https://vault.tools.sap/",
    "namespace": "ccoio/projects/cx-chatbot/",
    "approle_mount_point": "botuser"
}

SLACK_NOTIFICATION_LIST = [
    "W01AG1MNWHW"
]

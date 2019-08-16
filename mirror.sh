#!/usr/bin/env bash
set -ex

# 换源
cp /var/www/flask_bbs/misc/sources.list /etc/apt/sources.list
mkdir -p /root/.pip
cp /var/www/flask_bbs/misc/pip.conf /root/.pip/pip.conf
apt-get update
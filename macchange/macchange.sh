#!/bin/sh

echo "Current $1 MAC:"
ifconfig $1 |grep ether

mac=`openssl rand -hex 6 | sed 's/\(..\)/\1:/g; s/.$//'`
sudo ifconfig $1 ether $mac

echo "New $1 MAC:"
ifconfig $1 |grep ether

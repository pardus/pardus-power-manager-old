#!/bin/bash
ps aux | grep /usr/bin/pardus-power-manager | grep -v grep | cut -d ' ' -f 5 | xargs kill -9 || true
exec pardus-power-manager show
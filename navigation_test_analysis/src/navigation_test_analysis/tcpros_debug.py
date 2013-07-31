#!/usr/bin/env python
f = '/share/uhr-se/tcpros_error.bag'
o = '/share/uhr-se/tcpros_fixed.bag'
from rosbagPatcher.rosbagPatcher import BagFilePatcher
patcher = BagFilePatcher( f, o )
patcher.patch()

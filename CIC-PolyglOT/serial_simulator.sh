#!/bin/bash
sudo socat pty,raw,echo=1,link=/dev/ttyS0 pty,raw,echo=1,link=/dev/ttyS1
sudo socat pty,raw,echo=1,link=/dev/ttyS2 pty,raw,echo=1,link=/dev/ttyS3

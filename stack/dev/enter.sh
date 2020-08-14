#!/bin/bash

# create matching user if user does not exist (just do this once per user)
if ! id "$1" > /dev/null 2>&1; then

    # create user
    useradd -s /bin/bash -u $2 $1 -m
    adduser $1 sudo
    echo "$1 ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

    # add python user bin to PYTHONPATH
    su $1 -c 'echo "export PATH=$HOME/.local/bin:$PATH" >> ~/.bashrc'

    # set default workdir
    su $1 -c 'echo "cd /rested" >> ~/.bashrc'

    # install in editable mode
    su $1 -c 'pip install --user -e /rested'
fi

su $1

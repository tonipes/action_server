#!/usr/bin/env python

import sys
import getopt
import yaml
import falcon

from server import Server

default_config = 'config_server.yml'
default_action = 'config_action.yml'

opt_arr = ['actions=', 'config=',]
opt_str = ''

def usage():
    pass

def main(args):
    config_file = args.get('--config', default_config)
    action_file = args.get('--actions', default_action)

    with open(config_file, 'r') as f:
        config = yaml.load(f)
    with open(action_file, 'r') as f:
        actions = yaml.load(f)
    try:
        server = Server(config, actions)
        server.start()
    except (KeyboardInterrupt, SystemExit):
        server.stop()
        print("Shutting down")

if __name__ == "__main__":
    try:
        opt, rem = getopt.getopt(sys.argv[1:], opt_str, opt_arr)
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    arg_dict = dict(opt)
    main(arg_dict)

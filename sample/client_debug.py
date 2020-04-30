# -*- coding: utf-8 -*-
"""
This sample is designed for client module debugging.

Prepare for Beebotte access information in a config file, which includes:
    channel_token : str
        Channel token.
    ca_cert : str
        Path to a SSL server certificate.
    topic_base : str
        Topic name, i.e., 'channel/resource'.
        None to use non-SSL connection.
and specify the config file with -c option.
"""

#
# Copyright (c) 2020, Shigemi ISHIDA
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import mqbeebotte

#==========================================================================
# argument parser
def arg_parser():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--conffile", type=str, action="store",
                    default="config.py",
                    help="config file (default: config.py)",
                    )
    return ap

#---------------------------------------------------------------------------
# load any class file
def load_class(class_file):
    import os
    import sys
    import importlib
    # add class file path to import path
    base_path = os.path.dirname(class_file)
    base_file, base_ext = os.path.splitext(os.path.basename(class_file))
    sys.path.append(base_path)
    base_name = base_file.split("_")[:2]

    return importlib.import_module(base_file)

#==========================================================================
if __name__ == '__main__':
    import sys
    import time
    import re

    # setup logger
    from logging import getLogger, StreamHandler, Formatter
    from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG
    logger = getLogger(__name__)
    log_handler = StreamHandler()
    log_handler.setLevel(DEBUG)
    log_handler.setFormatter(Formatter(
        '%(asctime)s.%(msecs)03d [%(levelname)s] (%(name)s:%(process)d) '+ '%(message)s',
        '%Y-%m-%dT%H:%M:%S'
        ))
    logger.addHandler(log_handler)
    logger.setLevel(DEBUG)

    # add a log handler to a client class to derive debug messages
    mqbeebotte.client.logger.addHandler(log_handler)
    mqbeebotte.client.logger.setLevel(DEBUG)

    # parse arguments
    parser = arg_parser()
    args = parser.parse_args()

    # load config file
    try:
        config = load_class(args.conffile)
    except ImportError:
        logger.critical('cannot find config file {}'.format(args.conffile))
        sys.stderr.write('Error: config file {} not found"\n'.format(args.conffile))
        sys.exit(1)

    # make a list of parameters in config file
    param_names = list(config.__dict__.keys())
    param_names.sort()
    param_names = list(filter(
        lambda x: re.match(r'^[^_]', x),
        param_names
        ))

    # extract config
    host = config.host if 'host' in param_names else None
    port = config.port if 'port' in param_names else None
    ca_cert = config.ca_cert if 'ca_cert' in param_names else None

    # create a client instance
    client = mqbeebotte.client(host, port, ca_cert)
    client.connect(config.channel_token)
    client.start()

    client.subscribe(config.topic_base + '/test/#')
    while True:
        try:
            time.sleep(5)
            client.publish(config.topic_base + '/test/2', 'test message 2')
            client.publish(config.topic_base + '/test/3', 'test message 3')
        except KeyboardInterrupt:
            logger.info("Stop requested.")
            break

    logger.info("Stopping...")
    client.stop(block_wait=True)
    del client

# -*- coding: utf-8 -*-
"""
This sample is designed for client module debugging.

Prepare for Beebotte access information in the config file 'config.py'
including:
    channel_token : str
        Channel token.
    ca_cert : str
        Path to a SSL server certificate.
    topic_base : str
        Topic name, i.e., 'channel/resource'.
        None to use non-SSL connection.
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

import time
import mqbeebotte

#=========================================================================
# This sample comes with config.py.
# Please modify config.py before executing this sample.
#=========================================================================
def on_connect(client, userdata, flags, respons_code):
    print('Connected to Beebotte')
    return

#--------------------------------------------------------------------------
def on_message(client, userdata, msg):
    print('[{}] {}'.format(msg.topic, str(msg.payload)))
    return

#=========================================================================
# Before execute any MQTT client code, you need to create a channel and resource
# on Beebotte.

# Load config file.
import config

# Create an client instance.
try:
    ca_cert = config.ca_cert
except AttributeError:
    ca_cert = None
client = mqbeebotte.client(ca_cert=ca_cert)

# And connect to Beebotte.
client.connect(config.channel_token, on_connect=on_connect, on_message=on_message)
# Start network loop thread.
# Thread is running in a non-blocking manner.
client.start()

#--------------------------------------------------------------------------
# You can do anything after this including executing subscribe and publish.
#--------------------------------------------------------------------------

# Subscribe to mutiple topics.
# Generate target topic names.
topics = [
    '1',
    '2',
    '3',
    '4',
]
sub_topics = list(map(lambda x: config.topic_base + '/' + x, topics))
print('Subscribe to {}'.format(', '.join(sub_topics)))
# Give a list to subscribe() to subscribe to multiple topics.
client.subscribe(sub_topics)

for cnt in range(1,4):
    # I usually hook Ctrl-C to close connection properly.
    try:
        time.sleep(5)
        # Publish a message to a topic 'test/res/cnt'
        print('Publish a message to {}/{:d}'.format(config.topic_base, cnt))
        client.publish('{}/{:d}'.format(config.topic_base, cnt), 'test count {:d}'.format(cnt))
    except KeyboardInterrupt:
        print('Stop requested.')
        break

# wait for the final on_message call.
time.sleep(5)

# Stop network loop thread.
# When block_wait is set to True, stop() blocks until the thread stops.
# Default block_wait is False.  In a non-blocking manner, you need to
# wait until the thead stops using client.join().
client.stop(block_wait=True)

# Disconnect and removes the client instance.
del client

# -*- coding: utf-8 -*-
"""
This is a simple client sample.
Change channel_token in this file to access Beebotte.
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

# Topic name must be 'channel/resource'.
# In this example, you need to create a channel named 'test' that includes
# a resource named 'res'.
# I've tested several codes and found that wildcard such as 'channel/resource/#'
# seems to work properly.
topic = 'test/res'

# Copy and paste your channel token.
# I recommend to use a separate config file to keep this value.
##### THIS IS A SECRET KEY.  DO NOT COMMIT THIS VALUE TO YOUR REPOSITORY #####
channel_token = 'channel_token_here' 

# Create an client instance.
client = mqbeebotte.client()
# And connect to Beebotte.
client.connect(channel_token, on_connect=on_connect, on_message=on_message)
# Start network loop thread.
# Thread is running in a non-blocking manner.
client.start()

#--------------------------------------------------------------------------
# You can do anything after this including executing subscribe and publish.
#--------------------------------------------------------------------------

# Subscribe to a topic with wildcard, i.e, topic 'test/res/#'.
print('Subscribe to {}'.format(topic + '/#'))
client.subscribe(topic + '/#')

for cnt in range(3):
    # I usually hook Ctrl-C to close connection properly.
    try:
        time.sleep(5)
        # Publish a message to a topic 'test/res/1'
        print('Publish a message to ' + topic + '/1')
        client.publish(topic + '/1', 'test count {:d}'.format(cnt))
    except KeyboardInterrupt:
        print('Stop requested.')
        break

# wait for the final on_message call.
time.sleep(5)

# Stop network loop thread.
# When block_wait is set to True, stop() blocks until the thread stops.
# Default block_wait is set to False.
# In a non-blocking manner, you need to wait until the thead stops
# using client.join().
client.stop(block_wait=True)

# Disconnect and removes the client instance.
del client

# -*- coding: utf-8 -*-
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


#==========================================================================
# This file is used in client_advanced.py.
#==========================================================================

# Topic name must be 'channel/resource'.
# In this example, you need to create a channel named 'test' that includes
# a resource named 'res'.
# I've tested several codes and found that wildcard such as 'channel/resource/#'
# seems to work properly.
topic_base = 'test/res'

# Copy and paste your channel token.
##### THIS IS A SECRET KEY.  DO NOT COMMIT THIS VALUE TO YOUR REPOSITORY #####
channel_token = 'channel_token_here'

# If you want to use SSL connection, specify a path to a certificate file.
# A certificate file is derived on Beebotte document page.
# See https://beebotte.com/docs/mqtt for more details.
ca_cert = './mqtt.beebotte.com.pem'

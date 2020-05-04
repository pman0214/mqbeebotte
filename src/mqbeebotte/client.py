# -*- coding: utf-8 -*-

# Copyright (c) 2020, Shigemi ISHIDA
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the Institute nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import threading
import paho.mqtt.client as mqtt
from logging import getLogger, NullHandler

#======================================================================
class client(threading.Thread):
    """
    Beebotte MQTT client API class

    Attributes
    ----------
    logger : logging.Logger
        Logger object class attribute.  Default handler is NullHandler().
    HOST : str
        Default host name class attribute, i.e., mqtt.beebotte.com.
    PORT : int
        Default port number class attribute, i.e., 1883.
    PORT_SSL : int
        Default port number class attribute, i.e., 8883, for SSL connection.
    host : str
        MQTT server name to connect.
    port : int
        MQTT server port number.
    ca_cert : str
        CA Certificate file path.
    topics : list
        Subscribed topics.
    """

    logger = getLogger(__name__)
    logger.addHandler(NullHandler())
    HOST = 'mqtt.beebotte.com'
    PORT = 1883
    PORT_SSL = 8883

    #----------------------------------------------------------------------
    def __init__(self, host=None, port=None, ca_cert=None, *, logger=None):
        """
        Creates and maintains connection parameters and a logger instance.
        
        Parameters
        ----------
        host : str, default None
            Beebotte MQTT server hostname, None to use default value,
            i.e., mqtt.beebotte.com.
        port : int, default None
            Beebotte MQTT server port number, None to use default value,
            i.e., 1883 for non-SSL connection and 8883 for SSL connection.
        ca_cert : str, default None
            CA Certificate file path, None for non-SSL connection.
        logger : logging.Logger, default None
            Logger object, None to use module internal logging object.
        """

        super().__init__()

        self.host = host if host is not None else client.HOST
        self.ca_cert = ca_cert
        if port is not None:
            self.port = port
        else:
            self.port = client.PORT if self.ca_cert is None else client.PORT_SSL
        #
        if logger is not None:
            client.logger = logger

        self.topics = []

        self._pubs = {}
        self._pubs_lock = threading.RLock()
        self._client = None
        self._is_running = False

        return

    #----------------------------------------------------------------------
    def __del__(self):
        """
        Closes all the messaging with the MQTT server.
        """

        self.disconnect()
        return

    #----------------------------------------------------------------------
    def __on_connect(self, client, userdata, flags, respons_code):
        client.logger.debug('connected to {}'.format(self.host))
        return
   
    #----------------------------------------------------------------------
    def __on_message(self, client, userdata, msg):
        client.logger.debug('{} {}'.format(msg.topic, str(msg.payload)))
        client.logger.debug(msg.payload.decode("utf-8"))
        return

    #----------------------------------------------------------------------
    def __check_published(self):
        remove_targets = []
        with self._pubs_lock:
            for mid, pub in self._pubs.items():
                if pub.is_published():
                    remove_targets.append(mid)

        with self._pubs_lock:
            for mid in remove_targets:
                client.logger.debug('remove mid={:d}'.format(mid))
                del self._pubs[mid]

        return

    #----------------------------------------------------------------------
    def __unsubscribe_multiple(self, topics):
        for topic in topics:
            # check if topic is subscribed
            if topic in self.topics:
                client.logger.debug('unsubscribe from {}'.format(topic))
                self._client.unsubscribe(topic)
                self.topics.remove(topic)
                client.logger.debug('unsubscribed from {}'.format(topic))
            else:
                client.logger.debug('not subscribed to {}'.format(topic))

        return True

    #----------------------------------------------------------------------
    def __subscribe_multiple(self, topic_qos):
        # check if qos is provided
        if type(topic_qos[0]) is tuple:
            # extract topics
            topics = list(map(lambda x: x[0], topic_qos))
        else:
            topics = topic_qos.copy()
            topic_qos = list(zip(topics, [0]*len(topics)))

        # check if topics are already subscribed
        if len(set(topics) & set(self.topics)) != 0:
            subed_topics = set(topics) & set(self.topics)
            client.logger.error('topics are already subscribed: {}'.format(', '.join(list(subed_topics))))
            return False

        client.logger.debug('subscribe topics {}'.format(', '.join(topics)))
        result, mid = self._client.subscribe(topic_qos)
        if result is not mqtt.MQTT_ERR_SUCCESS:
            client.logger.error('subscribe error')
            return False

        self.topics.extend(topics)
        client.logger.debug('subscribed topics {}'.format(', '.join(topics)))

        return True

    #----------------------------------------------------------------------
    def connect(self, token, on_connect=None, on_message=None):
        """
        Connects to a MQTT server.

        Parameters
        ----------
        token : str
            Token string for Beebotte MQTT server.
            You can derive the token for a channel on Beebotte web
            https://beebotte.com.
        on_connect : function, default None
            Callback function called when an instance connected to
            the connected MQTT server.
            See https://pypi.org/project/paho-mqtt/ for more details.
        on_message : function, default None
            Callback function called when an instance gets message
            from the connected MQTT server.
            See https://pypi.org/project/paho-mqtt/ for more details.

        Returns
        -------
        is_success : bool
            True on success, False when any error occurs.
        """
        if self._client is not None:
            client.logger.debug('already connected to {}' + self.host)
            return False

        self._client = mqtt.Client()
        self._client.on_connect = on_connect if on_connect is not None else self.__on_connect
        self._client.on_message = on_message if on_message is not None else self.__on_message
        self._client.username_pw_set('token:{}'.format(token))
        if self.ca_cert is not None:
            client.logger.debug('use ca_cert: {}'.format(self.ca_cert))
            self._client.tls_set(self.ca_cert)

        client.logger.debug('connecting to {}:{:d}'.format(self.host, self.port))
        self._client.connect(self.host, self.port)
        client.logger.debug('connected to ' + self.host)

        return True

    #----------------------------------------------------------------------
    def disconnect(self):
        """
        Disconnects from a MQTT server.

        Returns
        -------
        is_success : bool
            True on success, False when any error occurs.
        """
        if self._client is None:
            return True

        self._client.loop_start()

        # unsubscribe from all topics
        client.logger.debug('unsubscribe all topics')
        self.unsubscribe(None)

        # wait for all publish requests to be published
        client.logger.debug('wait for all topics to be published')
        with self._pubs_lock:
            while len(self._pubs) > 0:
                mid, pub = self._pubs.popitem()
                client.logger.debug('wait for mid={:d}'.format(mid))
                pub.wait_for_publish()

        self._client.loop_stop()
        self._client.disconnect()
        self._client = None

        return True

    #----------------------------------------------------------------------
    def unsubscribe(self, topics):
        """
        Unsubscribes from a single topic or multiple topics.

        Parameters
        ----------
        topics : list or str
            A list of topics or a name of topic to be unsubscribed.
            None to unsubscribe from all the subscribed topics.

        Returns
        -------
        is_success : bool
            True on success, False when any error occurs.
        """
        if self._client is None:
            client.logger.error('cannot unsubscribe: not connected')
            return False

        if topics is None:
            client.logger.debug('unsubscribe from all: {}'.format(', '.join(self.topics)))
            self._client.unsubscribe(self.topics)
            self.topics = []
            client.logger.debug('unsubscribed all')
            return True

        if type(topics) is list:
            return self.__unsubscribe_multiple(topics)

        if topics in self.topics:
            client.logger.debug('unsubscribe from {}'.format(topics))
            self._client.unsubscribe(topics)
            self.topics.remove(topics)
            client.logger.debug('unsubscribed from {}'.format(topics))
        else:
            client.logger.debug('not subscribed to {}'.format(topics))

        return True

    #----------------------------------------------------------------------
    def subscribe(self, topics, qos=0):
        """
        Subscribes to a single topic or multiple topics.

        Parameters
        ----------
        topics : list or str
            A list of topics, a list of tuple of (topic, qos),
            or a name of topic to be subscribed.
        qos : int, default 0
            The integer of 0, 1, or 2 to specify Quality of Service
            for the subscription.  When topics is a list, qos is ignored.

        Returns
        -------
        is_success : bool
            True on success, False when any error occurs.
        """
        if self._client is None:
            client.logger.error('cannot subscribe: not connected')
            return False

        if type(topics) is list:
            return self.__subscribe_multiple(topics)

        if topics in self.topics:
            client.logger.warning('already subscribed to {}'.format(topics))
            return True

        if type(topics) is not str:
            client.logger.error('invalid variable for topic name')
            return False

        client.logger.debug('subscribe to {}'.format(topics))
        result, mid = self._client.subscribe(topics, qos)
        if result is not mqtt.MQTT_ERR_SUCCESS:
            client.logger.error('subscribe error')
            return False

        self.topics.append(topics)
        client.logger.debug('subscribed to {}, mid={:d}'.format(topics, mid))

        return True

    #----------------------------------------------------------------------
    def publish(self, topic, msg, qos=0, retain=False):
        """
        Publishes a message to a topic.

        Parameters
        ----------
        topic : str
            The name of publish target topic.
        msg : str or byte
            A message to be published.
        qos : int, default 0
            An integer of 0, 1, or 2 to specify Quality of Service for publish.
        retain : bool
            A flag to indicate that the message will be retained.

        Returns
        -------
        is_success : bool
            True on success, False when any error occurs.
        """
        if self._client is None:
            client.logger.error('cannot publish: not connected')
            return False

        client.logger.debug('publish {}'.format(topic))
        pub = self._client.publish(topic, msg, qos, retain)
        with self._pubs_lock:
            self._pubs[pub.mid] = pub
        client.logger.debug('published {}'.format(topic))

        return True

    #----------------------------------------------------------------------
    def start(self):
        """
        Starts network loop thread.
        """
        return super().start()

    #----------------------------------------------------------------------
    def stop(self, block_wait=False):
        """
        Stops network loop thread.

        Parameters
        ----------
        block_wait : bool
            A flag to indicate to wait for the thread to be stopped.
        """

        # do nothing if the thread is not running
        if not self._is_running:
            return

        client.logger.debug('stop')
        self._is_running = False
        if block_wait:
            self.join()

        return

    #----------------------------------------------------------------------
    def run(self):
        if self._client is None:
            return False

        self._is_running = True
        while self._is_running:
            self._client.loop()
            self.__check_published()

        return True

#======================================================================

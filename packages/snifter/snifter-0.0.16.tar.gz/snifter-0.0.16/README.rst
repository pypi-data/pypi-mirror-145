=======
snifter
=======

**Listen to and inspect AWS SNS topic data!**

Because SNS data is ephemeral, we need to make a place to receive and
store the data if we want to inspect it.  While you can subscribe your
email address, it's not very handy to do so (SMS is obviously not
better). A clean (if slightly over-complex) method for doing this is
to create a temporary SQS queue, then subscribe the queue to the SNS
topic you want to inspect, and *then* watch that queue.

Snifter does all that in a single command.  The queue is build and
torn down for you, and it will endlessly listen to that queue,
including dropping into an interactive debug session that will let you
inspect the payload in detail.

Provide a profile and a topic, the queue will be torn down when it
catches Ctrl+c

===========
Basic Usage
===========

.. code-block:: bash

    $ snifter --profile=dev-power --topic=tim-manager-events
    Listening...
    Listening...
    ^CListening...
    Deleted queue with URL https://us-west-2.queue.amazonaws.com/024726604032/sns-listener_tim-manager-events_88fc71e98a.

===========
Debug Usage
===========

Providing the --debug flag will cause you to drop into a debugger when something is popped from the queue, PDB behavior applies.  The payload of the SNS message ('Message') is assigned a namespace ('m').  This means that you get tab completion on the dynamic keys in your message payload.

.. image:: https://user-images.githubusercontent.com/419355/161634911-f0103e13-5c14-4628-84bc-5a001323de7a.gif
   :width: 600px

====
Help
====

.. code-block:: bash

    $ snifter --help
    usage: snifter [-h] [-p PROFILE] [-d] [-t TOPIC]

    Listen to an SNS topic

    optional arguments:
      -h, --help            show this help message and exit
      -p PROFILE, --profile PROFILE
                            AWS profile name
      -d, --debug           Drop into debugger to inspect message
      -t TOPIC, --topic TOPIC
                            SNS topic name

=====
Login
=====
.. image:: https://user-images.githubusercontent.com/419355/161607497-637e13e6-32a2-4d70-8336-9153691d4d61.gif
   :width: 600px

=========
Listening
=========
.. image:: https://user-images.githubusercontent.com/419355/161607493-9fd60169-0aab-4637-b709-593cf315e6eb.gif
   :width: 600px

==========================
Inspecting (with debug on)
==========================
.. code-block:: bash

    $ snifter --profile=dev-power --topic=tim-manager-events --debug
    Listening...
    Listening...
    Attempting decode of body
    Dropping into debugger for inspection
    Local message namespace is 'm'
    PDB commands: 'c' to continue, 'exit()' to exit
    [2] > /home/ahonnecke/src/snifter/src/snifter/main.py(161)listen()
    -> message.delete()
    (Pdb++) list
    156  	                print("PDB commands: 'c' to continue, 'exit()' to exit")
    157  	                breakpoint()
    158  	            else:
    159  	                print(f"Recieved message, {show}")
    160
    161  ->	            message.delete()
    162
    163  	        print("Listening...")
    164  	        sleep(1)
    165
    166
    (Pdb++) print(m.curve_angle)
    None
    (Pdb++) print(m.failed_rsu_ids)
    ['590d0953-444d-4f0a-842d-3ad425394baf', '8bfacac8-9c8f-41e6-b9a3-09641913da8a', 'd4d7cc04-b98a-4ad8-b9b6-801966c84f68', 'e7e259da-926c-4c0e-93cd-a8507bda76b3']

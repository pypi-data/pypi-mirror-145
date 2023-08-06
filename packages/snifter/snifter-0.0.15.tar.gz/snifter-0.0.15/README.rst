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
.. image:: https://user-images.githubusercontent.com/419355/161607489-40bea93f-a5b3-4056-888b-944916151822.gif
   :width: 600px

.. code-block:: bash

    $ snifter -d
    Profile was not passed, choose a profile: dev-power
    Choose topic: tim-manager-events
    Listening...
    Listening...
    Listening...
    Listening...
    Listening...
    Listening...
    Listening...
    Listening...
    Dropping into debugger for inspection
    Local message variable is 'm'
    PDB commands: 'c' to continue, 'exit()' to exit
    (Pdb++)
    (Pdb++) list
    143  	                print("PDB commands: 'c' to continue, 'exit()' to exit")
    144  	                breakpoint()
    145  	            else:
    146  	                print(f"Recieved message, {m.body}")
    147
    148  ->	            m.delete()
    149
    150  	        print("Listening...")
    151  	        sleep(1)
    152
    153
    (Pdb++) print(m.body)

# Synchronous message interface in Bitcoin client

Bitcoin internally uses a synchronous message delivery system. It is mainly
used to decouple the wallet (wallet.a) functionalities from the validation (included in
 server.a).

The pattern used an observer pattern where a class that wants to receive a specific
message has just to extend `CValidationInterface` (in validatorinterface.h),
 override the methods for which it wants to receive the messages and register
 itself calling `RegisterValidationInterface()` passing the listener instance
 during the application initialization.

## Class structure

`CValidationInterface` in validatorinterface.h:  
this class expose an extendable interface for callbacks.

`MainSignalsInstance` in validatorinterface.h:  
this struct contains a list of the existing callbacks that are each bound to a
`boost::signals2::signal`[1]. This the way how calls from `CMainSignals` are connected
to the equivalent in `CValidationInterface`.
It also contains an instance of `SingleThreadedSchedulerClient` as messaging queue.

`CMainSignals` in validatorinterface.h:
this class takes care of registering the callback functions.

The call flow unfolds like this:

1. a call to `CMainSignals::SomeFunction()` is made, this function is the sender
entry point.

2. the previous function just delegates the call to `m_internals->CMainSignals::SomeFunction()`,
where `m_internals` is a pointer to the instance of `MainSignalsInstance`.

3. The call is now redirected to the right `CValidationInterface` method that has
been defined in the mapping created in `RegisterValidationInterface()`.

4. The final recipient method in each class implementing `CValidationInterface` and
overriding it, it is then executed.

## ZMQ support
Since there was a lack of an easy way to notify external entities of events happening
inside the node, bitcoin added support for ZMQ[2]. ZMQ[3] is used as one-direction
queuing system to broadcast notifications to listeners.

This support is brought through the registration of `CZMQNotificationInterface`,
using `CZMQNotificationInterface::Create()` during the startup of the node using
again `RegisterValidationInterface()`.


## References
[1] Boost documentation, URL https://www.boost.org/doc/libs/1_47_0/doc/html/boost/signals2/signal.html.  
[2] ZMQ usage in bitcoin, https://github.com/bitcoin/bitcoin/blob/master/doc/zmq.md.  
[3] ZMQ website, URL http://zeromq.org/.  

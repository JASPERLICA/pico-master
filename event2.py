from python_event_bus import EventBus

def call_example_event():
    EventBus.call("example_event", "Hello from test.py")
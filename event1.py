from python_event_bus import EventBus
from event2 import call_example_event

@EventBus.on("example_event")
def on_example_event(data):
    print(f"Example event called with data: {data}")

call_example_event()
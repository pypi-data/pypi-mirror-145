class Event:
    def __init__(self):
        self.listeners = []

    def __iadd__(self, listener):
        """Shortcut for using += to add a listener."""
        self.listeners.append(listener)
        return self

    def __isub__(self, listener):
        """Shortcut for using -= to add a listener."""
        self.listeners.remove(listener)
        return self

    def notify(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)
            
    async def async_notify(self, *args, **kwargs):
        for listener in self.listeners:
            await listener(*args, **kwargs)

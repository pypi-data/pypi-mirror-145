"""Light implementation of the Observer design pattern."""
import typing


class Observable:
    """Allows observers to be notified of something by subscribing to this class.

    Each Observable instance can be attached to some other instances to compose a hierarchy of
    observables where each level propagates (forwards) the notifications coming from its sublevels.

    Note: this implementation of the observer patter is NOT thread safe!"""

    def __init__(self):
        self._observers = []

    def attach(self, callback: typing.Callable) -> None:
        """Appends the given callback (lambda function) to the observers."""
        self._observers.append(callback)

    def notify(self) -> None:
        """Notifies all the observers"""
        for obs in self._observers:
            obs()

    def forward(self, other: "Observable") -> None:
        """Forwards the notifications coming from another observable as if they were triggered
        by the current instance)."""
        assert other != self
        other.attach(self.notify)

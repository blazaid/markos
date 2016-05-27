import random
from collections import defaultdict

__version__ = '0.0.2'


class MarkovChain:
    class End:
        pass

    END = End()

    def __init__(self):
        self.events = defaultdict(lambda: defaultdict(lambda: 0))
        self.start_events = defaultdict(lambda: 0)

    def train(self, chain):
        previous_event = chain[0]
        self.start_events[previous_event] += 1
        for event in chain[1:]:
            self.events[previous_event][event] += 1
            previous_event = event
        self.events[previous_event][MarkovChain.END] += 1

    def select(self, choices):
        total_events = sum(weight for event, weight in choices)
        r = random.uniform(0, total_events)
        upto = 0
        for event, weight in choices:
            if upto + weight >= r:
                return event
            else:
                upto += weight

    def generate(self, event=None, max_events=None, end=True):
        # Si no especificamos evento, cogemos uno al azar de entre todos los existentes.
        if event is None:
            event = self.select(self.start_events.items())
        yield event

        stop = not event in self.events or event is MarkovChain.END
        while not stop:
            # Obtenemos los posibles eventos a los que pasar
            choices = [
                (event, weight)
                for event, weight in self.events[event].items()
                if event is not MarkovChain.END or event is MarkovChain.END and end
                ]
            if choices:
                # Seleccionamos el siguiente evento según su fecuencia absoluta
                event = self.select(choices)
                if event is not MarkovChain.END:
                    yield event
                # Calculamos si debemos terminar
                if max_events is not None:
                    max_events -= 1
                event_starts_transition = event in self.events
                last_element = max_events is not None and max_events <= 1
                stop = not event_starts_transition or last_element
            else:
                stop = True

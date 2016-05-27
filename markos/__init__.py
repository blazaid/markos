import random
from collections import defaultdict

__version__ = '0.0.3'


class MarkovChain:
    class Start:
        pass

    START = Start()

    class End:
        pass

    END = End()

    def __init__(self, grade=0):
        self.events = defaultdict(lambda: defaultdict(lambda: 0))
        self.grade = grade

    def train(self, chain):
        chain = [MarkovChain.START] + chain + [MarkovChain.END]
        previous_event = [chain[0]]
        for event in chain[1:]:
            self.events[tuple(previous_event)][event] += 1
            if len(previous_event) > self.grade:
                previous_event.pop(0)
            previous_event.append(event)

    def select(self, choices):
        choices = list(choices)
        total_events = sum(weight for event, weight in choices)
        r = random.uniform(0, total_events)
        upto = 0
        for event, weight in choices:
            if upto + weight >= r:
                return event
            else:
                upto += weight

    def next_events(self, event, end):
        return (
            (event, weight)
            for event, weight in self.events[tuple(event)].items()
            if event is not MarkovChain.END or event is MarkovChain.END and end
        )

    def generate(self, event=None, max_events=None, end=True):
        # Si no especificamos evento, cogemos uno al azar de entre todos los existentes.
        selected_event = event or self.select(self.next_events([MarkovChain.START], end))
        yield selected_event
        previous_event = [MarkovChain.START]
        if len(previous_event) > self.grade:
            previous_event.pop(0)
        previous_event += [selected_event] if isinstance(selected_event, str) else list(selected_event)

        stop = tuple(previous_event) not in self.events or MarkovChain.END in previous_event
        while not stop:
            # Obtenemos los posibles eventos a los que pasar
            choices = self.next_events(previous_event, end)
            if choices:
                # Seleccionamos el siguiente evento según su fecuencia absoluta
                event = self.select(choices)
                if event is not MarkovChain.END:
                    yield event
                if len(previous_event) > self.grade:
                    previous_event.pop(0)
                previous_event.append(event)
                # Calculamos si debemos terminar
                if max_events is not None:
                    max_events -= 1
                event_starts_transition = tuple(previous_event) in self.events
                last_element = max_events is not None and max_events <= 1
                stop = not event_starts_transition or last_element
            else:
                stop = True

from pyfyre.widgets import *

class CounterApp(UsesState):
    def __init__(self):
        super().__init__()
        self.count = 0

    def increment(self, event):
        self.count = self.count + 1
        self.update()

    def decrement(self, event):
        self.count = self.count - 1
        self.update()

    def build(self):
        return Container(
            className="counter-app",
            children=[
                Text("Counter app example:"),
                Container(
                    className="counters",
                    children=[
                        Button(
                            "-",
                            onClick=self.decrement,
                            className="btn-counter"
                        ),
                        Text(self.count),
                        Button(
                            "+",
                            onClick=self.increment,
                            className="btn-counter"
                        )
                    ]
                )
            ]
        )
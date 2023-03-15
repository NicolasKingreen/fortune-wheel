from text import Label


class Debug:

    def __init__(self, *params):
        self.params = list(params)
        self.ys = []

        self.labels = []
        for i, param in enumerate(self.params):
            y = i * 32
            new_label = Label(param, (0, y))

            self.ys.append(y)
            self.labels.append(new_label)

    def add_parameter(self, parameter):
        self.params.append(parameter)
        self.labels.append(Label(parameter, (0, self.ys[-1] + 32)))

    def draw(self, surface):
        for label in self.labels:
            label.draw(surface)

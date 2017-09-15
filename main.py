class Gate(object):
    def __init__(self, current_state="locked"):
        self.__state = current_state
        self.__actions = {}

        self.listen(state="locked", event="coin", action=lambda gate: gate.go_to('unlocked'))
        self.listen(state="locked", event="through", action=lambda gate: gate.alarm())
        self.listen(state="locked", event="power", action=lambda gate: gate.go_to('no_entry'))
        self.listen(state="no_entry", event="power", action=lambda gate: gate.go_to('locked'))
        self.listen(state="no_entry", event="through", action=lambda gate: gate.alarm())
        self.listen(state="unlocked", event="through", action=lambda gate: gate.go_to('locked'))
        self.listen(state="unlocked", event="coin", action=lambda gate: gate.thank_you())
        self.listen(state="unlocked", event="power", action=lambda gate: gate.go_to('no_entry'))

    def alarm(self):
        print "ALARM ALARM"

    def thank_you(self):
        print "THANK YOU <3"

    def listen(self, state, event, action):
        key = "{0}:{1}".format(state, event)
        self.__actions[key] = self.__actions.get(key) or []
        self.__actions[key].append(action)

    def current_state(self):
        return self.__state

    def go_to(self, state):
        self.__state = state

    def coin(self): self.__trigger("coin")
    def through(self): self.__trigger("through")
    def power(self): self.__trigger("power")

    def __trigger(self, event):
        key = "{0}:{1}".format(self.current_state(), event)
        actions = self.__actions.get(key) or []
        [action(self) for action in actions]

    def __events_for_state(self):
        return self.__transitions[self.current_state()]


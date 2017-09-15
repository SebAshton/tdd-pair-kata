class StateMachine(object):
    def __init__(self, current_state, context):
        self.__actions = {}
        self.__state = current_state
        self.__context = context

    def listen(self, state, event, action):
        key = "{0}:{1}".format(state, event)
        self.__actions[key] = self.__actions.get(key) or []
        self.__actions[key].append(action)

    def current_state(self):
        return self.__state

    def go_to(self, state):
        self.__state = state

    def trigger(self, event):
        key = "{0}:{1}".format(self.current_state(), event)
        actions = self.__actions.get(key) or []
        [action(self.__context) for action in actions]


class Gate(object):
    def __init__(self, current_state="locked"):
        self.state_machine = StateMachine(current_state=current_state, context=self)

        self.state_machine.listen(state="locked", event="coin", action=lambda gate: self.go_to('unlocked'))
        self.state_machine.listen(state="locked", event="through", action=lambda gate: self.alarm())
        self.state_machine.listen(state="locked", event="power", action=lambda gate: self.go_to('no_entry'))
        self.state_machine.listen(state="no_entry", event="power", action=lambda gate: self.go_to('locked'))
        self.state_machine.listen(state="no_entry", event="through", action=lambda gate: self.alarm())
        self.state_machine.listen(state="unlocked", event="through", action=lambda gate: self.go_to('locked'))
        self.state_machine.listen(state="unlocked", event="coin", action=lambda gate: self.thank_you())
        self.state_machine.listen(state="unlocked", event="power", action=lambda gate: self.go_to('no_entry'))

    def alarm(self):
        print "ALARM ALARM"

    def thank_you(self):
        print "THANK YOU <3"

    def current_state(self):
        return self.state_machine.current_state()

    def go_to(self, state):
        self.state_machine.go_to(state)

    def coin(self): self.state_machine.trigger("coin")
    def through(self): self.state_machine.trigger("through")
    def power(self): self.state_machine.trigger("power")

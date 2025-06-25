from graphviz import Digraph

def visualize_moore_machine(moore_machine):
    dot = Digraph()

    # Add nodes (states)
    for state, output in moore_machine.get_outputs().items():
        if state == moore_machine.start_state:
            # Highlight starting state with a distinct shape or color
            dot.node(state, label=f"{state}\n(Output: {output})", shape="doublecircle", color="green", style="filled")
        else:
            dot.node(state, label=f"{state}\n(Output: {output})")

    # Add transitions
    for state, transitions in moore_machine.get_transitions().items():
        for input_symbol, next_state in transitions.items():
            dot.edge(state, next_state, label=input_symbol)

    # Render the graph
    dot.render('moore_machine', format='png', view=True)  # This saves and opens the image.


class MealyMachine:
    def __init__(self):
        self.states = {}
        self.start_state = None

    def add_state(self, state_name):
        if state_name not in self.states:
            self.states[state_name] = {}

    def set_transition(self, from_state, input_symbol, to_state, output_symbol):
        self.add_state(from_state)
        self.add_state(to_state)
        self.states[from_state][input_symbol] = (to_state, output_symbol)

    def set_start_state(self, state_name):
        self.start_state = state_name

    def get_transitions(self):
        return self.states

class MooreMachine:
    def __init__(self):
        self.states = {}  # {state_name: output_symbol}
        self.transitions = {}  # {state_name: {input_symbol: next_state}}
        self.start_state = None

    def add_state(self, state_name, output_symbol):
        self.states[state_name] = output_symbol
        self.transitions[state_name] = {}

    def set_transition(self, from_state, input_symbol, to_state):
        self.transitions[from_state][input_symbol] = to_state

    def set_start_state(self, state_name):
        self.start_state = state_name

    def get_transitions(self):
        return self.transitions

    def get_outputs(self):
        return self.states

def mealy_to_moore(mealy_machine):
    moore_machine = MooreMachine()
    state_map = {}
    queue = []  # To dynamically process states
    visited = set()  # Track visited (Mealy state, output) pairs

    # Initialize with the start state
    mealy_start_state = mealy_machine.start_state
    mealy_start_output = next(iter(mealy_machine.get_transitions()[mealy_start_state].values()))[1]
    start_key = (mealy_start_state, mealy_start_output)
    start_moore_state = f"{mealy_start_state}_{mealy_start_output}"
    state_map[start_key] = start_moore_state
    moore_machine.add_state(start_moore_state, mealy_start_output)
    moore_machine.set_start_state(start_moore_state)
    queue.append(start_key)

    # Process states dynamically
    while queue:
        current_key = queue.pop(0)
        current_state, current_output = current_key
        current_moore_state = state_map[current_key]

        # Skip if already processed
        if current_key in visited:
            continue
        visited.add(current_key)

        # Process all transitions from the current Mealy state
        for input_symbol, (next_state, output_symbol) in mealy_machine.get_transitions()[current_state].items():
            next_key = (next_state, output_symbol)
            if next_key not in state_map:
                # Dynamically add the new Moore state
                new_moore_state = f"{next_state}_{output_symbol}"
                state_map[next_key] = new_moore_state
                moore_machine.add_state(new_moore_state, output_symbol)
                queue.append(next_key)  # Enqueue for further processing

            # Add the transition
            moore_next_state = state_map[next_key]
            moore_machine.set_transition(current_moore_state, input_symbol, moore_next_state)

    return moore_machine


def print_moore_machine_ascii(moore_machine):
    print("Moore Machine Transition Diagram (ASCII Art):\n")
    
    # Highlight the starting state
    print(f"--> Start State: {moore_machine.start_state}\n")

    for state, transitions in moore_machine.get_transitions().items():
        is_start = " (Start State)" if state == moore_machine.start_state else ""
        print(f"State {state} (Output: {moore_machine.get_outputs()[state]}){is_start}")
        for input_symbol, next_state in transitions.items():
            print(f"  |-- {input_symbol} --> {next_state}")
        print()


if __name__ == "__main__":
    # Define a Mealy machine
    mealy = MealyMachine()
    mealy.set_start_state("S0")
    mealy.set_transition("S0", '0', "S0", '0')
    mealy.set_transition("S0", '1', "S1", '0')
    mealy.set_transition("S1", '1', "S1", '1')
    mealy.set_transition("S1", '0', "S0", '1')

    # Convert to Moore machine
    moore = mealy_to_moore(mealy)

    # Print the Moore machine
    print_moore_machine_ascii(moore)

    # Visualize the Moore machine
    visualize_moore_machine(moore)
from gamestate import *
import network
import random

class Controller:
    def __init__(self, id: str, controller_callable):
        self.ID = id
        self.CONTROLLER_CALLABLE = controller_callable
    
    def getShot(self, gamestate) -> tuple[float, float]:
        return self.CONTROLLER_CALLABLE(gamestate)

class randomController(Controller):
    def __init__(self, id: str):
        super().__init__(id, self.shootRandomly)
    
    def shootRandomly(self, gamestate: GameState):
        return (3.14 * (random.random() - 0.5), random.random())

# class mixedStrategyController(Controller):
#     def __init__(self, id: str, strategy: list[float]):
#         self.strategy = strategy
#         super().__init__(id, self.pickWeightedRandomMove)
    
#     def pickWeightedRandomMove(self, gamestate: GameState):
#         moves = list(gamestate.ALLOWED_MOVES.keys())
#         return random.choices(moves, self.strategy)[0]

class basicNeuralNetworkController(Controller):
    def __init__(self, id: str, network: network.Network):
        self.network = network
        super().__init__(id, self.pickNeuralNetworkAdvisedMove)

    def pickNeuralNetworkAdvisedMove(self, gamestate: GameState):
        input = [0, 0, 0, 0]
        for peg in gamestate.PEGS:
            input[0] += 1
            if peg.isOrange: input[1] += 1
        input[2] = gamestate.SCORE/100000
        input[3] = gamestate.BALLS
        
        for _ in range(4, self.network.getInputSize()):
            input.append(random.random())

        self.network.updateInputs(input)
        self.network.update()
        out = self.network.readOutput()
        while out[0] > 1.5:
            out[0] -= 3
        while out[0] < -1.5:
            out[0] += 3
        return out

class orangeAwareNeuralNetworkController(Controller):
    def __init__(self, id: str, network: network.Network):
        self.network = network
        super().__init__(id, self.pickNeuralNetworkAdvisedMove)
        self.peg_memory = None

    def pickNeuralNetworkAdvisedMove(self, gamestate: GameState):
        if self.peg_memory is None:
            self.peg_memory = {}
            for i in range(0, len(gamestate.PEGS)):
                peg = gamestate.PEGS[i]
                self.peg_memory[(peg.pos.x, peg.pos.y)] = (i, int(peg.isOrange))
        input = []
        # note to self: make this not suck
        for _ in range(0, len(self.peg_memory.keys())):
            input.append(0)

        for peg in gamestate.PEGS:
            memory = self.peg_memory[(peg.pos.x, peg.pos.y)]
            input[memory[0]] = memory[1]

        for _ in range(len(self.peg_memory.keys()), self.network.getInputSize()):
            input.append(random.random())

        self.network.updateInputs(input)
        self.network.update()
        out = self.network.readOutput()
        while out[0] > 1.5:
            out[0] -= 3
        while out[0] < -1.5:
            out[0] += 3
        return out
    
class fullNeuralNetworkController(Controller):
    def __init__(self, id: str, network: network.Network):
        self.network = network
        super().__init__(id, self.pickNeuralNetworkAdvisedMove)
        self.peg_memory = None

    def pickNeuralNetworkAdvisedMove(self, gamestate: GameState):
        if self.peg_memory is None:
            self.peg_memory = {}
            for i in range(0, len(gamestate.PEGS)):
                peg = gamestate.PEGS[i]
                self.peg_memory[(peg.pos.x, peg.pos.y)] = (i, int(peg.isOrange), int(peg.isPowerUp))
        input = []
        # note to self: make this not suck
        for _ in range(0, 3*len(self.peg_memory.keys())):
            input.append(0)
        
        for peg_pos in self.peg_memory.keys():
            memory = self.peg_memory[peg_pos]
            input[3 * memory[0] + 1] = memory[1]
            input[3 * memory[0] + 2] = memory[2]

        for peg in gamestate.PEGS:
            input[3 * self.peg_memory[(peg.pos.x, peg.pos.y)][0]] = 1

        for _ in range(3*len(self.peg_memory.keys()), self.network.getInputSize()):
            input.append(random.random())

        self.network.updateInputs(input)
        self.network.update()
        out = self.network.readOutput()
        while out[0] > 1.5:
            out[0] -= 3
        while out[0] < -1.5:
            out[0] += 3
        return out
class OutofBoundsError(Exception):
    '''this exception is raised when trying to get to a node that odes not exist on a stack'''
    def __init__(self,placement):
        self.placement = placement

class NonIntegerIntoStack(Exception):
    '''this exception is raised when trying to put a non-integer onto the stack'''
    def __init__(self,thing):
        self.thing = thing

class NotAValidInstructionError(Exception):
    '''this exception is raised when trying to call an instruction that does not exist'''
    def __init__(self,instruction):
        self.instruction = instruction

class LoopNotClosed(Exception):
    '''this exception is raised when a statement that requires an 'end' statement following it doesnt have one'''
    def __init__(self,statement):
        self.statement = statement

class NoDefaultPresent(Exception):
    '''this exception is raised when a parameter without a default value is not present'''
    def __init__(self,parameter):
        self.parameter = parameter

class NameStartsWithDollar(Exception):
    '''this exception is raised when a routine which name starts with a dollar sign ($) is ade'''
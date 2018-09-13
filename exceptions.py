class OutofBoundsError(Exception):
    '''this exception is used when trying to get to a node that odes not exist on a stack'''
    def __init__(self,placement):
        self.placement = placement
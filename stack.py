class Stack():
    class node():
        def __init__(self,value):
            self.value = value
            self.back =  None
            self.next = None
    def __init__(self):
        self.base = None #top of the stack
        self.bottom = None #bottom of the stack
    def __iter__(self):
        self.current = self.base
        return self
    def __next__(self):
        if self.current is None:
            raise StopIteration
        else:
            ret_value = self.current.value
            self.current = self.current.next
            return ret_value
    def __str__(self):
        ret = ''
        for x in self:
            ret+=str(x)+'\n'
        return ret
    def push(self,value):
        '''add a new value to the stack'''
        if self.base is None:
            self.base = self.node(value)
            self.bottom = self.base
        else:
            new_node = self.node(value)
            new_node.back = self.bottom
            self.bottom.next = new_node
            self.bottom = new_node
    def pop(self):
        '''remove the top value of the stack'''
        if self.bottom.back is None:
            self.base = None
            self.bottom = None
        else:
            self.bottom.back.next = None
            self.bottom = self.bottom.back
    def add(self):
        '''remove the top two values from the stack and push their addition together'''
        a = self.bottom.value
        self.pop()
        b = self.bottom.value
        self.pop()
        self.push(a+b)
    def dup(self):
        '''create a copy of the top of the stack and put it at the top of the stack'''
        self.push(self.bottom.value)
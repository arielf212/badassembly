class Stack():
    class node():
        def __init__(self,value):
            self.value = value
            self.back =  None
            self.next = None
    def __init__(self):
        self.base = None #top of the stack
        self.top = None #bottom of the stack
        self.length = 0
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
        ret = '['
        for x in self:
            ret+=str(x)+','
        return ret+']'
    def __len__(self):
        return self.length
    def get_node(self,placement):
        node = self.top
        for x in range(self.length):
            if x == placement:
                return node
            node = node.back
        return None
    def push(self,value,placement=0):
        '''add a new value to the stack'''
        if self.base is None:
            self.base = self.node(value)
            self.top = self.base
        else:
            new_node = self.node(value)
            old_node = self.get_node(placement)
            new_node.back = old_node
            new_node.next = self.get_node(placement+1)
            old_node.next = new_node
            old_node = new_node
        self.length+=1
    def pop(self,placement=0):
        '''remove the top value of the stack'''
        node = self.get_node(placement)
        if node.back is None:
            self.base = None
            self.top = None
        else:
            node.back.next = self.node.next
            node.next.back = self.node.back
        self.length-=1
    def add(self,placement1=0,placement2=1,placement=0):
        '''remove the top two values from the stack and push their addition together'''
        a = self.get_node(placement1)
        b = self.get_node(placement2)
        self.push(a+b,0)
    def dup(self,old_placement,dup_placement):
        '''create a copy of the top of the stack and put it at the top of the stack'''
        self.push(self.get_node(old_placement),dup_placement)
    def clear(self):
        self.base = None
        self.top = None
        self.length = None

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
        return ret[:-1]+']'
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
            node = self.node(value)
            back_node = self.get_node(placement)
            next_node = back_node.next
            node.back = back_node
            node.next = next_node
            if back_node is not None:
                back_node.next = node
            if next_node is not None:
                next_node.back = node
            if placement == 0: #if the node is put on top of the stack
                self.top = node
            elif placement == self.length: #if put at the base of the stack
                self.base = node
        self.length+=1
    def pop(self,placement=0):
        '''remove the top value of the stack'''
        node = self.get_node(placement)
        if self.length == 1:
            self.base = None
            self.top = None
        else:
            if node.back is not None:
                node.back.next = node.next
            else:
                self.base = node.next
            if node.next is not None:
                node.next.back = node.back
            else:
                self.top = node.back
        self.length-=1
    def add(self,placement1=0,placement2=1,placement=0):
        '''remove the top two values from the stack and push their addition together'''
        a = self.get_node(placement1).value
        b = self.get_node(placement2).value
        self.push(a+b,placement)
    def dup(self,old_placement,dup_placement):
        '''create a copy of the top of the stack and put it at the top of the stack'''
        self.push(self.get_node(old_placement),dup_placement)
    def clear(self):
        self.base = None
        self.top = None
        self.length = None

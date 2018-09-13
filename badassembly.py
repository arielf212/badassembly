import stack
import exceptions
#import sys
def run_file(file,main,line=0,code='',loop=1,jumpfrom=('main',0)):
    if not code:
        with open(file) as file_instructions:
            lines = file_instructions.read().split('\n')
    else:
        lines = list(filter(None,code.split('\n')))
    if file in stacks:
        st = stacks[file]
    else:
        st = stack.Stack()
        stacks[file] = st
    pop = 0 #last number poped off the stack
    while loop > 0:
        current_line = line
        try:
            while current_line < len(lines):
                attr = lines[current_line].split(' ')
                attr = optimize_attr(attr,default_params[attr[0]],loop,pop)
                include = ''
                if '-' in lines[current_line]:
                    line = 0
                    for i in range(len(attr)):
                        if '-' in attr[i] and i != 0:
                            include, line = attr[i].split('-')
                            line = int(line)
                if attr[0] == 'push': #push <number>
                    st.push(int(attr[1]),int(attr[2])) #pushes <number> onto the top of stack
                elif attr[0] == 'pop': #pop
                    pop = st.get_node(int(attr[1]))
                    st.pop(int(attr[1])) #removes the number at the top of the stack
                elif attr[0] == 'add': #add <number1> <number2> <placement>
                    st.add(int(attr[1]),int(attr[2]),int(attr[3])) #adds the top two numbers at the top of the stack together, removes them and pushes the sum onto the stack
                elif attr[0] == 'ifeq': #ifeq <number> <address>
                    if st.top.value == int(attr[1]): #if <number> is equal to the number at the top of the stack, jump to <address>
                        jumpfrom = file,current_line
                        if not include:
                            current_line = int(attr[2])
                            continue
                        else:
                            run_file(include,False,line=line,jumpfrom=jumpfrom)
                elif attr[0] == 'ifunq': #ifnuq <number> <address>
                    if st.top.value != int(attr[1]): #if <number> isnt equal to the number at the top of the stack jump to <address>
                        jumpfrom = file, current_line
                        if not include:
                            current_line = int(attr[2])
                            continue
                        else:
                            run_file(include,False,line=line,jumpfrom=jumpfrom)
                elif attr[0] == 'clear':
                    st = stack.Stack()
                elif attr[0] == 'jump': #jump <address>
                    jumpfrom = file, current_line #jump to <address>
                    if not include:
                        current_line = int(attr[2])
                        continue
                    else:
                        run_file(include,False,line=line,jumpfrom=jumpfrom)
                elif attr[0] == 'print': #print <placement>
                    print(st.get_node(int(attr[1])).value) #prints the top of the stack
                elif attr[0] == 'dup': #dup <old> <new>
                    for x in range(3-len(attr)):
                        attr.append(0)
                    st.dup(int(attr[1]),int(attr[2])) #puts a copy of the number at the top of the stack onto the top of the stack
                elif attr[0] == 'loop': #loop <counter> \n <code> \n end
                    input_loop = int(attr[1])
                    imput_code = ''
                    current_line+=1
                    while lines[current_line] != 'end':
                        imput_code+=lines[current_line]+'\n'
                        current_line+=1
                    run_file(file,main,code=imput_code,loop=input_loop)
                elif attr[0] == 'ret': #ret <number1>......<numberX>
                    # returns to the last line you jumped from and pushes all of the proceeding numbers onto the stack in order of appearance
                    if jumpfrom[0] == file: #if jump was inside of the file
                        for num in attr[1:]:
                            st.push(num)
                        current_line = jumpfrom[1]
                    else:
                        return attr[1:]
                elif attr[0] == 'quit': #quit
                    print('END') #stops the program
                    break
                current_line += 1
        except exceptions.OutofBoundsError:
            print('line {}: {}.\noutofboundserror: tried to access a stack slot not yet created'.format(current_line,lines[current_line]))
        loop-=1
def optimize_attr(attr,default_params,loop,pop):
    '''changes attr based on the default params'''
    if 'default' in attr or len(attr) < len(default_params) or '$' in ''.join(attr):
        for x in range(len(default_params)):
            if len(attr)-1 < x: #if parameters werent found then put the default param for that slot
                attr.append(default_params[x])
            elif attr[x] == 'default': #generates default parameters
                attr[x] = default_params[x]
            elif attr[x].startswith('$'): #replace a variable with its value
                if attr[x] == '$ask': # $ask takes input from user
                    attr[x] = input('enter input')
                elif attr[x] == '$loop': # $loop is the amount of iterations left
                    attr[x] = loop
                elif attr[x] == '$pop': # $pop is the last number poped out
                    attr[x] = pop
    return attr

if __name__ == '__main__':
    class sys():
        argv = ['a','setof3']
    if len(sys.argv) == 0:
        print('This is an interpreter for the badassembly language. please input a file location to proceed')
    else:
        default_params = {
            'push': ['push', '0', '0'],
            'pop': ['pop', '0'],
            'add': ['add', '0', '1', '0'],
            'ifeq': ['ifeq', '0', '0'],
            'ifunq': ['ifunq', '0', '0'],
            'clear': ['clear'],
            'jump': ['jump', '0'],
            'print': ['print', '0'],
            'loop': ['loop', '1'],
            'dup': ['dup', '0', '0'],
            'ret': ['ret'],
            'quit': ['quit']
        }
        stacks = {'main':stack.Stack()}
        run_file(sys.argv[1],True)
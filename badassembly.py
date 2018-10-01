import stack
import exceptions
#import sys
def run_file(file,line=0,code='',loop=1,jumpfrom=None,params = {}):
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
    pop = 0 #last number popped off the stack
    while loop > 0:
        current_line = line
        try:
            while current_line < len(lines):
                if lines[current_line].startswith('#') or not lines[current_line]:
                    current_line+=1
                    continue
                attr = list(filter(None,lines[current_line].split(' ')))
                if attr[0] not in default_params:
                    raise exceptions.NotAValidInstructionError(attr[0])
                attr = optimize_attr(attr,default_params[attr[0]],params,st,loop,pop)
                include = file
                if '-' in lines[current_line]:
                    line = 0
                    for i in range(len(attr)):
                        if '-' in attr[i] and i != 0:
                            include, line = attr[i].split('-')
                            line = int(line)
                if attr[0] == 'push': #push <number>
                    st.push(attr[1],attr[2]) #pushes <number> onto the top of stack
                elif attr[0] == 'pushin':
                    old_st = stacks[jumpfrom]
                    st.push(old_st.get_node(attr[1]))
                elif attr[0] == 'pop': #pop
                    pop = st.get_node(attr[1])
                    st.pop(attr[1]) #removes the number at the top of the stack
                elif attr[0] == 'add': #add <number1> <number2> <placement>
                    st.add(attr[1],attr[2],attr[3]) #adds the top two numbers at the top of the stack together, removes them and pushes the sum onto the stack
                elif attr[0] == 'div':
                    st.div(attr[1],attr[2],attr[3])
                elif attr[0] == 'ifeq': #ifeq <number> <address>
                    if int(attr[1]) != int(attr[2]): #if <number> is equal to the number at the top of the stack, jump to <address>
                        current_line = get_indented_code(lines,current_line)[1]
                elif attr[0] == 'ifunq': #ifnuq <number> <address>
                    if int(attr[1]) == int(attr[2]): #if <number> isnt equal to the number at the top of the stack jump to <address>
                        current_line = get_indented_code(lines,current_line)[1]
                elif attr[0] == 'clear':
                    st = stack.Stack()
                    stacks[file] = st
                elif attr[0] == 'print': #print <placement>
                    print(st.get_node(attr[1]).value) #prints the top of the stack
                elif attr[0] == 'dup': #dup <old> <new>
                    for x in range(3-len(attr)):
                        attr.append(0)
                    st.dup(attr[1],attr[2]) #puts a copy of the number at the top of the stack onto the top of the stack
                elif attr[0] == 'loop': #loop <counter> \n <code> \n end
                    input_loop = int(attr[1])
                    input_code, current_line = get_indented_code(lines,current_line)
                    run_file(file,code=input_code,loop=input_loop,params=params,jumpfrom=jumpfrom)
                elif attr[0] == 'rout':
                    input_params = [x if x.startswith('$') else '$'+x for x in attr[2:]]
                    input_params = {x.split(':')[0]:(x.split(':')[1] if x.find(':')>=0 else 'nod') for x in input_params}
                    name = attr[1]
                    if name[0] == '$':
                        raise exceptions.NameStartsWithDollar
                    code, current_line = get_indented_code(lines,current_line)
                    if file not in callable_functions:
                        callable_functions[file] = {}
                    callable_functions[file][name] = {'params': list(input_params.keys()), 'default': [attr[1]] + list(input_params.values()), 'code': code}
                elif attr[0] == 'call':
                    routine = callable_functions[include][attr[1]]
                    attr = optimize_attr(attr[1:],routine['default'],params,st,loop,pop)
                    input_params = {routine['params'][x]:attr[x+1] for x in range(len(routine['params']))}
                    run_file(include,code=routine['code'],params=input_params,jumpfrom=jumpfrom)
                elif attr[0] == 'ret': #ret <number1>......<numberX>
                    # returns to the last line you jumped from and pushes all of the proceeding numbers onto the stack in order of appearance
                    ret_stack = stacks[jumpfrom]
                    for param in attr[1:]:
                        ret_stack.push(param,'0')
                    return
                elif attr[0] == 'quit': #quit
                    print('END') #stops the program
                    break
                current_line += 1
        except exceptions.OutofBoundsError as error:
            print('line {}: {}\nOutOfBoundsError: tried to access stack slot {} that was not yet created'.format(current_line+1,lines[current_line],error.placement))
        except exceptions.NonIntegerIntoStack as error:
            print('line {}: {}\nNonIntegerIntoStack: tried to put a non integer ({}) onto the stack'.format(current_line+1,lines[current_line],error.thing))
        except exceptions.NotAValidInstructionError as error:
            print('line {}: {}\nNotAValidInstruction: the instruction "{}" is not a valid instruction'.format(current_line+1,lines[current_line],error.instruction))
        except exceptions.LoopNotClosed as error:
            print('line {}: EOF\nEndStatementNotEncountered: the instruction "{}" was not closed'.format(current_line+1,error.statement))
        except exceptions.NoDefaultPresent as error:
            print('line {}: {}\nNoDefaultPresented: parameter number {} was not present and does not have a default'.format(current_line+1,lines[current_line],error.parameter))
        except exceptions.NameStartsWithDollar:
            print('line {}: {}\nNameStartsWithDollar: creating a routine which name starts with a dollar sign is not allowed'.format(current_line+1,lines[current_line]))
        loop-=1

def optimize_attr(attr,default_params,func_params,st,loop,pop):
    '''changes attr based on the default params'''
    if 'd' in attr or len(attr) < len(default_params) or '$' in ''.join(attr):
        if '...' in default_params:
            loop_amount = len(attr)
        else:
            loop_amount = len(default_params)
        for x in range(loop_amount):
            if (len(attr) <= x or attr[x] == 'd') and (len(default_params) <= x or default_params[x] in ['nod','...']): #if no default is present, raises a NoDefaultPresent exception
                raise exceptions.NoDefaultPresent(x)
            elif len(attr) <= x: #if parameters werent found then put the default param for that slot
                attr.append(default_params[x])
            elif attr[x] == 'd': #generates default parameters
                attr[x] = default_params[x]
            elif attr[x].startswith('$'): #replace a variable with its value
                if attr[x] in func_params:
                    attr[x] = func_params[attr[x]]
                elif attr[x] == '$ask': # $ask takes input from user
                    attr[x] = input('enter input')
                elif attr[x] == '$loop': # $loop is the amount of iterations left
                    attr[x] = loop
                elif attr[x] == '$pop': # $pop is the last number poped out
                    attr[x] = pop
                elif attr[x] == '$len': #$len is the length of the stack - the amount of numbers you have on it
                    attr[x] = str(st.length)
                elif attr[x][1:].isdigit():
                    attr[x] = str(st.get_node(attr[x][1:]).value)
    return attr

def get_indented_code(lines,current_line):
    '''gets all of the code lines inside of a <name> - end statement.
       returns the code inside and the current line. if end of file reached will throw an LoopNotClosed Exception'''
    error_line = lines[current_line]
    current_line += 1
    end = 1
    input_code = ''
    while end and current_line < len(lines):
        if lines[current_line] == 'end':
            end -= 1
            if not end:
                break
        elif lines[current_line].split(' ')[0] in ['loop', 'rout', 'ifeq', 'ifunq', 'inst']:
            end += 1
        input_code += lines[current_line] + '\n'
        current_line += 1
    if current_line == len(lines):
        raise exceptions.LoopNotClosed(error_line)
    return input_code, current_line
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
            'div': ['div', '1', '0', '0'],
            'ifeq': ['ifeq', '0', '0', '0'],
            'ifunq': ['ifunq', '0', '0', '0'],
            'end':   ['end'], #this is added just a failsafe
            'clear': ['clear'],
            'jump': ['jump', '0'],
            'print': ['print', '0'],
            'loop': ['loop', 'nod'],
            'dup': ['dup', '0', '0'],
            'ret': ['ret','...'],
            'rout': ['rout', 'nod', '...'],
            'call': ['call', 'nod','...'],
            'quit': ['quit']
        }
        callable_functions = {}
        stacks = {'main':stack.Stack()}
        run_file(sys.argv[1],jumpfrom=sys.argv[1])
import stack
#import sys
def run_file(file, line=0, st = None):
    with open(file) as file_instructions:
        lines = file_instructions.read().split('\n')
        current_line = 0
        if st is None:
            st = stack.Stack()
        while current_line < len(lines):
            attr = lines[current_line].split(' ')
            include = ''
            line = 0
            if '-' in lines[current_line]:
                for i in range(len(attr)):
                    if '-' in attr[i] and i != 0:
                        include, line = attr[i].split('-')
            if attr[0] == 'push':
                st.push(int(attr[1]))
            elif attr[0] == 'pop':
                st.pop()
            elif attr[0] == 'add':
                st.add()
            elif attr[0] == 'ifeq':
                if st.bottom.value == int(attr[1]):
                    if not include:
                        current_line = int(attr[2])
                        continue
                    else:
                        st = run_file(include, line=line ,st=st)
            elif attr[0] == 'ifunq':
                if st.bottom.value != int(attr[1]):
                    if not include:
                        current_line = int(attr[2])
                        continue
                    else:
                        st = run_file(include, line=line ,st=st)
            elif attr[0] == 'jump':
                if not include:
                    current_line = int(attr[2])
                    continue
                else:
                    st = run_file(include, line=line, st=st)
            elif attr[0] == 'print':
                print(st.bottom.value)
            elif attr[0] == 'dup':
                st.dup()
            elif attr[0] == 'ret':
                return st
            elif attr[0] == 'quit':
                current_line = 'QUIT'
                continue
            current_line += 1
        if current_line == 'QUIT':
            print('end')

if __name__ == '__main__':
    class sys():
        argv = ['a','setof3']
    if len(sys.argv) == 0:
        print('This is an interpreter for the badassembly language. please input a file location to proceed')
    else:
        run_file(sys.argv[1])

import sys

#print(sys.argv[1])

# name=sys.argv[1]
# print(f"hello!,{name}")

if len(sys.argv)<2:
    print("exiting....")
    sys.exit(1)
a=sys.argv[1]   # already script name (file)is one of the argv  
                # if u pass arg in run i.e python sys_module.py 10(a),then no of argvs are =2 so program will execute  
                # if u don't pass arg in run len(sys.argv) is <2 so exits.
                # it'll run only if u provide the required args in run mentioned through sys.argv[1]

print(sys.version)          # 3.12.9 | packaged by Anaconda, Inc. | (main, Feb  6 2025, 18:49:16) [MSC v.1929 64 bit (AMD64)]
print(sys.version_info)     # sys.version_info(major=3, minor=12, micro=9, releaselevel='final', serial=0)

print(sys.path)       #['D:\\practice', 'C:\\Users\\SVCS\\anaconda3\\envs\\fullstack-agentic-ai\\python312.zip', 'C:\\Users\\SVCS\\anaconda3\\envs\\fullstack-agentic-ai\\DLLs', 'C:\\Users\\SVCS\\anaconda3\\envs\\fullstack-agentic-ai\\Lib', 'C:\\Users\\SVCS\\anaconda3\\envs\\fullstack-agentic-ai', 'C:\\Users\\SVCS\\anaconda3\\envs\\fullstack-agentic-ai\\Lib\\site-packages']

# Reading a line from standard input
print("Enter your name: ")
name = sys.stdin.readline().strip()

# Writing to standard output
sys.stdout.write(f"Hello, {name}!\n")

# Writing to standard error (useful for logs/errors)
sys.stderr.write("This is an error message.\n")


# SETTING RECURSION LIMIT
sys.setrecursionlimit(1000)  #This tells Python: “Don’t let recursion go beyond 1000 function calls.”  Saves code from crashing

def recurse(n):
    print(f"Recursion depth: {n}")
    recurse(n + 1)
try:
    recurse(1)
except RecursionError:
    print("Recursion limit reached!")


import cfunctions

print 'Server'

# buf = cfunctions.malloc(100)
msg = cfunctions.getmem()
cfunctions.memset(msg, 0, 100)
# cfunctions.initmutex()

# print 'buf:' + str(buf)

while True:
#     cfunctions.enter()
    print cfunctions.memread(msg)
#     cfunctions.leave()
    raw_input('')
import cfunctions


print 'Client'

msg = cfunctions.getmem()
# cfunctions.initmutex()

s = raw_input('Cliente escribe: ')

# cfunctions.enter()
cfunctions.memwrite(msg, s)
# cfunctions.leave()
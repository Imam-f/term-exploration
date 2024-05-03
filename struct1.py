import struct
 
var = struct.pack('hhll', 5, 10, 15, 20)
print(var)
print("Size of String representation is {}.".format(struct.calcsize('hhll')))

var = struct.pack('lhlh', 5, 10, 15, 20)
print(var)
print("Size of String representation is {}.".format(struct.calcsize('lhlh')))

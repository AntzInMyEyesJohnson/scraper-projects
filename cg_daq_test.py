from collections import namedtuple
import socket, time, struct, csv

CgRecord = namedtuple('CgRecord', ['signal', 'offset', 'bitposition', 'size'])

def load_dae(n):
    with open('CG DATA/DAE%d.csv' % (n)) as file:
        lines = file.readlines()
        def parse(item): # if an item is numeric parse it otherwise just return
            return int(item) if item.isdigit() else item.rstrip()
        # split the lines and pass the list as unpacked (*) parameters to the CgRecord constructor
        lines = [CgRecord(*[parse(item) for item in line.split(',')]) for line in lines]
        return lines

# header bytes taken from DAE Message Format.doc
headers = {6: 2, 11: 3, 16: 4, 21: 5, 26: 6, 31: 7, 36: 8}
headers = {k: load_dae(v) for k, v in headers.items()} # remap values by loading dae data

# currently not used
def checksum(data):
    check = 0
    for byte in range(len(data) - 2):
        check += byte
    check = check % (2 ** 16)
    return check == struct.unpack('!H', data[-2:]) # return whether check matches last two bytes as unsigned short

# create masks of size 1, 2, and 4
masks = {v: int('1' * v, 2) for v in [1, 2, 4]}

# the struct module is used to unpack binary data (think bytebuffer)
def value(data, cg_item):
    start = int(cg_item.offset)# already accounted for
    if cg_item.size == '32':
        end = start + 4
       #print(struct.unpack('f',struct.pack('f',(data[start:end]))))
        #if (int(cg_item.offset) == 151):
        # print("data: " + str(cg_item.offset) + ".[0]" + str(int(data[start:end][0])) + ".[1]" + str(int(data[start:end][1])) + ".[2]" + str(int(data[start:end][2])) + ".[3]" + str(int(data[start:end][3])))
        # print("data: " + str(cg_item.offset) + "-" + str(data[start:end]))
        # #print(data[start]+data[start+1]+data[start+2]+data[start+3])
        # print("data: " + str(cg_item.offset) + "." + str(start) + "-" + str(data[start]))
        # print("data: " + str(cg_item.offset) + "." + str(start+1) + "-" + str(data[start+1]))
        # print("data: " + str(cg_item.offset) + "." + str(start+2) + "-" + str(data[start+2]))
        # print("data: " + str(cg_item.offset) + "." + str(start+3) + "-" + str(data[start+3]))
        # print("data: " + str(cg_item.offset) + "." + str(end) + "-" + str(data[end]))
        # print("data: " + str(cg_item.offset) + "=" + str(struct.unpack('f',data[start:end])[0]))
        return struct.unpack('!f', data[start:end])[0] # unpack float
    elif cg_item.size == '16':
        end = start + 2
        # print("data: " + str(cg_item.offset) + "." + str(data[start:end]))
        return struct.unpack('!h', data[start:end])[0] # unpack short
    elif cg_item.size == '8':
        # print("data: " + str(cg_item.offset) + "." + str(data[start]))
        return data[start] # return byte
    else: # if we need to do weird manipulation
        mask = masks[int(cg_item.size)] # get bit mask of length size
        shift = 8-int(cg_item.size)-cg_item.bitposition
        mask = mask << shift # upshift to match position (0 is leftmost bit)
        # print("data: " + str(cg_item.offset) + "." + str((data[start] & mask) >> shift))
        return (data[start] & mask) >> shift # mask the byte and downshift

#UDP_IP = '192.168.1.70' # fill this in
#UDP_PORT = 1776 # fill this in
#SECONDS_TO_RUN = 10 # fill this in

with open('packetbytes3.txt', 'r') as infile:
    line = infile.readline().strip().split(",")
    #bytedata = [int(line[0:2],16)]+[int(i,16) for i in line[0:]]
    bytedata = [int(i,16) for i in line[0:]]
    #packet = bytes(bytedata)
    #for col in inreader:
    #    data.extend(int(col[0]))
    #print(packet)
    with open('output.csv', 'w') as outfile:
        print(bytedata[50:54])
        packet = bytes(bytedata)
        print(packet)
        dae = packet[0]
        print(str(packet[50])+str(packet[51])+str(packet[52])+str(packet[53]))
        readings = [str()]
        print(dae in headers)
        if dae in headers:
            for cg_item in headers[dae]:
                readings.extend((cg_item.signal, str(value(packet, cg_item))))
            #print(','.join(readings).replace('(','').replace(')','').replace(',,',','))
            #outfile.write(','.join(readings).replace('(','').replace(')','').replace(',,',','))
            #outfile.write('\n')

"""
    with open('output.csv', 'w') as outfile:
        start = time.time()
        t = start
        while t - start < SECONDS_TO_RUN:
            data = inreader.(4096)
            dae = data[0] # header byte
            readings = [str(t)]
            if dae in headers:
                for cg_item in headers[dae]: # get item list for DAE
                    readings.extend((cg_item.signal, str(value(data, cg_item))))
                outfile.write(','.join(readings))
                outfile.write('\n')
            t = time.time() # update time
"""
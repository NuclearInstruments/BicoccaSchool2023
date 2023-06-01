from scisdk.scisdk import SciSDK
import matplotlib.pyplot as plt
from struct import unpack

# initialize Sci-SDK library
sdk = SciSDK()
#DT1260
res = sdk.AddNewDevice("usb:28686","dt1260", "./library/RegisterFile.json","board0")
if res != 0:
    print ("Script exit due to connection error")
    exit()


# configure all algorithm parameters

res = sdk.SetRegister("board0:/Registers/THRESHOLD", 2350)
res += sdk.SetRegister("board0:/Registers/DELTA", 50)
res += sdk.SetRegister("board0:/Registers/INT_LENGTH", 120)
res += sdk.SetRegister("board0:/Registers/PRE_LENGTH", 4)
res += sdk.SetRegister("board0:/Registers/GAIN", 1000)
res += sdk.SetRegister("board0:/Registers/BLLEN", 6)
res += sdk.SetRegister("board0:/Registers/COINC_WIDTH", 10)
res += sdk.SetRegister("board0:/Registers/FAKE_CH", 500)

if res != 0:
    print ("Configuration error")
    exit()



res = sdk.SetParameterString("board0:/MMCComponents/CP_0.thread", "true")
res = sdk.SetParameterInteger("board0:/MMCComponents/CP_0.timeout", 500)
res = sdk.SetParameterString("board0:/MMCComponents/CP_0.acq_mode", "blocking")
# allocate buffer raw, size 1024
res, buf = sdk.AllocateBuffer("board0:/MMCComponents/CP_0", 100)
res = sdk.ExecuteCommand("board0:/MMCComponents/CP_0.stop", "")
res = sdk.ExecuteCommand("board0:/MMCComponents/CP_0.start", "")
res = sdk.SetParameterString("board0:/MMCComponents/CP_0.data_processing", "decode")

E00 = []
E01 = []
E10 = []
E11 = []
while True:
    res, buf = sdk.ReadData("board0:/MMCComponents/CP_0", buf)
    if res == 0:
        for i in range(0, int(buf.info.valid_data)):
  
            print("header:      ", hex(buf.data[i].row[0]))
            print("timestamp:   ",buf.data[i].row[1] )
            x0 = buf.data[i].row[2] >> 16
            x1 = buf.data[i].row[2] & 0xFFFF
            y0 = buf.data[i].row[3] >> 16
            y1 = buf.data[i].row[3] & 0xFFFF
            # print("x0:          ", x0)
            # print("x1:          ", x1)
            # print("y1:          ", y0)
            # print("y2:          ", y1)
            # print("-----------------")
            E00.append(x0+y0)
            E01.append(x0+y1)
            E10.append(x1+y0)
            E11.append(x1+y1)
        print(len(E00))
        if len(E00) > 10000:
            break
# plot 4 histograms on the same windows in 4 different subplot 
plt.subplot(2,2,1)
plt.hist(E00, bins=256)
plt.subplot(2,2,2)
plt.hist(E01, bins=256)
plt.subplot(2,2,3)
plt.hist(E10, bins=256)
plt.subplot(2,2,4)
plt.hist(E11, bins=256)
plt.show()


while True:
    pass

# array_energy = []
# array_time = []
# while True:
#     res, buf = sdk.ReadData("board0:/MMCComponents/CP_0", buf)
#     if res == 0:
#         for i in range(0, int(buf.info.valid_samples/8)):
#             # E E E E          T T T T
#             # i*8 -> i*8+4     i*8+4 -> i*8+8
#             E = unpack('<L', buf.data[i*8:i*8+4])[0]
#             T = unpack('<L', buf.data[i*8+4:(i+1)*8])[0]
#             array_energy.append(E)
#             array_time.append(T)
#     print(len(array_energy))
#     if len(array_energy) > 100000:
#         break

# time_delta = []
# for i in range(1, len(array_time)):
#     time_delta.append(array_time[i] - array_time[i-1])

# #plt.hist(array_energy, bins=256)
# #plt.scatter(array_time, array_energy, s=1)
# plt.hist(time_delta, bins=256)
# plt.show()
# while True:
#     pass
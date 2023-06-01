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
res += sdk.SetRegister("board0:/Registers/DELTAHIST", 50)
res += sdk.SetRegister("board0:/Registers/INT_LENGTH", 120)
res += sdk.SetRegister("board0:/Registers/PRE_LENGTH", 4)
res += sdk.SetRegister("board0:/Registers/PILEUP", 0)
res += sdk.SetRegister("board0:/Registers/GAININT", 1500)
res += sdk.SetRegister("board0:/Registers/OFFSET_INT", 0)
res += sdk.SetRegister("board0:/Registers/BL_LENGTH", 6)

if res != 0:
    print ("Configuration error")
    exit()

# # set oscilloscope parameters on the board
# res = sdk.SetParameterString("board0:/MMCComponents/Oscilloscope_0.data_processing","decode")
# res = sdk.SetParameterInteger("board0:/MMCComponents/Oscilloscope_0.trigger_level",2250)
# res = sdk.SetParameterString("board0:/MMCComponents/Oscilloscope_0.trigger_mode","analog")
# res = sdk.SetParameterInteger("board0:/MMCComponents/Oscilloscope_0.trigger_channel", 0)
# res = sdk.SetParameterInteger("board0:/MMCComponents/Oscilloscope_0.pretrigger", 150)
# res = sdk.SetParameterInteger("board0:/MMCComponents/Oscilloscope_0.decimator", 0)
# res = sdk.SetParameterString("board0:/MMCComponents/Oscilloscope_0.acq_mode", "blocking")

# # allocate buffer (sciSDK detects automatically buffer type)
# res, buf = sdk.AllocateBuffer("board0:/MMCComponents/Oscilloscope_0")
# if res == 0:
#     res = sdk.ExecuteCommand("board0:/MMCComponents/Oscilloscope_0.reset_read_valid_flag", "")
#     # read data
#     res, buf = sdk.ReadData("board0:/MMCComponents/Oscilloscope_0", buf)

# print(res)

# if res == 0:
#     # store analog data inside a file
#     for j in range(0,3):
#         analog_str = ""
#         channel_memory_offset = buf.info.samples_analog * j
#         for i in range(channel_memory_offset, channel_memory_offset+buf.info.samples_analog):
#             analog_str = analog_str + str(buf.analog[i]) + "\t"
#         print(analog_str)
#         print("------------\n")


#     digital_str = ""
#     # read digital data from channel 1
#     for i in range(0,buf.info.samples_digital):
#         digital_str = digital_str + str(buf.digital[i]) + "\n"
#     digital_str = ""
#     # read digital data from channel 2
#     for i in range(buf.info.samples_digital,buf.info.samples_digital*2):
#         digital_str = digital_str + str(buf.digital[i]) + "\n"

#     array_plot = []
#     for j in range(0,3):
#         channel_memory_offset = 0
#         for i in range(channel_memory_offset, channel_memory_offset+buf.info.samples_analog):
#             array_plot.append(buf.analog[i])

#     plt.plot(array_plot)
#     plt.show()


res = sdk.SetParameterString("board0:/MMCComponents/List_1.thread", "true")
res = sdk.SetParameterInteger("board0:/MMCComponents/List_1.timeout", 500)
res = sdk.SetParameterString("board0:/MMCComponents/List_1.acq_mode", "blocking")
# allocate buffer raw, size 1024
res, buf = sdk.AllocateBuffer("board0:/MMCComponents/List_1", 100)
res = sdk.ExecuteCommand("board0:/MMCComponents/List_1.stop", "")
res = sdk.ExecuteCommand("board0:/MMCComponents/List_1.start", "")
array_energy = []
array_time = []
while True:
    res, buf = sdk.ReadData("board0:/MMCComponents/List_1", buf)
    if res == 0:
        for i in range(0, int(buf.info.valid_samples/8)):
            # E E E E          T T T T
            # i*8 -> i*8+4     i*8+4 -> i*8+8
            E = unpack('<L', buf.data[i*8:i*8+4])[0]
            T = unpack('<L', buf.data[i*8+4:(i+1)*8])[0]
            array_energy.append(E)
            array_time.append(T)
    print(len(array_energy))
    if len(array_energy) > 100000:
        break

time_delta = []
for i in range(1, len(array_time)):
    time_delta.append(array_time[i] - array_time[i-1])

#plt.hist(array_energy, bins=256)
#plt.scatter(array_time, array_energy, s=1)
plt.hist(time_delta, bins=256)
plt.show()
while True:
    pass
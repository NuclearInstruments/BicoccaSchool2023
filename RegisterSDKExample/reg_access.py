from scisdk.scisdk import SciSDK

# initialize scisdk library
sdk = SciSDK()
#DT1260
res = sdk.AddNewDevice("usb:28686","dt1260", "./library/RegisterFile.json","board0")
if res != 0:
    print ("Script exit due to connetion error")
    exit()

regA=100
regB=151
regC = 0
sdk.SetRegister("board0:/Registers/A", regA)
sdk.SetRegister("board0:/Registers/B", regB)
err, regC = sdk.GetRegister("board0:/Registers/C")
print("Register C = (A+B) value is ", regC)


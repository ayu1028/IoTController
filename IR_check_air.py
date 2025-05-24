import time
from gpiozero import Button
import json

# obtain read pin number
pin = 5
# obtain wait interval (us)
wait = 4e4
# baud [us]
T = 425
# signal length for air-con command
len_signal = 633

button = Button(pin)

def current():
    return time.time() * 1e6

def find_all_string_indices(arr, target):
    return [i for i, x in enumerate(arr) if x == target]

def scanSignal():
    buffer = [0.0] * 1024
    current_time = 0.0
    current_state = 0
    last_state = 0
    offset = 0

    last_state = button.is_pressed

    print("scanning start")
    while True:
        current_time = current()
        if offset and current_time > buffer[offset - 1] + wait:
            break

        current_state = button.is_pressed
        if current_state != last_state:
            buffer[offset] = current_time
            offset += 1
            last_state = current_state

    print("Scanning end")

    data = []
    for i in range(1, offset):
        data.append(int(buffer[i] - buffer[i - 1]))
    
    return data

def binary_change(signalList: list):
    data = [ x/T for x in signalList ]
    data_bit = []

    if len(signalList) != len_signal:
        print("")

    for i in range(len(data)):
        if i == len(data)-1:
            data_bit.append('trailer')
            break

        if i & 1:
            if i == 1:
                data_bit.append('header')
            elif i == 3 or i == 327:
                data_bit.append('leader')
            elif i == 325:
                data_bit.append('trailer')
            elif data[i] < 2:
                data_bit.append(0)
            else:
                data_bit.append(1)

    return data_bit

def frame_change_bin(frame: list):
    bin_string_array = []
    step = 8

    for i in range(0, len(frame), step):
        if i == len(frame)-1:
            break
        array = frame[i:i+step]
        array.reverse()
        binary_string_reverse = "".join(map(str, array))
        bin_string_array.append(binary_string_reverse)
    
    return bin_string_array

def frame_change_hex(frame_bin: list):
    hex_string_array = []
    for string_data in frame_bin:
        bin_value = int(string_data, 2)
        hex_string_array.append(format(bin_value, "02X"))

    return hex_string_array


# def compareSignal(signal1: list, signal2: list):
#     signal1Len, signal2Len = len(signal1), len(signal2)
#     if signal1Len != signal2Len:
#         print(f"scan data length(len:{signal1Len}) and exist data length(len:{signal2Len}) are not equal")
#         return signal2
    
#     data = []
#     for i in range(signal1Len):
#         data.append(int((signal1[i] + signal2[i])*0.5))

#     return data

def main():
    fileName = "IR_data_air_compare.json"
    while True:
        signalName = input('input signal name("q" to suit):')
        if signalName == "q":
            print("finish scanning")
            break

        while True:
            scanData = scanSignal()
            if len(scanData) != len_signal:
                input("scanning error, press enter to scan again.")
            else:
                print('OK')
                break

        scanData_bit = binary_change(scanData)

        leaderIndices = find_all_string_indices(scanData_bit, "leader")
        trailerIndices = find_all_string_indices(scanData_bit, "trailer")

        frame1 = scanData_bit[leaderIndices[0]+1:trailerIndices[0]]
        frame2 = scanData_bit[leaderIndices[1]+1:trailerIndices[1]]

        frame1_bin = frame_change_bin(frame1)
        frame1_hex = frame_change_hex(frame1_bin)

        frame2_bin = frame_change_bin(frame2)
        frame2_hex = frame_change_hex(frame2_bin)
 
        signalData = { signalName: {'signal': scanData,
                                    'bin': scanData_bit,
                                    'bin_r':{
                                        'frame1': frame1_bin,
                                        'frame2': frame2_bin,
                                    },
                                    'hex':{
                                        'frame1': frame1_hex,
                                        'frame2': frame2_hex,
                                    },},}

        try:
            with open(fileName, "r") as f:
                inputData = json.load(f)
        except FileNotFoundError:
            inputData = {}
        
        inputData.update(signalData)

        # if not inputData.get(signalName): # if there is no signalName key
        #     inputData.update(signalData)

        # else:
        #     action = input(f"{signalName} already exists, choose your action(1: overwrite, 2:compare and overwrite, 3: none):")
        #     if action == 1:
        #         inputData.update(signalData)

        #     if action == 2:
        #         comparedData = compareSignal(signalData[signalName], inputData[signalName])
        #         updateData = {signalName: comparedData }
        #         inputData.update(updateData)

        #     if action == 3:
        #         pass

        with open(fileName, "w") as f:
            # f.write(json.dumps(inputData, sort_keys=True).replace("],", "],\n")+"\n")
            saveData = json.dumps(inputData, sort_keys=False).replace("},", "},\n")
            saveData = saveData.replace("],", "],\n")
            saveData = saveData.replace("{", "{\n")
            f.write(saveData + "\n")
        
        print(f"{signalName} signal output end")

    return 0

if __name__ == "__main__":
    main()

import serial
import damp11113

class ardstatusError(Exception):
    pass

# Open the serial port from the Arduino
class ardstatus:
    def __init__(self, arduinopath):
        try:
            self.ard = serial.Serial(arduinopath, 9600)
        except:
            raise ardstatusError('Could not open serial port')

    def soutput(self, output_num, state):
        try:
            if output_num == 1:
                if state == 1:
                    self.ard.write(b'output1: on')
                elif state == 0:
                    self.ard.write(b'output1: off')
            elif output_num == 2:
                if state == 1:
                    self.ard.write(b'output2: on')
                elif state == 0:
                    self.ard.write(b'output2: off')
            elif output_num == 3:
                if state == 1:
                    self.ard.write(b'output3: on')
                elif state == 0:
                    self.ard.write(b'output3: off')
            elif output_num == 4:
                if state == 1:
                    self.ard.write(b'output4: on')
                elif state == 0:
                    self.ard.write(b'output4: off')
            elif output_num == 5:
                if state == 1:
                    self.ard.write(b'output5: on')
                elif state == 0:
                    self.ard.write(b'output5: off')
            elif output_num == 6:
                if state == 1:
                    self.ard.write(b'output6: on')
                elif state == 0:
                    self.ard.write(b'output6: off')
            elif output_num == 7:
                if state == 1:
                    self.ard.write(b'output7: on')
                elif state == 0:
                    self.ard.write(b'output7: off')
            elif output_num == 8:
                if state == 1:
                    self.ard.write(b'output8: on')
                elif state == 0:
                    self.ard.write(b'output8: off')
            elif output_num == 9:
                if state == 1:
                    self.ard.write(b'output9: on')
                elif state == 0:
                    self.ard.write(b'output9: off')
            elif output_num == 10:
                if state == 1:
                    self.ard.write(b'output10: on')
                elif state == 0:
                    self.ard.write(b'output10: off')
            elif output_num == 11:
                if state == 1:
                    self.ard.write(b'output11: on')
                elif state == 0:
                    self.ard.write(b'output11: off')
            elif output_num == 12:
                if state == 1:
                    self.ard.write(b'output12: on')
                elif state == 0:
                    self.ard.write(b'output12: off')
        except:
            raise ardstatusError('Could not write to serial port')

    def sinput(self, inputstate):
        # read the serial port
        try:
            _data = self.ard.readline()
            data = damp11113.byte2str(_data)
            # return the data
            if inputstate == 1:
                if data == 'input1: on':
                    return 1
                elif data == 'input1: off':
                    return 0
            elif inputstate == 2:
                if data == 'input2: on':
                    return 1
                elif data == 'input2: off':
                    return 0
            elif inputstate == 3:
                if data == 'input3: on':
                    return 1
                elif data == 'input3: off':
                    return 0
            elif inputstate == 4:
                if data == 'input4: on':
                    return 1
                elif data == 'input4: off':
                    return 0
        except:
            raise ardstatusError('Could not read serial port')

    def slcd(self, message, line):
        try:
            if line == 1:
                self.ard.write(bytes(f'{message} 1', 'utf-8'))
            elif line == 2:
                self.ard.write(bytes(f'{message} 2', 'utf-8'))
        except:
            raise ardstatusError('Could not write to serial port')
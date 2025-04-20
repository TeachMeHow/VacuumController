#keyboardWin.py

import keyboard


class Buffer:
    pwd = "1234"
    buffer = ''
    def check_password(self, event: keyboard.KeyboardEvent):
        c = event.name
        self.buffer = self.buffer + c
        print(self.buffer)
        print(event.device)
        if len(self.buffer) >= 4:
            if self.buffer == self.pwd:
                print("TRUE")
            else:
                print("FALSE")
            self.buffer = ''
        
try:
    buffer = Buffer()
    keyboard.on_press(buffer.check_password)
    keyboard.wait()
except KeyboardInterrupt:
    pass
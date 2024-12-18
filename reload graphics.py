# kboard means Keyboard, if you can't be bothered to think
print("Choices: 1. reload graphics, 2. goodbye, 3. go yeet self 4. wait (needs curseforge to work)")
choice=int(input("enter a number (1,2,3,4):"))
if choice ==1: import os
# if choice ==1: os.system("pip install pynput")
# uncomment if you
if choice ==1: import pynput
if choice ==1: from pynput.keyboard import Key, Controller
if choice ==1: kboard = Controller()
if choice ==1: kboard.press(Key.ctrl_l)
if choice ==1: kboard.press(Key.shift_l)
if choice ==1: kboard.press(Key.cmd_l)
if choice ==1: kboard.press('b')
if choice ==1: kboard.release('b')
if choice ==1: kboard.release(Key.cmd_l)
if choice ==1: kboard.release(Key.shift_l)
if choice ==1: kboard.release(Key.ctrl_l)
elif choice ==2: print("ok bye")
elif choice ==3: os.system("shutdown -r -fw -t 10")
elif choice ==4: os.system("C:\\Users\\Oem\\curseforge\\minecraft\\Install\\assets\\virtual\\legacy\\sounds\\records\\wait.ogg")

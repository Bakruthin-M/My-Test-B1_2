import pyautogui
import time

print("Automation starts in 5 seconds...")
time.sleep(5)

pyautogui.write("Hello from Python automation!", interval=0.05)
pyautogui.press("enter")
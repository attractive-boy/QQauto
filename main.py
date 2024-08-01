import os
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import psutil
import pyautogui
import pygetwindow as gw
import re
import win32file
import win32con
import win32api

class AudioMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("音频文件监控和QQ拨打")
        self.audio_file_path = None
        self.root.geometry("400x300")  # 设置窗口大小为 400x300
        self.select_button = tk.Button(root, text="选择音频文件", command=self.select_audio_file)
        self.select_button.pack(pady=10)

        self.qq_label = tk.Label(root, text="输入QQ号:")
        self.qq_label.pack(pady=5)
        self.qq_entry = tk.Entry(root)
        self.qq_entry.pack(pady=5)

        self.start_button = tk.Button(root, text="开始监控", command=self.start_monitoring, state=tk.DISABLED)
        self.start_button.pack(pady=20)

    def select_audio_file(self):
        self.audio_file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
        if self.audio_file_path:
            self.start_button.config(state=tk.NORMAL)

    def start_monitoring(self):
        self.qq_number = self.qq_entry.get()
        if not self.qq_number:
            messagebox.showwarning("输入错误", "请输入QQ号")
            return

        self.monitor_thread = threading.Thread(target=self.monitor_audio_file_access)
        self.monitor_thread.start()

    def is_file_in_use(self,file_path):
        try:
            file_handle = win32file.CreateFile(
                file_path,
                win32con.GENERIC_READ,
                0,  # No sharing
                None,
                win32con.OPEN_EXISTING,
                0,
                None
            )
            win32file.CloseHandle(file_handle)
            return False  # File is not in use
        except win32api.error as e:
            if e.args[0] == 32:  # ERROR_SHARING_VIOLATION
                return True  # File is in use
            else:
                raise  # Reraise if not the expected error
    def monitor_audio_file_access(self):
        # try:
            #修改按钮文字为监控中，禁用点击
            self.start_button.config(text="监控中", state=tk.DISABLED)
            monitored_file = self.audio_file_path
            while True:
                if self.is_file_in_use(monitored_file):
                    self.trigger_qq_call()  
        # except Exception as e:
        #     print(f"Error occurred: {e}")
        #     self.start_button.config(text="开始监控", state=tk.NORMAL) 
    def call(self):
        # 点击窗体中心 右键清屏
        time.sleep(1)
         # 在屏幕上找到图像
        location = pyautogui.locateCenterOnScreen('./img/call.png', confidence=0.8)
        if location:
            
            time.sleep(1)
            pyautogui.click(location)
            print(f"Clicked on 'call' button at location: {location}")
        
            while True:
                time.sleep(1)   
                try: 
                    called = pyautogui.locateCenterOnScreen('./img/calling.png', confidence=0.5)
                    if called:
                        continue
                except pyautogui.ImageNotFoundException as e:
                    pass
                try: 
                    called = pyautogui.locateCenterOnScreen('./img/incall.png', confidence=0.8)
                    if called:
                        break
                except pyautogui.ImageNotFoundException as e:
                    pass
                try:
                    location = pyautogui.locateCenterOnScreen('./img/call.png', confidence=0.8)
                    if location:
                        pyautogui.click(location)
                        continue
                except pyautogui.ImageNotFoundException as e:
                    pass
                    
                
                    
    def trigger_qq_call(self):
        # 使用PyAutoGUI模拟QQ拨打电话的过程
        # 假设QQ已经登录并且在桌面上
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'alt', 'z') 
        time.sleep(2)
        search = pyautogui.locateCenterOnScreen('./img/searchbar.png', confidence=0.5)
        if search:
            pyautogui.click(search)
            pyautogui.typewrite(self.qq_number)
            time.sleep(1)
            pyautogui.press('enter')
            self.call()

        # pyautogui.typewrite('3830444542')
        
        
        time.sleep(1)
        

if __name__ == "__main__":
    #查看当前时间是否大于8月2日
    if time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) > '2024-08-03 00:00:00':
        print("程序已过期，请重新下载")
        exit()
    root = tk.Tk()
    app = AudioMonitorApp(root)
    root.mainloop()

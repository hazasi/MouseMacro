import pyautogui
import keyboard
import json
import time
import psutil
import win32gui
import win32con
import win32process
from pynput import mouse
from ctypes import windll

class MouseAutomation:
    def __init__(self):
        self.recording = False
        self.actions = []
        self.start_time = None
        self.target_process_name = "Caravan.exe"
        self.play_count = 1
        self.play_interval = 1.0  # in seconds
        self.stop_playback = False
        self.actions_loaded = False
        self.mouse_listener = None
        self.mouse_control_enabled = True

    def start_recording(self):
        self.recording = True
        self.actions = []
        self.start_time = time.time()
        print("Recording started...")

    def stop_recording(self):
        self.recording = False
        print("Recording stopped.")

    def list_actions(self):
        for action in self.actions:
            print(action)

    def save_actions(self, filename='actions.json'):
        data = {
            'actions': self.actions,
            'play_count': self.play_count,
            'play_interval': self.play_interval
        }
        with open(filename, 'w') as f:
            json.dump(data, f)
        print(f"Actions saved to {filename}")

    def load_actions(self, filename='actions.json'):
        with open(filename, 'r') as f:
            data = json.load(f)
            self.actions = data['actions']
            self.play_count = data.get('play_count', 1)
            self.play_interval = data.get('play_interval', 1.0)
            self.actions_loaded = True
        print(f"Actions loaded from {filename}")

    def play_actions(self):
        self.stop_playback = False
        for count in range(self.play_count):
            if self.stop_playback:
                print("Playback stopped.")
                break
            hwnd = self.get_target_window()
            if hwnd:
                self.bring_window_to_foreground(hwnd)
                self.enable_mouse_control(False)
                self.start_time = time.time()  # Set start time before playing actions
                for action in self.actions:
                    if self.stop_playback:
                        print("Playback stopped.")
                        break
                    delay = action['time'] - (time.time() - self.start_time)
                    if delay > 0:
                        print(f"Waiting for {delay:.2f} seconds before next action...")
                        time.sleep(delay)
                    pyautogui.click(action['x'], action['y'])
                if count < self.play_count - 1 and not self.stop_playback:
                    self.enable_mouse_control(True)
                    print(f"Waiting for {self.play_interval} seconds before next playback...")
                    self.countdown(self.play_interval)
                    self.enable_mouse_control(False)
                print(f"Playback {count + 1}/{self.play_count} completed.")
                # Ensure the window is brought to foreground again for the next cycle
                hwnd = self.get_target_window()
                if hwnd:
                    self.bring_window_to_foreground(hwnd)
            else:
                print(f"Window with process name {self.target_process_name} not found.")
                break
        self.enable_mouse_control(True)
        if not self.stop_playback:
            print("All actions played.")

    def countdown(self, interval):
        for i in range(int(interval), 0, -1):
            print(f"Next playback in {i} seconds...", end='\r')
            time.sleep(1)
        print(" " * 30, end='\r')  # Clear the line

    def get_target_window(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == self.target_process_name:
                pid = proc.info['pid']
                def enum_windows_proc(hwnd, lParam):
                    _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                    if found_pid == pid:
                        lParam.append(hwnd)
                hwnds = []
                win32gui.EnumWindows(enum_windows_proc, hwnds)
                return hwnds[0] if hwnds else None
        return None

    def bring_window_to_foreground(self, hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)

    def on_click(self, x, y, button, pressed):
        if self.recording and pressed and button == mouse.Button.left:
            hwnd = self.get_target_window()
            if hwnd:
                self.bring_window_to_foreground(hwnd)
            action = {
                'time': time.time() - self.start_time,
                'type': 'click',
                'x': x,
                'y': y
            }
            self.actions.append(action)
            print(action)

    def enable_mouse_control(self, enable):
        self.mouse_control_enabled = enable
        if enable:
            if self.mouse_listener is None:
                self.mouse_listener = mouse.Listener(on_click=self.on_click)
                self.mouse_listener.start()
        else:
            if self.mouse_listener is not None:
                self.mouse_listener.stop()
                self.mouse_listener = None

    def set_play_count(self, count):
        self.play_count = count
        print(f"Play count set to {self.play_count}")

    def set_play_interval(self, interval):
        self.play_interval = interval
        print(f"Play interval set to {self.play_interval} seconds")

    def console_menu(self):
        while True:
            print("\nConsole Menu:")
            print(f"Actions loaded: {'Yes' if self.actions_loaded else 'No'}")
            print(f"Play count: {self.play_count}")
            print(f"Play interval: {self.play_interval} seconds")
            print("1. Start recording (F7)")
            print("2. Stop recording (F8)")
            print("3. List actions (F9)")
            print("4. Play actions (F10)")
            print("5. Save actions (F11)")
            print("6. Load actions (F12)")
            print("7. Set play count")
            print("8. Set play interval")
            print("9. Stop playback (F4)")
            print("0. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.start_recording()
            elif choice == '2':
                self.stop_recording()
            elif choice == '3':
                self.list_actions()
            elif choice == '4':
                self.play_actions()
            elif choice == '5':
                self.save_actions()
            elif choice == '6':
                self.load_actions()
            elif choice == '7':
                count = int(input("Enter play count: "))
                self.set_play_count(count)
            elif choice == '8':
                interval = float(input("Enter play interval (seconds): "))
                self.set_play_interval(interval)
            elif choice == '9':
                self.stop_playback = True
                print("Playback stopped.")
            elif choice == '0':
                break
            else:
                print("Invalid choice. Please try again.")

automation = MouseAutomation()

keyboard.add_hotkey('F7', automation.start_recording)
keyboard.add_hotkey('F8', automation.stop_recording)
keyboard.add_hotkey('F9', automation.list_actions)
keyboard.add_hotkey('F10', automation.play_actions)
keyboard.add_hotkey('F11', lambda: automation.save_actions('actions.json'))
keyboard.add_hotkey('F12', lambda: automation.load_actions('actions.json'))
keyboard.add_hotkey('F4', lambda: setattr(automation, 'stop_playback', True))

automation.enable_mouse_control(True)

automation.console_menu()

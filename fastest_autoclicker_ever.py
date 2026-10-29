import threading
import time
import tkinter as tk
import pyautogui

# Safety fail-safe: move mouse to any corner of the screen to abort
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.001


class FastAutoClicker:

  def __init__(self, root):
    self.root = root
    self.root.title("The Fastest Autoclicker in Existence")
    self.root.geometry("360x240")
    self.root.resizable(False, False)
    self.root.configure(bg="#1e1e1e")

    self.clicking = False
    self.click_thread = None

    # Styling colors
    self.bg_color = "#1e1e1e"
    self.fg_color = "#ffffff"
    self.accent_color = "#00ffcc"
    self.btn_bg = "#333333"

    # Title Label
    self.title_label = tk.Label(
        root,
        text="THE FASTEST AUTOCLICKER",
        font=("Helvetica", 13, "bold"),
        bg=self.bg_color,
        fg=self.accent_color,
    )
    self.title_label.pack(pady=15)

    # Status Label
    self.status_label = tk.Label(
        root,
        text="Status: STOPPED",
        font=("Helvetica", 12, "bold"),
        bg=self.bg_color,
        fg="#ff4444",
    )
    self.status_label.pack(pady=5)

    # Instructions
    self.instruction_label = tk.Label(
        root,
        text="Press [ F4 ] to Toggle Start/Stop\nInterval: 5ms (200 CPS Sweet Spot)",
        font=("Helvetica", 10),
        bg=self.bg_color,
        fg="#aaaaaa",
        justify=tk.CENTER,
    )
    self.instruction_label.pack(pady=10)

    # Manual Toggle Button
    self.toggle_btn = tk.Button(
        root,
        text="START / STOP (F4)",
        font=("Helvetica", 10, "bold"),
        bg=self.btn_bg,
        fg=self.fg_color,
        activebackground=self.accent_color,
        activeforeground="#000000",
        relief=tk.FLAT,
        padx=10,
        pady=5,
        command=self.toggle_clicking,
    )
    self.toggle_btn.pack(pady=10)

    # Bind hotkey
    self.root.bind("<F4>", lambda event: self.toggle_clicking())
    self.setup_global_hotkey()

  def click_loop(self):
    interval = 0.005  # 5ms sweet spot mode
    next_click = time.perf_counter()

    while self.clicking:
      try:
        pyautogui.click()
      except Exception:
        break

      next_click += interval
      sleep_time = next_click - time.perf_counter()
      if sleep_time > 0:
        time.sleep(sleep_time)
      else:
        next_click = time.perf_counter()

  def toggle_clicking(self, event=None):
    if not self.clicking:
      self.clicking = True
      self.status_label.config(text="Status: RUNNING ⚡", fg=self.accent_color)
      self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
      self.click_thread.start()
    else:
      self.clicking = False
      self.status_label.config(text="Status: STOPPED", fg="#ff4444")

  def setup_global_hotkey(self):
    try:
      import keyboard

      keyboard.add_hotkey("f4", self.toggle_clicking)
    except ImportError:
      pass


if __name__ == "__main__":
  root = tk.Tk()
  app = FastAutoClicker(root)
  root.mainloop()
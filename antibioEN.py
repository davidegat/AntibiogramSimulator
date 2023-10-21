import tkinter as tk
from tkinter import ttk
import random
import math
from PIL import Image, ImageTk
import pygame
import sys
import ctypes

def hide_terminal_window():
    if sys.platform == "win32":
        ctypes.windll.user32.ShowWindow(
            ctypes.windll.kernel32.GetConsoleWindow(), 0)
        
class AntibiogramSimulation:
    def __init__(self, root):
        hide_terminal_window()
        pygame.mixer.init()
        pygame.init()
        self.track_sound = pygame.mixer.Sound("audio.mp3")
        self.track_sound.set_volume(0.4)
        self.track_channel = self.track_sound.play(loops=-1)
        
        self.root = root
        self.root.title("Antibiogram Simulation")

        self.fixed_font = ("Arial", 13)
        self.fixed_font2 = ("Arial", 15, "bold")
        self.root.option_add("*TButton*Padding", [5, 5])

        self.style = ttk.Style()
        self.style.configure("TButton", font=self.fixed_font)

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.grid(row=1, column=0, columnspan=3)

        self.bacteria_culture_radius = 250
        self.bacteria_culture_x = 400
        self.bacteria_culture_y = 300
        self.bacteria_culture_color = 'violet'

        self.antibiotic_size = 20
        self.antibiotic_outlines = [0, 5, 20]
        self.antibiotics = []

        self.antibiotic_names = ["Amoxicillin", "Ciprofloxacin", "Erythromycin"]
        self.bacteria_names = [
    "\nBlood Culture\n\nAdd the three antibiotics and\nwait for resuts",
    "\nUrine Culture\n\nAdd the three antibiotics and\nwait for resuts",
    "\nSputum Culture\n\nAdd the three antibiotics and\nwait for resuts",
    "\nFecal Culture\n\nAdd the three antibiotics and\nwait for resuts",
    "\nWound Swab Culture\n\nAdd the three antibiotics and\nwait for resuts"
]


        self.animation_speed = 3000

        self.create_widgets()

        self.bacteria_name = tk.StringVar()
        self.bacteria_name.set(random.choice(self.bacteria_names))
        title_label = ttk.Label(root, textvariable=self.bacteria_name)
        title_label.grid(row=0, column=1)
        title_label.config(font=self.fixed_font)

        self.create_initial_big_circle()

        self.days_remaining = 0
        self.day_counter_label = ttk.Label(root, text=f"Day\n{self.days_remaining}")
        self.day_counter_label.grid(row=0, column=0)
        self.day_counter_label.config(font=self.fixed_font2)

    def create_widgets(self):
        for i, outline_size in enumerate(self.antibiotic_outlines):
            button_text = f"{self.antibiotic_names[i]}"
            add_antibiotic_button = ttk.Button(self.root, text=button_text, command=lambda size=outline_size: self.add_antibiotic(size))
            add_antibiotic_button.grid(row=2, column=i)
            add_antibiotic_button["style"] = "TButton"

        reset_button = ttk.Button(self.root, text="Reset", command=self.reset)
        reset_button.grid(row=3, column=1)
        reset_button["style"] = "TButton"

        self.random_label = ttk.Label(self.root, text="Example of\nculture", cursor="hand2", font=self.fixed_font2)
        self.random_label.grid(row=0, column=2)
        self.random_label.bind("<Button-1>", self.open_image_window)

    def create_initial_big_circle(self):
        self.bacteria_culture_id = self.canvas.create_oval(
            self.bacteria_culture_x - self.bacteria_culture_radius,
            self.bacteria_culture_y - self.bacteria_culture_radius,
            self.bacteria_culture_x + self.bacteria_culture_radius,
            self.bacteria_culture_y + self.bacteria_culture_radius,
            fill=self.bacteria_culture_color
        )

    def add_antibiotic(self, outline_size):
        while True:
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, self.bacteria_culture_radius - self.antibiotic_size - outline_size - 10)

            x = self.bacteria_culture_x + distance * math.cos(angle)
            y = self.bacteria_culture_y + distance * math.sin(angle)

            antibiotic_color = 'gray'

            overlap = False
            for _, x1, y1, s1, os1 in self.antibiotics:
                if math.sqrt((x - x1) ** 2 + (y - y1) ** 2) < (self.antibiotic_size + os1 + 10):
                    overlap = True
                    break

            if not overlap:
                antibiotic_id = self.canvas.create_oval(
                    x - self.antibiotic_size, y - self.antibiotic_size,
                    x + self.antibiotic_size, y + self.antibiotic_size,
                    fill=antibiotic_color,
                    outline='white',
                    width=0
                )

                label_text = ""
                if outline_size == 0:
                    label_text = "A"
                elif outline_size == 5:
                    label_text = "C"
                elif outline_size == 20:
                    label_text = "E"

                text_label = self.canvas.create_text(x, y, text=label_text, font=self.fixed_font, fill='white')

                self.antibiotics.append((antibiotic_id, x, y, self.antibiotic_size, outline_size, text_label))

                self.animate_outline_growth(antibiotic_id, x, y, self.antibiotic_size, outline_size)
                break

    def animate_outline_growth(self, antibiotic_id, x, y, size, target_outline_size):
        current_outline_size = 0
        step = 1

        def update_outline():
            nonlocal current_outline_size
            if current_outline_size < target_outline_size:
                current_outline_size += step
                self.canvas.itemconfigure(antibiotic_id, width=current_outline_size)
                self.root.after(self.animation_speed, update_outline)
            else:
                self.days_remaining += 1
                self.update_counter_label()

        update_outline()
        self.antibiotics[-1] = (antibiotic_id, x, y, size, target_outline_size)

    def reset(self):
        self.canvas.delete("all")
        self.antibiotics = []
        self.create_initial_big_circle()
        self.days_remaining = 0
        self.update_counter_label()

    def update_counter_label(self):
        self.day_counter_label["text"] = f"Day\n{self.days_remaining}"
        if self.days_remaining >= 3:
            self.display_statistics()
                
    def open_image_window(self, event):
        image_window = tk.Toplevel(self.root)
        image_window.title("Culture and Antibiogram")
        image_path = 'antibio.jpeg'
        img = Image.open(image_path)
        img = ImageTk.PhotoImage(img)
        image_label = tk.Label(image_window, image=img)
        image_label.image = img
        image_label.pack()

    def display_statistics(self):
        statistics_window = tk.Toplevel(self.root)
        statistics_window.title("Antibiogram Result")

        table = ttk.Treeview(statistics_window, columns=("Antibiotic", "Sensitivity"), show="headings")
        table.heading("#1", text="Antibiotic")
        table.heading("#2", text="Sensitivity")
        table.pack()

        data = [("Amoxicillin", "Resistant"),
                ("Ciprofloxacin", "Partially Sensitive"),
                ("Erythromycin", "Sensitive")]

        for row in data:
            table.insert("", "end", values=row)


if __name__ == "__main__":
    root = tk.Tk()
    app = AntibiogramSimulation(root)
    root.mainloop()

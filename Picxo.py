import tkinter as tk
from tkinter import filedialog, colorchooser, simpledialog

class PixelArt:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1200x2000")  # Définit la taille de la fenêtre
        self.canvas_width = 280
        self.canvas_height = 520
        self.canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Centre le canevas
        self.pixels = []
        self.color = "black"
        self.size = 3  # Taille des pixels
        self.drawing = False
        self.last_x, self.last_y = 0, 0
        self.grid_size_x = self.canvas_width // self.size
        self.grid_size_y = self.canvas_height // self.size
        self.frames = [self.create_grid()]  # Liste des frames
        self.current_frame = 0
        self.onion_skin = False
        self.create_menu()
        self.create_buttons()
        self.canvas.bind("<1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_pixel)
        self.master.bind("1", self.toggle_onion_skin)
        self.master.bind("<Right>", self.next_frame)
        self.master.bind("<Left>", self.previous_frame)

    def create_menu(self):
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="⚙️", menu=self.file_menu)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Load", command=self.load)
        self.file_menu.add_command(label="New Frame", command=self.new_frame)

    def create_buttons(self):
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack()
        self.clear_button = tk.Button(self.button_frame, text="🗑️", command=self.clear)
        self.clear_button.pack(side=tk.LEFT)
        self.color_button = tk.Button(self.button_frame, text="Color/Colour", command=self.change_color)
        self.color_button.pack(side=tk.LEFT)
        self.size_button = tk.Button(self.button_frame, text="Size", command=self.change_size)
        self.size_button.pack(side=tk.LEFT)
        self.fill_button = tk.Button(self.button_frame, text="Fill", command=self.fill)
        self.fill_button.pack(side=tk.LEFT)

    def create_grid(self):
        grid = []
        for i in range(self.grid_size_y):
            row = []
            for j in range(self.grid_size_x):
                row.append("white")
            grid.append(row)
        return grid

    def start_drawing(self, event):
        self.drawing = True
        self.last_x, self.last_y = event.x, event.y

    def draw_pixel(self, event):
        if self.drawing:
            x, y = event.x, event.y
            x_grid = x // self.size
            y_grid = y // self.size
            if x_grid < self.grid_size_x and y_grid < self.grid_size_y:
                self.frames[self.current_frame][y_grid][x_grid] = self.color
                self.canvas.create_rectangle(x_grid * self.size, y_grid * self.size, (x_grid + 1) * self.size, (y_grid + 1) * self.size, 
                                             fill=self.color, outline=self.color)

    def save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(f"{self.size}\n")  # Sauvegarde la taille des pixels
                for frame in self.frames:
                    for row in frame:
                        for color in row:
                            file.write(color + " ")
                        file.write("\n")
                    file.write("\n")

    def load(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                self.size = int(file.readline().strip())  # Charge la taille des pixels
                self.frames = []
                frame = []
                for line in file:
                    if line.strip():
                        row = line.strip().split()
                        frame.append(row)
                    else:
                        if frame:
                            self.frames.append(frame)
                            frame = []
                if frame:
                    self.frames.append(frame)
            self.grid_size_x = len(self.frames[0][0])
            self.grid_size_y = len(self.frames[0])
            self.current_frame = 0
            self.canvas.delete("all")
            self.draw_grid()

    def new_frame(self):
        choice = simpledialog.askstring("Nouvelle frame", "Charger une frame vide (vide) ou à partir d'un fichier (fichier) ?")
        if choice == "vide":
            self.frames.append(self.create_grid())
        elif choice == "fichier":
            file_path = filedialog.askopenfilename()
            if file_path:
                with open(file_path, "r") as file:
                    self.size = int(file.readline().strip())  # Charge la taille des pixels
                    frame = []
                    for line in file:
                        row = line.strip().split()
                        frame.append(row)
                    self.frames.append(frame)
        self.current_frame = len(self.frames) - 1
        self.canvas.delete("all")
        self.draw_grid()

    def clear(self):
        self.canvas.delete("all")
        self.frames[self.current_frame] = self.create_grid()
        self.draw_grid()

    def change_color(self):
        self.color = colorchooser.askcolor()[1]
        
    def change_size(self):
        new_size = simpledialog.askinteger("Taille du pixel", "Entrez la nouvelle taille des pixels (ex: 5, 10):")
        if new_size:
            self.size = new_size
            self.grid_size_x = self.canvas_width // self.size
            self.grid_size_y = self.canvas_height // self.size
            for i in range(len(self.frames)):
                self.frames[i] = self.create_grid()
            self.draw_grid()

    def fill(self):
        target_color = colorchooser.askcolor()[1]
        self.fill_color(self.color, target_color)
        self.draw_grid()

    def fill_color(self, color, target_color):
        for i in range(self.grid_size_y):
            for j in range(self.grid_size_x):
                if self.frames[self.current_frame][i][j] == color:
                    self.frames[self.current_frame][i][j] = target_color

    def toggle_onion_skin(self, event):
        self.onion_skin = not self.onion_skin
        print(f"Onion skin {'enabled' if self.onion_skin else 'disabled'}")
        self.draw_grid()

    def next_frame(self, event):
        if self.current_frame < len(self.frames) - 1:
            self.current_frame += 1
            self.canvas.delete("all")
            self.draw_grid()

    def previous_frame(self, event):
        if self.current_frame > 0:
            self.current_frame -= 1
            self.canvas.delete("all")
            self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        if self.onion_skin and self.current_frame > 0:
            self.draw_onion_skin()
        for i in range(self.grid_size_y):
            for j in range(self.grid_size_x):
                self.canvas.create_rectangle(j * self.size, i * self.size, (j + 1) * self.size, (i + 1) * self.size, 
                                             fill=self.frames[self.current_frame][i][j], outline=self.frames[self.current_frame][i][j])

    def draw_onion_skin(self):
        previous_frame = self.frames[self.current_frame - 1]
        for i in range(self.grid_size_y):
            for j in range(self.grid_size_x):
                self.canvas.create_rectangle(j * self.size, i * self.size, (j + 1) * self.size, (i + 1) * self.size, 
                                             fill=previous_frame[i][j], outline=previous_frame[i][j], stipple="gray50")

    def run(self):
        self.draw_grid()
        self.master.mainloop()

def main():
    root = tk.Tk()
    pixel_art = PixelArt(root)
    pixel_art.run()

if __name__ == "__main__":
    main()
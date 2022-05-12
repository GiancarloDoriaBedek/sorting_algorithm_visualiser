import random

import tkinter as tk
from tkinter import StringVar, ttk

from algorithms import algorithm_dict


class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Sorting Algorithm Visualizer')
        self.resizable(False, False)
        self.geometry('900x600')
        self.config(bg = 'black')

        self.available_algorithms = algorithm_dict
        self.color_list = list()

        self.initialize_frames()
        self.place_frames()

    
    def initialize_frames(self):
        """
        Initializes frames
        """
        self.selection_frame = SelectionFrame(self)
        self.canvas_frame = CanvasFrame(self)


    def place_frames(self):
        """
        Places frames in a grid
        """
        self.selection_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.canvas_frame.grid(row=1, column=0)


    def generate(self):
        fill_color = '#ae0000'

        size = int(self.selection_frame.size_scale.get())
        max_value = int(self.selection_frame.max_scale.get())
        
        self.data = [random.randrange(0, max_value+1) for _ in range(size)]
        self.color_list = [fill_color for i in self.data]
        self.draw_data()


    def draw_data(self, old_highlight_idx=[], new_highlight_idx=[]):
        """
        Draws data points from self.data on a canvas as a bar graph. Colors each bar by editing and reading 
        from a list of colors in which each element corresponds with an element in data on the same index.

        old_highlight_idx - indexes of elements in data that need to be changed to standard fill color
        (indexes of elements that have changed places or have been compared in the last cycle)

        new_highlight_idx - indexes of elements in data that need to be changed to highlight color 
        (indexes of elements that have changed places in the latest swap or have been compared)
        """
        fill_color = '#ae0000'
        highlight_color = '#ff8484'

        # Changes elements of color_list to the default value
        for i in old_highlight_idx:
            self.color_list[i] = fill_color

        # Changes elements of the color_list to the highlighted value
        for i in new_highlight_idx:
            self.color_list[i] = highlight_color

        # Initialize canvas for new data visualization
        canvas = self.canvas_frame.canvas
        canvas.delete('all')

        # Initializing all the values needed to draw data on canvas
        canvas_height = int(canvas['height'])
        canvas_width = int(canvas['width'])
        bar_width = canvas_width / (len(self.data) + 1)
        offset = (canvas_width / len(self.data)) // 2

        # Needed to normalize values to the canvas height
        largest_data_point = max(self.data)

        # Loops through all data points and draws a corresponding bar on a canvas
        for i, height in enumerate(self.data):
            # Calculate normalized data point value
            normalized_height = (height / largest_data_point) * (canvas_height - 20)

            # 2 oposite 2 dimensional points are needed to draw a rectangle on a canvas
            # Calculate top left point
            x0 = i*bar_width + offset
            y0 = canvas_height - normalized_height

            # Calculate bottom right point
            x1 = (i + 1) * bar_width + offset
            y1 = canvas_height

            # Draw data point on canvas
            canvas.create_rectangle(x0, y0, x1, y1, fill=self.color_list[i], outline= '#870000')

        # Updates visuals
        self.update_idletasks()

    
    def finished_sort_display(self):
        """
        After data is sorted, highlight the whole bar chart step by step from least to largest
        """
        for i in range(len(self.data)):
            self.draw_data([], new_highlight_idx=[j for j in range(i+1)])


    def start_algorithm(self):
        """
        Gets selected algorithm and executes it on data
        """
        # If data is not yet initialized: Do nothing
        if not self.data:
            return

        # Gets preferd temporal delay between each step of an algorithm
        time_delay = float(self.selection_frame.speed_scale.get())

        # Gets the name of a selected algorithm and executes it using its name as a key in a 
        # dictionary of all available algorithms
        selected_algorithm_name = self.selection_frame.algorithm_menu.get()
        self.available_algorithms[selected_algorithm_name](self.data, self.draw_data, time_delay)
        self.finished_sort_display()


class SelectionFrame(tk.Frame):
    def __init__(self, master):
        """
        Top frame with all user inputs
        """
        tk.Frame.__init__(self, master)
        self.config(bg = 'black')
        self.selected_algorithm = StringVar()

        self.initialize_elements()
        self.place_elements()


    def initialize_elements(self):
        """
        Initializes all the widgets
        """
        # Widget styling
        bg_color = 'black'
        text_color = 'lightgrey'
        self.set_combostyle()

        algorithm_names = [key for key, _ in self.master.available_algorithms.items()]

        # Algorithm choice
        self.algorithm_label = tk.Label(self, text='Algorithm', font='Helvetica 14', bg=bg_color, fg=text_color)
        self.algorithm_menu = ttk.Combobox(self, textvariable=self.selected_algorithm, values=algorithm_names, font='Helvetica 12', width=20)
        self.algorithm_menu['state'] = 'readonly'
        self.algorithm_menu.current(0)

        # Speed choice
        self.speed_label = tk.Label(self, text='Animation Speed [s]', font='Helvetica 14', bg=bg_color, fg=text_color)
        self.speed_scale = tk.Scale(self, from_=0.0, to=2.0, length=200, digits=3, resolution=0.05, **self.slider_style())

        # Data size choice
        self.size_label = tk.Label(self, text='Size', font='Helvetica 14', bg=bg_color, fg=text_color)
        self.size_scale = tk.Scale(self, from_=3, to=256, length=200, digits=2, resolution=0.2, **self.slider_style())

        # Largest choice
        self.max_value_label = tk.Label(self, text='Max Value', font='Helvetica 14', bg=bg_color, fg=text_color)
        self.max_scale = tk.Scale(self, from_=1, to=2048, length=200, digits=2, resolution=0.2, **self.slider_style())

        # Buttons
        self.start_button = tk.Button(self, text='Start', font='Helvetica 14', width=12, command=self.master.start_algorithm, bg='#ae0000', fg=text_color)
        self.generate_button = tk.Button(self, text='Generate', font='Helvetica 14', width=12, command=self.master.generate, bg='#ae0000', fg=text_color)


    def place_elements(self):
        """
        Places all the widgets in a grid
        """
        # Algorithm choice
        self.algorithm_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.SE)
        self.algorithm_menu.grid(row=0, column=1, padx=5, pady=5, sticky=tk.SW)

        # Speed choice
        self.speed_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.SE)
        self.speed_scale.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        # Data size choice
        self.size_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.SE)
        self.size_scale.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        # Largest choice
        self.max_value_label.grid(row=1, column=2, padx=5, pady=5, sticky=tk.SE)
        self.max_scale.grid(row=1, column=3, padx=5, pady=5, sticky=tk.W)

        # Buttons
        self.start_button.grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.generate_button.grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)


    def set_combostyle(self):
        """
        Creates and initializes a syle for comboboxes
        """
        combostyle = ttk.Style()
        combostyle.theme_create('combostyle', parent='alt', settings = {
            'TCombobox':
            {
                'configure':
                {
                    'selectbackground': 'lightgrey',
                    'fieldbackground': 'lightgrey',
                    'background': 'grey',
                    'selectforeground': 'black'
                }
            }
            })
        combostyle.theme_use('combostyle')


    def slider_style(self):
        """
        Creates a style for sliders and returns it as a dictionary to be used as a kwarg
        in creation of slider objects. 
        """
        return {
            'orient': tk.HORIZONTAL, 
            'bg': 'black', 
            'fg': 'lightgrey', 
            'bd': 0, 
            'troughcolor': 'lightgrey', 
            'highlightbackground': 'black',
            'highlightcolor': 'lightgrey',
            'font': 'Helvetica 12'
        }


class CanvasFrame(tk.Frame):
    def __init__(self, master):
        """
        Lower frame containing only a canvas on which bar chart is drawn
        """
        tk.Frame.__init__(self, master)
        self.config(bg='black')
        self.initialize_elements()
        self.place_elements()

    def initialize_elements(self):
        self.canvas = tk.Canvas(self, width=885, height=472, bg='black', highlightbackground='lightgrey')

    def place_elements(self):
        self.canvas.grid(row=0, column=0, padx=5, pady=5)


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
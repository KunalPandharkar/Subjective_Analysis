import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import flask
class SubjectiveAnalysisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Subjective Analysis")
        self.root.geometry("800x600")

        # create left frame
        self.left_frame = tk.Frame(self.root, width=400, height=600, bd=2, relief=tk.SUNKEN)
        self.left_frame.pack(side=tk.LEFT, padx=5, pady=5)

        # create right frame
        self.right_frame = tk.Frame(self.root, width=400, height=600, bd=2, relief=tk.SUNKEN)
        self.right_frame.pack(side=tk.RIGHT, padx=5, pady=5)

        # create vertical separator
        self.separator = tk.Frame(self.root, height=600, width=3, bd=1, relief=tk.SOLID)
        self.separator.pack(side=tk.LEFT, padx=5)

        # create widgets for left frame
        self.upload_button = tk.Button(self.left_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(padx=10, pady=10)

        self.label_entry = tk.Entry(self.left_frame, width=50)
        self.label_entry.pack(padx=10, pady=10)

        self.marks_entry = tk.Entry(self.left_frame, width=50)
        self.marks_entry.pack(padx=10, pady=10)

        self.submit_button = tk.Button(self.left_frame, text="Submit", command=self.update_right_frame)
        self.submit_button.pack(padx=10, pady=10)

        # create widgets for right frame
        self.display_label = tk.Label(self.right_frame, text="")
        self.display_label.pack(padx=10, pady=10)

        self.display_marks = tk.Label(self.right_frame, text="")
        self.display_marks.pack(padx=10, pady=10)

        self.piechart = plt.pie([0, 100], labels=['Selected', 'Not Selected'], autopct='%1.1f%%')
        self.canvas = FigureCanvasTkAgg(self.piechart[0], master=self.right_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(padx=10, pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        self.label_entry.delete(0, tk.END)
        self.label_entry.insert(0, file_path)

    def update_right_frame(self):
        self.image_label = self.label_entry.get()
        self.image_marks = self.marks_entry.get()
        self.display_label.config(text=self.image_label)
        self.display_marks.config(text=self.image_marks)
        self.piechart = plt.pie([int(self.image_marks), 100 - int(self.image_marks)],
                                labels=['Selected', 'Not Selected'], autopct='%1.1f%%')
        self.canvas.figure.clf()
        self.canvas.figure.subplots_adjust(top=0.8)
        self.canvas.figure.suptitle(f'Marks: {self.image_marks}/100', fontsize=12)
        self.canvas.figure.add_subplot(111)
        self.canvas.figure.gca().pie(self.piechart[0], labels=self.piechart[1], autopct='%1.1f%%')
        self.canvas.draw()

    def submit(self):
        image_path = self.image_path.get()
        std_answer = self.std_answer.get("1.0", "end-1c")
        marks = int(self.image_marks.get())

        # update image info on the right frame
        self.right_image_path.set(image_path)
        self.right_std_answer.set(std_answer)
        self.right_marks.set(marks)

        # update pie chart
        self.piechart = [marks, 100 - marks]
        self.canvas.figure.clf()
        self.canvas.figure.suptitle("Marks Distribution")
        self.canvas.figure.add_subplot(111)
        self.canvas.figure.gca().pie(self.piechart, labels=["Selected", "Remaining"], autopct='%1.1f%%')
        self.canvas.draw()

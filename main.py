import tkinter as tk
from tkinter import messagebox, ttk, filedialog, Frame
from tkcalendar import DateEntry
# import yaml
from ruamel.yaml import YAML
import glob
import os
import sys
import shutil
from datetime import datetime

yaml = YAML(typ='rt')
if getattr(sys, 'frozen', False):
    # Running as executable
    basedir = os.path.join(os.path.dirname(sys.executable), "..")
elif __file__:
    # Running as Python file
    basedir = os.path.dirname(__file__)

class ParamsApp:
    def __init__(self, root):
        self.root = root
        self.rfmw_entries = []
        self.params = {}
        self.mode = "write"  # starts in 'write' mode

        self.root.title("Enter Parameters")
        # self.root.geometry("600x600")

        self.style = ttk.Style()
        self.style.configure("Basic", background="#FAFAFA", font=("Helvetica", 12))
        # Set font
        # self.font = ("Helvetica", 12)
        
        # Get some default settings
        self.get_defaults()

        # Set background color
        # self.bg_color = "#FAFAFA"
        # self.root.configure(bg=self.bg_color)
        # Create GUI elements
        self.create_gui_elements()

    def get_defaults(self):
        try:
            with open(os.path.join(basedir, "persistent_options.yaml")) as f:
                options = yaml.load(f)
        except:

            messagebox.showinfo("Minor error", "No YAML found for persistent options. Defaulting to hard-coded ones.")
            options = {"container_defaults": ["SCHOTT 2R", "SCHOTT 6R", "SCHOTT 10R", "SiO2 10mL"],
                        "lyophilizer_defaults": ["LyoStar3", "REVO", "MicroFD", "LabConco"],
                        "formulation_defaults": ["Sucrose 5%", "Mannitol 5%", "Sucrose 10%"],
                        "project_defaults": ["RF", "Strain Gauge"],
                        "dest_folder": os.path.join(basedir, "..", "AllLyoData"),
            }
            
        self.container_defaults = options["container_defaults"]
        self.lyo_defaults = options["lyophilizer_defaults"]
        self.formulation_defaults = options["formulation_defaults"]
        self.dest_folder = options["dest_folder"]
        if self.dest_folder[1] == ".":
            self.dest_folder = os.path.join(basedir, options["dest_folder"])

        self.dest_folder_var = tk.StringVar()
        self.dest_folder_var.set(self.dest_folder)

    def create_gui_elements(self):

        # Left frame -------------
        left_frame = Frame(self.root)
        left_frame.pack(side="left", fill="y", expand=True)
        center_frame = Frame(self.root)
        center_frame.pack(side="left", fill="y", expand=True)
        right_frame = Frame(self.root)
        right_frame.pack(side="left", fill="y", expand=True)
        self.finish_button = ttk.Button(self.root, text="FINISH", command=self.finish)
        self.finish_button.pack(side="right", fill="y", padx=10, pady=10)

        self.find_procdat_button = ttk.Button(left_frame, text="Locate Raw Data Files", command=self.find_procdat)
        self.find_procdat_button.pack()
        ttk.Label(left_frame, text="Filenames (plural--process and other)").pack()
        self.procfilesvar = tk.StringVar()
        self.procdat_entry = ttk.Entry(left_frame, textvariable=self.procfilesvar, width=40)
        self.procdat_entry.pack()
        ttk.Label(left_frame, text="Destination folder").pack()
        self.find_dest_button = ttk.Button(left_frame, text="Locate Destination Folder", command=self.find_dest_folder)
        self.find_dest_button.pack()
        self.dest_entry = ttk.Entry(left_frame, textvariable=self.dest_folder_var, width=40)
        self.dest_entry.pack()
        self.cal = self.create_calendar_entry("Process start date", left_frame)
        self.hour = self.create_labeled_combobox("Process start hour (0-23)", left_frame, [str(i) for i in range(24)])


        # Parameter widgets
        self.user_entry = self.create_labeled_entry("User Full Name", left_frame)
        self.lyo_entry = self.create_labeled_combobox("Lyo Name", left_frame, self.lyo_defaults)
        self.cont_option = self.create_labeled_combobox("Container Type/Size", center_frame, self.container_defaults)
        self.cont_count = self.create_labeled_entry("Number of Containers/Vials", center_frame)
        self.formulation_option = self.create_labeled_combobox("Formulation", center_frame, self.formulation_defaults)
        self.concentration = self.create_labeled_entry("Total Solids Content (g/mL)", center_frame)
        self.fill = self.create_labeled_entry("Fill Volume (mL)", center_frame)
        self.cin_checkbutton = self.create_labeled_checkbutton("CIN", center_frame)
        self.annealing_checkbutton = self.create_labeled_checkbutton("Annealing", center_frame)
        self.freezethaw_checkbutton = self.create_labeled_checkbutton("Freeze-thaw", center_frame)
        self.project_option = self.create_labeled_combobox("Project", right_frame, ["NIIMBL RF", "Strain Gauge"])

        # RF/MW Run? options
        self.is_rf_mw_run = tk.BooleanVar()
        label = ttk.Label(right_frame, text="RF/MW Run?", )
        label.pack()
        yes_option = ttk.Radiobutton(right_frame, text="Yes", variable=self.is_rf_mw_run, value=True, command=self.toggle_rf_mw_entries, )
        no_option = ttk.Radiobutton(right_frame, text="No", variable=self.is_rf_mw_run, value=False, command=self.toggle_rf_mw_entries)
        yes_option.pack()
        no_option.pack()

        # RF/MW fields
        self.rfmw_labels = ['Power (W)', 'Frequency (GHz)']
        for label_text in self.rfmw_labels:
            label = ttk.Label(right_frame, text=label_text, )
            entry = ttk.Entry(right_frame, state='disabled', )
            self.rfmw_entries.append(entry)

            label.pack()
            entry.pack()

        # Separate Closed-Loop option
        self.closed_loop_checkbutton = self.create_labeled_checkbutton("Closed-Loop", right_frame)

        self.comments_entry = self.create_labeled_entry("Comments", right_frame)
        # ttk.Label(self.root, text="Comments").pack()
        # self.comments_entry = tk.Text(self.root, height=2, width=15)
        # self.comments_entry.pack()


        # Search results
        # self.results_text = tk.Text(self.root)
        # self.results_text.pack()
        # self.results_text.config(state='disabled')

    # def toggle_mode(self):
    #     if self.mode == "write":
    #         self.mode = "search"
    #         self.mode_button.config(text="Switch to Write Mode")
    #         self.finish_button.config(text="SEARCH", command=self.search)
    #     else:
    #         self.mode = "write"
    #         self.mode_button.config(text="Switch to Search Mode")
    #         self.finish_button.config(text="FINISH", command=self.finish)

    def toggle_rf_mw_entries(self):
        if self.is_rf_mw_run.get() == 1:
            for entry in self.rfmw_entries:
                entry.config(state='normal')
        else:
            for entry in self.rfmw_entries:
                entry.config(state='disabled')

    def find_procdat(self):
        self.procfilenames = filedialog.askopenfilenames()
        print(f"{len(self.procfilenames)} filename(s) acquired:")
        for n in self.procfilenames:
            print(n)
        self.procfilesvar.set(self.procfilenames)

    def find_dest_folder(self):
        self.dest_folder = filedialog.askdirectory()
        print(f"Destination folder: {self.dest_folder}")
        self.dest_folder_var.set(self.dest_folder)

   
    def create_calendar_entry(self, text, frame):
        label = ttk.Label(frame, text=text)
        label.pack()
        now = datetime.now()
        cal = DateEntry(frame, year = now.year, month=now.month, day=now.day)
        cal.pack()
        return cal

    def create_labeled_entry(self, text, frame):
        label = ttk.Label(frame, text=text)
        label.pack()
        entry = ttk.Entry(frame)
        entry.pack()
        return entry

    def create_labeled_combobox(self, text, frame, options):
        label = ttk.Label(frame, text=text)
        label.pack()
        combo_box = ttk.Combobox(frame, values=options)
        combo_box.set(options[0])  # default value
        combo_box.pack()
        return combo_box

    def create_labeled_checkbutton(self, text, frame,):
        var = tk.BooleanVar(value=False)
        checkbutton = ttk.Checkbutton(frame, text=text, variable=var, )
        checkbutton.pack()
        return var

    def read_state(self): 
        params = {
            'start date' : self.cal.get_date(),
            'user': self.user_entry.get(),
            'lyophilizer': self.lyo_entry.get(),
            'formulation': self.formulation_option.get(),
            'concentration': float(self.concentration.get()),
            'fill': float(self.fill.get()),
            'CIN': self.cin_checkbutton.get(),
            'annealing': self.annealing_checkbutton.get(),
            'closed loop' : self.closed_loop_checkbutton.get(),
            'freezethaw' : self.freezethaw_checkbutton.get(),
            'original filenames' : self.procfilenames,
            'comments' : self.comments_entry.get() + " ",
            'project' : self.project_option.get(),
        }
        
        params['containers'] = {}
        params['containers']['type'] = self.cont_option.get()
        params['containers']['count'] = int(self.cont_count.get())
        if self.is_rf_mw_run.get():
            # rfmw_params = {self.rfmw_labels[i]: entry.get() for i, entry in enumerate(self.rfmw_entries)}
            params["RF"] = {}
            for name, entry in zip(self.rfmw_labels, self.rfmw_entries):
                params["RF"][name.lower().split(" ")[1]] = float(entry.get())
        else:
            params["RF"] = False

        # params.update(rfmw_params)

        return params

    def finish(self):
        self.params = self.read_state()

        
        if "" in self.params.values():
            messagebox.showinfo("Error", "All fields must be filled out")
            return

        now = datetime.now()
        datetime_str = now.strftime("%Y-%m-%d %H:%M")
        self.params['timestamp'] = datetime_str

        fname_base, fname_yaml = self.write_to_yaml(self.params)

        messagebox.showinfo("Partial Success", f"Parameters saved to {fname_yaml}")

        if len(self.procfilenames) == 1: # If a single string, do once
            name = self.procfilenames[0]
            ext = os.path.splitext(name)[1]
            shutil.copy(name, os.path.join(self.dest_folder, fname_base + ext)) 
            messagebox.showinfo("Complete Success", f"Process file copied to {fname_base}{ext}")
        else:
            for i, name in enumerate(self.procfilenames):
                ext = os.path.splitext(name)[1]
                shutil.copy(name, os.path.join(self.dest_folder, fname_base + f"_{i+1}" + ext)) 
            messagebox.showinfo("Complete Success", f"Process files copied to {fname_base}_#{ext}")


        self.root.quit()

    def write_to_yaml(self, params):
        with open(os.path.join(basedir, "metadata_template.yaml")) as f:
            template_params = yaml.load(f)

        if not set(template_params.keys()).issubset(params.keys()):
            print(params.keys())
            messagebox.showinfo("Error", "Not all fields in template are being written.\n(Software error: let Isaac know)")
            # raise ValueError("Not all fields in template are being written.")

        for key in params.keys():
            template_params[key] = params[key]

        user_initials = ''.join([w[0].capitalize() for w in params['user'].split(" ")])
        if params["lyophilizer"] == "LyoStar3":
            lyo_abbrev = "LS"
        elif params["lyophilizer"] == "REVO":
            lyo_abbrev = "REVO"
        elif params["lyophilizer"] == "MicroFD":
            lyo_abbrev = "MFD"
        elif params["lyophilizer"] == "LabConco":
            lyo_abbrev = "LC"
        else:
            messagebox.showinfo("Error", f"Unknown lyophilizer name given: {params['lyophilizer']}. Will be abbreviated by taking capital letters.")
            lyo_abbrev = "".join([c for c in params["lyophilizer"] if c.isupper()])
            # raise ValueError()
        # now = datetime.now()
        # date = now.strftime("%Y-%m-%d-%H")
        date = self.cal.get_date().strftime("%Y-%m-%d")
        hour = int(self.hour.get())
        fname_base = f"{date}-{hour:02d}_{lyo_abbrev}_{user_initials}"
        fname = fname_base + ".yaml"
        # dest_folder = os.path.join(sys.path[0] , "..", "AllLyoData")
        # dest_folder = os.path.join(basedir, "..", "AllLyoData")
        print(self.dest_folder)
        with open(os.path.join(self.dest_folder, fname), 'w') as f:
            yaml.dump(template_params, f)

        return fname_base, fname

root = tk.Tk()
app = ParamsApp(root)
root.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
# from tkcalendar import DateEntry
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
        self.folder_name = os.path.join(basedir, "..", "AllLyoData")
        
        self.container_defaults = ["SCHOTT 2R",
                                   "SCHOTT 6R",
                                   "SCHOTT 10R",
                                   "SiO2 10mL",
        ]
        # Set background color
        # self.bg_color = "#FAFAFA"
        # self.root.configure(bg=self.bg_color)

        # Create GUI elements
        self.create_gui_elements()

    def create_gui_elements(self):
        # self.mode_button = ttk.Button(self.root, text="Switch to Search Mode", command=self.toggle_mode)
        # self.mode_button.pack()

        self.find_procdat_button = ttk.Button(self.root, text="Locate Raw Data Files", command=self.find_procdat)
        self.find_procdat_button.pack()
        ttk.Label(text="Filenames (plural--process and other)").pack()
        self.procfilesvar = tk.StringVar()
        self.procdat_entry = ttk.Entry(textvariable=self.procfilesvar, width=40)
        self.procdat_entry.pack()

        # Parameter widgets
        self.user_entry = self.create_labeled_entry("User Full Name")
        self.lyo_entry = self.create_labeled_combobox("Lyo Name", ["LyoStar3", "REVO", "MicroFD"])
        self.cont_option = self.create_labeled_combobox("Container Type/Size", self.container_defaults)
        self.cont_count = self.create_labeled_entry("Number of Containers/Vials")
        self.formulation_option = self.create_labeled_combobox("Formulation", ["Sucrose 5%", "Mannitol 5%", "Sucrose 10%"])
        self.concentration = self.create_labeled_entry("Total Solids Content (g/mL)")
        self.fill = self.create_labeled_entry("Fill Volume (mL)")
        self.cin_checkbutton = self.create_labeled_checkbutton("CIN")
        self.annealing_checkbutton = self.create_labeled_checkbutton("Annealing")
        self.freezethaw_checkbutton = self.create_labeled_checkbutton("Freeze-thaw")
        self.project_option = self.create_labeled_combobox("Project", ["NIIMBL RF", "Strain Gauge"])

        # RF/MW Run? options
        self.is_rf_mw_run = tk.BooleanVar()
        label = ttk.Label(self.root, text="RF/MW Run?", )
        label.pack()
        yes_option = ttk.Radiobutton(self.root, text="Yes", variable=self.is_rf_mw_run, value=True, command=self.toggle_rf_mw_entries, )
        no_option = ttk.Radiobutton(self.root, text="No", variable=self.is_rf_mw_run, value=False, command=self.toggle_rf_mw_entries)
        yes_option.pack()
        no_option.pack()

        # RF/MW fields
        self.rfmw_labels = ['Power (W)', 'Frequency (GHz)']
        for label_text in self.rfmw_labels:
            label = ttk.Label(self.root, text=label_text, )
            entry = ttk.Entry(self.root, state='disabled', )
            self.rfmw_entries.append(entry)

            label.pack()
            entry.pack()

        # Separate Closed-Loop option
        self.closed_loop_checkbutton = self.create_labeled_checkbutton("Closed-Loop")

        self.comments_entry = self.create_labeled_entry("Comments")
        # ttk.Label(self.root, text="Comments").pack()
        # self.comments_entry = tk.Text(self.root, height=2, width=15)
        # self.comments_entry.pack()

        self.finish_button = ttk.Button(self.root, text="FINISH", command=self.finish)
        self.finish_button.pack()

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

   
    def create_labeled_entry(self, text):
        label = ttk.Label(self.root, text=text)
        label.pack()
        entry = ttk.Entry(self.root)
        entry.pack()
        return entry

    def create_labeled_combobox(self, text, options):
        label = ttk.Label(self.root, text=text)
        label.pack()
        combo_box = ttk.Combobox(self.root, values=options)
        combo_box.set(options[0])  # default value
        combo_box.pack()
        return combo_box

    def create_labeled_checkbutton(self, text):
        var = tk.BooleanVar(value=False)
        checkbutton = ttk.Checkbutton(self.root, text=text, variable=var, )
        checkbutton.pack()
        return var

    def read_state(self): 
        params = {
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
            shutil.copy(name, os.path.join(self.folder_name, fname_base + ext)) 
            messagebox.showinfo("Complete Success", f"Process file copied to {fname_base}{ext}")
        else:
            for i, name in enumerate(self.procfilenames):
                ext = os.path.splitext(name)[1]
                shutil.copy(name, os.path.join(self.folder_name, fname_base + f"_{i+1}" + ext)) 
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
        else:
            messagebox.showinfo("Error", f"Invalid lyophilizer name given: {params['lyophilizer']}")
            # raise ValueError()
        now = datetime.now()
        date = now.strftime("%Y-%m-%d-%H")
        fname_base = f"{date}_{lyo_abbrev}_{user_initials}"
        fname = fname_base + ".yaml"
        # folder_name = os.path.join(sys.path[0] , "..", "AllLyoData")
        # folder_name = os.path.join(basedir, "..", "AllLyoData")
        print(self.folder_name)
        with open(os.path.join(self.folder_name, fname), 'w') as f:
            yaml.dump(template_params, f)

        return fname_base, fname

root = tk.Tk()
app = ParamsApp(root)
root.mainloop()

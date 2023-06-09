import tkinter as tk
from tkinter import messagebox, ttk
import yaml
import glob
import os
from datetime import datetime

class ParamsApp:
    def __init__(self, root):
        self.root = root
        self.rfmw_entries = []
        self.params = {}
        self.mode = "write"  # starts in 'write' mode

        self.root.title("Enter Parameters")
        self.root.geometry("600x600")

        # Set font
        self.font = ("Helvetica", 12)
        
        # Set background color
        self.bg_color = "#FAFAFA"
        self.root.configure(bg=self.bg_color)

        # Create GUI elements
        self.create_gui_elements()

    def create_gui_elements(self):
        self.mode_button = tk.Button(self.root, text="Switch to Search Mode", command=self.toggle_mode, font=self.font, bg=self.bg_color)
        self.mode_button.pack()

        # Parameter widgets
        self.user_entry = self.create_labeled_entry("User Full Name")
        self.vial_option = self.create_labeled_combobox("Vial", ["SCHOTT 6R", "SCHOTT 2R", "SCHOTT 20R"])
        self.lyo_entry = self.create_labeled_combobox("Lyo Name", ["LyoStar", "REVO", "MicroFD"])
        self.formulation_option = self.create_labeled_combobox("Formulation", ["Sucrose 5%", "Mannitol 5%", "Sucrose 10%"])
        self.cin_checkbutton = self.create_labeled_checkbutton("CIN")
        self.annealing_checkbutton = self.create_labeled_checkbutton("Annealing")

        # RF/MW Run? options
        self.is_rf_mw_run = tk.IntVar()
        label = tk.Label(self.root, text="Is it RF/MW Run?", bg=self.bg_color, font=self.font)
        label.pack()
        yes_option = tk.Radiobutton(self.root, text="Yes", variable=self.is_rf_mw_run, value=1, command=self.toggle_rf_mw_entries, bg=self.bg_color, font=self.font)
        no_option = tk.Radiobutton(self.root, text="No", variable=self.is_rf_mw_run, value=0, command=self.toggle_rf_mw_entries, bg=self.bg_color, font=self.font)
        yes_option.pack()
        no_option.pack()

        # RF/MW fields
        self.rfmw_labels = ['Power', 'Frequency']
        for label_text in self.rfmw_labels:
            label = tk.Label(self.root, text=label_text, bg=self.bg_color, font=self.font)
            entry = tk.Entry(self.root, state='disabled', font=self.font)
            self.rfmw_entries.append(entry)

            label.pack()
            entry.pack()

        # Separate Closed-Loop option
        self.closed_loop_checkbutton = self.create_labeled_checkbutton("Closed-Loop")

        self.comments_entry = self.create_labeled_entry("Comments")

        self.finish_button = tk.Button(self.root, text="FINISH", command=self.finish, font=self.font, bg=self.bg_color)
        self.finish_button.pack()

        # Search results
        self.results_text = tk.Text(self.root, font=self.font)
        self.results_text.pack()
        self.results_text.config(state='disabled')

    def toggle_mode(self):
        if self.mode == "write":
            self.mode = "search"
            self.mode_button.config(text="Switch to Write Mode")
            self.finish_button.config(text="SEARCH", command=self.search)
        else:
            self.mode = "write"
            self.mode_button.config(text="Switch to Search Mode")
            self.finish_button.config(text="FINISH", command=self.finish)

    def toggle_rf_mw_entries(self):
        if self.is_rf_mw_run.get() == 1:
            for entry in self.rfmw_entries:
                entry.config(state='normal')
        else:
            for entry in self.rfmw_entries:
                entry.config(state='disabled')

   
    def create_labeled_entry(self, text):
        label = tk.Label(self.root, text=text)
        label.pack()
        entry = tk.Entry(self.root)
        entry.pack()
        return entry

    def create_labeled_combobox(self, text, options):
        label = tk.Label(self.root, text=text)
        label.pack()
        combo_box = ttk.Combobox(self.root, values=options)
        combo_box.set(options[0])  # default value
        combo_box.pack()
        return combo_box

    def create_labeled_checkbutton(self, text):
        var = tk.IntVar()
        checkbutton = tk.Checkbutton(self.root, text=text, variable=var)
        checkbutton.pack()
        return var

    def read_state(self): 
        params = {
            'user': self.user_entry.get(),
            'vial': self.vial_option.get(),
            'lyophilizer': self.lyo_entry.get(),
            'formulation': self.formulation_option.get(),
            'CIN': self.cin_checkbutton.get(),
            'Annealing': self.annealing_checkbutton.get(),
            'Is RF/MW Run?': self.is_rf_mw_run.get(),
        }
        
        if self.is_rf_mw_run.get():
            rfmw_params = {self.rfmw_labels[i]: entry.get() for i, entry in enumerate(self.rfmw_entries)}
        else:
            rfmw_params = {label: 'N/A' for label in self.rfmw_labels}

        params.update(rfmw_params)
        params['Closed-Loop'] = self.closed_loop_checkbutton.get()
        params['Comments'] = self.comments_entry.get()

    def finish(self):
        self.params = self.read_state()

        if "" in self.params.values():
            messagebox.showinfo("Error", "All fields must be filled out")
            return

        now = datetime.now()
        datetime_str = now.strftime("%m/%d/%Y %H:%M")
        self.params['DateTime'] = datetime_str

        fname = self.write_to_yaml(self.params)

        messagebox.showinfo("Success", f"Parameters saved to {fname}")
        self.root.quit()

    def write_to_yaml(self, params):
        user_initials = ''.join([w[0].capitalize() for w in self.params['user'].split(" ")])
        if self.params["lyophilizer"] == "LyoStar":
            lyo_abbrev = "LS"
        elif self.params["lyophilizer"] == "REVO":
            lyo_abbrev = "REVO"
        elif self.params["lyophilizer"] == "MicroFD":
            lyo_abbrev = "MFD"
        else:
            raise ValueError("Invalid lyophilizer name given.")
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        fname = f"{date}_{lyo_abbrev}_{user_initials}.yaml"
        with open(fname, 'w') as f:
            yaml.dump(params, f)
        return fname

    def search(self):
        # search_params = {  # Note: Assumes all fields are optional for search
        #     'Vial': self.vial_option.get(),
        #     'Lyo Name': self.lyo_entry.get(),
        #     'Formulation': self.formulation_option.get(),
        #     'CIN': "Yes" if self.cin_checkbutton.get() else "No",
        #     'Annealing': "Yes" if self.annealing_checkbutton.get() else "No",
        #     'Is RF/MW Run?': "Yes" if self.is_rf_mw_run.get() == 1 else "No",
        # }
        # if self.is_rf_mw_run.get() == 1:
        #     self.rfmw_params = {self.rfmw_labels[i]: entry.get() for i, entry in enumerate(self.rfmw_entries)}
        # else:
        #     self.rfmw_params = {label: 'N/A' for label in self.rfmw_labels}
        # search_params.update(self.rfmw_params)
        # search_params['Closed-Loop'] = "Yes" if self.closed_loop_checkbutton.get() else "No"
        search_params = self.read_state()

        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)
        for filename in glob.glob('*.yaml'):
            with open(filename, 'r') as f:
                params = yaml.safe_load(f)
                # TODO: handle nested parameters more carefully
                if all(params.get(key) == value for key, value in search_params.items() if value != ""):
                    self.results_text.insert(tk.END, f"{filename}\n")
        self.results_text.config(state='disabled')

root = tk.Tk()
app = ParamsApp(root)
root.mainloop()

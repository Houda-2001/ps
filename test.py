import customtkinter as ctk
import serial
import tkinter.filedialog as fd

class STMFlasherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("STM Flasher")
        self.geometry("400x300")
        
        self.port_label = ctk.CTkLabel(self, text="Port Série:")
        self.port_label.pack(pady=10)
        
        self.port_entry = ctk.CTkEntry(self)
        self.port_entry.pack(pady=10)
        
        self.browse_button = ctk.CTkButton(self, text="Sélectionner le fichier", command=self.browse_file)
        self.browse_button.pack(pady=10)
        
        self.flash_button = ctk.CTkButton(self, text="Flasher", command=self.flash_firmware)
        self.flash_button.pack(pady=10)
        
        self.log_text = ctk.CTkTextbox(self, height=10)
        self.log_text.pack(pady=10)
        
        self.selected_file = None
    
    def browse_file(self):
        self.selected_file = fd.askopenfilename()
        self.log(f"Fichier sélectionné: {self.selected_file}")
    
    def flash_firmware(self):
        port = self.port_entry.get()
        if not port or not self.selected_file:
            self.log("Veuillez spécifier un port série et un fichier à flasher.")
            return
        
        try:
            ser = serial.Serial(port, 115200, timeout=1)
            with open(self.selected_file, 'rb') as firmware:
                data = firmware.read()
                ser.write(data)
                self.log("Flashage terminé.")
            ser.close()
        except Exception as e:
            self.log(f"Erreur: {str(e)}")
    
    def log(self, message):
        self.log_text.insert(ctk.END, message + "\n")
        self.log_text.see(ctk.END)

if __name__ == "__main__":
    app = STMFlasherApp()
    app.mainloop()






*********************************************
import customtkinter as ctk
import serial
import tkinter.filedialog as fd
import json
import os

class STMFlasherApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("STM Flasher")
        self.geometry("600x400")
        
        self.pfin_label = ctk.CTkLabel(self, text="Numéro .pfin:")
        self.pfin_label.pack(pady=10)
        
        self.pfin_entry = ctk.CTkEntry(self)
        self.pfin_entry.pack(pady=10)
        
        self.load_pfin_button = ctk.CTkButton(self, text="Charger .pfin", command=self.load_pfin)
        self.load_pfin_button.pack(pady=10)
        
        self.option_menus = {
            "calib": None,
            "fs": None,
            "teckbook": None
        }
        
        self.option_labels = {
            "calib": ctk.CTkLabel(self, text="Calibration:"),
            "fs": ctk.CTkLabel(self, text="FS:"),
            "teckbook": ctk.CTkLabel(self, text="Teckbook:")
        }
        
        for label in self.option_labels.values():
            label.pack(pady=5)
        
        self.flash_button = ctk.CTkButton(self, text="Flasher", command=self.flash_firmware)
        self.flash_button.pack(pady=10)
        
        self.log_text = ctk.CTkTextbox(self, height=10)
        self.log_text.pack(pady=10)
        
        self.files = {"calib": None, "fs": None, "teckbook": None}
    
    def load_pfin(self):
        pfin_number = self.pfin_entry.get()
        if not pfin_number:
            self.log("Veuillez entrer un numéro .pfin.")
            return
        
        try:
            with open("bdd.json", "r") as f:
                options = json.load(f)
            
            if pfin_number in options:
                self.populate_options(options[pfin_number])
            else:
                self.log(f"Aucune option disponible pour le numéro .pfin: {pfin_number}")
        except Exception as e:
            self.log(f"Erreur lors du chargement du fichier JSON: {str(e)}")
    
    def populate_options(self, options):
        for ftype in self.option_menus:
            if self.option_menus[ftype]:
                self.option_menus[ftype].destroy()
            
            self.option_menus[ftype] = ctk.CTkOptionMenu(self, values=options[ftype], command=lambda choice, ftype=ftype: self.set_file(choice, ftype))
            self.option_menus[ftype].pack(pady=5)
        
        self.log("Options chargées avec succès.")
    
    def set_file(self, choice, ftype):
        self.files[ftype] = choice
        self.log(f"{ftype.capitalize()} sélectionné: {choice}")
    
    def flash_firmware(self):
        port = self.pfin_entry.get()
        if not port:
            self.log("Veuillez spécifier un port série.")
            return
        
        missing_files = [ftype for ftype, fpath in self.files.items() if not fpath]
        if missing_files:
            self.log(f"Fichiers manquants: {', '.join(missing_files)}")
            return
        
        try:
            ser = serial.Serial(port, 115200, timeout=1)
            for ftype, fname in self.files.items():
                file_path = f"{fname}.bin"  # Assuming the files are in the current directory and have .bin extension
                with open(file_path, 'rb') as firmware:
                    data = firmware.read()
                    ser.write(data)
                    self.log(f"Flashage {ftype} terminé.")
            ser.close()
        except Exception as e:
            self.log(f"Erreur: {str(e)}")
    
    def log(self, message):
        self.log_text.insert(ctk.END, message + "\n")
        self.log_text.see(ctk.END)

if __name__ == "__main__":
    app = STMFlasherApp()
    app.mainloop()


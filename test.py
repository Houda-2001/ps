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

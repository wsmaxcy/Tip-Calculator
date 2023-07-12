import customtkinter as ctk
from datetime import date
from CTkMessagebox import CTkMessagebox
from googleapiclient.discovery import build
from google.oauth2 import service_account


class TipSplitterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Tip Wizard")
        self.geometry("1235x365")
        self.iconbitmap("./data/wizard.ico")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Tip Wizard", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.splitting_tips_label = ctk.CTkLabel(self.sidebar_frame, text="Who is splitting tips:")
        self.splitting_tips_label.grid(row=1, column=0, padx=5, pady=0)
        self.splitting_tips_entry = ctk.CTkEntry(self.sidebar_frame)
        self.splitting_tips_entry.grid(row=2, column=0, padx=5, pady=0)

        self.total_tips_label = ctk.CTkLabel(self.sidebar_frame, text="Total Tips:")
        self.total_tips_label.grid(row=3, column=0, padx=5, pady=0)
        self.total_tips_entry = ctk.CTkEntry(self.sidebar_frame)
        self.total_tips_entry.grid(row=4, column=0, padx=5, pady=0)

        self.add_worker_button = ctk.CTkButton(self.sidebar_frame, text="Add Worker", command=self.add_worker)
        self.add_worker_button.grid(row=5, column=0, padx=20, pady=10)

        self.remove_worker_button = ctk.CTkButton(self.sidebar_frame, text="Remove Worker", command=self.remove_worker)
        self.remove_worker_button.grid(row=6, column=0, padx=20, pady=10)

        self.calculate_button = ctk.CTkButton(self.sidebar_frame, text="Calculate Tipout", command=self.calculate_tipout)
        self.calculate_button.grid(row=7, column=0, padx=20, pady=10)

        self.export_button = ctk.CTkButton(self.sidebar_frame, text="Export",hover_color='darkred', fg_color="transparent", border_width=2, command=self.export)
        self.export_button.grid(row=8, column=0, padx=20, pady=10)

        self.workers_frame = ctk.CTkFrame(self)
        self.workers_frame.grid(row=0, column=1, rowspan=6, padx=10, pady=10, sticky="nsew")

        self.worker_entries = []

    def add_worker(self):
        worker_frame = ctk.CTkFrame(self.workers_frame)
        worker_frame.pack(pady=5)

        name_label = ctk.CTkLabel(worker_frame, text="Name:")
        name_label.grid(row=0, column=0, padx=5, pady=3)
        name_entry = ctk.CTkEntry(worker_frame)
        name_entry.grid(row=0, column=1, padx=5, pady=3)

        hours_label = ctk.CTkLabel(worker_frame, text="Hours:")
        hours_label.grid(row=0, column=2, padx=5, pady=3)
        hours_optionmenu = ctk.CTkOptionMenu(worker_frame, values=['0', '1', '2', '3', '4', '5', '6', '7', '8' , '9', '10', '11', '12'])
        hours_optionmenu.grid(row=0, column=3, padx=5, pady=3)

        minutes_label = ctk.CTkLabel(worker_frame, text="Minutes:")
        minutes_label.grid(row=0, column=4, padx=5, pady=3)
        minutes_optionmenu = ctk.CTkOptionMenu(worker_frame, values=['00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55'])
        minutes_optionmenu.grid(row=0, column=5, padx=5, pady=3)

        tipout_label = ctk.CTkLabel(worker_frame, text="Tipout:")
        tipout_label.grid(row=0, column=6, padx=5, pady=3)
        tipout_entry = ctk.CTkEntry(worker_frame, state="readonly")
        tipout_entry.grid(row=0, column=7, padx=5, pady=3)

        notes_label = ctk.CTkLabel(worker_frame, text="Notes:")
        notes_label.grid(row=0, column=8, padx=5, pady=3)
        notes_entry = ctk.CTkEntry(worker_frame)
        notes_entry.grid(row=0, column=9, padx=5, pady=3)

        self.worker_entries.append((worker_frame, name_entry, hours_optionmenu, minutes_optionmenu, notes_entry, tipout_entry))

    def remove_worker_entry(self, worker_frame):
        worker_frame.pack_forget()
        self.worker_entries = [entry for entry in self.worker_entries if entry[0] != worker_frame]

    def remove_worker(self):
        if self.worker_entries:
            worker_frame, *_ = self.worker_entries[-1]
            self.remove_worker_entry(worker_frame)

    def calculate_tipout(self):
        total_tips_entry = self.total_tips_entry.get()

        if not total_tips_entry:
            CTkMessagebox(message="Please enter the total tips.", title="Error", icon='cancel')
            return

        try:
            total_tips = float(total_tips_entry)
        except ValueError:
            CTkMessagebox(message="Please enter a valid number for Total Tips.", title="Error", icon='cancel')
            return
        
        total_minutes = 0
        for _, _, hours_optionmenu, minutes_optionmenu, _, _ in self.worker_entries:
            hours = int(hours_optionmenu.get())
            minutes = int(minutes_optionmenu.get())
            total_minutes += (hours * 60) + minutes

        # Calculate the tipout for each worker based on time worked
        for _, _, hours_optionmenu, minutes_optionmenu, _, tipout_entry in self.worker_entries:
            hours = int(hours_optionmenu.get())
            minutes = int(minutes_optionmenu.get())
            time_worked_minutes = (hours * 60) + minutes

            if total_minutes == 0:
                CTkMessagebox(message="Please enter shift time larger than 0.", title="Error", icon='cancel')
                return


            tipout = total_tips * (time_worked_minutes / total_minutes)
            tipout_entry.configure(state="normal")
            tipout_entry.delete(0, "end")
            tipout_entry.insert(0, f"${tipout:.2f}")
            tipout_entry.configure(state="readonly")

    def export(self):
        the_date = date.today().strftime("%m/%d/%Y")
        splitting_tips = self.splitting_tips_entry.get()
        total_tips_entry = self.total_tips_entry.get()

        if not splitting_tips:
            CTkMessagebox(message="Please enter who is splitting the tips.", title="Error", icon='cancel')
            return

        if not total_tips_entry:
            CTkMessagebox(message="Please enter the total tips.", title="Error", icon='cancel')
            return

        try:
            total_tips = float(total_tips_entry)
        except ValueError:
            CTkMessagebox(message="Please enter a valid number for Total Tips.", title="Error", icon='cancel')
            return

        workers = []
        for _, name_entry, hours_optionmenu, minutes_optionmenu, notes_entry, tipout_entry in self.worker_entries:
            name = name_entry.get()
            hours = int(hours_optionmenu.get())
            minutes = int(minutes_optionmenu.get())
            tipout = tipout_entry.get()
            notes = notes_entry.get()

            if not name:
                CTkMessagebox(message="Please fill in all names of workers.", title="Error", icon='cancel')
                return

            if not tipout:
                CTkMessagebox(message="Please calculate the tipout.", title="Error", icon='cancel')
                return
            
            if hours == 0 and minutes == 0:
                CTkMessagebox(message="Please enter a shift time larger than 0.", title="Error", icon='cancel')
                return

            if minutes < 10:
                minutes = f"0{minutes}"

            worker = {
                "Date": the_date,
                "Tip Splitter": splitting_tips,
                "Total Tips": total_tips,
                "Name": name,
                "Shift Time": str(hours) + ":" + str(minutes),
                "Tipout": tipout,
                "Tip Percentage": f"{float(tipout[1:]) / float(total_tips) * 100:.2f}%",
                "Notes": notes,
            }
            workers.append(worker)

        if not workers:
            CTkMessagebox(message="Please add at least one worker.", title="Error", icon='cancel')
            return

        def add_rows_to_sheet(rows_data):
            sheet_id = '17Hm5gskvupWPwcfV2_5SP65qzMrgpxDXGC6mG0YxJI4'
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
            service_account_file = './data/creds.json'
            credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)
            service = build('sheets', 'v4', credentials=credentials)
            sheet_range = 'Sheet1!A:Z'  # Replace with the desired sheet and range

            body = {
                'values': rows_data
            }
            result = service.spreadsheets().values().append(
                spreadsheetId=sheet_id,
                range=sheet_range,
                valueInputOption='RAW',
                body=body
            ).execute()

        # Perform the export functionality
        cleaned = []
        for worker in workers:
            cleaned.append(list(worker.values()))

        add_rows_to_sheet(cleaned)

        # Clear the table of worker entries
        self.worker_entries = []
        for child in self.workers_frame.winfo_children():
            child.destroy()

        msg = CTkMessagebox(message="The tips have been logged. Would you like to close Tip Wizard?", title="Export Successful", icon='check', option_1="No", option_2="Okay")

        response = msg.get()

        if response == "Okay":
            self.destroy()


if __name__ == "__main__":
    app = TipSplitterApp()
    app.mainloop()



import re
import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
from PIL import Image, ImageTk

class EditVoterInfoWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Edit Voter Information")
        self.configure(bg="#f0f0f0")

         # Load and resize the background image
        img = Image.open("basicblue.jpg")
        img = img.resize((parent.winfo_screenwidth(), parent.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(img)

        # Create a label to hold the background image
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.username_label = tk.Label(self, text="Enter Username:", font=("Helvetica", 12), bg="#f0f0f0")
        self.username_label.pack()
        self.username_entry = tk.Entry(self, font=("Helvetica", 12))
        self.username_entry.pack(pady=5)

        self.old_password_label = tk.Label(self, text="Enter Old Password:", font=("Helvetica", 12), bg="#f0f0f0")
        self.old_password_label.pack()
        self.old_password_entry = tk.Entry(self, show="*", font=("Helvetica", 12))
        self.old_password_entry.pack(pady=5)

        self.new_password_label = tk.Label(self, text="Enter New Password:", font=("Helvetica", 12), bg="#f0f0f0")
        self.new_password_label.pack()
        self.new_password_entry = tk.Entry(self, show="*", font=("Helvetica", 12))
        self.new_password_entry.pack(pady=5)

        self.confirm_password_label = tk.Label(self, text="Confirm New Password:", font=("Helvetica", 12), bg="#f0f0f0")
        self.confirm_password_label.pack()
        self.confirm_password_entry = tk.Entry(self, show="*", font=("Helvetica", 12))
        self.confirm_password_entry.pack(pady=5)

        search_button = tk.Button(self, text="CHANGE", command=self.search_voter, font=("Helvetica", 12))
        search_button.pack(pady=10)
        

    def search_voter(self):
        username = self.username_entry.get()
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if username.strip() == "" or old_password.strip() == "" or new_password.strip() == "" or confirm_password.strip() == "":
            messagebox.showerror("Error", "All fields are required.")
            return
        
        if new_password != confirm_password:
            messagebox.showerror("Error", "New password and confirm password do not match.")
            return
        
        if self.validate(username, old_password):
            self.update_password(username, new_password)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def validate(self, username, password):
        try:
            with open("voters.txt", "r") as file:
                for line in file:
                    stored_username, stored_password = line.strip().split(",")
                    if username == stored_username and password == stored_password:
                        return True
        except FileNotFoundError:
            messagebox.showerror("Error", "Candidates information file not found.")
        return False

    def update_password(self, username, new_password):
        try:
            with open("voters.txt", "r") as file:
                lines = file.readlines()
            
            with open("voters.txt", "w") as file:
                for line in lines:
                    stored_username, stored_password = line.strip().split(",")
                    if username == stored_username:
                        line = f"{username},{new_password}\n"
                    file.write(line)
                
            messagebox.showinfo("Success", "Password updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update password: {e}")

class ViewVoterInfoWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("View Voter Information")
        self.geometry("400x300")
        self.configure(bg="#f0f0f0")

         # Load and resize the background image
        img = Image.open("basicblue.jpg")
        img = img.resize((parent.winfo_screenwidth(), parent.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(img)

        # Create a label to hold the background image
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.voter_list_label = tk.Label(self, text="Registered Voters", font=("Helvetica", 16), bg="#f0f0f0")
        self.voter_list_label.pack(pady=10)
        

        self.voter_listbox = tk.Listbox(self, font=("Helvetica", 12), bg="white", selectmode="browse")
        self.voter_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.load_voters()

        

    def load_voters(self):
        try:
            with open("voters.csv", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    self.voter_listbox.insert(tk.END, f"Username: {row[0]}, Email: {row[1]}, Phone: {row[2]}")
        except FileNotFoundError:
            messagebox.showerror("Error", "No voter information found.")

class EditCandidatesWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Edit Candidates")
        self.geometry("300x200")
        self.configure(bg="#f0f0f0")

         # Load and resize the background image
        img = Image.open("basicblue.jpg")
        img = img.resize((parent.winfo_screenwidth(), parent.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(img)

        # Create a label to hold the background image
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        label = tk.Label(self, text="Edit Candidates", font=("Helvetica", 16), bg="#f0f0f0")
        label.pack(pady=10)

        add_button = tk.Button(self, text="Add Candidate", command=self.add_candidate, font=("Helvetica", 12))
        add_button.pack(pady=5)

        remove_button = tk.Button(self, text="Remove Candidate", command=self.remove_candidate, font=("Helvetica", 12))
        remove_button.pack(pady=5)

        done_button = tk.Button(self, text="Done", command=self.destroy, font=("Helvetica", 12))
        done_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

    def add_candidate(self):
        candidate_name = simpledialog.askstring("Add Candidate", "Enter candidate name:")
        if candidate_name:
            CandidatePage.candidates.append({"name": candidate_name, "votes": 0})
            self.update_candidates()

    def remove_candidate(self):
        candidate_name = simpledialog.askstring("Remove Candidate", "Enter candidate name to remove:")
        if candidate_name:
            # Remove the candidate from the candidates list
            self.remove_candidate_from_list(candidate_name)
            # Update the GUI to reflect the changes
            self.update_candidates()

    def remove_candidate_from_list(self, candidate_name):
        # Assuming CandidatePage.candidates is a list of dictionaries with a 'name' key
        self.master.CandidatePage.candidates = [c for c in self.master.CandidatePage.candidates if c["name"] != candidate_name]

    def save_candidates_to_csv(self):
        with open("candidates.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Votes"])  # Header row
            for candidate in CandidatePage.candidates:
                writer.writerow([candidate["name"], candidate["votes"]])
                
    def save_candidates_to_csv(self):
        with open("candidates.csv", "a", newline="") as file:
            writer = csv.writer(file)
            for candidate in CandidatePage.candidates:
                writer.writerow([candidate["name"], candidate["votes"]])

class CandidatePage(tk.Toplevel):
    candidates = []

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Choose a Candidate")
        self.geometry("400x300")
        self.configure(bg="#f0f0f0")

         # Load and resize the background image
        img = Image.open("background3.jpg")
        img = img.resize((parent.winfo_screenwidth(), parent.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(img)

        # Create a label to hold the background image
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.load_candidates()

        label = tk.Label(self, text="Choose a Candidate", font=("Helvetica", 16), bg="#f0f0f0")
        label.pack(pady=10)

        self.candidate_labels = []
        self.vote_buttons = []

        for i, candidate in enumerate(self.candidates, start=1):
            candidate_frame = tk.Frame(self, bg="#f0f0f0")
            candidate_frame.pack(pady=5)

            candidate_label = tk.Label(candidate_frame, text=f"{candidate['name']}", font=("Helvetica", 12), bg="#f0f0f0")
            candidate_label.pack(side="left", padx=10)
            self.candidate_labels.append(candidate_label)

            vote_button = tk.Button(candidate_frame, text="Vote", command=lambda idx=i-1: self.vote(idx), font=("Helvetica", 10))
            vote_button.pack(side="right", padx=10)
            self.vote_buttons.append(vote_button)

    def load_candidates(self):
        self.candidates = []  # Clear the candidates list first
        try:
            with open("candidates.csv", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    self.candidates.append({"name": row[0], "votes": int(row[1])})
        except FileNotFoundError:
            pass

    def update_candidates(self):
        # Remove old labels and buttons
        for label in self.candidate_labels:
            label.pack_forget()
        for button in self.vote_buttons:
            button.pack_forget()

        self.candidate_labels = []
        self.vote_buttons = []

        for i, candidate in enumerate(self.candidates, start=1):
            candidate_frame = tk.Frame(self, bg="#f0f0f0")
            candidate_frame.pack(pady=5)

            candidate_label = tk.Label(candidate_frame, text=f"{candidate['name']}", font=("Helvetica", 12), bg="#f0f0f0")
            candidate_label.pack(side="left", padx=10)
            self.candidate_labels.append(candidate_label)

            vote_button = tk.Button(candidate_frame, text="Vote", command=lambda idx=i-1: self.vote(idx), font=("Helvetica", 10))
            vote_button.pack(side="right", padx=10)
            self.vote_buttons.append(vote_button)

    def vote(self, candidate_index):
        self.candidates[candidate_index]["votes"] += 1
        self.save_votes_to_csv()
        messagebox.showinfo("Success", f"You voted for {self.candidates[candidate_index]['name']}")
        self.withdraw()

    def save_votes_to_csv(self):
        with open("candidates.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for candidate in self.candidates:
                writer.writerow([candidate["name"], candidate["votes"]])

class LoginPageVoter(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Voter Login")
        self.configure(bg="#f0f0f0")

        # Load and resize the background image
        img = Image.open("background2.jpg")
        img = img.resize((parent.winfo_screenwidth(), parent.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(img)

        # Create a label to hold the background image
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        label = tk.Label(self, text="Enter your login details:", font=("Helvetica", 16), bg="#f0f0f0")
        label.pack(pady=10)

        self.username_label = tk.Label(self, text="Username:", font=("Helvetica", 12), bg="#f0f0f0")
        self.username_label.pack()
        self.username_entry = tk.Entry(self, font=("Helvetica", 12))
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Password:", font=("Helvetica", 12), bg="#f0f0f0")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*", font=("Helvetica", 12))
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self, text="Login", command=self.login, font=("Helvetica", 12))
        login_button.pack(pady=10)
        
        self.username_label = tk.Label(self, text="!!! LIVE POLL RESULTS !!!", font=("Helvetica", 25), fg="red")
        self.username_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)


        self.voting_results_label = tk.Label(self, text="", font=("Helvetica", 18), bg="skyblue")
        self.voting_results_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)


        # Periodically update voting results
        self.refresh_interval = 10 * 1000  # Refresh every 10 seconds (milliseconds)
        self.update_voting_results()

    def update_voting_results(self):
        # Fetch the latest voting data from the backend
        latest_results = self.fetch_latest_results()

        # Update the voting results label with the latest data
        self.voting_results_label.config(text=latest_results)

        # Schedule the next update after the refresh interval
        self.after(self.refresh_interval, self.update_voting_results)

    def fetch_latest_results(self):
        # Fetch the latest voting data from the backend (e.g., candidates and their votes)
        # Perform any necessary calculations or formatting
        # Return the formatted voting results as a string
        try:
            with open("candidates.csv", newline="") as file:
                reader = csv.reader(file)
                results = []
                for row in reader:
                    candidate_name, votes = row
                    results.append(f"{candidate_name}: {votes} votes")
                return "\n".join(results)
        except FileNotFoundError:
            return "No voting data available."

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
    
        if username.strip() == "" or password.strip() == "":
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
    
        if self.validate(username, password):
            if self.has_voted(username):
                messagebox.showinfo("Info", "You have already voted.")
                self.withdraw()
            else:
                messagebox.showinfo("Success", "Login Successful!")
                self.mark_voted(username)  # Mark the user as voted
                candidate_page = CandidatePage(self)
                self.withdraw()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def validate(self, username, password):
        # Assuming the format of the "voters.txt" file is "username,password" per line
        # Check if the username and password pair exists in the file
        with open("voters.txt", "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(",")
                if username == stored_username and password == stored_password:
                    return True
        return False

    def has_voted(self, username):
        # Check if the user has already voted
        with open("votedvoters.txt", "r") as file:
            return any(line.strip() == username for line in file)

    def mark_voted(self, username):
        # Mark the user as voted by appending their username to the votedvoters.txt file
        with open("votedvoters.txt", "a") as file:
            file.write(username + "\n")

class LoginPageAdmin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Admin Login")
        self.configure(bg="#f0f0f0")

        # Load and resize the background image
        img = Image.open("background5.jpg")
        img = img.resize((parent.winfo_screenwidth(), parent.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(img)

        # Create a label to hold the background image
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        label = tk.Label(self, text="ADMIN, Enter your login details:", font=("Helvetica", 16), bg="#f0f0f0")
        label.pack(pady=10)

        username_label = tk.Label(self, text="Username:", font=("Helvetica", 12), bg="#f0f0f0")
        username_label.pack()
        self.username_entry = tk.Entry(self, font=("Helvetica", 12))
        self.username_entry.pack(pady=5)

        password_label = tk.Label(self, text="Password:", font=("Helvetica", 12), bg="#f0f0f0")
        password_label.pack()
        self.password_entry = tk.Entry(self, show="*", font=("Helvetica", 12))
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self, text="Login", command=self.login, font=("Helvetica", 12))
        login_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username.strip() == "" or password.strip() == "":
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return
        
        if self.validate(username, password):
            messagebox.showinfo("Success", "Login Successful!")
            welcome_admin_window = WelcomeAdminWindow(self)
            self.withdraw()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def validate(self, username, password):
    # Assuming the format of the "voters.txt" file is "username,password" per line
    # Check if the username and password pair exists in the file
        with open("admin.txt", "r") as file:
            for line in file:
                stored_username, stored_password = line.strip().split(" ")
                if username == stored_username and password == stored_password:
                    return True

        return False

class WelcomeAdminWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Welcome Admin")
        self.configure(bg="#f0f0f0")

        img = Image.open("background6.jpg")
        img = img.resize((parent.winfo_screenwidth(), parent.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(img)

        # Create a label to hold the background image
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        welcome_label = tk.Label(self, text="Welcome Admin!", font=("Helvetica", 20), bg="#f0f0f0")
        welcome_label.pack(pady=20)
        
        welcome_label = tk.Label(self, text="Select function do you want to perform:", font=("Helvetica", 16), bg="#f0f0f0")
        welcome_label.pack(pady=20)

        edit_candidates_button = tk.Button(self, text="Edit Candidates", command=self.edit_candidates, font=("Helvetica", 12))
        edit_candidates_button.pack(pady=10)

        view_candidates_button = tk.Button(self, text="View Candidates Information", command=self.view_candidates_info, font=("Helvetica", 12))
        view_candidates_button.pack(pady=5)

        view_voters_button = tk.Button(self, text="View Voter Information", command=self.view_voter_info, font=("Helvetica", 12))
        view_voters_button.pack(pady=5)

        change_voter_info_button = tk.Button(self, text="Change Voter Information", command=self.change_voter_info, font=("Helvetica", 12))
        change_voter_info_button.pack(pady=5)

        view_candidates_button = tk.Button(self, text="Click to view RESULT", command=self.view_result, font=("Helvetica", 12))
        view_candidates_button.pack(pady=5)

    def change_voter_info(self):
        
        edit_voter_info_window = EditVoterInfoWindow(self)    

    def edit_candidates(self):
        edit_candidates_window = EditCandidatesWindow(self)

    def view_candidates_info(self):
        view_candidates_info_window = tk.Toplevel(self)
        view_candidates_info_window.title("View Candidates Information")
        view_candidates_info_window.configure(bg="#f0f0f0")

        candidates_label = tk.Label(view_candidates_info_window, text="Candidates Information", font=("Helvetica", 16), bg="#f0f0f0")
        candidates_label.pack(pady=10)

        try:
            with open("candidates.csv", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    candidate_name, votes = row
                    candidate_info_label = tk.Label(view_candidates_info_window, text=f"{candidate_name}: {votes} votes", font=("Helvetica", 12), bg="#f0f0f0")
                    candidate_info_label.pack()
        except FileNotFoundError:
            messagebox.showerror("Error", "No candidate information found.")

    def view_voter_info(self):
        view_voter_info_window = tk.Toplevel(self)
        view_voter_info_window.title("View Voter Information")
        view_voter_info_window.configure(bg="#f0f0f0")

        voters_label = tk.Label(view_voter_info_window, text="Logged-in Voters Information", font=("Helvetica", 16), bg="#f0f0f0")
        voters_label.pack(pady=10)

        try:
            with open("voters.txt", "r") as file:
                logged_in_voters = file.readlines()
                if logged_in_voters:
                    for voter in logged_in_voters:
                        voter_label = tk.Label(view_voter_info_window, text=voter.strip(), font=("Helvetica", 12), bg="#f0f0f0")
                        voter_label.pack()
                else:
                    messagebox.showinfo("Info", "No voters are currently logged in.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Candidates file not found.")

    def view_result(self):
        try:
            with open("candidates.csv", newline="") as file:
                reader = csv.reader(file)
                max_votes = -1
                winner_name = ""
                for row in reader:
                    candidate_name, votes = row
                    votes = int(votes)
                    if votes > max_votes:
                        max_votes = votes
                        winner_name = candidate_name

                if winner_name:
                    messagebox.showinfo("Election Result", f"The winner is {winner_name} with {max_votes} votes!")
                else:
                    messagebox.showinfo("Election Result", "No result available yet.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Candidates information file not found.")

class LoginPageRegister(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Register")
        self.configure(bg="#f0f0f0")

 # Load and resize the background image
        img = Image.open("background4.jpg")
        img = img.resize((parent.winfo_screenwidth(), parent.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(img)

        # Create a label to hold the background image
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        label = tk.Label(self, text="Enter your registration details:", font=("Helvetica", 16), bg="#f0f0f0")
        label.pack(pady=10)

        self.full_name_label = tk.Label(self, text="Full Name:", font=("Helvetica", 12), bg="#f0f0f0")
        self.full_name_label.pack()
        self.full_name_entry = tk.Entry(self, font=("Helvetica", 12))
        self.full_name_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Password:", font=("Helvetica", 12), bg="#f0f0f0")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*", font=("Helvetica", 12))
        self.password_entry.pack(pady=5)

        self.email_label = tk.Label(self, text="Email:", font=("Helvetica", 12), bg="#f0f0f0")
        self.email_label.pack()
        self.email_entry = tk.Entry(self, font=("Helvetica", 12))
        self.email_entry.pack(pady=5)

        self.phone_number_label = tk.Label(self, text="Phone Number:", font=("Helvetica", 12), bg="#f0f0f0")
        self.phone_number_label.pack()
        self.phone_number_entry = tk.Entry(self, font=("Helvetica", 12))
        self.phone_number_entry.pack(pady=5)

        register_button = tk.Button(self, text="Register", command=self.register_user, font=("Helvetica", 12))
        register_button.pack(pady=10)

    def register_user(self):
        full_name = self.full_name_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        phone_number = self.phone_number_entry.get()
        
        if not full_name or not password or not email or not phone_number:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email address")
            return
        
        if not self.validate_phone_number(phone_number):
            messagebox.showerror("Error", "Invalid phone number")
            return
        
        with open("voters.txt", "a") as file:
            file.write(f"{full_name},{password}\n")
        
        messagebox.showinfo("Success", "Registration successful")
        self.withdraw()

    def validate_email(self, email):
        # Regular expression for email validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

    def validate_phone_number(self, phone_number):
        # Regular expression for phone number validation
        pattern = r'^[0-9]{10}$'
        return re.match(pattern, phone_number)

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load and resize the background image
        img = Image.open("background.jpg")
        img = img.resize((parent.winfo_screenwidth(), parent.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(img)

        # Create a label to hold the background image
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a frame for the content with border
        content_frame = tk.Frame(self, bg="#f0f0f0", bd=2, relief="solid")
        content_frame.place(relx=0.025, rely=0.4, anchor=tk.W, relwidth=0.38, relheight=0.4)

        # # Label for the title with left alignment
        label = tk.Label(content_frame, text="Welcome to Online Voting System", font=("Helvetica", 20), bg="#f0f0f0", fg="black")
        label.place(relx=0.1, rely=0.15, anchor=tk.W)

        # Login buttons
        button_y_offset = 0.3
        button_spacing = 10

        login_button_user = tk.Button(content_frame, text="Login as Voter", 
                                      command=self.open_login_window_voter, 
                                      bg="#007bff", fg="white", font=("Helvetica", 12))
        login_button_user.place(relx=0.28, rely=button_y_offset, anchor=tk.W)

        login_button_admin = tk.Button(content_frame, text="Login as Admin", 
                                       command=self.open_login_window_admin, 
                                       bg="#007bff", fg="white", font=("Helvetica", 12))
        login_button_admin.place(relx=0.28, rely=button_y_offset + 0.15, anchor=tk.W)

        # Register message and button
        register_message = tk.Label(content_frame, text="Don't have an account? Register here:", bg="#f0f0f0", fg="black", font=("Helvetica", 12))
        register_message.place(relx=0.16, rely=button_y_offset + 0.3, anchor=tk.W)

        register_button = tk.Button(content_frame, text="Register", 
                                    command=self.open_login_window_register, 
                                    bg="#28a745", fg="white", font=("Helvetica", 12))
        register_button.place(relx=0.3, rely=button_y_offset + 0.4, anchor=tk.W)

    def open_login_window_voter(self):
        login_window = LoginPageVoter(self)

    def open_login_window_admin(self):
        login_window = LoginPageAdmin(self)

    def open_login_window_register(self):
        login_window = LoginPageRegister(self)
  
class SampleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Online Voting System")
        
         # Calculate the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Set the window geometry to fill most of the screen
        window_width = int(screen_width * 0.9)  # Adjust the width as needed
        window_height = int(screen_height * 0.9)  # Adjust the height as needed
        window_geometry = f"{window_width}x{window_height}+{screen_width // 20}+{screen_height // 20}"
        self.geometry(window_geometry)

        container = tk.Frame(self, bg="#f0f0f0")
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (MainPage,):
            frame = F(container, self)
            self.frames[F] = frame
            frame.pack(fill="both", expand=True)

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

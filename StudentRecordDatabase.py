import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


class StudentRecordGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record Manager")
        self.root.geometry("1420x550")
        self.root.configure(bg='#f0f0f0')

        # Initialize database
        self.init_database()

        # Create GUI elements
        self.create_widgets()

        # Load initial data
        self.refresh_student_list()

    def init_database(self):
        """Initialize the database connection and create table"""
        try:
            self.connection = sqlite3.connect("students.db")
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    grade TEXT,
                    email TEXT
                )
            """)
            self.connection.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error initializing database: {e}")

    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Title
        title_label = tk.Label(
            self.root,
            text="Student Record Manager",
            font=("Arial", 18, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=10)

        # Main frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left frame for form
        left_frame = tk.Frame(main_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Form title
        form_title = tk.Label(
            left_frame,
            text="Student Information",
            font=("Arial", 14, "bold"),
            bg='#ffffff',
            fg='#34495e'
        )
        form_title.pack(pady=10)

        # Form fields
        form_frame = tk.Frame(left_frame, bg='#ffffff')
        form_frame.pack(padx=20, pady=10, fill=tk.X)

        # ID field
        tk.Label(form_frame, text="Student ID (numbers only):", bg='#ffffff', font=("Arial", 10)).grid(row=0, column=0,
                                                                                                       sticky='w',
                                                                                                       pady=5)
        self.id_entry = tk.Entry(form_frame, font=("Arial", 10), width=25)
        self.id_entry.grid(row=0, column=1, pady=5, padx=(10, 0), sticky='ew')

        # Name field
        tk.Label(form_frame, text="Name:", bg='#ffffff', font=("Arial", 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.name_entry = tk.Entry(form_frame, font=("Arial", 10), width=25)
        self.name_entry.grid(row=1, column=1, pady=5, padx=(10, 0), sticky='ew')

        # Grade field
        tk.Label(form_frame, text="Grade (optional):", bg='#ffffff', font=("Arial", 10)).grid(row=2, column=0,
                                                                                              sticky='w', pady=5)
        self.grade_entry = tk.Entry(form_frame, font=("Arial", 10), width=25)
        self.grade_entry.grid(row=2, column=1, pady=5, padx=(10, 0), sticky='ew')

        # Email field
        tk.Label(form_frame, text="Email (must contain @):", bg='#ffffff', font=("Arial", 10)).grid(row=3, column=0,
                                                                                                    sticky='w', pady=5)
        self.email_entry = tk.Entry(form_frame, font=("Arial", 10), width=25)
        self.email_entry.grid(row=3, column=1, pady=5, padx=(10, 0), sticky='ew')

        form_frame.columnconfigure(1, weight=1)

        # Buttons frame
        button_frame = tk.Frame(left_frame, bg='#ffffff')
        button_frame.pack(pady=20)

        # Add button
        self.add_btn = tk.Button(
            button_frame,
            text="Add Student",
            command=self.add_student,
            bg='#27ae60',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        )
        self.add_btn.pack(side=tk.LEFT, padx=5)

        # Update button
        self.update_btn = tk.Button(
            button_frame,
            text="Update Student",
            command=self.update_student,
            bg='#3498db',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        )
        self.update_btn.pack(side=tk.LEFT, padx=5)

        # Delete button
        self.delete_btn = tk.Button(
            button_frame,
            text="Delete Student",
            command=self.delete_student,
            bg='#e74c3c',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        )
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        # Clear button
        self.clear_btn = tk.Button(
            button_frame,
            text="Clear Form",
            command=self.clear_form,
            bg='#95a5a6',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # Right frame for student list
        right_frame = tk.Frame(main_frame, bg='#ffffff', relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Student list title
        list_title = tk.Label(
            right_frame,
            text="Student Records",
            font=("Arial", 14, "bold"),
            bg='#ffffff',
            fg='#34495e'
        )
        list_title.pack(pady=10)

        # Treeview for student list
        tree_frame = tk.Frame(right_frame, bg='#ffffff')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create treeview
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Grade', 'Email'), show='headings', height=15)

        # Define headings
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Grade', text='Grade')
        self.tree.heading('Email', text='Email')

        # Configure column widths
        self.tree.column('ID', width=60)
        self.tree.column('Name', width=120)
        self.tree.column('Grade', width=80)
        self.tree.column('Email', width=150)

        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind tree selection
        self.tree.bind('<ButtonRelease-1>', self.on_tree_select)

        # Refresh button
        refresh_btn = tk.Button(
            right_frame,
            text="Refresh List",
            command=self.refresh_student_list,
            bg='#f39c12',
            fg='white',
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5
        )
        refresh_btn.pack(pady=10)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg='#ecf0f1',
            font=("Arial", 9)
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def validate_id_input(self, id_input):
        """Validate that the ID input contains only numbers"""
        if not id_input or not id_input.strip():
            return None, "ID cannot be empty."

        id_str = id_input.strip()

        if not id_str.isdigit():
            return None, "ID must contain only numbers (0-9)."

        id_int = int(id_str)
        if id_int <= 0:
            return None, "ID must be a positive number greater than 0."

        return id_int, None

    def validate_email_input(self, email_input):
        """Validate that the email input contains an @ sign"""
        if not email_input or not email_input.strip():
            return None, None  # Empty email is allowed

        email_str = email_input.strip()

        if '@' not in email_str:
            return None, "Email must contain an @ sign."

        parts = email_str.split('@')
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return None, "Email must have text both before and after the @ sign."

        return email_str, None

    def clear_form(self):
        """Clear all form fields"""
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.status_var.set("Form cleared")

    def on_tree_select(self, event):
        """Handle tree selection - populate form with selected student data"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']

            # Clear and populate form
            self.clear_form()
            self.id_entry.insert(0, values[0])
            self.name_entry.insert(0, values[1])
            self.grade_entry.insert(0, values[2] if values[2] != 'N/A' else '')
            self.email_entry.insert(0, values[3] if values[3] != 'N/A' else '')

            self.status_var.set(f"Selected student ID: {values[0]}")

    def add_student(self):
        """Add a new student"""
        try:
            # Get form data
            id_input = self.id_entry.get()
            name = self.name_entry.get().strip()
            grade = self.grade_entry.get().strip()
            email = self.email_entry.get().strip()

            # Validate ID
            validated_id, id_error = self.validate_id_input(id_input)
            if id_error:
                messagebox.showerror("Invalid ID", id_error)
                return

            # Validate name
            if not name:
                messagebox.showerror("Invalid Name", "Name cannot be empty.")
                return

            # Validate email
            validated_email, email_error = self.validate_email_input(email)
            if email_error:
                messagebox.showerror("Invalid Email", email_error)
                return

            # Insert into database
            self.cursor.execute(
                "INSERT INTO students (id, name, grade, email) VALUES (?, ?, ?, ?)",
                (validated_id, name, grade if grade else None, validated_email)
            )
            self.connection.commit()

            messagebox.showinfo("Success", f"Student '{name}' with ID {validated_id} added successfully!")
            self.clear_form()
            self.refresh_student_list()
            self.status_var.set("Student added successfully")

        except sqlite3.IntegrityError:
            messagebox.showerror("Database Error", f"Student with ID {validated_id} already exists.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error adding student: {e}")

    def update_student(self):
        """Update an existing student"""
        try:
            # Get form data
            id_input = self.id_entry.get()
            name = self.name_entry.get().strip()
            grade = self.grade_entry.get().strip()
            email = self.email_entry.get().strip()

            # Validate ID
            validated_id, id_error = self.validate_id_input(id_input)
            if id_error:
                messagebox.showerror("Invalid ID", id_error)
                return

            # Check if student exists
            self.cursor.execute("SELECT * FROM students WHERE id = ?", (validated_id,))
            if not self.cursor.fetchone():
                messagebox.showerror("Student Not Found", f"No student found with ID {validated_id}")
                return

            # Validate name if provided
            if name and not name.strip():
                messagebox.showerror("Invalid Name", "Name cannot be empty.")
                return

            # Validate email if provided
            if email:
                validated_email, email_error = self.validate_email_input(email)
                if email_error:
                    messagebox.showerror("Invalid Email", email_error)
                    return
            else:
                validated_email = None

            # Update database
            self.cursor.execute(
                "UPDATE students SET name = ?, grade = ?, email = ? WHERE id = ?",
                (name if name else None, grade if grade else None, validated_email, validated_id)
            )
            self.connection.commit()

            if self.cursor.rowcount > 0:
                messagebox.showinfo("Success", f"Student with ID {validated_id} updated successfully!")
                self.clear_form()
                self.refresh_student_list()
                self.status_var.set("Student updated successfully")
            else:
                messagebox.showerror("Update Failed", "No changes were made.")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error updating student: {e}")

    def delete_student(self):
        """Delete a student"""
        try:
            # Get ID from form
            id_input = self.id_entry.get()

            # Validate ID
            validated_id, id_error = self.validate_id_input(id_input)
            if id_error:
                messagebox.showerror("Invalid ID", id_error)
                return

            # Confirm deletion
            response = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete student with ID {validated_id}?"
            )

            if response:
                # Delete from database
                self.cursor.execute("DELETE FROM students WHERE id = ?", (validated_id,))
                self.connection.commit()

                if self.cursor.rowcount > 0:
                    messagebox.showinfo("Success", f"Student with ID {validated_id} deleted successfully!")
                    self.clear_form()
                    self.refresh_student_list()
                    self.status_var.set("Student deleted successfully")
                else:
                    messagebox.showerror("Student Not Found", f"No student found with ID {validated_id}")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error deleting student: {e}")

    def refresh_student_list(self):
        """Refresh the student list in the treeview"""
        try:
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Fetch all students
            self.cursor.execute("SELECT * FROM students ORDER BY id")
            rows = self.cursor.fetchall()

            # Populate treeview
            for row in rows:
                self.tree.insert('', tk.END, values=(
                    row[0],  # ID
                    row[1],  # Name
                    row[2] if row[2] else 'N/A',  # Grade
                    row[3] if row[3] else 'N/A'  # Email
                ))

            self.status_var.set(f"Showing {len(rows)} students")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error refreshing student list: {e}")

    def on_closing(self):
        """Handle application closing"""
        try:
            self.connection.close()
        except:
            pass
        self.root.destroy()


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = StudentRecordGUI(root)

    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
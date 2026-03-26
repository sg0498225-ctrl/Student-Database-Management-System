import tkinter as tk
from tkinter import messagebox, ttk
from database import (add_student, get_all_students, delete_student, 
                      update_student, search_students)

class StudentDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Database System")
        self.root.geometry("800x600")
        
        # ID for edit/delete
        self.selected_id = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Input frame
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0)
        self.name_entry = ttk.Entry(input_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Age:").grid(row=0, column=2)
        self.age_entry = ttk.Entry(input_frame, width=10)
        self.age_entry.grid(row=0, column=3, padx=5)
        
        ttk.Label(input_frame, text="Grade:").grid(row=0, column=4)
        self.grade_entry = ttk.Entry(input_frame, width=10)
        self.grade_entry.grid(row=0, column=5, padx=5)
        
        # Buttons frame
        btn_frame = ttk.Frame(input_frame)
        btn_frame.grid(row=1, column=0, columnspan=6, pady=10)
        
        ttk.Button(btn_frame, text="Add Student", command=self.add_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View All", command=self.view_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Search", command=self.search).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit", command=self.edit_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_student).pack(side=tk.LEFT, padx=5)
        
        # Search entry
        ttk.Label(input_frame, text="Search:").grid(row=2, column=0)
        self.search_entry = ttk.Entry(input_frame, width=20)
        self.search_entry.grid(row=2, column=1, padx=5)
        
        # Listbox
        self.listbox = tk.Listbox(self.root, height=20, width=100)
        self.listbox.grid(row=1, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
    
    def add_student(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        grade = self.grade_entry.get()
        if name and age.isdigit() and grade:
            student_id = add_student(name, int(age), grade)
            messagebox.showinfo("Success", f"Student added with ID: {student_id}")
            self.clear_entries()
            self.view_all()
        else:
            messagebox.showerror("Error", "Please fill all fields correctly (age must be number).")
    
    def view_all(self):
        students = get_all_students()
        self.listbox.delete(0, tk.END)
        for s in students:
            self.listbox.insert(tk.END, f"ID: {s['id']} | Name: {s['name']} | Age: {s['age']} | Grade: {s['grade']}")
    
    def search(self):
        query = self.search_entry.get()
        if query:
            students = search_students(query)
            self.listbox.delete(0, tk.END)
            for s in students:
                self.listbox.insert(tk.END, f"ID: {s['id']} | Name: {s['name']} | Age: {s['age']} | Grade: {s['grade']}")
        else:
            self.view_all()
    
    def on_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            item = self.listbox.get(selection[0])
            self.selected_id = int(item.split('ID: ')[1].split(' |')[0])
    
    def edit_student(self):
        if not self.selected_id:
            messagebox.showerror("Error", "Select a student first.")
            return
        name = self.name_entry.get()
        age = self.age_entry.get()
        grade = self.grade_entry.get()
        if name and age.isdigit() and grade:
            if update_student(self.selected_id, name, int(age), grade):
                messagebox.showinfo("Success", "Student updated.")
                self.clear_entries()
                self.view_all()
            else:
                messagebox.showerror("Error", "Student not found.")
        else:
            messagebox.showerror("Error", "Fill all fields correctly.")
    
    def delete_student(self):
        if not self.selected_id:
            messagebox.showerror("Error", "Select a student first.")
            return
        if messagebox.askyesno("Confirm", "Delete selected student?"):
            if delete_student(self.selected_id):
                messagebox.showinfo("Success", "Student deleted.")
                self.clear_entries()
                self.view_all()
    
    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
        self.selected_id = None

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentDatabaseApp(root)
    root.mainloop()

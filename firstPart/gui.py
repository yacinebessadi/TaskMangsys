import tkinter as tk
from tkinter import ttk, messagebox
from customtkinter import CTk, CTkButton, CTkLabel, CTkEntry, CTkOptionMenu, CTkToplevel, CTkFrame, CTkScrollableFrame, set_appearance_mode, set_default_color_theme
from tasks import TasksList, Data, TaskDeleted

class TaskGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management System")
        self.root.geometry("900x500")
        self.root.minsize(800, 400)
        self.my_tasks = TasksList()

        # Set default theme and appearance
        set_appearance_mode("Light")  # Default to Light mode
        set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"
        self.current_mode = "Light"  # Track the current mode

        # Configure grid for responsiveness
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Main Frame
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.grid(sticky="nsew")

        # Title Section
        self.title_label = CTkLabel(
            self.main_frame,
            text="Task Management System",
            font=("Helvetica", 24, "bold"),
            text_color="#ffffff",
            fg_color="#0078d4",
            corner_radius=8,
            width=600,
            height=50,
        )
        self.title_label.grid(row=0, column=0, columnspan=5, pady=10)

        # Info Section
        self.info_label = ttk.Label(
            self.main_frame,
            text=(
                "You can add, delete, update, and search tasks using this system.\n"
                "Each task has a unique ID, description, priority, and status."
            ),
            font=("Arial", 10),
            background="#e8f4fc",
            foreground="#333333",
            anchor="center",
        )
        self.info_label.grid(row=1, column=0, columnspan=5, pady=10, sticky="ew")

        # Buttons Section
        self.setup_buttons()

        # Theme Toggle Button
        self.theme_button = CTkButton(
            self.main_frame,
            text="Toggle Theme",
            command=self.toggle_theme,
            width=150,
        )
        self.theme_button.grid(row=3, column=2, pady=20)

    def setup_buttons(self):
        """Create and style buttons."""
        button_style = {"width": 150, "height": 40, "corner_radius": 8}

        self.add_task_button = CTkButton(
            self.main_frame, text="Add a Task", command=self.add_task, **button_style
        )
        self.delete_task_button = CTkButton(
            self.main_frame, text="Delete a Task", command=self.open_delete_window, **button_style
        )
        self.display_tasks_button = CTkButton(
            self.main_frame, text="Display Tasks", command=self.open_display_window, **button_style
        )
        self.search_task_button = CTkButton(
            self.main_frame, text="Search by Priority", command=self.search_by_priority, **button_style
        )
        self.update_task_button = CTkButton(
            self.main_frame, text="Update Status", command=self.update_task_status, **button_style
        )

        # Place buttons in a grid
        self.add_task_button.grid(row=2, column=0, padx=10, pady=10)
        self.delete_task_button.grid(row=2, column=1, padx=10, pady=10)
        self.display_tasks_button.grid(row=2, column=2, padx=10, pady=10)
        self.search_task_button.grid(row=2, column=3, padx=10, pady=10)
        self.update_task_button.grid(row=2, column=4, padx=10, pady=10)

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        if self.current_mode == "Light":
            set_appearance_mode("Dark")
            self.current_mode = "Dark"
        else:
            set_appearance_mode("Light")
            self.current_mode = "Light"

    def add_task(self):
        """Open a window to add a new task."""
        add_task_window = CTkToplevel(self.root)
        add_task_window.title("Add New Task")
        add_task_window.geometry("400x300")
        add_task_window.grab_set()

        # Bring the window to the front
        add_task_window.lift()
        add_task_window.focus_force()

        # Task ID
        CTkLabel(add_task_window, text="Task ID:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.id_entry = CTkEntry(add_task_window, width=200)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Description
        CTkLabel(add_task_window, text="Description:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.desc_entry = CTkEntry(add_task_window, width=200)
        self.desc_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Priority
        CTkLabel(add_task_window, text="Priority:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.priority_var = tk.StringVar(value="1")
        self.priority_menu = CTkOptionMenu(
            add_task_window, variable=self.priority_var, values=["1", "2", "3", "4", "5"]
        )
        self.priority_menu.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Status
        CTkLabel(add_task_window, text="Status:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.status_var = tk.StringVar(value="Pending")
        self.status_menu = CTkOptionMenu(
            add_task_window, variable=self.status_var, values=["Pending", "In Progress", "Completed"]
        )
        self.status_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Submit Button
        submit_button = CTkButton(
            add_task_window, text="Submit", command=self.get_task, width=150
        )
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def get_task(self):
        """Retrieve task details and add to the task list."""
        try:
            task_id = int(self.id_entry.get())
            if self.my_tasks.IsDuplicateID(task_id):
                messagebox.showerror("Error", "Task ID already exists. Please use a unique ID.")
                return
            description = self.desc_entry.get().strip()
            priority = int(self.priority_var.get())
            
            # Map status strings to integers
            status_mapping = {
                "Pending": 1,
                "In Progress": 2,
                "Completed": 3
            }
            status = status_mapping[self.status_var.get()]

            task_data = Data(task_id, description, priority, status)
            self.my_tasks.AddTask(task_data)
            messagebox.showinfo("Success", f"Task with ID {task_id} added successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def open_delete_window(self):
        """Open a window to delete a task."""
        delete_task_window = CTkToplevel(self.root)
        delete_task_window.title("Delete Task")
        delete_task_window.geometry("400x200")

        # Bring the window to the front and make it modal
        delete_task_window.lift()
        delete_task_window.focus_force()
        delete_task_window.grab_set()

        # Task ID
        CTkLabel(delete_task_window, text="Task ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.delete_id_entry = CTkEntry(delete_task_window, width=200)
        self.delete_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Delete Button
        delete_button = CTkButton(
            delete_task_window,
            text="Delete",
            command=self.get_delete_id,
            width=150
        )
        delete_button.grid(row=1, column=0, columnspan=2, pady=10)

    def get_delete_id(self):
        """Retrieve the task ID and delete the task."""
        try:
            task_id = self.delete_id_entry.get().strip()
            if not task_id:
                messagebox.showerror("Error", "Task ID cannot be empty.")
                return
            if not task_id.isdigit():
                messagebox.showerror("Error", "Task ID must be a valid integer.")
                return
            task_id = int(task_id)

            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Task ID {task_id}?")
            if not confirm:
                return

            self.my_tasks.DeleteTask(task_id)
            messagebox.showinfo("Success", f"Task with ID {task_id} deleted successfully!")
        except TaskDeleted as e:
            messagebox.showinfo("Success", str(e))
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            
    def open_display_window(self):
        """Open a window to display all tasks."""
        display_window = CTkToplevel(self.root)
        display_window.title("All Tasks")
        display_window.geometry("650x400")

        # Bring the window to the front and make it modal
        display_window.lift()
        display_window.focus_force()
        display_window.grab_set()

        # Create a frame with scrollbar
        display_frame = CTkFrame(display_window)
        display_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Create Treeview
        tree = ttk.Treeview(display_frame, columns=("ID", "Description", "Priority", "Status"), show="headings")
        
        # Configure columns
        tree.heading("ID", text="ID")
        tree.heading("Description", text="Description")
        tree.heading("Priority", text="Priority")
        tree.heading("Status", text="Status")
        
        tree.column("ID", width=50)
        tree.column("Description", width=300)
        tree.column("Priority", width=80)
        tree.column("Status", width=120)
        
        # Create vertical scrollbar
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Clear any existing items
        tree.delete(*tree.get_children())
        
        # Populate tree with tasks
        tasks = []
        cur_task = self.my_tasks.head
        
        if cur_task is None:
            messagebox.showinfo("Info", "No tasks found.")
            return
        
        # Map status integers to strings for display
        status_mapping = {
            1: "Pending",
            2: "In Progress",
            3: "Completed"
        }
        
        while cur_task:
            status_text = status_mapping.get(cur_task.data.status, "Unknown")
            tasks.append((cur_task.data.id, cur_task.data.description, cur_task.data.priority, status_text))
            cur_task = cur_task.next
        
        for task in tasks:
            tree.insert("", "end", values=task)

    def search_by_priority(self):
        """Open a window to search tasks by priority."""
        search_window = CTkToplevel(self.root)
        search_window.title("Search by Priority")
        search_window.geometry("400x400")

        # Bring the window to the front and make it modal
        search_window.lift()
        search_window.focus_force()
        search_window.grab_set()

        # Priority selection
        CTkLabel(search_window, text="Select Priority:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.search_priority_var = tk.StringVar(value="1")
        priority_menu = CTkOptionMenu(
            search_window, variable=self.search_priority_var, values=["1", "2", "3", "4", "5"]
        )
        priority_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Search button
        search_button = CTkButton(
            search_window, 
            text="Search", 
            command=lambda: self.perform_search(search_window), 
            width=150
        )
        search_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Results frame (will be populated after search)
        self.results_frame = CTkFrame(search_window)
        self.results_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        search_window.grid_rowconfigure(2, weight=1)
        search_window.grid_columnconfigure(0, weight=1)
    
    def perform_search(self, parent_window):
        """Search for tasks with the selected priority."""
        try:
            priority = int(self.search_priority_var.get())
            
            # Clear the results frame
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            
            # Create treeview for results
            result_tree = ttk.Treeview(self.results_frame, columns=("ID", "Description", "Priority", "Status"), show="headings")
            
            result_tree.heading("ID", text="ID")
            result_tree.heading("Description", text="Description")
            result_tree.heading("Priority", text="Priority")
            result_tree.heading("Status", text="Status")
            
            result_tree.column("ID", width=50)
            result_tree.column("Description", width=200)
            result_tree.column("Priority", width=60)
            result_tree.column("Status", width=100)
            
            result_tree.pack(fill="both", expand=True)
            
            # Search for tasks with the selected priority
            matching_tasks = self.my_tasks.SearchByPriority(priority)
            
            if not matching_tasks:
                messagebox.showinfo("Search Result", f"No tasks found with priority {priority}.")
                return
            
            # Map status integers to strings for display
            status_mapping = {
                1: "Pending",
                2: "In Progress",
                3: "Completed"
            }
            
            # Populate tree with matching tasks
            for task in matching_tasks:
                status_text = status_mapping.get(task.status, "Unknown")
                result_tree.insert("", "end", values=(task.id, task.description, task.priority, status_text))
                
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    
    def update_task_status(self):
        """Open a window to update task status."""
        update_window = CTkToplevel(self.root)
        update_window.title("Update Task Status")
        update_window.geometry("450x200")

        # Bring the window to the front and make it modal
        update_window.lift()
        update_window.focus_force()
        update_window.grab_set()

        # Task ID
        CTkLabel(update_window, text="Task ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.update_id_entry = CTkEntry(update_window, width=150)
        self.update_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # New Status
        CTkLabel(update_window, text="New Status:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.update_status_var = tk.StringVar(value="Pending")
        status_menu = CTkOptionMenu(
            update_window, 
            variable=self.update_status_var, 
            values=["Pending", "In Progress", "Completed"]
        )
        status_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Update button
        update_button = CTkButton(
            update_window,
            text="Update",
            command=self.perform_update,
            width=150
        )
        update_button.grid(row=2, column=0, columnspan=2, pady=10)
    
    def perform_update(self):
        """Update the status of a task."""
        try:
            task_id = self.update_id_entry.get().strip()
            if not task_id:
                messagebox.showerror("Error", "Task ID cannot be empty.")
                return
            if not task_id.isdigit():
                messagebox.showerror("Error", "Task ID must be a valid integer.")
                return
            task_id = int(task_id)
            
            # Map status strings to integers
            status_mapping = {
                "Pending": 1,
                "In Progress": 2,
                "Completed": 3
            }
            status = status_mapping[self.update_status_var.get()]
            
            # Check if the task exists
            if not self.my_tasks.IsDuplicateID(task_id):
                messagebox.showerror("Error", f"No task found with ID {task_id}.")
                return
                
            # Update the task status
            self.my_tasks.UpdateStatus(task_id, status)
            messagebox.showinfo("Success", f"Task with ID {task_id} updated successfully!")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    root = CTk()
    gui = TaskGUI(root)
    root.mainloop()
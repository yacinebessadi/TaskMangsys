from tkinter import *
from tkinter import ttk
from tkinter import messagebox, StringVar, OptionMenu
from tasks import TasksList, Data,TaskDeleted 

class taskGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management System")
        self.root.geometry("900x500") 
        self.root.config(bg="#f5f5f5")
        self.setup_ui()
        self.my_tasks = TasksList()

        # Title Section
        title = Label(self.root,text="Task Management System",font=("Helvetica", 20, "bold"),fg="#ffffff",bg="#0078d4",width=40,height=2,
        )
        title.grid(row=0, column=0, columnspan=5, pady=10)

        # Info Section
        paragraph = """You can add, delete, update, and search tasks using this system.Each task has a unique ID, description, priority, and status."""
        text_widget = Text(self.root,wrap=WORD,height=4,width=120,bd=0,bg="#e8f4fc",fg="#333333",font=("Arial", 10))
        text_widget.insert(END, paragraph)
        text_widget.config(state=DISABLED)  #  read-only
        text_widget.grid(row=1, column=0, columnspan=5, pady=10, padx=10, sticky=W)

    def setup_ui(self):
        # Configure the columns for equal weight
        for col in range(5):
            self.root.grid_columnconfigure(col, weight=1)

        # Button Styling
        button_style = {"width": 15, "height": 2, "font": ("Arial", 10), "bg": "#0078d4", "fg": "#ffffff"}

        # Create buttons
        self.add_task_button = Button(self.root, text="Add a Task", **button_style, command=self.add_task)
        self.open_delete_window_button = Button(self.root, text="Delete A Task", **button_style, command=self.open_delete_window)
        self.display_tasks_button = Button(self.root, text="Display Tasks", **button_style, command=self.open_display_window)
        self.search_by_priority_button = Button(self.root, text="Search by Priority", **button_style, command=self.search_by_priority)
        self.update_stat_btn = Button(self.root, text="Update Status", **button_style, command=self.update_task_status)

        # Place buttons in the grid with consistent spacing
        self.add_task_button.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")
        self.open_delete_window_button.grid(row=2, column=1, pady=10, padx=10, sticky="nsew")
        self.display_tasks_button.grid(row=2, column=2, pady=10, padx=10, sticky="nsew")
        self.search_by_priority_button.grid(row=2, column=3, pady=10, padx=10, sticky="nsew")
        self.update_stat_btn.grid(row=2, column=4, pady=10, padx=10, sticky="nsew")

    def add_task(self):
        add_task_window = Toplevel(self.root)
        add_task_window.title("Add New Task")
        add_task_window.geometry("400x300")
        add_task_window.config(bg="#f9f9f9")  

        Label(add_task_window, text="Task ID:", font=("Arial", 10), bg="#f9f9f9").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.id_entry = Entry(add_task_window, width=30)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        Label(add_task_window, text="Description:", font=("Arial", 10), bg="#f9f9f9").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.desc_entry = Text(add_task_window, width=30, height=4)
        self.desc_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(add_task_window, text="Priority:", font=("Arial", 10), bg="#f9f9f9").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.priority_var = StringVar(value="1")
        OptionMenu(add_task_window, self.priority_var, *["1", "2", "3", "4", "5"]).grid(row=2, column=1, padx=10, pady=5, sticky="w")

        Label(add_task_window, text="Status:", font=("Arial", 10), bg="#f9f9f9").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.status_var = StringVar(value="Pending")
        OptionMenu(add_task_window, self.status_var, *["Pending", "In Progress", "Completed"]).grid(row=3, column=1, padx=10, pady=5, sticky="w")

        submit_button = Button(
            add_task_window,
            text="Submit",
            font=("Arial", 10, "bold"),
            bg="#0078d4",
            fg="#ffffff",
            command=self.get_task,
        )
        submit_button.grid(row=4, column=0, columnspan=2, pady=10)
    def get_task(self):
        try:
            id=int(self.id_entry.get())
            if self.my_tasks.IsDuplicateID(id):
                messagebox.showerror("Error","Task ID already exists. Please Enter an ID that you \n Haven't Used Before")
                return
            description=self.desc_entry.get("1.0",END).strip()#get the descp and remove any white spaces by strip()
            #Priority
            prio = int(self.priority_var.get())
            #status 
            status = self.status_var.get()
            
            tasks_data=Data(id,description,prio,status)
            self.my_tasks.AddTask(tasks_data)
            messagebox.showinfo("Success", f"Task with id {id} added successfully!")
            self.clear_ui()
            self.setup_ui()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def clear_ui(self):
        self.id_entry.delete(0, END)
        self.desc_entry.delete("1.0", END)
        self.priority_var.set("1")
        self.status_var.set("Pending")
    
    def open_delete_window(self):
        DeleteTask = Toplevel(self.root)
        DeleteTask.title("Delete Task")
        delete = Label(DeleteTask, text="Enter Task ID to Delete:")
        delete.grid(row=0, column=0, pady=10)
        self.delete_id = Entry(DeleteTask, width=30)
        self.delete_id.grid(row=0, column=1, pady=10)
        delete_button = Button(DeleteTask, text="Delete", command=self.GetDeleteId)
        delete_button.grid(row=0, column=2, pady=10)
    
    def GetDeleteId(self):
        try:
            id = int(self.delete_id.get())
            self.my_tasks.DeleteTask(id)
        except TaskDeleted as e:
            messagebox.showinfo("Success", str(e))
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    

    def open_display_window(self):
        DisplayTask = Toplevel(self.root)
        DisplayTask.title("Display Tasks")
        tree = ttk.Treeview(DisplayTask, columns=("ID", "Description", "Priority", "Status"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Description", text="Description")
        tree.heading("Priority", text="Priority")
        tree.heading("Status", text="Status")
        tree.column("ID", width=50)
        tree.column("Description", width=200)
        tree.column("Priority", width=100)
        tree.column("Status", width=100)
        tree.pack(fill=BOTH, expand=True)

        tree.delete(*tree.get_children())
        tasks = []
        cur_task = self.my_tasks.head
        if cur_task is None:
            messagebox.showinfo("Info", "Task List is Empty")
            return
        
        while cur_task:
            tasks.append(cur_task.data)
            cur_task = cur_task.next
        
        for task in tasks:
            tree.insert("", "end", values=(task.id, task.description, task.priority, task.status))


    def search_by_priority(self):
        self.SearchWindow=Toplevel(self.root)
        self.SearchWindow.title("Tasks By Priority")
        self.SearchWindow.geometry("300x200")
        search_label = Label(self.SearchWindow, text="Select Priority to Search:")
        search_label.grid(row=1,column=0) 

        self.priority_var = StringVar(self.SearchWindow)
        self.priority_var.set("1")
        options = ["1", "2", "3", "4", "5"]
        self.priority_menu = OptionMenu(self.SearchWindow, self.priority_var, *options)
        self.priority_menu.grid(row=1,column=2)


        search_button=Button(self.SearchWindow,text="Search",width=25,command=self.perform_search)
        search_button.grid(row=2,columnspan=3)

    def perform_search(self):
     try:
        priority=int(self.priority_var.get())
        tasks=self.my_tasks.SearchByPriority(priority)
        tree = ttk.Treeview(self.SearchWindow, columns=("ID", "Description", "Priority", "Status"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Description", text="Description")
        tree.heading("Priority", text="Priority")
        tree.heading("Status", text="Status")
        tree.column("ID", width=50)
        tree.column("Description", width=200)
        tree.column("Priority", width=100)
        tree.column("Status", width=100)
        tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")


        tree.delete(*tree.get_children())
        for task in tasks:
            tree.insert("", "end", values=(task.id, task.description, task.priority, task.status))

     except ValueError as e:
        messagebox.showinfo("Search Result", str(e))
     except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    
    def update_task_status(self):
        update_stat_window=Toplevel(self.root)
        update_stat_window.title("Update Task Status")
        update_stat_window.geometry("400x400")


        update_label=Label(update_stat_window,text="Please Enter The Id")
        update_label.grid(row=1,column=0)

        self.update_id_entry=Entry(update_stat_window,width=30)
        self.update_id_entry.grid(row=1,column=1)

        self.updated_status_var = StringVar(value="Pending")
        OptionMenu(update_stat_window, self.updated_status_var, *["Pending", "In Progress", "Completed"]).grid(row=1, column=2)
        
        update_button = Button(update_stat_window, text="Update", command=self.perform_update,width=30)
        update_button.grid(row=2, columnspan=2, pady=10)

        
    
    def perform_update(self):
        try:
            task_id = self.update_id_entry.get()
            if not task_id.isdigit():
              raise ValueError("Task ID must be a valid integer.")
            task_id = int(task_id) 
            status=self.updated_status_var.get()

            #check if the id exists (i use IsDuplicateId if yes that mean it exsists) 

            if self.my_tasks.IsDuplicateID(task_id):
                status_mapping ={
                        "Pending": 1,
                        "In Progress": 2,
                        "Completed": 3
                           }
                status=status_mapping[status]
                self.my_tasks.UpdateStatus(task_id,status)
                messagebox.showinfo("Success", f"Task with ID {task_id} updated successfully!")
            else:
                messagebox.showwarning("Id","Id Does Not Exist")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")



 
if __name__ == "__main__":
    root = Tk()
    gui = taskGUI(root)
    root.mainloop() 

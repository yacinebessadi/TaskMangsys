class Data:
    def __init__(self, id, description, priority, status):
        self.id = id
        self.description = description
        self.priority = priority
        self.status = status 
        self.next = None

class Task:
    def __init__(self, data):
        self.data = data
        self.next = None

class TaskDeleted(Exception):
      def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class TasksList:
    def __init__(self):
        self.head = None
  

    def AddTask(self, data):
        new_task = Task(data)
        if not self.head:
            self.head = new_task
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_task
        self.SortTasks()
    def SortTasks(self):
        if not self.head or not self.head.next:#i am checking here if the list have one task only
            return
        cur_task=self.head
        tasks=[]
        while cur_task:
            tasks.append(cur_task.data)
            cur_task=cur_task.next
        tasks.sort(key=lambda task: task.priority)
        cur_task=self.head
        for task in tasks:
            cur_task.data=task
            cur_task=cur_task.next

    def DisplayTasks(self):
        tasks = []
        cur_task = self.head
        if cur_task is None :
            print("List Task is Empty")
            return
        while cur_task:
            tasks.append(cur_task.data)
            cur_task = cur_task.next
        for task in tasks:
            print(f"ID: {task.id}, Description: {task.description}, Priority: {task.priority}, Status: {task.status}")

    def ValidPrio(self, priority):
      if priority < 1 or priority > 5:
        raise ValueError("Priority must be between 1 and 5")
      return priority

    def CheckStatus(self, status):
        if status not in [1, 2, 3]:
            raise ValueError("Status must be 1 (Pending), 2 (In Progress), or 3 (Completed)")
        return status

    def TaskStatus(self, status):
        status_mapping = {
            1: 'Pending',
            2: 'In Progress',
            3: 'Completed'
        }
        status = self.CheckStatus(status)  # Ensures valid input
        return status_mapping[status]   # Directly return the value
    
    def DeleteTask(self, id):
        cur_task = self.head
        prev_task = None
        while cur_task:
          if cur_task.data.id == id:
            if prev_task is None:
               self.head = cur_task.next
            else:
             prev_task.next = cur_task.next
            raise TaskDeleted(f"Task with Id {id} Deleted")
          prev_task = cur_task
          cur_task = cur_task.next
        raise ValueError(f"Task with ID {id} not found.")
        
    def UpdateStatus(self,id,status):
        cur_task=self.head
        while cur_task:
            if cur_task.data.id==id:
               
               cur_task.data.status=self.TaskStatus(status)
               print(f"Task with ID {id} status updated to {cur_task.data.status}")
               return
            cur_task=cur_task.next
        raise ValueError(f"Task with ID {id} not found.")
    
    def SearchByPriority(self, priority):
        cur_task = self.head
        tasks = []
        while cur_task:
            if cur_task.data.priority == priority:
                tasks.append(cur_task.data)
            cur_task = cur_task.next
        if not tasks:
            raise ValueError(f"No tasks found with priority {priority}")
        return tasks

    def IsDuplicateID(self, id):
      cur_task = self.head
      while cur_task:
        if cur_task.data.id == id:
            return True
        cur_task = cur_task.next
      return False
def get_unique_id(tasks_list):
    id = int(input("Please Enter the task ID: "))
    if tasks_list.IsDuplicateID(id):
        print("Task ID already exists. Please enter a unique ID.")
        return get_unique_id(tasks_list)
    return id
    
              
        



def main():
    my_tasks = TasksList()
  
    print("Task Management System")
    print("Enter 1 for Add a Task")
    print("Enter 2 for displaying Tasks")
    print("Enter 3 for deleting a Task")
    print("Enter 4 for updating a Task status")
    print("Enter 5 to Search By Priority")
    print("Enter 0 for exit")
    while True:
      try:
       choice=int(input("Your choice: "))
       if choice==1:
            while True:
                id=get_unique_id(my_tasks)                          
                description = input("Please Enter the task description: ")
                priority = int(input("Please enter a priority between 1 and 5: "))
                priority = my_tasks.ValidPrio(priority)
                status = int(input("1 for Pending- 2 for In Progress- 3 for Completed: "))
                status = my_tasks.TaskStatus(status)
                task_data = Data(id, description, priority, status)
                my_tasks.AddTask(task_data)
                continue_adding = input("Do you want to add another task? (yes/no): ")
                if continue_adding.lower() != "yes":
                    break
            print("All tasks have been added.")

       elif choice==2:
            my_tasks.DisplayTasks()
       elif choice==3:
            print("Please Enter Task Id you want to delete")
            id=int(input())
            my_tasks.DeleteTask(id)
       elif choice == 4:
            id = int(input("Enter the task ID to update status: "))
            print("Enter the new Status \
                    1 for Pending- 2 for In Progress- 3 for Completed: ")
            status=int(input())

            my_tasks.UpdateStatus(id,status)
       elif choice==5:
            priority=int(input("Enter the priority to search for: "))
            priority = my_tasks.ValidPrio(priority)
            my_tasks.SearchByPriority(priority)
       elif choice==0:
            break
      except ValueError:
       print("Please enter a valid number.")
       continue

if __name__ == "__main__":
    main()
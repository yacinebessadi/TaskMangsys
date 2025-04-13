#include "TASK.h"
#include "TASK.h"

void sortTaskPriority(Task** head) {
    if (*head == NULL || (*head)->next == NULL) {
        // No need to sort if the list is empty or has only one task
        return;
    }

    Task *current = *head;
    Task *maxNode;
    Task temp;

    while (current != NULL) {
        maxNode = current; // Assume current node has the highest priority

        Task *runner = current->next;
        while (runner != NULL) {
            if (runner->priority > maxNode->priority) {
                maxNode = runner; // Update maxNode if a higher priority is found
            }
            runner = runner->next;
        }

        // Swap data between current and maxNode
        if (maxNode != current) {
            // Swap the data fields
            temp.id = current->id;
            strcpy(temp.description, current->description);
            temp.priority = current->priority;
            strcpy(temp.status, current->status);

            current->id = maxNode->id;
            strcpy(current->description, maxNode->description);
            current->priority = maxNode->priority;
            strcpy(current->status, maxNode->status);

            maxNode->id = temp.id;
            strcpy(maxNode->description, temp.description);
            maxNode->priority = temp.priority;
            strcpy(maxNode->status, temp.status);
        }

        current = current->next; // Move to the next node
    }
}


void insertTask(Task** head) {
    Task* P = (Task*)malloc(sizeof(Task));
    if (P == NULL) {
        printf("Memory allocation failed!\n");
        return;
    }

    printf("Enter Task ID: ");
    scanf("%d", &P->id);
    getchar(); // Consume the newline character left by scanf

    printf("Enter Task Description: \n");
    fgets(P->description, MAX, stdin);
    //removing /n from the string to not leading to undefined behaivor 

    size_t len = strlen(P->description);
    if (len > 0 && P->description[len - 1] == '\n') {
        P->description[len - 1] = '\0';
    }

    printf("Enter Task Priority (1 to 5): \n");
    do{
        scanf("%d", &P->priority);
    } while (P->priority < 1 || P->priority > 5);
    getchar();

    printf("Enter Task Status (1)Pending, 2) In Progress, 3) Completed): ");
    int sta;
    do
    {
    scanf("%d",&sta);
    } while (!(sta==1 || sta==2 || sta==3));
    
    
    getchar();
    switch (sta)
    {
    case 1:
        strcpy(P->status,"Pending");
    
        break;
    case 2:
        strcpy(P->status,"In Progress");
        break;
    case 3:
        strcpy(P->status,"Completed");
        break;

    default:
    printf("Enter a valid choice please");
        break;
    }
    /*
    fgets(P->status, 20, stdin);
    len = strlen(P->status);
    if (len > 0 && P->status[len - 1] == '\n') 
    {
      P->status[len - 1] = '\0';
    }*/

    // Link the new node to the head of the list
    P->next = *head;
    *head = P;
    FILE* file = fopen("tasks.txt", "a"); // Open in append mode
    if (file == NULL) {
        printf("Error opening file for writing!\n");
        return;
    }
    fprintf(file, "%d;%s;%d;%s\n", P->id, P->description, P->priority, P->status);
    fclose(file);


    printf("Task added successfully!\n");
}


//Still waiting for the sorting of the prority


void deleteTask(Task** head, int num)
{
    if (*head == NULL)
    {   printf("List is empty.\n");
        return;
    }
Task*P=*head;
    if (P->id==num)//case where we delete the first task in the list
    {
        *head=P->next;
        free(*head);
       // P=(*head)->next;
        //free(*head);
        //*head=P;
        printf("Task with ID %d deleted successfully.\n", num);
        return;
    }
    Task *Q=NULL;
    while (P!=NULL &P->id!=num)
    {
        Q=P;
        P=P->next;
    }
    if (P==NULL)
    {
       printf("No Task with ID of %d \n",num);
       return;
    }

    Q->next=P->next;
    free(P);
    printf("Task with ID %d deleted successfully.\n", num);


}


void updateTaskStatus(Task** head, int id)
{
    if (*head == NULL)
    {   printf("List is empty.\n");
        return;
    }
    Task*P=*head;
    printf("Enter \n1) For Pending \n2) In Progress\n3) Completed\n");
    int change;
    scanf("%d",&change);
    while (P!=NULL & P->id!=id)
    {
        P=P->next;
    }
    if (P==NULL)//the task with the "ID" not found
    {
     printf("Id Not found");
    }
    //Now we update P status
    switch (change)
    {
    case 1:
        strcpy(P->status, "Pending");
        break;
    case 2:
        strcpy(P->status,"In Progress");
    break;
    case 3: 
        strcpy(P->status,"Completed");
    default:
    printf("You did not enter a valid choice");
        break;
    }
}


void loadTasksFromFile(Task** head) {
    FILE* file = fopen("tasks.txt", "r");
    if (file == NULL) {
        printf("No task file found. Starting with an empty list.\n");
        return;
    }

    char buffer[MAX];
    while (fgets(buffer, MAX, file)) {
        Task* newTask = (Task*)malloc(sizeof(Task));
        if (newTask == NULL) {
            printf("Memory allocation failed!\n");
            fclose(file);
            return;
        }

        // Parse the line from the file
        sscanf(buffer, "%d;%[^;];%d;%[^\n]", &newTask->id, newTask->description, &newTask->priority, newTask->status);

        // Add to the front of the linked list
        newTask->next = *head;
        *head = newTask;
    }

    fclose(file);
    printf("Tasks loaded successfully from file.\n");
}

void display(Task* head) {
     loadTasksFromFile(&head);
    Task* runner = head;
    int i = 1;

    // Display tasks with status "Pending"
    printf("\nPending Tasks:\n");
    while (runner != NULL) {
        if (strcmp(runner->status, "Pending") == 0) {
            printf("     Task %d\n", i);
            printf("ID: %d\n", runner->id);
            printf("Description: %s\n", runner->description);
            printf("Priority: %d\n", runner->priority);
            printf("Status: %s\n", runner->status);
            puts("----------------------");
            i++;
        }
        runner = runner->next;
    }
    
    // Display tasks with status "In Progress"
    printf("\nIn Progress Tasks:\n");
    runner = head;
    i = 1;
    while (runner != NULL) {
        if (strcmp(runner->status, "In Progress") == 0) {
            printf("     Task %d\n", i);
            printf("ID: %d\n", runner->id);
            printf("Description: %s\n", runner->description);
            printf("Priority: %d\n", runner->priority);
            printf("Status: %s\n", runner->status);
            puts("----------------------");
            i++;
        }
        runner = runner->next;
    }
    // Display tasks with status "Completed"
    printf("\nCompleted Tasks:\n");
    runner = head;
    i = 1;
    while (runner != NULL) {
        if (strcmp(runner->status, "Completed") == 0) {
            printf("     Task %d\n", i);
            printf("ID: %d\n", runner->id);
            printf("Description: %s\n", runner->description);
            printf("Priority: %d\n", runner->priority);
            printf("Status: %s\n", runner->status);
            puts("----------------------");
            i++;
        }
        runner = runner->next;
    }
}


void searchByPriority(Task* head, int priority)
{
    Task *runner =head;
    if (runner == NULL) 
    {   printf("Task list is empty.\n");
        printf("_____________________________________");
        return;
    }
    int i=1;
while (runner!=NULL)
{
   
    if (runner->priority==priority)
    {
        printf("Task %d \n--------",i);
        printf("ID: %d\n", runner->id);
        printf("Description: %s\n", runner->description);
        printf("Priority: %d\n", runner->priority);
        printf("Status: %s\n", runner->status);
        puts("----------------------");
        i+=1;   
    }
  runner=runner->next;
Sleep(500);
}

}

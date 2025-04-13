#include "TASK.h"
#include <stdbool.h>

int main(){
    Task* taskList = NULL; 
    int choice=0;

    printf("This Is A Simple Task Management System\n");
    printf("_____________________________________");
    // when the user press 6 it will exit 
    while(choice!=6)
    {
        printf("\nTask Menu:\n");
        printf("1: Add A Task\n");
        printf("2: Delete A Task\n");
        printf("3: Update Status\n");
        printf("4: Display Tasks\n");
        printf("5: Search by Priority\n");
        printf("6: Exit\n");
        printf("_____________________________________");
        printf("Enter your choice: ");
        scanf("%d", &choice);//reading the choice of the user 
        switch (choice)
        {
            case 1: // entered a 1 so Add a task 
                   while (choice==1)//add task loop
                   {
                        insertTask(&taskList); 
                        printf("Do you want to add another task? Enter 1 for Yes, 6 for No: ");
                         /*  //asking the user if they want to add another one  if the user pressed 1 we will add a new one if the user pressed 6 then we will exit the add task loop then but i will give him another try to pick again whatver delete or display or any other features regardless if they press 6 again we will exit all of the program  */                                             
                        scanf("%d", &choice);
                        //getchar();
                   }
                   sortTaskPriority(&taskList);

                choice=0;//reset is as a default so it wont exsit the main loop when the user choose to not insert new task
                break;// this will allow to do other things as i mentioned 

            case 2: // Delete a task
                  printf("Enter the task you want to delete by ID\n");
                  int id;
                  scanf("%d",&id);
                  deleteTask(&taskList,id);
                break;

            case 3: // Update status
                 printf("Updating status of a task \n! Please Eneter the Id of the task you want to Update:  ");
                 scanf("%d",&id);
                 updateTaskStatus(&taskList,id);

                break;

            case 4: // Display tasks
                display(taskList);
                break;

            case 5: // Search by priority
                  printf("Enter the priority number (1 to 5) to search for tasks: ");
                  int prio;
                  scanf("%d",&prio);
                  searchByPriority(taskList,prio);

                break;
                
            case 6: // Exit
                printf("Exiting program. Goodbye!\n");
                return 0;

            default: // Invalid choice
                printf("Invalid choice! Please select a valid option.\n");
        }
    }
    

    return 0;
}

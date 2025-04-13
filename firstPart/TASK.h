#ifndef TASK_H
#define TASK_H
#include <stdio.h>
#include <stdlib.h>
#include<stdbool.h>
#include <string.h>
#include <windows.h>

#define MAX 100
// Structure for a task
typedef struct Task {
    
    int id;             // Unique identifier
    char description[MAX]; // Task description
    int priority;       // Priority (1 to 5)
    char status[20];    // Status ("Pending", "In Progress", "Completed")
    struct Task* next;  // Pointer to the next task in the list
} Task;

// Function declarations
void insertTask(Task** head);
void display(Task* head);
void deleteTask(Task** head, int num);
void updateTaskStatus(Task** head, int id);
void searchByPriority(Task* head, int priority);
void sortTaskPriority(Task**head);
#endif // TASK_H

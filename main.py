import argparse
import sys
import os
import json

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_task(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

parser = argparse.ArgumentParser()

parser.add_argument("task", type=str, nargs="?", help="Task to add")
parser.add_argument("-l", "--list", help="List all tasks", action="store_true")
parser.add_argument("-c", "--complete", type=int, help="Mark a task as complete by ID")
parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")
parser.add_argument("-v", "--version", help="Display the apps version", action="version", version="0.0.1")


args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
    

if args.list:
    tasks = load_tasks()
    if len(tasks) == 0:
        print("There are no tasks to be shown.")
        sys.exit(0)

    for task in tasks:
        status = "x" if task["done"] else " "
        print(f"[{status}] {task['id']}: {task['task']}")
    sys.exit(0)
elif args.complete:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == args.complete:
            task["done"] = True
            save_task(tasks)
            print(f"Task {args.complete} marked as complete")
            break
elif args.delete:
    tasks = load_tasks()
    newTasks = []
    for task in tasks:
        if task["id"] != args.delete:
            newTasks.append(task)   
    save_task(newTasks)
    print(f"Task {args.delete} was deleted")
elif args.task:
    tasks = load_tasks()
    if len(tasks) == 0:
        nextId = 1
    else:
        nextId = tasks[-1]["id"] + 1
    tasks.append({"id": nextId, "task": args.task, "done": False})
    save_task(tasks)

    print(f"Task {args.task} added with ID of {nextId}")
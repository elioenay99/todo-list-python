class TaskManager:
    def __init__(self, file_path='tasks.txt'):
        self.file_path = file_path
        self.tasks = self.load_tasks()

    def add_task(self, task, priority):
        self.tasks.append((task, priority, False))
        self.save_tasks()

    def edit_task(self, index, new_task, new_priority):
        self.tasks[index] = (new_task, new_priority, self.tasks[index][2])
        self.save_tasks()

    def remove_task(self, index):
        self.tasks.pop(index)
        self.save_tasks()

    def mark_task_done(self, index):
        task, priority, done = self.tasks[index]
        self.tasks[index] = (task, priority, not done)
        self.save_tasks()

    def filter_tasks(self, filter_option):
        if filter_option == "Todas":
            return self.tasks
        elif filter_option == "Pendentes":
            return [task for task in self.tasks if not task[2]]
        elif filter_option == "Concluídas":
            return [task for task in self.tasks if task[2]]

    def load_tasks(self):
        try:
            with open(self.file_path, 'r') as file:
                tasks = file.readlines()
            tasks = [tuple(task.strip().split("||")) for task in tasks]
            tasks = [(task[0], task[1], task[2] == "True") for task in tasks]
        except FileNotFoundError:
            tasks = []
        return tasks

    def save_tasks(self):
        with open(self.file_path, 'w') as file:
            for task, priority, done in self.tasks:
                file.write(f"{task}||{priority}||{done}\n")

class TaskManager:
    def __init__(self, file_path='tasks.txt'):
        self.file_path = file_path
        self.tasks = self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, index):
        self.tasks.pop(index)
        self.save_tasks()

    def load_tasks(self):
        try:
            with open(self.file_path, 'r') as file:
                tasks = file.readlines()
            tasks = [task.strip() for task in tasks]
        except FileNotFoundError:
            tasks = []
        return tasks

    def save_tasks(self):
        with open(self.file_path, 'w') as file:
            for task in self.tasks:
                file.write(f"{task}\n")
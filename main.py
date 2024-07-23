import tkinter as tk
from tkinter import messagebox

from todo_manager import TaskManager


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tarefas")

        self.task_manager = TaskManager()

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.frame, width=50, height=10, selectmode=tk.SINGLE)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=10)

        self.add_button = tk.Button(root, text="Adicionar Tarefas", command=self.add_task)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(root, text="Remover Tarefas", command=self.remove_task)
        self.remove_button.pack(pady=5)

        self.load_tasks()

    def add_task(self):
        task = self.entry.get()
        if task:
            self.task_manager.add_task(task)
            self.task_listbox.insert(tk.END, task)
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Cuidado", "Você não colocou nenhuma tarefa.")

    def remove_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.task_manager.remove_task(selected_task_index)
            self.task_listbox.delete(selected_task_index)
        except IndexError:
            messagebox.showwarning("Cuidado", "Você não selecionou nenhuma tarefa para remover.")

    def load_tasks(self):
        tasks = self.task_manager.load_tasks()
        for task in tasks:
            self.task_listbox.insert(tk.END, task)


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
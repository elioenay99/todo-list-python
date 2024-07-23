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

        self.task_listbox = tk.Listbox(self.frame, width=100, height=5, selectmode=tk.SINGLE)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.priority_var = tk.StringVar(value="Média")
        self.priority_menu = tk.OptionMenu(self.button_frame, self.priority_var, "Alta", "Média", "Baixa")
        self.priority_menu.grid(row=2, column=0)

        self.add_button = tk.Button(self.button_frame, text="Adicionar Tarefas", command=self.add_task)
        self.add_button.grid(row=1, column=0)

        self.edit_button = tk.Button(self.button_frame, text="Editar Tarefas", command=self.edit_task)
        self.edit_button.grid(row=1, column=1)

        self.remove_button = tk.Button(self.button_frame, text="Remover Tarefas", command=self.remove_task)
        self.remove_button.grid(row=1, column=2)

        self.mark_done_button = tk.Button(self.button_frame, text="Marcar como Concluída", command=self.mark_task_done)
        self.mark_done_button.grid(row=2, column=1)

        self.filter_var = tk.StringVar(value="Todas")
        self.filter_menu = tk.OptionMenu(self.button_frame, self.filter_var, "Todas", "Pendentes", "Concluídas",
                                         command=self.filter_tasks)
        self.filter_menu.grid(row=2, column=2)

        self.load_tasks()

    def add_task(self):
        task = self.entry.get()
        priority = self.priority_var.get()
        if task:
            self.task_manager.add_task(task, priority)
            self.task_listbox.insert(tk.END, f"{task} [{priority}]")
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Cuidado", "Você não colocou nenhuma tarefa.")

    def edit_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            task = self.entry.get()
            priority = self.priority_var.get()
            if task:
                self.task_manager.edit_task(selected_task_index, task, priority)
                self.task_listbox.delete(selected_task_index)
                self.task_listbox.insert(selected_task_index, f"{task} [{priority}]")
                self.entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Cuidado", "Você não colocou nenhuma tarefa.")
        except IndexError:
            messagebox.showwarning("Cuidado", "Você não selecionou nenhuma tarefa para editar.")

    def remove_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.task_manager.remove_task(selected_task_index)
            self.task_listbox.delete(selected_task_index)
        except IndexError:
            messagebox.showwarning("Cuidado", "Você não selecionou nenhuma tarefa para remover.")

    def mark_task_done(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.task_manager.mark_task_done(selected_task_index)
            self.task_listbox.delete(selected_task_index)
            task, priority, done = self.task_manager.tasks[selected_task_index]
            self.task_listbox.insert(selected_task_index,
                                     f"{task} [{priority}] - Concluída" if done else f"{task} [{priority}]")
        except IndexError:
            messagebox.showwarning("Cuidado", "Você não selecionou nenhuma tarefa para marcar como concluída.")

    def filter_tasks(self, filter_option):
        self.task_listbox.delete(0, tk.END)
        tasks = self.task_manager.filter_tasks(filter_option)
        for task, priority, done in tasks:
            display_text = f"{task} [{priority}]"
            if done:
                display_text += " - Concluída"
            self.task_listbox.insert(tk.END, display_text)

    def load_tasks(self):
        tasks = self.task_manager.load_tasks()
        for task, priority, done in tasks:
            display_text = f"{task} [{priority}]"
            if done:
                display_text += " - Concluída"
            self.task_listbox.insert(tk.END, display_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

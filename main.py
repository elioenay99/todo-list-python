import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os

from todo_manager import TaskManager


def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry("+0+0")
    tooltip_label = ttk.Label(tooltip, text=text, background="yellow", relief='solid', borderwidth=1,
                              font=("Arial", 10))
    tooltip_label.pack()
    tooltip.withdraw()

    def on_enter(event):
        x = widget.winfo_rootx() + 30
        y = widget.winfo_rooty() + 30
        tooltip.wm_geometry(f"+{x}+{y}")
        tooltip.deiconify()

    def on_leave(event):
        tooltip.withdraw()

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tarefas")

        self.task_manager = TaskManager()

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("TLabel", font=("Arial", 12))

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(self.frame, width=100, height=5, selectmode=tk.SINGLE, font=("Arial", 12))
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        self.entry = ttk.Entry(root, width=50, font=("Arial", 12))
        self.entry.pack(pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.priority_var = tk.StringVar(value="Média")
        self.priority_menu = ttk.OptionMenu(self.button_frame, self.priority_var, "Média", "Alta", "Média", "Baixa")
        self.priority_menu.grid(row=2, column=0)

        self.add_button = ttk.Button(self.button_frame, text="Adicionar Tarefas", command=self.add_task)
        self.add_button.grid(row=1, column=0, padx=5, pady=5)
        create_tooltip(self.add_button, "Adicionar nova tarefa")

        self.edit_button = ttk.Button(self.button_frame, text="Editar Tarefas", command=self.edit_task)
        self.edit_button.grid(row=1, column=1, padx=5, pady=5)
        create_tooltip(self.edit_button, "Editar tarefa selecionada")

        self.remove_button = ttk.Button(self.button_frame, text="Remover Tarefas", command=self.remove_task)
        self.remove_button.grid(row=1, column=2, padx=5, pady=5)
        create_tooltip(self.remove_button, "Remover tarefa selecionada")

        self.mark_done_button = ttk.Button(self.button_frame, text="Marcar como Concluída", command=self.mark_task_done)
        self.mark_done_button.grid(row=2, column=1, padx=5, pady=5)
        create_tooltip(self.mark_done_button, "Marcar tarefa selecionada como concluída")

        self.filter_var = tk.StringVar(value="Todas")
        self.filter_menu = ttk.OptionMenu(self.button_frame, self.filter_var, "Todas", "Todas", "Pendentes",
                                          "Concluídas",
                                          command=self.filter_tasks)
        self.filter_menu.grid(row=2, column=2)

        self.load_icons()
        self.load_tasks()

    def load_icons(self):
        # Load icons for buttons
        icon_size = (20, 20)
        try:
            self.add_icon = ImageTk.PhotoImage(
                Image.open("icons/add.png").resize(icon_size, Image.Resampling.LANCZOS))
            self.edit_icon = ImageTk.PhotoImage(
                Image.open("icons/edit.png").resize(icon_size, Image.Resampling.LANCZOS))
            self.remove_icon = ImageTk.PhotoImage(
                Image.open("icons/remove.png").resize(icon_size, Image.Resampling.LANCZOS))
            self.done_icon = ImageTk.PhotoImage(
                Image.open("icons/done.png").resize(icon_size, Image.Resampling.LANCZOS))

            self.add_button.config(image=self.add_icon, compound=tk.LEFT)
            self.edit_button.config(image=self.edit_icon, compound=tk.LEFT)
            self.remove_button.config(image=self.remove_icon, compound=tk.LEFT)
            self.mark_done_button.config(image=self.done_icon, compound=tk.LEFT)
        except Exception as e:
            messagebox.showerror("Erro ao carregar ícones", str(e))

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

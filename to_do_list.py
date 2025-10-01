# todo_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
from typing import List, Dict, Any

class TodoAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List Manager")
        self.root.geometry("800x600")
        self.filename = "todos_gui.json"
        self.todos = self.load_todos()
        
        self.setup_ui()
        self.refresh_list()
    
    def load_todos(self) -> List[Dict[str, Any]]:
        """Load todos from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_todos(self):
        """Save todos to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.todos, f, indent=2)
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎯 Todo List Manager", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        # Task entry
        ttk.Label(input_frame, text="New Task:").grid(row=0, column=0, sticky=tk.W)
        self.task_entry = ttk.Entry(input_frame, width=50)
        self.task_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 5))
        self.task_entry.bind('<Return>', lambda e: self.add_todo())
        
        # Priority and category frame
        options_frame = ttk.Frame(input_frame)
        options_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(5, 10))
        
        ttk.Label(options_frame, text="Priority:").grid(row=0, column=0, padx=(0, 10))
        self.priority_var = tk.StringVar(value="medium")
        priority_combo = ttk.Combobox(options_frame, textvariable=self.priority_var, 
                                     values=["high", "medium", "low"], state="readonly", width=10)
        priority_combo.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(options_frame, text="Category:").grid(row=0, column=2, padx=(0, 10))
        self.category_var = tk.StringVar(value="general")
        category_combo = ttk.Combobox(options_frame, textvariable=self.category_var, 
                                     values=["general", "work", "personal", "shopping", "health"], width=15)
        category_combo.grid(row=0, column=3)
        
        # Add button
        add_btn = ttk.Button(input_frame, text="Add Todo", command=self.add_todo)
        add_btn.grid(row=3, column=0, pady=(5, 10))
        
        # Filter frame
        filter_frame = ttk.Frame(main_frame)
        filter_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filter:").grid(row=0, column=0, padx=(0, 10))
        self.filter_var = tk.StringVar(value="all")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                   values=["all", "pending", "completed"], state="readonly", width=10)
        filter_combo.grid(row=0, column=1, padx=(0, 20))
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_list())
        
        ttk.Label(filter_frame, text="Category:").grid(row=0, column=2, padx=(0, 10))
        self.category_filter_var = tk.StringVar(value="all")
        category_filter_combo = ttk.Combobox(filter_frame, textvariable=self.category_filter_var,
                                           values=["all", "general", "work", "personal", "shopping", "health"], 
                                           state="readonly", width=10)
        category_filter_combo.grid(row=0, column=3)
        category_filter_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_list())
        
        # Treeview for todos
        columns = ('id', 'task', 'priority', 'category', 'status', 'created')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.tree.heading('id', text='ID')
        self.tree.heading('task', text='Task')
        self.tree.heading('priority', text='Priority')
        self.tree.heading('category', text='Category')
        self.tree.heading('status', text='Status')
        self.tree.heading('created', text='Created')
        
        # Define columns
        self.tree.column('id', width=50)
        self.tree.column('task', width=300)
        self.tree.column('priority', width=80)
        self.tree.column('category', width=100)
        self.tree.column('status', width=80)
        self.tree.column('created', width=120)
        
        self.tree.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=3, column=3, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Mark Complete", command=self.complete_todo).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_todo).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Edit", command=self.edit_todo).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Statistics", command=self.show_stats).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_list).grid(row=0, column=4, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).grid(row=0, column=5, padx=5)
    
    def add_todo(self):
        """Add a new todo"""
        task = self.task_entry.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Please enter a task!")
            return
        
        todo = {
            'id': len(self.todos) + 1,
            'task': task,
            'priority': self.priority_var.get(),
            'category': self.category_var.get(),
            'created_at': datetime.now().isoformat(),
            'completed': False,
            'completed_at': None
        }
        
        self.todos.append(todo)
        self.save_todos()
        self.refresh_list()
        self.task_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Added: {task}")
    
    def refresh_list(self):
        """Refresh the todo list display"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Filter todos
        filtered_todos = self.todos
        
        # Status filter
        if self.filter_var.get() == "pending":
            filtered_todos = [todo for todo in filtered_todos if not todo['completed']]
        elif self.filter_var.get() == "completed":
            filtered_todos = [todo for todo in filtered_todos if todo['completed']]
        
        # Category filter
        if self.category_filter_var.get() != "all":
            filtered_todos = [todo for todo in filtered_todos if todo['category'] == self.category_filter_var.get()]
        
        # Add to treeview
        for todo in filtered_todos:
            status = "Completed" if todo['completed'] else "Pending"
            created_date = datetime.fromisoformat(todo['created_at']).strftime("%Y-%m-%d")
            
            self.tree.insert('', tk.END, values=(
                todo['id'],
                todo['task'],
                todo['priority'].title(),
                todo['category'].title(),
                status,
                created_date
            ))
    
    def get_selected_todo(self):
        """Get the currently selected todo"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a todo!")
            return None
        
        item = selection[0]
        todo_id = int(self.tree.item(item)['values'][0])
        
        for todo in self.todos:
            if todo['id'] == todo_id:
                return todo, item
        
        return None
    
    def complete_todo(self):
        """Mark selected todo as completed"""
        result = self.get_selected_todo()
        if result:
            todo, item = result
            if not todo['completed']:
                todo['completed'] = True
                todo['completed_at'] = datetime.now().isoformat()
                self.save_todos()
                self.refresh_list()
                messagebox.showinfo("Success", f"Completed: {todo['task']}")
            else:
                messagebox.showinfo("Info", "Todo is already completed!")
    
    def delete_todo(self):
        """Delete selected todo"""
        result = self.get_selected_todo()
        if result:
            todo, item = result
            if messagebox.askyesno("Confirm", f"Delete: {todo['task']}?"):
                self.todos = [t for t in self.todos if t['id'] != todo['id']]
                self.save_todos()
                self.refresh_list()
    
    def edit_todo(self):
        """Edit selected todo"""
        result = self.get_selected_todo()
        if result:
            todo, item = result
            
            # Create edit dialog
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Todo")
            edit_window.geometry("400x300")
            edit_window.transient(self.root)
            edit_window.grab_set()
            
            ttk.Label(edit_window, text="Task:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
            task_var = tk.StringVar(value=todo['task'])
            task_entry = ttk.Entry(edit_window, textvariable=task_var, width=40)
            task_entry.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
            
            ttk.Label(edit_window, text="Priority:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
            priority_var = tk.StringVar(value=todo['priority'])
            priority_combo = ttk.Combobox(edit_window, textvariable=priority_var,
                                         values=["high", "medium", "low"], state="readonly")
            priority_combo.grid(row=1, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
            
            ttk.Label(edit_window, text="Category:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
            category_var = tk.StringVar(value=todo['category'])
            category_combo = ttk.Combobox(edit_window, textvariable=category_var,
                                         values=["general", "work", "personal", "shopping", "health"])
            category_combo.grid(row=2, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
            
            status_var = tk.BooleanVar(value=todo['completed'])
            status_check = ttk.Checkbutton(edit_window, text="Completed", variable=status_var)
            status_check.grid(row=3, column=0, columnspan=2, pady=10)
            
            def save_changes():
                todo['task'] = task_var.get()
                todo['priority'] = priority_var.get()
                todo['category'] = category_var.get()
                todo['completed'] = status_var.get()
                if todo['completed'] and not todo.get('completed_at'):
                    todo['completed_at'] = datetime.now().isoformat()
                
                self.save_todos()
                self.refresh_list()
                edit_window.destroy()
                messagebox.showinfo("Success", "Todo updated successfully!")
            
            ttk.Button(edit_window, text="Save", command=save_changes).grid(row=4, column=0, columnspan=2, pady=20)
            
            edit_window.columnconfigure(1, weight=1)
    
    def show_stats(self):
        """Show statistics dialog"""
        total = len(self.todos)
        completed = sum(1 for todo in self.todos if todo['completed'])
        pending = total - completed
        
        if total > 0:
            completion_rate = (completed / total) * 100
        else:
            completion_rate = 0
        
        stats_text = f"""
📊 Statistics:

Total todos: {total}
Completed: {completed}
Pending: {pending}
Completion rate: {completion_rate:.1f}%

Categories:
"""
        # Category breakdown
        categories = {}
        for todo in self.todos:
            cat = todo['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in categories.items():
            stats_text += f"  {cat.title()}: {count}\n"
        
        messagebox.showinfo("Statistics", stats_text)
    
    def clear_all(self):
        """Clear all todos"""
        if not self.todos:
            messagebox.showinfo("Info", "No todos to clear!")
            return
        
        if messagebox.askyesno("Confirm", "Clear ALL todos? This cannot be undone!"):
            self.todos = []
            self.save_todos()
            self.refresh_list()
            messagebox.showinfo("Success", "All todos cleared!")

def main():
    root = tk.Tk()
    app = TodoAppGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
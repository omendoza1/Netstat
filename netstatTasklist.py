import tkinter as tk
from tkinter import ttk, messagebox
import psutil

class NetworkInfoApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Información de Red")
        self.window.geometry("800x600")

        self.blacklist = []

        self.treeview = ttk.Treeview(window)
        self.treeview.pack(fill='both', expand=True)

        self.treeview['columns'] = ('protocol', 'local_address', 'remote_address', 'pid', 'process_name')

        for col in self.treeview['columns']:
            self.treeview.heading(col, text=col, anchor='w')
            self.treeview.column(col, anchor='w')

        self.refresh_button = tk.Button(window, text="Refrescar", command=self.refresh_process_list)
        self.refresh_button.pack(side='left')

        self.kill_button = tk.Button(window, text="Acciones - Terminar Proceso", command=self.kill_process)
        self.kill_button.pack(side='left')

    
        self.refresh_process_list()

    def refresh_process_list(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)

        connections = psutil.net_connections(kind='inet')

        for conn in connections:
            process = psutil.Process(conn.pid)
            if process.name() not in self.blacklist:
                self.treeview.insert('', 'end', values=(conn.type, f"{conn.laddr}", f"{conn.raddr}", conn.pid, process.name()))

    

    def revoke_process(self):
        cur_item = self.treeview.focus()
        if cur_item:
            values_lst = self.treeview.item(cur_item)['values']
            if values_lst:
                process_name = values_lst[4]
                if process_name in self.blacklist:
                    self.blacklist.remove(process_name)
                    messagebox.showinfo("Éxito", f"El proceso {process_name} fue removido de la lista negra exitosamente")
                else:
                    messagebox.showinfo("Error", f"El proceso {process_name} no está en la lista negra")
            else: 
                messagebox.showerror("Error", "No se ha seleccionado un proceso")

        self.refresh_process_list()

    def kill_process(self):
        cur_item = self.treeview.focus()

        if cur_item:
            values_lst = self.treeview.item(cur_item)['values']
            if values_lst:
                pid = int(values_lst[3])
            else: 
                messagebox.showerror("Error", "No se ha seleccionado un proceso")
                return

            try:
                p = psutil.Process(pid)

                try:
                    p.terminate()
                except:
                    p.kill()

                messagebox.showinfo("Éxito", "El proceso fue terminado exitosamente")

            except psutil.NoSuchProcess:
                messagebox.showerror("Error", "El proceso no existe")
            except psutil.AccessDenied:
                messagebox.showerror("Error", "No se pudo terminar el proceso debido al acceso denegado")

            self.refresh_process_list()
        else: 
            messagebox.showerror("Error", "No se ha seleccionado un proceso")

        self.refresh_process_list()


window = tk.Tk()
app = NetworkInfoApp(window)
window.mainloop()
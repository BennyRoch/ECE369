import tkinter as tk
from tkinter import ttk, messagebox
import socket
import threading

class DoorLockGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Door Lock Control System")
        self.root.geometry("400x500")

        # Connection variables
        self.client_socket = None
        self.is_connected = False
        self.is_authenticated = False
        self.receive_thread = None

        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Connection frame
        self.connection_frame = ttk.LabelFrame(self.main_frame, text="Connection", padding="5")
        self.connection_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.connection_frame, text="IP Address:").grid(row=0, column=0, sticky=tk.W)
        self.ip_entry = ttk.Entry(self.connection_frame, width=20)
        self.ip_entry.grid(row=0, column=1, padx=5)
        self.ip_entry.insert(0, "192.168.1.100")  # Default IP

        ttk.Label(self.connection_frame, text="Port:").grid(row=1, column=0, sticky=tk.W)
        self.port_entry = ttk.Entry(self.connection_frame, width=20)
        self.port_entry.grid(row=1, column=1, padx=5)
        self.port_entry.insert(0, "12345")  # Default port

        self.connect_button = ttk.Button(self.connection_frame, text="Connect", command=self.connect_to_server)
        self.connect_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Login frame
        self.login_frame = ttk.LabelFrame(self.main_frame, text="Login", padding="5")
        self.login_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky=tk.W)
        self.username_entry = ttk.Entry(self.login_frame, width=20)
        self.username_entry.grid(row=0, column=1, padx=5)

        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky=tk.W)
        self.password_entry = ttk.Entry(self.login_frame, width=20, show="*")
        self.password_entry.grid(row=1, column=1, padx=5)

        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.logout_button = ttk.Button(self.login_frame, text="Logout", command=self.logout)
        self.logout_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Control frame
        self.control_frame = ttk.LabelFrame(self.main_frame, text="Door Control", padding="5")
        self.control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.unlock_button = ttk.Button(self.control_frame, text="Unlock Door", command=self.unlock_door)
        self.unlock_button.grid(row=0, column=0, padx=5, pady=5)

        self.lock_button = ttk.Button(self.control_frame, text="Lock Door", command=self.lock_door)
        self.lock_button.grid(row=0, column=1, padx=5, pady=5)

        # Status frame
        self.status_frame = ttk.LabelFrame(self.main_frame, text="System Status", padding="5")
        self.status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.status_text = tk.Text(self.status_frame, height=10, width=40)
        self.status_text.grid(row=0, column=0, padx=5, pady=5)
        self.status_text.config(state=tk.DISABLED)

        # Disable controls initially
        self.toggle_controls(False)

    def toggle_controls(self, enabled):
        state = "normal" if enabled else "disabled"
        self.unlock_button.config(state=state)
        self.lock_button.config(state=state)
        self.logout_button.config(state=state)

    def connect_to_server(self):
        if self.is_connected:
            self.disconnect_from_server()
            return
        try:
            ip = self.ip_entry.get()
            port = int(self.port_entry.get())
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, port))

            self.is_connected = True
            self.connect_button.config(text="Disconnect")
            self.status_update("Connected to server")

            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True
            self.receive_thread.start()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")

    def disconnect_from_server(self):
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        self.is_connected = False
        self.is_authenticated = False
        self.connect_button.config(text="Connect")
        self.toggle_controls(False)
        self.status_update("Disconnected from server")

    def login(self):
        if not self.is_connected:
            messagebox.showerror("Error", "Not connected to server")
            return

        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        try:
            self.client_socket.send(f"login:{username}:{password}\n".encode())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send login request: {str(e)}")

    def unlock_door(self):
        if not self.is_authenticated:
            messagebox.showerror("Error", "Not authenticated")
            return
        try:
            self.client_socket.send("open_sesame\n".encode())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send unlock command: {str(e)}")

    def lock_door(self):
        if not self.is_authenticated:
            messagebox.showerror("Error", "Not authenticated")
            return
        try:
            self.client_socket.send("close_sesame\n".encode())
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send lock command: {str(e)}")

    def logout(self):
        if not self.is_authenticated:
            messagebox.showerror("Error", "Not authenticated")
            return
        try:
            self.client_socket.send("logout\n".encode())
            self.is_authenticated = False
            self.toggle_controls(False)
            self.status_update("Logged out successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send logout command: {str(e)}")

    def status_update(self, message):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)

    def receive_messages(self):
        while self.is_connected:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break

                self.status_update(f"Received: {data.strip()}")

                if "Login successful" in data:
                    self.is_authenticated = True
                    self.toggle_controls(True)
                elif "Invalid username or password" in data or "Session timed out" in data:
                    self.is_authenticated = False
                    self.toggle_controls(False)

            except Exception as e:
                self.status_update(f"Error receiving data: {str(e)}")
                break
        self.disconnect_from_server()

if __name__ == "__main__":
    root = tk.Tk()
    app = DoorLockGUI(root)
    root.mainloop()

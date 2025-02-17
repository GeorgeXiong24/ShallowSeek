import tkinter as tk
from tkinter import ttk
import subprocess
import os

class ColorBlocksApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ShallowSeek")
        
        # Configure window size and resizing
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)
        
        # Show welcome dialog
        self.show_welcome_dialog()
        
        # Set dark theme colors and base font size
        self.root.configure(bg='#2B2D31')
        style = ttk.Style()
        style.configure('Dark.TFrame', background='#2B2D31')
        style.configure('Dark.TLabel', background='#2B2D31', foreground='white', font=("TkDefaultFont", 12))
        style.configure('Dark.TButton', background='#2B2D31', foreground='white', font=("TkDefaultFont", 12))
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10", style='Dark.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure main frame grid weights
        main_frame.grid_rowconfigure(1, weight=1)  # Input text
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Output box with scrollbar
        output_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        output_frame.grid(row=0, column=0, columnspan=2, pady=(5, 15), sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.grid_columnconfigure(0, weight=1)
        output_frame.grid_rowconfigure(0, weight=5)  # Increased weight for larger chat history
        
        self.output_text = tk.Text(output_frame, height=25, width=60, bg='#383A40', fg='white', insertbackground='white', state='disabled', font=("TkDefaultFont", 14))
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add scrollbar with dark theme
        scrollbar = ttk.Scrollbar(output_frame, orient='vertical', command=self.output_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure scrollbar style
        style = ttk.Style()
        style.configure('Vertical.TScrollbar', background='#383A40', troughcolor='#2B2D31', arrowcolor='white')
        scrollbar.configure(style='Vertical.TScrollbar')
        
        # Input box with Send button
        input_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        input_frame.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky=(tk.W, tk.E))
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.input_text = tk.Text(input_frame, height=8, width=60, bg='#383A40', fg='white', insertbackground='white', font=("TkDefaultFont", 12), pady=0)
        self.input_text.grid(row=0, column=0, padx=(5, 5), sticky=(tk.W, tk.E, tk.N))
        
        # Bind Enter key to process_input
        self.input_text.bind('<Return>', lambda event: self.process_input())
        
        send_button = ttk.Button(input_frame, text="Send", style='Send.TButton', command=self.process_input)
        send_button.grid(row=0, column=1, sticky=(tk.E))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=(0, 5), sticky=(tk.W, tk.E))
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        
        # Create buttons with dark theme
        button_style = ttk.Style()
        button_style.configure('Dark.TButton', font=("TkDefaultFont", 14), padding=(15, 15))
        
        # Adjust send button style for consistency
        style.configure('Send.TButton', font=("TkDefaultFont", 14), padding=(15, 15))
        
        self.button1 = ttk.Button(buttons_frame, text="ShallowThink(R1)", style='Dark.TButton',
                                command=lambda: self.toggle_button_color(self.button1))
        self.button1.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        self.button2 = ttk.Button(buttons_frame, text="Search", style='Dark.TButton',
                                command=lambda: self.toggle_button_color(self.button2))
        self.button2.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        self.button3 = ttk.Button(buttons_frame, text="Attach File", style='Dark.TButton',
                                command=self.show_attach_message)
        self.button3.grid(row=0, column=2, padx=10, pady=10, sticky=(tk.W, tk.E))
        
        # Initialize button states
        self.button_states = {}
        self.button1.state(['!pressed'])
        self.button2.state(['!pressed'])
        self.button3.state(['!pressed'])
        
        # Message label for attach file
        self.message_label = ttk.Label(main_frame, text="", style='Dark.TLabel')
        self.message_label.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        self.message_label.grid_remove()
    
    def show_attach_message(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("")
        dialog.geometry("300x150")
        dialog.configure(bg='#2B2D31')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog window relative to the main window
        dialog.geometry("+{}+{}".format(
            self.root.winfo_x() + (self.root.winfo_width() - 300) // 2,
            self.root.winfo_y() + (self.root.winfo_height() - 150) // 2
        ))
        
        # Configure dialog layout
        dialog.grid_rowconfigure(0, weight=1)
        dialog.grid_rowconfigure(1, weight=1)
        dialog.grid_columnconfigure(0, weight=1)
        
        # Add message label
        message_label = ttk.Label(dialog, text="Attach File is Unavailable", style='Dark.TLabel', font=("TkDefaultFont", 12))
        message_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Add OK button
        ok_button = ttk.Button(dialog, text="OK", style='Dark.TButton', command=dialog.destroy)
        ok_button.grid(row=1, column=0, pady=(0, 20))
        
        # Bind Enter key to close dialog
        dialog.bind('<Return>', lambda event: dialog.destroy())
        
        # Make dialog modal
        dialog.focus_set()
        dialog.wait_window()
    
    def hide_message(self):
        self.message_label.grid_remove()
        
    def show_welcome_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("")
        dialog.geometry("500x250")
        dialog.configure(bg='#2B2D31')
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Wait for the main window to be drawn and its geometry updated
        self.root.update_idletasks()
        
        # Calculate position to center the dialog relative to the main window
        x = self.root.winfo_x() + (self.root.winfo_width() - 400) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 200) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Configure dialog layout
        dialog.grid_rowconfigure(0, weight=1)
        dialog.grid_rowconfigure(1, weight=1)
        dialog.grid_columnconfigure(0, weight=1)
        
        # Add welcome message label
        message_label = ttk.Label(dialog, 
                                text="Hello! This is ShallowSeek!\nYou can ask me any question you want!\nCopyright © 2025 ShallowSeek by George Xiong, All Rights Reserved.", 
                                style='Dark.TLabel', 
                                font=("TkDefaultFont", 12),
                                justify='center')
        message_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Add OK button
        ok_button = ttk.Button(dialog, text="OK", style='Dark.TButton', command=dialog.destroy)
        ok_button.grid(row=1, column=0, pady=(0, 20))
        
        # Bind Enter key to close dialog
        dialog.bind('<Return>', lambda event: dialog.destroy())
        
        # Make dialog modal
        dialog.focus_set()
        dialog.wait_window()
        
    def toggle_button_color(self, button):
        style = ttk.Style()
        button_name = str(button)
        
        # Create unique style names for this button
        normal_style = f'Normal{button_name}.TButton'
        pressed_style = f'Pressed{button_name}.TButton'
        
        # Configure the styles if they don't exist
        if normal_style not in self.button_states:
            style.configure(normal_style, background='#383A40', foreground='white')
            style.configure(pressed_style, background='#5865F2', foreground='white')
            
            self.button_states[normal_style] = pressed_style
            self.button_states[pressed_style] = normal_style
            
            # Set initial style
            button.configure(style=normal_style)
        
        current_style = str(button.cget('style'))
        next_style = self.button_states.get(current_style)
        if next_style:
            button.configure(style=next_style)
            button.state(['pressed'] if next_style.startswith('Pressed') else ['!pressed'])

    def process_input(self):
        user_input = self.input_text.get("1.0", tk.END).strip()
        if user_input:
            # Enable output text widget for updating
            self.output_text.configure(state='normal')
            
            # Configure tags for message styling if not already configured
            if not 'user_message' in self.output_text.tag_names():
                self.output_text.tag_configure('user_message', justify='right', background='#5865F2', foreground='white', lmargin1=50, rmargin=8, spacing1=10, spacing3=5)
                self.output_text.tag_configure('assistant_message', justify='left', background='#383A40', foreground='white', lmargin1=8, rmargin=50, spacing1=10, spacing3=5)
                self.output_text.tag_configure('processing_message', justify='left', background='#383A40', foreground='white', lmargin1=8, rmargin=50, spacing1=10, spacing3=5, font=("TkDefaultFont", 10))
            
            # Add user input with right alignment and styling
            self.output_text.insert(tk.END, '\n')
            self.output_text.insert(tk.END, f"{user_input}\n", 'user_message')
            
            # Clear input text immediately after sending
            self.input_text.delete("1.0", tk.END)
            
            # Check if ShallowThink button is pressed
            if self.button1.state() == ('pressed',):
                # Generate random thinking time between 5-20 seconds
                import random
                think_time = random.randint(5, 20)
                
                # Show initial thinking message in a separate block
                self.output_text.insert(tk.END, '\n\n')  # Add extra spacing before thinking message
                thinking_message = f"Thinking for {think_time} seconds"
                self.output_text.insert(tk.END, thinking_message, 'assistant_message')
                self.output_text.see(tk.END)
                self.output_text.update()
                
                # Add dots with delay in the same block
                for _ in range(think_time * 2):  # 2 dots per second
                    self.root.after(500)  # Wait for 500ms (0.5 seconds)
                    self.output_text.configure(state='normal')
                    self.output_text.insert(tk.END, ".", 'assistant_message')
                    self.output_text.see(tk.END)
                    self.output_text.update()
                    self.output_text.configure(state='disabled')
                
                # Add extra spacing after thinking animation
                self.output_text.configure(state='normal')
                self.output_text.insert(tk.END, '\n\n')
                self.output_text.configure(state='normal')
            
            # Check if search button is pressed
            if self.button2.state() == ('pressed',):
                # Show searching message
                self.output_text.insert(tk.END, '\n')
                self.output_text.insert(tk.END, "searching through the web...\n", 'assistant_message')
                self.output_text.see(tk.END)
                self.output_text.update()
                
                # Wait for 3 seconds
                self.root.after(3000)
            
            # Process the input using the C++ processor
            try:
                processor_path = './output/processor'
                if not os.path.exists(processor_path):
                    raise FileNotFoundError(f"Processor file not found at {processor_path}. Please make sure the C++ processor is compiled.")
                
                process = subprocess.Popen([processor_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
                response, error = process.communicate(input=user_input)
                
                if process.returncode != 0:
                    raise RuntimeError(f"Processor exited with error code {process.returncode}")
                
                if error:
                    raise RuntimeError(f"Processor error: {error}")
                
                # Add loading animation before showing response
                self.output_text.insert(tk.END, '\n')
                self.output_text.insert(tk.END, "Processing...", 'processing_message')
                self.output_text.see(tk.END)
                self.output_text.update()
                
                # Wait for 3 seconds
                #self.root.after(3000)
                
                # Show the response after delay
                self.output_text.insert(tk.END, '\n')
                self.output_text.insert(tk.END, f"{response}\n", 'assistant_message')
            except FileNotFoundError as e:
                self.output_text.insert(tk.END, '\n')
                self.output_text.insert(tk.END, f"Setup Error: {str(e)}\n", 'assistant_message')
            except Exception as e:
                self.output_text.insert(tk.END, '\n')
                self.output_text.insert(tk.END, f"System Error: {str(e)}\n", 'assistant_message')
            
            # Disable output text widget after updating
            self.output_text.configure(state='disabled')
            # Scroll to the bottom of output
            self.output_text.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorBlocksApp(root)
    root.mainloop()
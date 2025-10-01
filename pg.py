# password_generator_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import string
import secrets
import pyperclip  # For clipboard functionality

class PasswordGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Password Generator")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔐 Password Generator", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Length frame
        length_frame = ttk.LabelFrame(main_frame, text="Password Length", padding="10")
        length_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.length_var = tk.IntVar(value=12)
        length_scale = ttk.Scale(length_frame, from_=8, to=128, 
                               variable=self.length_var, orient=tk.HORIZONTAL)
        length_scale.pack(fill=tk.X)
        
        self.length_label = ttk.Label(length_frame, text="Length: 12")
        self.length_label.pack()
        length_scale.configure(command=self.update_length_label)
        
        # Character types frame
        chars_frame = ttk.LabelFrame(main_frame, text="Character Types", padding="10")
        chars_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.upper_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=True)
        self.exclude_similar_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(chars_frame, text="Uppercase Letters (A-Z)", 
                       variable=self.upper_var).pack(anchor=tk.W)
        ttk.Checkbutton(chars_frame, text="Digits (0-9)", 
                       variable=self.digits_var).pack(anchor=tk.W)
        ttk.Checkbutton(chars_frame, text="Special Characters (!@#$% etc.)", 
                       variable=self.special_var).pack(anchor=tk.W)
        ttk.Checkbutton(chars_frame, text="Exclude similar characters (I, l, 1, O, 0)", 
                       variable=self.exclude_similar_var).pack(anchor=tk.W)
        
        # Quick generate frame
        quick_frame = ttk.LabelFrame(main_frame, text="Quick Generate", padding="10")
        quick_frame.pack(fill=tk.X, pady=(0, 10))
        
        quick_buttons_frame = ttk.Frame(quick_frame)
        quick_buttons_frame.pack()
        
        ttk.Button(quick_buttons_frame, text="Simple (8 chars)", 
                  command=lambda: self.quick_generate(8, False, True, False)).grid(row=0, column=0, padx=5)
        ttk.Button(quick_buttons_frame, text="Medium (12 chars)", 
                  command=lambda: self.quick_generate(12, True, True, False)).grid(row=0, column=1, padx=5)
        ttk.Button(quick_buttons_frame, text="Strong (16 chars)", 
                  command=lambda: self.quick_generate(16, True, True, True)).grid(row=0, column=2, padx=5)
        ttk.Button(quick_buttons_frame, text="Very Strong (20 chars)", 
                  command=lambda: self.quick_generate(20, True, True, True)).grid(row=0, column=3, padx=5)
        
        # Generate button
        generate_frame = ttk.Frame(main_frame)
        generate_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.generate_btn = ttk.Button(generate_frame, text="Generate Password", 
                                      command=self.generate_password)
        self.generate_btn.pack(pady=10)
        
        # Password display frame
        password_frame = ttk.LabelFrame(main_frame, text="Generated Password", padding="10")
        password_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(password_frame, textvariable=self.password_var, 
                                  font=('Courier', 12), state='readonly')
        password_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Password info
        self.info_text = scrolledtext.ScrolledText(password_frame, height=8, 
                                                  font=('Arial', 10))
        self.info_text.pack(fill=tk.BOTH, expand=True)
        self.info_text.config(state=tk.DISABLED)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X)
        
        ttk.Button(action_frame, text="Copy to Clipboard", 
                  command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="Generate Multiple", 
                  command=self.generate_multiple).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(action_frame, text="Clear", 
                  command=self.clear_all).pack(side=tk.LEFT)
    
    def update_length_label(self, value):
        """Update length label when slider moves"""
        self.length_label.config(text=f"Length: {int(float(value))}")
    
    def quick_generate(self, length, upper, digits, special):
        """Quick generate with preset settings"""
        self.length_var.set(length)
        self.upper_var.set(upper)
        self.digits_var.set(digits)
        self.special_var.set(special)
        self.update_length_label(length)
        self.generate_password()
    
    def generate_password(self):
        """Generate password based on current settings"""
        try:
            length = self.length_var.get()
            
            # Validate at least one character type is selected
            if not any([self.upper_var.get(), self.digits_var.get(), self.special_var.get()]):
                messagebox.showwarning("Warning", "Please select at least one character type!")
                return
            
            password = self._generate_secure_password(
                length=length,
                use_uppercase=self.upper_var.get(),
                use_digits=self.digits_var.get(),
                use_special=self.special_var.get(),
                exclude_similar=self.exclude_similar_var.get()
            )
            
            self.password_var.set(password)
            self.display_password_info(password)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password: {e}")
    
    def _generate_secure_password(self, length, use_uppercase, use_digits, use_special, exclude_similar):
        """Generate a secure password"""
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase if use_uppercase else ''
        digits = string.digits if use_digits else ''
        special = string.punctuation if use_special else ''
        
        # Exclude similar characters
        similar_chars = 'Il1O0' if exclude_similar else ''
        all_chars = lowercase + uppercase + digits + special
        
        if exclude_similar:
            all_chars = ''.join(c for c in all_chars if c not in similar_chars)
        
        # Ensure we have characters from each selected category
        password_chars = []
        
        password_chars.append(secrets.choice(lowercase))
        if uppercase:
            password_chars.append(secrets.choice(uppercase))
        if digits:
            password_chars.append(secrets.choice(digits))
        if special:
            password_chars.append(secrets.choice(special))
        
        # Fill remaining length
        remaining = length - len(password_chars)
        if remaining > 0:
            password_chars.extend(secrets.choice(all_chars) for _ in range(remaining))
        
        # Shuffle
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    def display_password_info(self, password):
        """Display detailed password information"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        # Calculate statistics
        length = len(password)
        upper_count = sum(1 for c in password if c.isupper())
        lower_count = sum(1 for c in password if c.islower())
        digit_count = sum(1 for c in password if c.isdigit())
        special_count = sum(1 for c in password if c in string.punctuation)
        
        # Calculate strength
        strength = self.calculate_strength(password)
        
        info = f"""🔐 PASSWORD ANALYSIS:
────────────────────────────────
Length: {length} characters
Strength: {strength}

CHARACTER BREAKDOWN:
• Uppercase letters: {upper_count}
• Lowercase letters: {lower_count}
• Digits: {digit_count}
• Special characters: {special_count}

ENTROPY: Approximately {self.calculate_entropy(password):.1f} bits
"""
        self.info_text.insert(1.0, info)
        self.info_text.config(state=tk.DISABLED)
    
    def calculate_strength(self, password):
        """Calculate password strength"""
        score = 0
        length = len(password)
        
        # Length scoring
        if length >= 8: score += 1
        if length >= 12: score += 1
        if length >= 16: score += 1
        if length >= 20: score += 1
        
        # Character variety
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        if has_upper and has_lower: score += 1
        if has_digit: score += 1
        if has_special: score += 1
        
        if score <= 2: return "Weak 🔴"
        elif score <= 4: return "Moderate 🟡"
        elif score <= 6: return "Strong 🟢"
        else: return "Very Strong 💪"
    
    def calculate_entropy(self, password):
        """Calculate password entropy in bits"""
        char_pool = 0
        if any(c.islower() for c in password): char_pool += 26
        if any(c.isupper() for c in password): char_pool += 26
        if any(c.isdigit() for c in password): char_pool += 10
        if any(c in string.punctuation for c in password): char_pool += 32
        
        if char_pool == 0:
            return 0
        
        import math
        return len(password) * math.log2(char_pool)
    
    def copy_to_clipboard(self):
        """Copy password to clipboard"""
        password = self.password_var.get()
        if password:
            try:
                pyperclip.copy(password)
                messagebox.showinfo("Success", "Password copied to clipboard!")
            except:
                messagebox.showerror("Error", "Could not copy to clipboard. Please install pyperclip: pip install pyperclip")
        else:
            messagebox.showwarning("Warning", "No password to copy!")
    
    def generate_multiple(self):
        """Generate multiple passwords"""
        try:
            count = tk.simpledialog.askinteger("Multiple Passwords", 
                                             "How many passwords to generate? (1-10)", 
                                             minvalue=1, maxvalue=10)
            if count:
                passwords = []
                for _ in range(count):
                    pwd = self._generate_secure_password(
                        length=self.length_var.get(),
                        use_uppercase=self.upper_var.get(),
                        use_digits=self.digits_var.get(),
                        use_special=self.special_var.get(),
                        exclude_similar=self.exclude_similar_var.get()
                    )
                    passwords.append(pwd)
                
                # Display multiple passwords
                multiple_window = tk.Toplevel(self.root)
                multiple_window.title(f"Generated {count} Passwords")
                multiple_window.geometry("500x400")
                
                text_area = scrolledtext.ScrolledText(multiple_window, font=('Courier', 10))
                text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                for i, pwd in enumerate(passwords, 1):
                    text_area.insert(tk.END, f"{i:2d}. {pwd}\n")
                
                text_area.config(state=tk.DISABLED)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate multiple passwords: {e}")
    
    def clear_all(self):
        """Clear all fields"""
        self.password_var.set("")
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
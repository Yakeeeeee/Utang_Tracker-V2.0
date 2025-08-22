import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
import csv
import os
from datetime import datetime, timedelta
import hashlib
import matplotlib
matplotlib.use('TkAgg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import random
import webbrowser
from PIL import Image, ImageTk
import json

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernUtangTracker:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("💰 Modern Utang Tracker")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.destroy)
        
        # Initialize data
        self.init_csv_files()
        
        # Current user and state
        self.current_user = None
        self.current_view = "login"
        self.selected_person_data = None
        self.selected_debt = None
        
        # Matplotlib figure and canvas
        self.fig = None
        self.canvas = None
        
        # Color scheme - will be updated based on theme
        self.colors = self.get_dark_colors()  # Start with dark mode
        self.current_theme = "dark"
        
        # Create main container with modern styling
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.colors["dark"])
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Start with login screen
        self.show_login_screen()
        
    def init_csv_files(self):
        """Initialize CSV files if they don't exist"""
        if not os.path.exists("users.csv"):
            with open("users.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["username", "password_hash", "registration_date"])
        
        if not os.path.exists("debt_data.csv"):
            with open("debt_data.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["user", "full_name", "amount", "relationship", "interest_rate", 
                               "date_added", "due_date", "notes", "status", "debt_id"])
        
        if not os.path.exists("payments.csv"):
            with open("payments.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["debt_id", "payment_amount", "payment_date"])
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def clear_main_frame(self):
        """Clear all widgets from main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def create_modern_button(self, parent, text, command, **kwargs):
        """Create a modern styled button"""
        default_kwargs = {
            "font": ctk.CTkFont(size=14, weight="bold"),
            "corner_radius": 10,
            "border_width": 2,
            "fg_color": self.colors["primary"],
            "hover_color": self.colors["secondary"],
            "text_color": "white",  # Always use white text for better visibility
            "height": 40
        }
        default_kwargs.update(kwargs)
        return ctk.CTkButton(parent, text=text, command=command, **default_kwargs)
    
    def create_modern_entry(self, parent, **kwargs):
        """Create a modern styled entry field"""
        default_kwargs = {
            "font": ctk.CTkFont(size=14),
            "corner_radius": 8,
            "border_width": 2,
            "fg_color": self.colors["light"],
            "border_color": self.colors["gray"],
            "text_color": "black" if self.current_theme == "light" else "white",  # Theme-appropriate text color
            "height": 40
        }
        default_kwargs.update(kwargs)
        return ctk.CTkEntry(parent, **default_kwargs)
    
    def create_modern_frame(self, parent, **kwargs):
        """Create a modern styled frame"""
        default_kwargs = {
            "corner_radius": 15,
            "border_width": 2,
            "fg_color": self.colors["light"],
            "border_color": self.colors["light_gray"]
        }
        default_kwargs.update(kwargs)
        return ctk.CTkFrame(parent, **default_kwargs)
    
    def show_login_screen(self):
        """Display modern login screen"""
        self.current_view = "login"
        self.clear_main_frame()
        
        # Create gradient-like background effect
        bg_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors["primary"])
        bg_frame.pack(fill="both", expand=True)
        
        # Center content
        center_frame = ctk.CTkFrame(bg_frame, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo and title
        logo_label = ctk.CTkLabel(center_frame, text="💰", 
                                 font=ctk.CTkFont(size=80))
        logo_label.pack(pady=(0, 10))
        
        title_label = ctk.CTkLabel(center_frame, text="Utang Tracker", 
                                 font=ctk.CTkFont(size=36, weight="bold"),
                                 text_color=self.colors["white"])
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ctk.CTkLabel(center_frame, text="Smart Debt Management System", 
                                    font=ctk.CTkFont(size=18),
                                    text_color=self.colors["light"])
        subtitle_label.pack(pady=(0, 30))
        
        author_label = ctk.CTkLabel(center_frame, text="By John Allen Esteleydes", 
                                  font=ctk.CTkFont(size=14, slant="italic"), 
                                  text_color=self.colors["light"])
        author_label.pack(pady=(0, 30))
        
        # Login form
        self.login_frame = self.create_modern_frame(center_frame)
        self.login_frame.pack(pady=20, padx=40, fill="x")
        
        # Username field
        username_label = ctk.CTkLabel(self.login_frame, text="👤 Username", 
                                    font=ctk.CTkFont(size=16, weight="bold"),
                                    text_color=self.colors["dark"])
        username_label.pack(pady=(20, 5))
        
        self.login_username_entry = self.create_modern_entry(self.login_frame, width=350)
        self.login_username_entry.pack(pady=(0, 15))
        
        # Password field
        password_label = ctk.CTkLabel(self.login_frame, text="🔒 Password", 
                                    font=ctk.CTkFont(size=16, weight="bold"),
                                    text_color=self.colors["dark"])
        password_label.pack(pady=(0, 5))
        
        self.login_password_entry = self.create_modern_entry(self.login_frame, width=350, show="•")
        self.login_password_entry.pack(pady=(0, 25))
        
        # Buttons
        button_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        button_frame.pack(pady=(0, 20))
        
        login_btn = self.create_modern_button(button_frame, text="🚀 Login", 
                                            command=self.login, width=160)
        login_btn.pack(side="left", padx=10)
        
        create_account_btn = self.create_modern_button(button_frame, text="✨ Create Account", 
                                                     command=self.show_register_screen, 
                                                     width=160, fg_color=self.colors["accent"])
        create_account_btn.pack(side="left", padx=10)
        
        # Bind Enter key to login
        self.login_username_entry.bind("<Return>", lambda e: self.login())
        self.login_password_entry.bind("<Return>", lambda e: self.login())
    
    def show_register_screen(self):
        """Display modern register screen"""
        self.current_view = "register"
        self.clear_main_frame()
        
        # Create gradient-like background effect
        bg_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors["accent"])
        bg_frame.pack(fill="both", expand=True)
        
        # Center content
        center_frame = ctk.CTkFrame(bg_frame, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo and title
        logo_label = ctk.CTkLabel(center_frame, text="✨", 
                                 font=ctk.CTkFont(size=80))
        logo_label.pack(pady=(0, 10))
        
        title_label = ctk.CTkLabel(center_frame, text="Create Account", 
                                 font=ctk.CTkFont(size=36, weight="bold"),
                                 text_color=self.colors["white"])
        title_label.pack(pady=(0, 30))
        
        # Register form
        self.register_frame = self.create_modern_frame(center_frame)
        self.register_frame.pack(pady=20, padx=40, fill="x")
        
        # Username field
        username_label = ctk.CTkLabel(self.register_frame, text="👤 Username", 
                                    font=ctk.CTkFont(size=16, weight="bold"),
                                    text_color=self.colors["dark"])
        username_label.pack(pady=(20, 5))
        
        self.register_username_entry = self.create_modern_entry(self.register_frame, width=350)
        self.register_username_entry.pack(pady=(0, 15))
        
        # Password field
        password_label = ctk.CTkLabel(self.register_frame, text="🔒 Password", 
                                    font=ctk.CTkFont(size=16, weight="bold"),
                                    text_color=self.colors["dark"])
        password_label.pack(pady=(0, 5))
        
        self.register_password_entry = self.create_modern_entry(self.register_frame, width=350, show="•")
        self.register_password_entry.pack(pady=(0, 25))
        
        # Buttons
        button_frame = ctk.CTkFrame(self.register_frame, fg_color="transparent")
        button_frame.pack(pady=(0, 20))
        
        register_btn = self.create_modern_button(button_frame, text="✨ Register", 
                                               command=self.register, width=160)
        register_btn.pack(side="left", padx=10)
        
        back_btn = self.create_modern_button(button_frame, text="← Back to Login", 
                                           command=self.show_login_screen, 
                                           width=160, fg_color=self.colors["gray"])
        back_btn.pack(side="left", padx=10)
        
        # Bind Enter key to register
        self.register_username_entry.bind("<Return>", lambda e: self.register())
        self.register_password_entry.bind("<Return>", lambda e: self.register())
    
    def login(self):
        """Handle user login"""
        username = self.login_username_entry.get().strip()
        password = self.login_password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("❌ Error", "Please enter both username and password")
            return
        
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username and row["password_hash"] == self.hash_password(password):
                    self.current_user = username
                    self.show_dashboard()
                    return
        
        messagebox.showerror("❌ Error", "Invalid username or password")
    
    def register(self):
        """Handle user registration"""
        username = self.register_username_entry.get().strip()
        password = self.register_password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("❌ Error", "Please enter both username and password")
            return
        
        if len(password) < 6:
            messagebox.showerror("❌ Error", "Password must be at least 6 characters long")
            return
        
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    messagebox.showerror("❌ Error", "Username already exists")
                    return
        
        with open("users.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, self.hash_password(password), datetime.now().strftime("%Y-%m-%d")])
        
        messagebox.showinfo("✅ Success", "Registration successful! You can now login.")
        self.show_login_screen()
    
    def show_dashboard(self):
        """Display modern dashboard with enhanced UI"""
        self.current_view = "dashboard"
        self.clear_main_frame()
        
        # Header with gradient effect
        header_frame = self.create_modern_frame(self.main_frame)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Welcome section
        welcome_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        welcome_frame.pack(side="left", padx=20, pady=15)
        
        welcome_label = ctk.CTkLabel(welcome_frame, text=f"👋 Welcome back, {self.current_user}!", 
                                   font=ctk.CTkFont(size=24, weight="bold"),
                                   text_color=self.colors["primary"])
        welcome_label.pack(side="left")
        
        # Quick stats
        consolidated_debts = self.get_consolidated_debts()
        total_remaining_who_owes_me = sum(p["remaining"] for p in consolidated_debts["Who owes me"])
        total_remaining_who_i_owe = sum(p["remaining"] for p in consolidated_debts["Who I owe"])
        
        stats_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        stats_frame.pack(side="left", padx=20, pady=15)
        
        ctk.CTkLabel(stats_frame, text=f"💰 You're owed: ₱{total_remaining_who_owes_me:.2f}", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.colors["success"]).pack(side="left", padx=10)
        
        ctk.CTkLabel(stats_frame, text=f"💸 You owe: ₱{total_remaining_who_i_owe:.2f}", 
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=self.colors["danger"]).pack(side="left", padx=10)
        
        # Header buttons
        button_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        button_frame.pack(side="right", padx=20, pady=15)
        
        # Theme selector
        theme_var = ctk.StringVar(value="Dark")
        theme_menu = ctk.CTkOptionMenu(button_frame, variable=theme_var,
                                     values=["Dark", "Light", "System"],
                                     command=self.change_theme, width=120, height=35)
        theme_menu.pack(side="left", padx=10)
        
        logout_btn = self.create_modern_button(button_frame, text="🚪 Logout", 
                                             command=self.show_login_screen, 
                                             width=100, height=35)
        logout_btn.pack(side="left", padx=10)
        
        # Tab view with modern styling
        self.tab_view = ctk.CTkTabview(self.main_frame, 
                                      fg_color=self.colors["light"],
                                      segmented_button_fg_color=self.colors["primary"],
                                      segmented_button_selected_color=self.colors["accent"],
                                      segmented_button_selected_hover_color=self.colors["secondary"])
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs with icons
        self.tab_view.add("📊 Debts")
        self.tab_view.add("📈 Analytics")
        self.tab_view.add("👤 Profile")
        self.tab_view.add("⚙️ Settings")
        
        # Debts tab content
        self.setup_debts_tab()
        
        # Analytics tab
        self.setup_analytics_tab()
        
        # Profile tab
        self.setup_profile_tab()
        
        # Settings tab
        self.setup_settings_tab()
        
        # Load initial data
        self.load_debts()
        self.load_analytics()
    
    def change_theme(self, choice):
        """Change application theme and refresh UI"""
        # Update CustomTkinter appearance
        ctk.set_appearance_mode(choice.lower())
        
        # Update our color scheme
        if choice.lower() == "dark":
            self.colors = self.get_dark_colors()
            self.current_theme = "dark"
        else:
            self.colors = self.get_light_colors()
            self.current_theme = "light"
        
        # Refresh the UI with new colors
        self.refresh_ui_colors()
    
    def refresh_ui_colors(self):
        """Refresh UI colors after theme change"""
        if hasattr(self, 'main_frame'):
            self.main_frame.configure(fg_color=self.colors["dark"])
        
        if hasattr(self, 'tab_view'):
            self.tab_view.configure(fg_color=self.colors["light"])
        
        # Clear matplotlib figure to force recreation with new theme
        if hasattr(self, 'fig') and self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.canvas = None
        
        # Refresh current view
        if self.current_view == "dashboard":
            self.show_dashboard()
        elif self.current_view == "add_debt":
            self.show_add_debt_form()
        elif self.current_view == "quick_add_debt":
            self.show_quick_add_debt_form()
        elif self.current_view == "edit_debt":
            if hasattr(self, 'selected_person_data'):
                self.show_edit_debt_form(self.selected_person_data)
        elif self.current_view == "add_payment":
            if hasattr(self, 'selected_person_data'):
                self.show_add_payment_form(self.selected_person_data)
    
    def setup_debts_tab(self):
        """Setup the debts tab with modern UI"""
        debts_tab = self.tab_view.tab("📊 Debts")
        
        # Action buttons with modern styling
        button_frame = ctk.CTkFrame(debts_tab, fg_color="transparent")
        button_frame.pack(pady=15, padx=20, fill="x")
        
        add_debt_btn = self.create_modern_button(button_frame, text="➕ Add New Debt",
                                               command=self.show_add_debt_form, width=180)
        add_debt_btn.pack(side="left", padx=10)
        
        quick_add_btn = self.create_modern_button(button_frame, text="⚡ Quick Add",
                                                command=self.show_quick_add_debt_form, width=180)
        quick_add_btn.pack(side="left", padx=10)
        
        export_btn = self.create_modern_button(button_frame, text="📤 Export Data",
                                             command=self.export_data, width=150, fg_color=self.colors["info"])
        export_btn.pack(side="left", padx=10)
        
        # Advanced search and filter frame
        filter_frame = self.create_modern_frame(debts_tab)
        filter_frame.pack(fill="x", padx=20, pady=10)
        
        # First row of filters
        filter_row1 = ctk.CTkFrame(filter_frame, fg_color="transparent")
        filter_row1.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(filter_row1, text="🔍 Search:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=5)
        self.search_entry = self.create_modern_entry(filter_row1, width=250, placeholder_text="Enter name to search...")
        self.search_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(filter_row1, text="👥 Relationship:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=5)
        self.filter_relationship_var = ctk.StringVar(value="All")
        relationship_menu = ctk.CTkOptionMenu(filter_row1, variable=self.filter_relationship_var,
                                            values=["All", "Who owes me", "Who I owe"],
                                            width=150, height=35, command=lambda x: self.load_debts())
        relationship_menu.pack(side="left", padx=5)
        
        # Second row of filters
        filter_row2 = ctk.CTkFrame(filter_frame, fg_color="transparent")
        filter_row2.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(filter_row2, text="📊 Status:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=5)
        self.filter_status_var = ctk.StringVar(value="All")
        status_menu = ctk.CTkOptionMenu(filter_row2, variable=self.filter_status_var,
                                      values=["All", "Overdue", "Pending", "Paid"],
                                      width=150, height=35, command=lambda x: self.load_debts())
        status_menu.pack(side="left", padx=5)
        
        ctk.CTkLabel(filter_row2, text="💰 Min Amount:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=5)
        self.min_amount_entry = self.create_modern_entry(filter_row2, width=120, placeholder_text="0")
        self.min_amount_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(filter_row2, text="💰 Max Amount:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=5)
        self.max_amount_entry = self.create_modern_entry(filter_row2, width=120, placeholder_text="∞")
        self.max_amount_entry.pack(side="left", padx=5)
        
        search_btn = self.create_modern_button(filter_row2, text="🔍 Apply Filters", 
                                             command=self.load_debts, width=150)
        search_btn.pack(side="left", padx=10)
        
        # Debts display area
        self.debt_scrollable_frame = ctk.CTkScrollableFrame(debts_tab, fg_color="transparent")
        self.debt_scrollable_frame.pack(fill="both", expand=True, pady=10, padx=20)
    
    def setup_analytics_tab(self):
        """Setup the analytics tab with modern UI"""
        analytics_tab = self.tab_view.tab("📈 Analytics")
        
        # Create scrollable frame for analytics
        self.analytics_scrollable_frame = ctk.CTkScrollableFrame(analytics_tab, fg_color="transparent")
        self.analytics_scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Set the analytics frame to the scrollable frame
        self.analytics_frame = self.analytics_scrollable_frame
    
    def setup_profile_tab(self):
        """Setup the profile tab with modern UI"""
        self.profile_frame = ctk.CTkFrame(self.tab_view.tab("👤 Profile"), fg_color="transparent")
        self.profile_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.show_profile_form()
    
    def setup_settings_tab(self):
        """Setup the settings tab with modern UI"""
        settings_tab = self.tab_view.tab("⚙️ Settings")
        
        # Settings content
        settings_frame = ctk.CTkFrame(settings_tab, fg_color="transparent")
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Account settings
        account_frame = self.create_modern_frame(settings_frame)
        account_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(account_frame, text="🔐 Account Settings", 
                    font=ctk.CTkFont(size=18, weight="bold"),
                    text_color=self.colors["primary"]).pack(pady=15)
        
        change_password_btn = self.create_modern_button(account_frame, text="🔑 Change Password",
                                                     command=self.show_change_password_form, width=200)
        change_password_btn.pack(pady=10)
        
        # Data management
        data_frame = self.create_modern_frame(settings_frame)
        data_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(data_frame, text="💾 Data Management", 
                    font=ctk.CTkFont(size=18, weight="bold"),
                    text_color=self.colors["primary"]).pack(pady=15)
        
        backup_btn = self.create_modern_button(data_frame, text="💾 Backup Data",
                                             command=self.backup_data, width=200, fg_color=self.colors["info"])
        backup_btn.pack(pady=5)
        
        restore_btn = self.create_modern_button(data_frame, text="📥 Restore Data",
                                              command=self.restore_data, width=200, fg_color=self.colors["warning"])
        restore_btn.pack(pady=5)
        
        clear_btn = self.create_modern_button(data_frame, text="🗑️ Clear All Data",
                                            command=self.clear_all_data, width=200, fg_color=self.colors["danger"])
        clear_btn.pack(pady=5)
        
        # About section
        about_frame = self.create_modern_frame(settings_frame)
        about_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(about_frame, text="ℹ️ About", 
                    font=ctk.CTkFont(size=18, weight="bold"),
                    text_color=self.colors["primary"]).pack(pady=15)
        
        about_text = """Utang Tracker v2.0
        
A modern debt management application designed to help you track and manage your financial obligations efficiently.

Features:
• Secure user authentication
• Comprehensive debt tracking
• Payment history management
• Advanced analytics and reporting
• Data export and backup
• Modern, intuitive interface

Developer: John Allen Esteleydes
Contact: esteleydesjohnallen0@gmail.com
YouTube: Yakee
Github: Yakeeeeee"""

        about_label = ctk.CTkLabel(about_frame, text=about_text,
                                 font=ctk.CTkFont(size=12),
                                 text_color=self.colors["gray"],
                                 justify="left")
        about_label.pack(pady=10, padx=20)
        
        # Social links
        social_frame = ctk.CTkFrame(about_frame, fg_color="transparent")
        social_frame.pack(pady=10)
        
        youtube_btn = self.create_modern_button(social_frame, text="📺 YouTube Channel",
                                              command=lambda: webbrowser.open("https://www.youtube.com/@mr.yakeee"),
                                              width=150, fg_color=self.colors["danger"])
        youtube_btn.pack(side="left", padx=5)
        
        email_btn = self.create_modern_button(social_frame, text="📧 Contact",
                                            command=lambda: webbrowser.open("mailto:esteleydesjohnallen0@gmail.com"),
                                            width=120, fg_color=self.colors["accent"])
        email_btn.pack(side="left", padx=5)

        github_btn = self.create_modern_button(social_frame, text="🐱 Github",
                                              command=lambda: webbrowser.open("https://github.com/Yakeeeeee"),
                                              width=150, fg_color=self.colors["info"])
        github_btn.pack(side="left", padx=5)
    
    def export_data(self):
        """Export debt data to CSV"""
        try:
            filename = f"debt_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Relationship", "Amount", "Interest Rate", "Date Added", "Due Date", "Notes", "Status"])
                
                debts = self.get_user_debts()
                for debt in debts:
                    writer.writerow([
                        debt["full_name"],
                        debt["relationship"],
                        debt["amount"],
                        debt["interest_rate"],
                        debt["date_added"],
                        debt["due_date"],
                        debt["notes"],
                        debt["status"]
                    ])
            
            messagebox.showinfo("✅ Success", f"Data exported successfully to {filename}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to export data: {str(e)}")
    
    def backup_data(self):
        """Backup all data files"""
        try:
            backup_dir = "backup"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Backup CSV files
            for filename in ["users.csv", "debt_data.csv", "payments.csv"]:
                if os.path.exists(filename):
                    backup_filename = f"{backup_dir}/{filename.replace('.csv', '')}_{timestamp}.csv"
                    with open(filename, "r", encoding="utf-8") as source:
                        with open(backup_filename, "w", encoding="utf-8") as backup:
                            backup.write(source.read())
            
            messagebox.showinfo("✅ Success", f"Data backed up successfully to {backup_dir} folder")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to backup data: {str(e)}")
    
    def restore_data(self):
        """Restore data from backup"""
        # This is a placeholder - in a real app you'd implement file selection and restoration
        messagebox.showinfo("ℹ️ Info", "Restore functionality would be implemented here")
    
    def clear_all_data(self):
        """Clear all data for current user"""
        if messagebox.askyesno("⚠️ Warning", 
                              "Are you sure you want to clear ALL your data? This action cannot be undone!"):
            try:
                # Clear debt data
                debts = []
                with open("debt_data.csv", "r") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row["user"] != self.current_user:
                            debts.append(row)
                
                with open("debt_data.csv", "w", newline="") as file:
                    fieldnames = ["user", "full_name", "amount", "relationship", "interest_rate", 
                                 "date_added", "due_date", "notes", "status", "debt_id"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(debts)
                
                # Clear payment data for deleted debts
                debt_ids = [d["debt_id"] for d in self.get_user_debts()]
                payments = []
                with open("payments.csv", "r") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        if row["debt_id"] in debt_ids:
                            payments.append(row)
                
                with open("payments.csv", "w", newline="") as file:
                    fieldnames = ["debt_id", "payment_amount", "payment_date"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(payments)
                
                messagebox.showinfo("✅ Success", "All data cleared successfully")
                self.load_debts()
                self.load_analytics()
            except Exception as e:
                messagebox.showerror("❌ Error", f"Failed to clear data: {str(e)}")

    def get_debt_status(self, debt):
        """Determine the status of a debt based on due date and remaining balance"""
        if debt["remaining"] == 0:
            return "Paid"
        if debt["due_date"] == "N/A":
            return "Pending"
        try:
            due_date = datetime.strptime(debt["due_date"], "%Y-%m-%d")
            today = datetime.now()
            if due_date < today:
                return "Overdue"
            return "Pending"
        except ValueError:
            return "Pending"
    
    def load_debts(self):
        """Load and display debt entries with modern UI"""
        for widget in self.debt_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Apply filters
        search_name = self.search_entry.get().strip().lower() if hasattr(self, 'search_entry') else ""
        relationship_filter = self.filter_relationship_var.get() if hasattr(self, 'filter_relationship_var') else "All"
        status_filter = self.filter_status_var.get() if hasattr(self, 'filter_status_var') else "All"
        min_amount = self.min_amount_entry.get().strip() if hasattr(self, 'min_amount_entry') else ""
        max_amount = self.max_amount_entry.get().strip() if hasattr(self, 'max_amount_entry') else ""
        
        try:
            min_amount = float(min_amount) if min_amount else float('-inf')
            max_amount = float(max_amount) if max_amount else float('inf')
        except ValueError:
            min_amount = float('-inf')
            max_amount = float('inf')
        
        consolidated_debts = self.get_consolidated_debts()
        
        # Create modern debt cards
        self.create_debt_cards(consolidated_debts, search_name, relationship_filter, status_filter, min_amount, max_amount)
    
    def create_debt_cards(self, consolidated_debts, search_name, relationship_filter, status_filter, min_amount, max_amount):
        """Create modern debt cards for display"""
        # Who owes me section
        owe_me_frame = self.create_modern_frame(self.debt_scrollable_frame)
        owe_me_frame.pack(fill="x", pady=10, padx=10)
        
        owe_me_header = ctk.CTkFrame(owe_me_frame, fg_color="transparent")
        owe_me_header.pack(fill="x", pady=10)
        
        ctk.CTkLabel(owe_me_header, text="💰 Who Owes Me", 
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color=self.colors["success"]).pack(side="left", padx=20)
        
        owe_me_count = len([p for p in consolidated_debts["Who owes me"] 
                           if p["remaining"] > 0 and self.filter_debt(p, search_name, relationship_filter, status_filter, min_amount, max_amount)])
        ctk.CTkLabel(owe_me_header, text=f"({owe_me_count} active)", 
                    font=ctk.CTkFont(size=14),
                    text_color=self.colors["gray"]).pack(side="left", padx=10)
        
        # Who I owe section
        i_owe_frame = self.create_modern_frame(self.debt_scrollable_frame)
        i_owe_frame.pack(fill="x", pady=10, padx=10)
        
        i_owe_header = ctk.CTkFrame(i_owe_frame, fg_color="transparent")
        i_owe_header.pack(fill="x", pady=10)
        
        ctk.CTkLabel(i_owe_header, text="💸 Who I Owe", 
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color=self.colors["danger"]).pack(side="left", padx=20)
        
        i_owe_count = len([p for p in consolidated_debts["Who I owe"] 
                           if p["remaining"] > 0 and self.filter_debt(p, search_name, relationship_filter, status_filter, min_amount, max_amount)])
        ctk.CTkLabel(i_owe_header, text=f"({i_owe_count} active)", 
                    font=ctk.CTkFont(size=14),
                    text_color=self.colors["gray"]).pack(side="left", padx=10)
        
        # Display filtered debts
        for person_data in consolidated_debts["Who owes me"]:
            if self.filter_debt(person_data, search_name, relationship_filter, status_filter, min_amount, max_amount):
                self.create_modern_debt_card(owe_me_frame, person_data)
        
        for person_data in consolidated_debts["Who I owe"]:
            if self.filter_debt(person_data, search_name, relationship_filter, status_filter, min_amount, max_amount):
                self.create_modern_debt_card(i_owe_frame, person_data)
    
    def create_modern_debt_card(self, parent, person_data):
        """Create a modern debt card widget"""
        remaining = person_data["remaining"]
        
        # Create card container
        card_frame = self.create_modern_frame(parent)
        card_frame.pack(fill="x", pady=8, padx=20)
        
        # Main card content
        content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        content_frame.pack(fill="x", pady=15, padx=20)
        
        # Left side - Person info
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        name_label = ctk.CTkLabel(info_frame, text=person_data["full_name"], 
                                font=ctk.CTkFont(size=18, weight="bold"),
                                text_color=self.colors["gray"])
        name_label.pack(anchor="w")
        
        relationship_label = ctk.CTkLabel(info_frame, text=f"👥 {person_data['relationship']}", 
                                       font=ctk.CTkFont(size=14),
                                       text_color=self.colors["gray"])
        relationship_label.pack(anchor="w", pady=(5, 0))
        
        # Center - Financial info
        financial_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        financial_frame.pack(side="left", padx=30)
        
        amount_text = f"₱{person_data['total_paid']:.2f}" if remaining == 0 else f"₱{remaining:.2f}"
        amount_color = self.colors["success"] if remaining == 0 else self.colors["danger"]
        amount_label = ctk.CTkLabel(financial_frame, text=amount_text, 
                                  font=ctk.CTkFont(size=20, weight="bold"),
                                  text_color=amount_color)
        amount_label.pack()
        
        # Status badge
        status = self.get_debt_status(person_data["debt_history"][-1])
        status_colors = {"Overdue": self.colors["danger"], "Pending": self.colors["warning"], "Paid": self.colors["success"]}
        status_frame = ctk.CTkFrame(financial_frame, fg_color=status_colors[status], corner_radius=15)
        status_frame.pack(pady=(5, 0))
        
        status_label = ctk.CTkLabel(status_frame, text=status, 
                                  font=ctk.CTkFont(size=12, weight="bold"),
                                  text_color=self.colors["white"])
        status_label.pack(padx=10, pady=2)
        
        # Right side - Actions
        actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        actions_frame.pack(side="right")
        
        # Action buttons
        view_btn = self.create_modern_button(actions_frame, text="👁️ Details", 
                                           command=lambda: self.toggle_debt_details(card_frame, person_data),
                                           width=100, height=35, fg_color=self.colors["info"])
        view_btn.pack(pady=2)
        
        if remaining > 0:
            pay_btn = self.create_modern_button(actions_frame, text="💳 Payment", 
                                              command=lambda: self.show_add_payment_form(person_data),
                                              width=100, height=35, fg_color=self.colors["accent"])
            pay_btn.pack(pady=2)
        else:
            reactivate_btn = self.create_modern_button(actions_frame, text="🔄 New Debt", 
                                                     command=lambda: self.show_add_debt_form(),
                                                     width=100, height=35, fg_color=self.colors["warning"])
            reactivate_btn.pack(pady=2)
        
        edit_btn = self.create_modern_button(actions_frame, text="✏️ Edit", 
                                           command=lambda: self.show_edit_debt_form(person_data),
                                           width=100, height=35, fg_color=self.colors["secondary"])
        edit_btn.pack(pady=2)
        
        delete_btn = self.create_modern_button(actions_frame, text="🗑️ Delete", 
                                             command=lambda: self.delete_person_debts(person_data),
                                             width=100, height=35, fg_color=self.colors["danger"])
        delete_btn.pack(pady=2)
        
        # Details section (initially hidden)
        details_frame = ctk.CTkFrame(card_frame, fg_color=self.colors["dark"])
        details_frame.pack_forget()
        
        card_frame.details_frame = details_frame
        card_frame.details_visible = False
        
        self.create_debt_details(details_frame, person_data)
    
    def create_debt_details(self, parent, person_data):
        """Create detailed view of debt information"""
        # Summary section
        summary_frame = ctk.CTkFrame(parent, fg_color="transparent")
        summary_frame.pack(fill="x", pady=10, padx=20)
        
        summary_text = f"""
💰 Financial Summary:
   • Total Borrowed: ₱{person_data['total_amount']:.2f}
   • Total Owed (with interest): ₱{person_data['total_owed']:.2f}
   • Total Paid: ₱{person_data['total_paid']:.2f}
   • Remaining Balance: ₱{person_data['remaining']:.2f}
        """
        
        summary_label = ctk.CTkLabel(summary_frame, text=summary_text.strip(),
                                   font=ctk.CTkFont(size=14),
                                   text_color=self.colors["gray"],
                                   justify="left")
        summary_label.pack(anchor="w")
        
        # Debt history
        history_label = ctk.CTkLabel(parent, text="📋 Debt History:",
                                   font=ctk.CTkFont(size=16, weight="bold"),
                                   text_color=self.colors["primary"])
        history_label.pack(pady=(20, 10), padx=20, anchor="w")
        
        for i, debt in enumerate(person_data['debt_history'], 1):
            debt_item_frame = ctk.CTkFrame(parent, fg_color=self.colors["light"])
            debt_item_frame.pack(fill="x", pady=2, padx=20)
            
            status = self.get_debt_status(debt)
            status_colors = {"Overdue": self.colors["danger"], "Pending": self.colors["warning"], "Paid": self.colors["success"]}
            
            debt_text = f"""
Debt #{i} - Added: {debt['date_added']} | Status: {status}
Amount: ₱{debt['amount']:.2f} | Interest: {debt['interest_rate']}% | Due: {debt['due_date']}
Total Owed: ₱{debt['owed']:.2f} | Paid: ₱{debt['payments']:.2f} | Remaining: ₱{debt['remaining']:.2f}
Notes: {debt['notes'] if debt['notes'] else 'None'}
            """
            
            debt_label = ctk.CTkLabel(debt_item_frame, text=debt_text.strip(),
                                    font=ctk.CTkFont(size=12),
                                    text_color=status_colors[status],
                                    justify="left")
            debt_label.pack(side="left", pady=10, padx=15)
            
            # Payment history
            payments = self.get_payment_history(debt["debt_id"])
            if payments:
                payment_text = "💳 Payments: " + ", ".join([f"₱{p['payment_amount']} ({p['payment_date']})" for p in payments])
                payment_label = ctk.CTkLabel(debt_item_frame, text=payment_text,
                                          font=ctk.CTkFont(size=10),
                                          text_color=self.colors["gray"])
                payment_label.pack(pady=(0, 10), padx=15)
    
    def toggle_debt_details(self, card_frame, person_data):
        """Toggle visibility of debt details"""
        if card_frame.details_visible:
            card_frame.details_frame.pack_forget()
            card_frame.details_visible = False
        else:
            card_frame.details_frame.pack(fill="x", pady=5, padx=20)
            card_frame.details_visible = True
    
    def filter_debt(self, person_data, search_name, relationship_filter, status_filter, min_amount, max_amount):
        """Filter debts based on criteria"""
        if search_name and search_name not in person_data["full_name"].lower():
            return False
        if relationship_filter != "All" and person_data["relationship"] != relationship_filter:
            return False
        if person_data["remaining"] < min_amount or person_data["remaining"] > max_amount:
            return False
        if status_filter != "All":
            has_matching_status = False
            for debt in person_data["debt_history"]:
                debt_status = self.get_debt_status(debt)
                if debt_status == status_filter:
                    has_matching_status = True
                    break
            if not has_matching_status:
                return False
        return True
    
    def load_analytics(self):
        """Load modern analytics with enhanced visualizations"""
        for widget in self.analytics_frame.winfo_children():
            widget.destroy()
        
        # Clear previous matplotlib figure
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.canvas = None
        
        # Date range filter with modern UI
        filter_frame = self.create_modern_frame(self.analytics_frame)
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        filter_label = ctk.CTkLabel(filter_frame, text="📅 Date Range Filter", 
                                  font=ctk.CTkFont(size=16, weight="bold"),
                                  text_color=self.colors["primary"])
        filter_label.pack(pady=15)
        
        date_inputs_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        date_inputs_frame.pack(pady=10)
        
        # Start date
        start_frame = ctk.CTkFrame(date_inputs_frame, fg_color="transparent")
        start_frame.pack(side="left", padx=20)
        
        ctk.CTkLabel(start_frame, text="From:", font=ctk.CTkFont(size=14, weight="bold")).pack()
        self.analytics_start_date_entry = self.create_modern_entry(start_frame, width=150, placeholder_text="YYYY-MM-DD")
        self.analytics_start_date_entry.pack(pady=5)
        
        start_cal_button = self.create_modern_button(start_frame, text="📅", width=50, height=35,
                                                   command=lambda: self.toggle_analytics_calendar("start"))
        start_cal_button.pack()
        
        self.analytics_start_cal = Calendar(filter_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.analytics_start_cal.pack_forget()
        
        # End date
        end_frame = ctk.CTkFrame(date_inputs_frame, fg_color="transparent")
        end_frame.pack(side="left", padx=20)
        
        ctk.CTkLabel(end_frame, text="To:", font=ctk.CTkFont(size=14, weight="bold")).pack()
        self.analytics_end_date_entry = self.create_modern_entry(end_frame, width=150, placeholder_text="YYYY-MM-DD")
        self.analytics_end_date_entry.pack(pady=5)
        
        end_cal_button = self.create_modern_button(end_frame, text="📅", width=50, height=35,
                                                 command=lambda: self.toggle_analytics_calendar("end"))
        end_cal_button.pack()
        
        self.analytics_end_cal = Calendar(filter_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.analytics_end_cal.pack_forget()
        
        # Apply filter button
        apply_filter_btn = self.create_modern_button(filter_frame, text="🔍 Apply Filter", 
                                                   command=self.load_analytics, width=150)
        apply_filter_btn.pack(pady=15)
        
        # Bind calendar selection events
        self.analytics_start_cal.bind("<<CalendarSelected>>",
                                    lambda e: self.update_date(self.analytics_start_date_entry, self.analytics_start_cal))
        self.analytics_end_cal.bind("<<CalendarSelected>>",
                                  lambda e: self.update_date(self.analytics_end_date_entry, self.analytics_end_cal))
        
        # Get date range
        start_date = self.analytics_start_date_entry.get().strip()
        end_date = self.analytics_end_date_entry.get().strip()
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else datetime.min
            end_date = datetime.strptime(end_date, "%Y-%m-%d") if end_date else datetime.max
        except ValueError:
            start_date = datetime.min
            end_date = datetime.max
        
        consolidated_debts = self.get_consolidated_debts(start_date, end_date)
        
        # Summary statistics with modern cards
        self.create_analytics_summary_cards(consolidated_debts)
        
        # Check if there's any data to display
        total_debts = len(consolidated_debts["Who owes me"]) + len(consolidated_debts["Who I owe"])
        
        if total_debts > 0:
            # Enhanced charts
            self.create_enhanced_charts(consolidated_debts, start_date, end_date)
        else:
            # Show no data message
            no_data_frame = ctk.CTkFrame(self.analytics_frame, fg_color="transparent")
            no_data_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            no_data_label = ctk.CTkLabel(no_data_frame, text="📊 No debt data available for the selected date range", 
                                       font=ctk.CTkFont(size=18, weight="bold"),
                                       text_color=self.colors["gray"])
            no_data_label.pack(expand=True)
            
            suggestion_label = ctk.CTkLabel(no_data_frame, text="Try adjusting the date range or add some debts first", 
                                         font=ctk.CTkFont(size=14),
                                         text_color=self.colors["light_gray"])
            suggestion_label.pack(pady=10)
    
    def create_analytics_summary_cards(self, consolidated_debts):
        """Create modern summary cards for analytics"""
        summary_frame = ctk.CTkFrame(self.analytics_frame, fg_color="transparent")
        summary_frame.pack(fill="x", padx=10, pady=10)
        
        summary_label = ctk.CTkLabel(summary_frame, text="📊 Financial Summary", 
                                   font=ctk.CTkFont(size=18, weight="bold"),
                                   text_color=self.colors["primary"])
        summary_label.pack(pady=10)
        
        # Create cards container
        cards_frame = ctk.CTkFrame(summary_frame, fg_color="transparent")
        cards_frame.pack(fill="x", pady=10)
        
        # Calculate statistics
        total_owed_who_owes_me = sum(p["total_owed"] for p in consolidated_debts["Who owes me"])
        total_owed_who_i_owe = sum(p["total_owed"] for p in consolidated_debts["Who I owe"])
        total_paid_who_owes_me = sum(p["total_paid"] for p in consolidated_debts["Who owes me"])
        total_paid_who_i_owe = sum(p["total_paid"] for p in consolidated_debts["Who I owe"])
        total_remaining_who_owes_me = sum(p["remaining"] for p in consolidated_debts["Who owes me"])
        total_remaining_who_i_owe = sum(p["remaining"] for p in consolidated_debts["Who I owe"])
        active_debts = sum(1 for p in consolidated_debts["Who owes me"] + consolidated_debts["Who I owe"]
                          for debt in p["debt_history"] if debt["remaining"] > 0)
        
        # Create individual stat cards
        stats = [
            ("💰 You're Owed", f"₱{total_remaining_who_owes_me:.2f}", self.colors["success"]),
            ("💸 You Owe", f"₱{total_remaining_who_i_owe:.2f}", self.colors["danger"]),
            ("💳 Total Paid (Owed to You)", f"₱{total_paid_who_owes_me:.2f}", self.colors["info"]),
            ("💳 Total Paid (You Owe)", f"₱{total_paid_who_i_owe:.2f}", self.colors["warning"]),
            ("📋 Active Debts", str(active_debts), self.colors["primary"])
        ]
        
        for i, (title, value, color) in enumerate(stats):
            card = self.create_modern_frame(cards_frame)
            card.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            
            ctk.CTkLabel(card, text=title, 
                        font=ctk.CTkFont(size=14, weight="bold"),
                        text_color=self.colors["gray"]).pack(pady=10)
            
            ctk.CTkLabel(card, text=value, 
                        font=ctk.CTkFont(size=20, weight="bold"),
                        text_color=color).pack(pady=5)
    
    def create_enhanced_charts(self, consolidated_debts, start_date, end_date):
        """Create enhanced charts with modern styling"""
        charts_frame = ctk.CTkFrame(self.analytics_frame, fg_color="transparent")
        charts_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        charts_label = ctk.CTkLabel(charts_frame, text="📈 Visual Analytics", 
                                  font=ctk.CTkFont(size=18, weight="bold"),
                                  text_color=self.colors["primary"])
        charts_label.pack(pady=10)
        
        try:
            # Create figure with modern styling - use theme-appropriate style
            if self.current_theme == "dark":
                plt.style.use('dark_background')
                text_color = 'white'
                fig_bg_color = self.colors["dark"]
            else:
                plt.style.use('seaborn-v0_8')  # More compatible light style
                text_color = 'black'
                fig_bg_color = self.colors["white"]
            
            self.fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))
            self.fig.patch.set_facecolor(fig_bg_color)
            
            # Pie chart: Debt distribution
            owe_me_total = sum(p["remaining"] for p in consolidated_debts["Who owes me"])
            i_owe_total = sum(p["remaining"] for p in consolidated_debts["Who I owe"])
            labels = ["Who Owes Me", "Who I Owe"]
            sizes = [owe_me_total, i_owe_total]
            colors = [self.colors["success"], self.colors["danger"]]
            
            if sum(sizes) > 0:
                wedges, texts, autotexts = ax1.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", 
                                                   startangle=90, shadow=True, explode=(0.05, 0.05))
                ax1.set_title("Debt Distribution", fontsize=14, fontweight='bold', pad=15, color=text_color)
                
                # Style the text
                for autotext in autotexts:
                    autotext.set_color(text_color)
                    autotext.set_fontweight('bold')
                
                # Style the labels
                for text in texts:
                    text.set_color(text_color)
                    text.set_fontweight('bold')
            else:
                ax1.text(0.5, 0.5, "No Data", ha="center", va="center", fontsize=14, fontweight='bold', color=text_color)
                ax1.set_title("Debt Distribution", fontsize=14, fontweight='bold', pad=15, color=text_color)
            
            # Bar chart: Remaining debt per person
            names = [p["full_name"] for p in consolidated_debts["Who owes me"] + consolidated_debts["Who I owe"]]
            amounts = [p["remaining"] for p in consolidated_debts["Who owes me"] + consolidated_debts["Who I owe"]]
            
            if amounts:
                bars = ax2.bar(range(len(names)), amounts, color=self.colors["info"], alpha=0.8, 
                              edgecolor=text_color, linewidth=1)
                ax2.set_xticks(range(len(names)))
                ax2.set_xticklabels(names, rotation=45, ha="right", color=text_color)
                ax2.set_title("Remaining Debt per Person", fontsize=14, fontweight='bold', pad=15, color=text_color)
                ax2.set_ylabel("Amount (₱)", fontsize=11, fontweight='bold', color=text_color)
                ax2.grid(True, alpha=0.3)
                ax2.tick_params(axis='both', colors=text_color)
                
                # Add value labels on bars
                for bar, amount in zip(bars, amounts):
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height + max(amounts)*0.01,
                            f'₱{amount:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold', color=text_color)
            else:
                ax2.text(0.5, 0.5, "No Data", ha="center", va="center", fontsize=14, fontweight='bold', color=text_color)
                ax2.set_title("Remaining Debt per Person", fontsize=14, fontweight='bold', pad=15, color=text_color)
            
            # Line plot: Payment history over time
            payments = self.get_payment_history_in_range(start_date, end_date)
            if payments:
                # Aggregate payments by month
                monthly_payments = {}
                for payment in payments:
                    payment_date = datetime.strptime(payment["payment_date"], "%Y-%m-%d")
                    month_key = payment_date.strftime("%Y-%m")
                    monthly_payments[month_key] = monthly_payments.get(month_key, 0) + float(payment["payment_amount"])
                
                dates = [datetime.strptime(month, "%Y-%m") for month in sorted(monthly_payments.keys())]
                amounts = [monthly_payments[month] for month in sorted(monthly_payments.keys())]
                
                ax3.plot(dates, amounts, marker='o', color=self.colors["accent"], linewidth=3, markersize=6)
                ax3.fill_between(dates, amounts, alpha=0.3, color=self.colors["accent"])
                ax3.set_title("Payment History Over Time", fontsize=14, fontweight='bold', pad=15, color=text_color)
                ax3.set_ylabel("Payment Amount (₱)", fontsize=11, fontweight='bold', color=text_color)
                ax3.grid(True, alpha=0.3)
                ax3.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
                ax3.xaxis.set_major_locator(mdates.MonthLocator())
                ax3.tick_params(axis='both', rotation=45, colors=text_color)
            else:
                ax3.text(0.5, 0.5, "No Payment Data", ha="center", va="center", fontsize=14, fontweight='bold', color=text_color)
                ax3.set_title("Payment History Over Time", fontsize=14, fontweight='bold', pad=15, color=text_color)
            
            plt.tight_layout()
            self.canvas = FigureCanvasTkAgg(self.fig, master=charts_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(pady=20)
            
        except Exception as e:
            # If charts fail, show error message
            error_label = ctk.CTkLabel(charts_frame, text=f"Error creating charts: {str(e)}", 
                                     font=ctk.CTkFont(size=14),
                                     text_color=self.colors["danger"])
            error_label.pack(pady=20)
            print(f"Chart creation error: {e}")
    
    def toggle_analytics_calendar(self, cal_type):
        """Toggle visibility of analytics calendar widget"""
        if cal_type == "start":
            calendar = self.analytics_start_cal
            other_calendar = self.analytics_end_cal
        else:
            calendar = self.analytics_end_cal
            other_calendar = self.analytics_start_cal
        
        if calendar.winfo_ismapped():
            calendar.pack_forget()
        else:
            if other_calendar and other_calendar.winfo_ismapped():
                other_calendar.pack_forget()
            calendar.pack(pady=5)
    
    def show_profile_form(self):
        """Show modern user profile information"""
        for widget in self.profile_frame.winfo_children():
            widget.destroy()
        
        # Profile header
        header_frame = self.create_modern_frame(self.profile_frame)
        header_frame.pack(fill="x", pady=10)
        
        profile_label = ctk.CTkLabel(header_frame, text="👤 User Profile", 
                                   font=ctk.CTkFont(size=24, weight="bold"),
                                   text_color=self.colors["primary"])
        profile_label.pack(pady=20)
        
        # Get user information
        registration_date = "Unknown"
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == self.current_user:
                    registration_date = row.get("registration_date", "2024-10-10")
                    break
        
        # Calculate debt statistics
        consolidated_debts = self.get_consolidated_debts()
        total_debts = sum(1 for p in consolidated_debts["Who owes me"] + consolidated_debts["Who I owe"]
                          for debt in p["debt_history"] if debt["remaining"] > 0)
        total_remaining_who_owes_me = sum(p["remaining"] for p in consolidated_debts["Who owes me"])
        total_remaining_who_i_owe = sum(p["remaining"] for p in consolidated_debts["Who I owe"])
        
        # Profile info
        info_frame = self.create_modern_frame(self.profile_frame)
        info_frame.pack(fill="x", pady=10)
        
        info_text = f"""
👤 Username: {self.current_user}
📅 Registration Date: {registration_date}
📊 Total Active Debts: {total_debts}
💰 Total Remaining (Who Owes Me): ₱{total_remaining_who_owes_me:.2f}
💸 Total Remaining (Who I Owe): ₱{total_remaining_who_i_owe:.2f}
        """
        
        info_label = ctk.CTkLabel(info_frame, text=info_text.strip(),
                                font=ctk.CTkFont(size=16),
                                text_color=self.colors["gray"],
                                justify="left")
        info_label.pack(pady=20, padx=20, anchor="w")
        
        # About section
        about_frame = self.create_modern_frame(self.profile_frame)
        about_frame.pack(fill="x", pady=10)
        
        about_label = ctk.CTkLabel(about_frame, text="ℹ️ About", 
                                 font=ctk.CTkFont(size=18, weight="bold"),
                                 text_color=self.colors["primary"])
        about_label.pack(pady=15)
        
        about_text = """This application was developed by John Allen Esteleydes to help manage personal debt tracking efficiently.

For support or questions, please contact:
📧 Email: esteleydesjohnallen0@gmail.com
📺 YouTube: Yakee
🐱 Github: Yakeeeeee"""

        about_content = ctk.CTkLabel(about_frame, text=about_text,
                                   font=ctk.CTkFont(size=14),
                                   text_color=self.colors["gray"],
                                   justify="left")
        about_content.pack(pady=10, padx=20, anchor="w")
        
        # Social links
        social_frame = ctk.CTkFrame(about_frame, fg_color="transparent")
        social_frame.pack(pady=15)
        
        youtube_btn = self.create_modern_button(social_frame, text="📺 YouTube Channel",
                                              command=lambda: webbrowser.open("https://www.youtube.com/@mr.yakeee"),
                                              width=180, fg_color=self.colors["danger"])
        youtube_btn.pack(side="left", padx=5)
        
        email_btn = self.create_modern_button(social_frame, text="📧 Contact",
                                            command=lambda: webbrowser.open("mailto:esteleydesjohnallen0@gmail.com"),
                                            width=150, fg_color=self.colors["accent"])
        email_btn.pack(side="left", padx=5)

        github_btn = self.create_modern_button(social_frame, text="🐱 Github",
                                              command=lambda: webbrowser.open("https://github.com/Yakeeeeee"),
                                              width=150, fg_color=self.colors["info"])
        github_btn.pack(side="left", padx=5)
    
    def show_change_password_form(self):
        """Show modern password change form"""
        for widget in self.profile_frame.winfo_children():
            widget.destroy()
        
        # Form header
        header_frame = self.create_modern_frame(self.profile_frame)
        header_frame.pack(fill="x", pady=10)
        
        title_label = ctk.CTkLabel(header_frame, text="🔑 Change Password", 
                                 font=ctk.CTkFont(size=24, weight="bold"),
                                 text_color=self.colors["primary"])
        title_label.pack(pady=20)
        
        # Form content
        form_frame = self.create_modern_frame(self.profile_frame)
        form_frame.pack(fill="x", pady=10, padx=100)
        
        # Current password
        ctk.CTkLabel(form_frame, text="🔒 Current Password:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["dark"]).pack(pady=10)
        
        self.current_password_entry = self.create_modern_entry(form_frame, width=400, show="•")
        self.current_password_entry.pack(pady=5)
        
        # New password
        ctk.CTkLabel(form_frame, text="🔑 New Password:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["dark"]).pack(pady=10)
        
        self.new_password_entry = self.create_modern_entry(form_frame, width=400, show="•")
        self.new_password_entry.pack(pady=5)
        
        # Confirm password
        ctk.CTkLabel(form_frame, text="✅ Confirm New Password:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["dark"]).pack(pady=10)
        
        self.confirm_password_entry = self.create_modern_entry(form_frame, width=400, show="•")
        self.confirm_password_entry.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=25)
        
        save_btn = self.create_modern_button(button_frame, text="💾 Save Changes", 
                                           command=self.update_password, width=160)
        save_btn.pack(side="left", padx=10)
        
        back_btn = self.create_modern_button(button_frame, text="← Back to Profile", 
                                           command=self.show_profile_form, width=160, fg_color=self.colors["gray"])
        back_btn.pack(side="left", padx=10)
    
    def update_password(self):
        """Update user's password with modern confirmation"""
        current_password = self.current_password_entry.get().strip()
        new_password = self.new_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        
        if not all([current_password, new_password, confirm_password]):
            messagebox.showerror("❌ Error", "Please fill all password fields")
            return
        
        if len(new_password) < 6:
            messagebox.showerror("❌ Error", "New password must be at least 6 characters long")
            return
        
        if new_password != confirm_password:
            messagebox.showerror("❌ Error", "New password and confirmation do not match")
            return
        
        # Verify current password
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == self.current_user:
                    if row["password_hash"] != self.hash_password(current_password):
                        messagebox.showerror("❌ Error", "Current password is incorrect")
                        return
                    break
            else:
                messagebox.showerror("❌ Error", "User not found")
                return
        
        # Confirm password change
        if not messagebox.askyesno("⚠️ Confirm Password Change", 
                                 "Are you sure you want to change your password?"):
            return
        
        # Update password
        users = []
        with open("users.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == self.current_user:
                    users.append({
                        "username": self.current_user,
                        "password_hash": self.hash_password(new_password),
                        "registration_date": row.get("registration_date", "2025-07-19")
                    })
                else:
                    users.append(row)
        
        with open("users.csv", "w", newline="") as file:
            fieldnames = ["username", "password_hash", "registration_date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)
        
        messagebox.showinfo("✅ Success", "Password updated successfully!")
        self.show_profile_form()
    
    # Core data management methods
    def get_consolidated_debts(self, start_date=None, end_date=None):
        """Get debts consolidated by person and relationship within date range"""
        debts = self.get_user_debts()
        consolidated = {"Who owes me": {}, "Who I owe": {}}
        
        for debt in debts:
            debt_date = datetime.strptime(debt["date_added"], "%Y-%m-%d")
            if start_date and debt_date < start_date:
                continue
            if end_date and debt_date > end_date:
                continue
                
            relationship = debt["relationship"]
            name = debt["full_name"]
            
            if name not in consolidated[relationship]:
                consolidated[relationship][name] = {
                    "full_name": name,
                    "relationship": relationship,
                    "debt_history": [],
                    "total_amount": 0,
                    "total_paid": 0,
                    "total_owed": 0,
                    "remaining": 0,
                    "latest_due_date": debt["due_date"] if debt["due_date"] != "N/A" else "N/A"
                }
            
            debt_payments = self.get_total_payments(debt["debt_id"], start_date, end_date)
            debt_owed = float(debt["amount"]) * (1 + float(debt["interest_rate"]) / 100)
            debt_remaining = debt_owed - debt_payments
            
            consolidated[relationship][name]["debt_history"].append({
                "debt_id": debt["debt_id"],
                "amount": float(debt["amount"]),
                "interest_rate": float(debt["interest_rate"]),
                "date_added": debt["date_added"],
                "due_date": debt["due_date"],
                "notes": debt["notes"],
                "payments": debt_payments,
                "owed": debt_owed,
                "remaining": debt_remaining
            })
            
            consolidated[relationship][name]["total_amount"] += float(debt["amount"])
            consolidated[relationship][name]["total_paid"] += debt_payments
            consolidated[relationship][name]["total_owed"] += debt_owed
            consolidated[relationship][name]["remaining"] += debt_remaining
            
            if debt["due_date"] != "N/A" and (consolidated[relationship][name]["latest_due_date"] == "N/A" or 
                                              debt["due_date"] > consolidated[relationship][name]["latest_due_date"]):
                consolidated[relationship][name]["latest_due_date"] = debt["due_date"]
        
        result = {
            "Who owes me": list(consolidated["Who owes me"].values()),
            "Who I owe": list(consolidated["Who I owe"].values())
        }
        
        return result
    
    def get_user_debts(self):
        """Get all debts for current user"""
        debts = []
        with open("debt_data.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["user"] == self.current_user:
                    debts.append(row)
        return debts
    
    def get_total_payments(self, debt_id, start_date=None, end_date=None):
        """Calculate total payments for a debt within date range"""
        total = 0
        with open("payments.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["debt_id"] == debt_id:
                    payment_date = datetime.strptime(row["payment_date"], "%Y-%m-%d")
                    if (start_date is None or payment_date >= start_date) and \
                       (end_date is None or payment_date <= end_date):
                        total += float(row["payment_amount"])
        return total
    
    def get_payment_history(self, debt_id):
        """Get payment history for a debt"""
        payments = []
        with open("payments.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["debt_id"] == debt_id:
                    payments.append(row)
        return payments
    
    def get_payment_history_in_range(self, start_date, end_date):
        """Get payment history within date range for all debts"""
        payments = []
        with open("payments.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                payment_date = datetime.strptime(row["payment_date"], "%Y-%m-%d")
                if (start_date is None or payment_date >= start_date) and \
                   (end_date is None or payment_date <= end_date):
                    debt = next((d for d in self.get_user_debts() if d["debt_id"] == row["debt_id"]), None)
                    if debt and debt["user"] == self.current_user:
                        payments.append(row)
        return sorted(payments, key=lambda x: x["payment_date"])
    
    def update_date(self, entry, calendar):
        """Update date entry with selected calendar date"""
        entry.delete(0, "end")
        entry.insert(0, calendar.get_date())
        calendar.pack_forget()
    
    def delete_person_debts(self, person_data):
        """Delete all debt entries and payments for a person"""
        if not messagebox.askyesno("⚠️ Confirm Delete", 
                                  f"Are you sure you want to delete ALL debts for {person_data['full_name']}?"):
            return
            
        debt_ids_to_delete = [debt["debt_id"] for debt in person_data["debt_history"]]
        
        # Filter out debts
        debts = []
        with open("debt_data.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["debt_id"] not in debt_ids_to_delete:
                    debts.append(row)
        
        with open("debt_data.csv", "w", newline="") as file:
            fieldnames = ["user", "full_name", "amount", "relationship", "interest_rate", 
                         "date_added", "due_date", "notes", "status", "debt_id"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(debts)
        
        # Filter out payments
        payments = []
        with open("payments.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["debt_id"] not in debt_ids_to_delete:
                    payments.append(row)
        
        with open("payments.csv", "w", newline="") as file:
            fieldnames = ["debt_id", "payment_amount", "payment_date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(payments)
        
        messagebox.showinfo("✅ Success", f"All debts for {person_data['full_name']} deleted successfully!")
        self.load_debts()
    
    def destroy(self):
        """Clean up resources and close the application"""
        if self.fig is not None:
            plt.close(self.fig)
        self.root.destroy()
    
    def show_add_debt_form(self):
        """Show modern add debt form"""
        self.current_view = "add_debt"
        self.clear_main_frame()
        
        # Header
        header_frame = self.create_modern_frame(self.main_frame)
        header_frame.pack(fill="x", pady=10)
        
        title_label = ctk.CTkLabel(header_frame, text="➕ Add New Debt", 
                                 font=ctk.CTkFont(size=24, weight="bold"),
                                 text_color=self.colors["primary"])
        title_label.pack(pady=20)
        
        # Form content
        scrollable_form = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        scrollable_form.pack(fill="both", expand=True, pady=10, padx=20)
        
        form_frame = self.create_modern_frame(scrollable_form)
        form_frame.pack(pady=20, padx=100, fill="x")
        
        # Form fields
        ctk.CTkLabel(form_frame, text="👤 Full Name:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["dark"]).pack(pady=10)
        
        self.name_entry = self.create_modern_entry(form_frame, width=400)
        self.name_entry.pack(pady=5)
        
        ctk.CTkLabel(form_frame, text="💰 Amount:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        self.amount_entry = self.create_modern_entry(form_frame, width=400)
        self.amount_entry.pack(pady=5)
        
        ctk.CTkLabel(form_frame, text="👥 Relationship Type:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        self.relationship_var = ctk.StringVar(value="Who owes me")
        relationship_menu = ctk.CTkOptionMenu(form_frame, variable=self.relationship_var,
                                            values=["Who owes me", "Who I owe"],
                                            width=400, height=35)
        relationship_menu.pack(pady=5)
        
        ctk.CTkLabel(form_frame, text="📈 Interest Rate (%):", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        self.interest_entry = self.create_modern_entry(form_frame, width=400)
        self.interest_entry.pack(pady=5)
        
        # Date fields
        ctk.CTkLabel(form_frame, text="📅 Date Added:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_frame.pack(pady=5)
        
        self.date_added_entry = self.create_modern_entry(date_frame, width=340)
        self.date_added_entry.pack(side="left", padx=(0, 5))
        self.date_added_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        self.date_added_cal_button = self.create_modern_button(date_frame, text="📅", width=50, height=35,
                                                             command=lambda: self.toggle_calendar(form_frame, 
                                                                self.date_added_entry, "date_added"))
        self.date_added_cal_button.pack(side="left")
        
        self.date_added_cal = Calendar(form_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.date_added_cal.pack_forget()
        self.date_added_cal.bind("<<CalendarSelected>>", 
                                lambda e: self.update_date(self.date_added_entry, self.date_added_cal))
        
        # Due date
        ctk.CTkLabel(form_frame, text="⏰ Due Date (optional):", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        due_date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        due_date_frame.pack(pady=5)
        
        self.due_date_entry = self.create_modern_entry(due_date_frame, width=340, placeholder_text="N/A")
        self.due_date_entry.pack(side="left", padx=(0, 5))
        
        self.due_date_cal_button = self.create_modern_button(due_date_frame, text="📅", width=50, height=35,
                                                           command=lambda: self.toggle_calendar(form_frame, 
                                                              self.due_date_entry, "due_date"))
        self.due_date_cal_button.pack(side="left")
        
        self.due_date_cal = Calendar(form_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.due_date_cal.pack_forget()
        self.due_date_cal.bind("<<CalendarSelected>>", 
                              lambda e: self.update_date(self.due_date_entry, self.due_date_cal))
        
        # Notes
        ctk.CTkLabel(form_frame, text="📝 Notes (optional):", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        self.notes_entry = ctk.CTkTextbox(form_frame, width=400, height=80)
        self.notes_entry.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=25)
        
        save_btn = self.create_modern_button(button_frame, text="💾 Save Debt", 
                                           command=self.save_debt, width=160)
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = self.create_modern_button(button_frame, text="❌ Cancel", 
                                             command=self.show_dashboard, width=160, fg_color=self.colors["gray"])
        cancel_btn.pack(side="left", padx=10)
    
    def show_quick_add_debt_form(self):
        """Show modern quick add debt form"""
        self.current_view = "quick_add_debt"
        self.clear_main_frame()
        
        # Header
        header_frame = self.create_modern_frame(self.main_frame)
        header_frame.pack(fill="x", pady=10)
        
        title_label = ctk.CTkLabel(header_frame, text="⚡ Quick Add Debt", 
                                 font=ctk.CTkFont(size=24, weight="bold"),
                                 text_color=self.colors["primary"])
        title_label.pack(pady=20)
        
        # Form content
        form_frame = self.create_modern_frame(self.main_frame)
        form_frame.pack(pady=20, padx=100, fill="x")
        
        # Form fields
        ctk.CTkLabel(form_frame, text="👤 Full Name:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        self.quick_name_entry = self.create_modern_entry(form_frame, width=400)
        self.quick_name_entry.pack(pady=5)
        
        ctk.CTkLabel(form_frame, text="💰 Amount:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        self.quick_amount_entry = self.create_modern_entry(form_frame, width=400)
        self.quick_amount_entry.pack(pady=5)
        
        ctk.CTkLabel(form_frame, text="👥 Relationship Type:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        self.quick_relationship_var = ctk.StringVar(value="Who owes me")
        relationship_menu = ctk.CTkOptionMenu(form_frame, variable=self.quick_relationship_var,
                                            values=["Who owes me", "Who I owe"],
                                            width=400, height=35)
        relationship_menu.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=25)
        
        save_btn = self.create_modern_button(button_frame, text="💾 Save Debt", 
                                           command=self.save_quick_debt, width=160)
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = self.create_modern_button(button_frame, text="❌ Cancel", 
                                             command=self.show_dashboard, width=160, fg_color=self.colors["gray"])
        cancel_btn.pack(side="left", padx=10)
    
    def save_quick_debt(self):
        """Save quick debt entry with default values"""
        name = self.quick_name_entry.get().strip()
        amount = self.quick_amount_entry.get().strip()
        relationship = self.quick_relationship_var.get()
        
        if not all([name, amount]):
            messagebox.showerror("❌ Error", "Please fill all required fields")
            return
        
        try:
            float(amount)
        except ValueError:
            messagebox.showerror("❌ Error", "Amount must be a number")
            return
        
        debt_id = f"{self.current_user}_{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        with open("debt_data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.current_user, name, amount, relationship, "0",
                           datetime.now().strftime("%Y-%m-%d"), "N/A", "", "active", debt_id])
        
        messagebox.showinfo("✅ Success", "Debt added successfully!")
        self.show_dashboard()
    
    def save_debt(self):
        """Save new debt entry with validation"""
        name = self.name_entry.get().strip()
        amount = self.amount_entry.get().strip()
        relationship = self.relationship_var.get()
        interest = self.interest_entry.get().strip()
        date_added = self.date_added_entry.get().strip()
        due_date = self.due_date_entry.get().strip()
        notes = self.notes_entry.get("1.0", "end").strip()
        
        if not all([name, amount, interest, date_added]):
            messagebox.showerror("❌ Error", "Please fill all required fields (Due Date is optional)")
            return
        
        try:
            float(amount)
            float(interest)
        except ValueError:
            messagebox.showerror("❌ Error", "Amount and interest rate must be numbers")
            return
        
        try:
            datetime.strptime(date_added, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("❌ Error", "Date added must be in YYYY-MM-DD format")
            return
        
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("❌ Error", "Due date must be in YYYY-MM-DD format")
                return
        else:
            due_date = "N/A"
        
        debt_id = f"{self.current_user}_{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        with open("debt_data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.current_user, name, amount, relationship, interest,
                           date_added, due_date, notes, "active", debt_id])
        
        messagebox.showinfo("✅ Success", "Debt added successfully!")
        self.show_dashboard()
    
    def toggle_calendar(self, parent, entry, cal_type):
        """Toggle visibility of calendar widget"""
        if cal_type == "date_added":
            calendar = self.date_added_cal
            other_calendar = self.due_date_cal if hasattr(self, 'due_date_cal') else None
        elif cal_type == "due_date":
            calendar = self.due_date_cal
            other_calendar = self.date_added_cal if hasattr(self, 'date_added_cal') else None
        else:
            calendar = self.edit_due_date_cal
            other_calendar = self.edit_date_added_cal if hasattr(self, 'edit_date_added_cal') else None
            
        if calendar.winfo_ismapped():
            calendar.pack_forget()
        else:
            if other_calendar and other_calendar.winfo_ismapped():
                other_calendar.pack_forget()
            calendar.pack(pady=5)
    
    def show_add_payment_form(self, person_data):
        """Show modern add payment form"""
        self.current_view = "add_payment"
        self.selected_person_data = person_data
        self.clear_main_frame()
        
        # Header
        header_frame = self.create_modern_frame(self.main_frame)
        header_frame.pack(fill="x", pady=10)
        
        title_label = ctk.CTkLabel(header_frame, text=f"💳 Add Payment for {person_data['full_name']}", 
                                 font=ctk.CTkFont(size=24, weight="bold"),
                                 text_color=self.colors["primary"])
        title_label.pack(pady=20)
        
        # Balance info
        balance_frame = self.create_modern_frame(self.main_frame)
        balance_frame.pack(fill="x", pady=10)
        
        balance_label = ctk.CTkLabel(balance_frame, text=f"💰 Current Balance: ₱{person_data['remaining']:.2f}", 
                                   font=ctk.CTkFont(size=18, weight="bold"),
                                   text_color=self.colors["danger"])
        balance_label.pack(pady=20)
        
        # Form content
        form_frame = self.create_modern_frame(self.main_frame)
        form_frame.pack(pady=20, padx=100, fill="x")
        
        # Payment amount
        ctk.CTkLabel(form_frame, text="💵 Payment Amount:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["dark"]).pack(pady=10)
        
        self.payment_entry = self.create_modern_entry(form_frame, width=400)
        self.payment_entry.pack(pady=5)
        
        # Payment date
        ctk.CTkLabel(form_frame, text="📅 Payment Date:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["dark"]).pack(pady=10)
        
        payment_date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        payment_date_frame.pack(pady=5)
        
        self.payment_date_entry = self.create_modern_entry(payment_date_frame, width=340)
        self.payment_date_entry.pack(side="left", padx=(0, 5))
        self.payment_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        self.payment_date_cal_button = self.create_modern_button(payment_date_frame, text="📅", width=50, height=35,
                                                               command=lambda: self.toggle_payment_calendar(form_frame))
        self.payment_date_cal_button.pack(side="left")
        
        self.payment_date_cal = Calendar(form_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.payment_date_cal.pack_forget()
        self.payment_date_cal.bind("<<CalendarSelected>>", 
                                  lambda e: self.update_date(self.payment_date_entry, self.payment_date_cal))
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=25)
        
        save_btn = self.create_modern_button(button_frame, text="💾 Save Payment", 
                                           command=self.save_payment, width=160)
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = self.create_modern_button(button_frame, text="❌ Cancel", 
                                             command=self.show_dashboard, width=160, fg_color=self.colors["gray"])
        cancel_btn.pack(side="left", padx=10)
    
    def toggle_payment_calendar(self, parent):
        """Toggle visibility of payment date calendar"""
        if self.payment_date_cal.winfo_ismapped():
            self.payment_date_cal.pack_forget()
        else:
            self.payment_date_cal.pack(pady=5)
    
    def save_payment(self):
        """Save payment for selected person with validation"""
        amount = self.payment_entry.get().strip()
        date = self.payment_date_entry.get().strip()
        
        if not amount or not date:
            messagebox.showerror("❌ Error", "Please enter payment amount and date")
            return
        
        try:
            payment_amount = float(amount)
        except ValueError:
            messagebox.showerror("❌ Error", "Payment amount must be a number")
            return
        
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("❌ Error", "Date must be in YYYY-MM-DD format")
            return
        
        remaining = self.selected_person_data["remaining"]
        
        if payment_amount > remaining:
            messagebox.showerror("❌ Error", f"Payment amount (₱{payment_amount:.2f}) exceeds remaining balance (₱{remaining:.2f})")
            return
        
        if payment_amount <= 0:
            messagebox.showerror("❌ Error", "Payment amount must be greater than zero")
            return
        
        # Apply payment to debts
        remaining_payment = payment_amount
        for debt in self.selected_person_data['debt_history']:
            if remaining_payment <= 0:
                break
            if debt['remaining'] > 0:
                payment_to_apply = min(remaining_payment, debt['remaining'])
                
                with open("payments.csv", "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([debt["debt_id"], payment_to_apply, date])
                
                remaining_payment -= payment_to_apply
        
        messagebox.showinfo("✅ Success", "Payment added successfully!")
        self.show_dashboard()
    
    def show_edit_debt_form(self, person_data):
        """Show modern edit debt form"""
        self.current_view = "edit_debt"
        self.selected_person_data = person_data
        self.clear_main_frame()
        
        # Header
        header_frame = self.create_modern_frame(self.main_frame)
        header_frame.pack(fill="x", pady=10)
        
        title_label = ctk.CTkLabel(header_frame, text=f"✏️ Edit Debt for {person_data['full_name']}", 
                                  font=ctk.CTkFont(size=24, weight="bold"),
                                  text_color=self.colors["primary"])
        title_label.pack(pady=20)
        
        # Current debt info
        current_debt_info = ctk.CTkLabel(header_frame, text="Select a debt below to edit its details", 
                                        font=ctk.CTkFont(size=14),
                                        text_color=self.colors["gray"])
        current_debt_info.pack(pady=(0, 20))
        
        self.current_debt_info_label = current_debt_info
        
        # Form content
        scrollable_form = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        scrollable_form.pack(fill="both", expand=True, pady=10, padx=20)
        
        form_frame = self.create_modern_frame(scrollable_form)
        form_frame.pack(pady=20, padx=100, fill="x")
        
        # Debt selection
        ctk.CTkLabel(form_frame, text="📋 Select Debt to Edit:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        # Create debt selection frame
        debt_selection_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        debt_selection_frame.pack(fill="x", pady=5)
        
        self.selected_debt_var = ctk.StringVar()
        self.selected_debt_var.set(person_data['debt_history'][0]['debt_id'])
        
        for i, debt in enumerate(person_data['debt_history']):
            debt_radio = ctk.CTkRadioButton(debt_selection_frame, 
                                           text=f"Debt #{i+1}: ₱{debt['amount']:.2f} - {debt['date_added']} - Status: {self.get_debt_status(debt)}",
                                           variable=self.selected_debt_var,
                                           value=debt['debt_id'],
                                           command=lambda: self.load_debt_for_edit())
            debt_radio.pack(anchor="w", pady=3, padx=10)
        
        # Form fields
        ctk.CTkLabel(form_frame, text="👤 Full Name:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        self.edit_name_entry = self.create_modern_entry(form_frame, width=400)
        self.edit_name_entry.pack(pady=5)
        self.edit_name_entry.insert(0, person_data['full_name'])
        
        ctk.CTkLabel(form_frame, text="💰 Amount:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        self.edit_amount_entry = self.create_modern_entry(form_frame, width=400)
        self.edit_amount_entry.pack(pady=5)
        
        ctk.CTkLabel(form_frame, text="👥 Relationship Type:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        self.edit_relationship_var = ctk.StringVar(value=person_data['relationship'])
        relationship_menu = ctk.CTkOptionMenu(form_frame, variable=self.edit_relationship_var,
                                            values=["Who owes me", "Who I owe"],
                                            width=400, height=35)
        relationship_menu.pack(pady=5)
        
        ctk.CTkLabel(form_frame, text="📈 Interest Rate (%):", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        self.edit_interest_entry = self.create_modern_entry(form_frame, width=400)
        self.edit_interest_entry.pack(pady=5)
        
        # Date fields
        ctk.CTkLabel(form_frame, text="📅 Date Added:", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_frame.pack(pady=5)
        
        self.edit_date_added_entry = self.create_modern_entry(date_frame, width=340)
        self.edit_date_added_entry.pack(side="left", padx=(0, 5))
        
        self.edit_date_added_cal_button = self.create_modern_button(date_frame, text="📅", width=50, height=35,
                                                                  command=lambda: self.toggle_edit_calendar(form_frame, 
                                                                     self.edit_date_added_entry, "date_added"))
        self.edit_date_added_cal_button.pack(side="left")
        
        self.edit_date_added_cal = Calendar(form_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.edit_date_added_cal.pack_forget()
        self.edit_date_added_cal.bind("<<CalendarSelected>>", 
                                    lambda e: self.update_date(self.edit_date_added_entry, self.edit_date_added_cal))
        
        # Due date
        ctk.CTkLabel(form_frame, text="⏰ Due Date (optional):", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        due_date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        due_date_frame.pack(pady=5)
        
        self.edit_due_date_entry = self.create_modern_entry(due_date_frame, width=340, placeholder_text="N/A")
        self.edit_due_date_entry.pack(side="left", padx=(0, 5))
        
        self.edit_due_date_cal_button = self.create_modern_button(due_date_frame, text="📅", width=50, height=35,
                                                                command=lambda: self.toggle_edit_calendar(form_frame, 
                                                                   self.edit_due_date_entry, "due_date"))
        self.edit_due_date_cal_button.pack(side="left")
        
        self.edit_due_date_cal = Calendar(form_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.edit_due_date_cal.pack_forget()
        self.edit_due_date_cal.bind("<<CalendarSelected>>", 
                                  lambda e: self.update_date(self.edit_due_date_entry, self.edit_due_date_cal))
        
        # Notes
        ctk.CTkLabel(form_frame, text="📝 Notes (optional):", 
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color=self.colors["gray"]).pack(pady=10)
        
        self.edit_notes_entry = ctk.CTkTextbox(form_frame, width=400, height=80)
        self.edit_notes_entry.pack(pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=25)
        
        save_btn = self.create_modern_button(button_frame, text="💾 Save Changes", 
                                           command=self.save_edited_debt, width=160)
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = self.create_modern_button(button_frame, text="❌ Cancel", 
                                             command=self.show_dashboard, width=160, fg_color=self.colors["gray"])
        cancel_btn.pack(side="left", padx=10)
        
        # Load initial debt data
        self.load_debt_for_edit()
    
    def load_debt_for_edit(self):
        """Load selected debt data into edit form"""
        if not hasattr(self, 'selected_debt_var'):
            return
            
        selected_debt_id = self.selected_debt_var.get()
        selected_debt = None
        
        for debt in self.selected_person_data['debt_history']:
            if debt['debt_id'] == selected_debt_id:
                selected_debt = debt
                break
        
        if selected_debt:
            # Update the info label
            if hasattr(self, 'current_debt_info_label'):
                self.current_debt_info_label.configure(text=f"Editing: ₱{selected_debt['amount']:.2f} - {selected_debt['date_added']} - Status: {self.get_debt_status(selected_debt)}")
            
            # Clear and populate fields
            self.edit_amount_entry.delete(0, "end")
            self.edit_amount_entry.insert(0, str(selected_debt['amount']))
            
            self.edit_interest_entry.delete(0, "end")
            self.edit_interest_entry.insert(0, str(selected_debt['interest_rate']))
            
            self.edit_date_added_entry.delete(0, "end")
            self.edit_date_added_entry.insert(0, selected_debt['date_added'])
            
            self.edit_due_date_entry.delete(0, "end")
            if selected_debt['due_date'] != "N/A":
                self.edit_due_date_entry.insert(0, selected_debt['due_date'])
            
            self.edit_notes_entry.delete("1.0", "end")
            if selected_debt.get('notes'):
                self.edit_notes_entry.insert("1.0", selected_debt['notes'])
    
    def toggle_edit_calendar(self, parent, entry, cal_type):
        """Toggle visibility of edit calendar widget"""
        if cal_type == "date_added":
            calendar = self.edit_date_added_cal
            other_calendar = self.edit_due_date_cal if hasattr(self, 'edit_due_date_cal') else None
        elif cal_type == "due_date":
            calendar = self.edit_due_date_cal
            other_calendar = self.edit_date_added_cal if hasattr(self, 'edit_date_added_cal') else None
        
        if calendar.winfo_ismapped():
            calendar.pack_forget()
        else:
            if other_calendar and other_calendar.winfo_ismapped():
                other_calendar.pack_forget()
            calendar.pack(pady=5)
    
    def save_edited_debt(self):
        """Save edited debt entry with validation"""
        name = self.edit_name_entry.get().strip()
        amount = self.edit_amount_entry.get().strip()
        relationship = self.edit_relationship_var.get()
        interest = self.edit_interest_entry.get().strip()
        date_added = self.edit_date_added_entry.get().strip()
        due_date = self.edit_due_date_entry.get().strip()
        notes = self.edit_notes_entry.get("1.0", "end").strip()
        selected_debt_id = self.selected_debt_var.get()
        
        if not all([name, amount, interest, date_added]):
            messagebox.showerror("❌ Error", "Please fill all required fields (Due Date is optional)")
            return
        
        try:
            float(amount)
            float(interest)
        except ValueError:
            messagebox.showerror("❌ Error", "Amount and interest rate must be numbers")
            return
        
        try:
            datetime.strptime(date_added, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("❌ Error", "Date added must be in YYYY-MM-DD format")
            return
        
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("❌ Error", "Due date must be in YYYY-MM-DD format")
                return
        else:
            due_date = "N/A"
        
        # Update the debt in CSV
        debts = []
        with open("debt_data.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["debt_id"] == selected_debt_id:
                    # Update the debt
                    debts.append({
                        "user": self.current_user,
                        "full_name": name,
                        "amount": amount,
                        "relationship": relationship,
                        "interest_rate": interest,
                        "date_added": date_added,
                        "due_date": due_date,
                        "notes": notes,
                        "status": "active",
                        "debt_id": selected_debt_id
                    })
                else:
                    debts.append(row)
        
        with open("debt_data.csv", "w", newline="") as file:
            fieldnames = ["user", "full_name", "amount", "relationship", "interest_rate", 
                         "date_added", "due_date", "notes", "status", "debt_id"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(debts)
        
        messagebox.showinfo("✅ Success", "Debt updated successfully!")
        self.show_dashboard()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

    def get_dark_colors(self):
        """Get dark mode color scheme"""
        return {
            "primary": "#1f538d",
            "secondary": "#14375e",
            "accent": "#4CAF50",
            "warning": "#FF9800",
            "danger": "#F44336",
            "success": "#4CAF50",
            "info": "#2196F3",
            "light": "#2d3748",  # Dark gray instead of light
            "dark": "#1a202c",   # Darker background
            "white": "#2d3748",  # Dark gray instead of white
            "gray": "#a0aec0",   # Lighter gray for text
            "light_gray": "#4a5568"  # Medium dark gray
        }
    
    def get_light_colors(self):
        """Get light mode color scheme"""
        return {
            "primary": "#1f538d",
            "secondary": "#14375e",
            "accent": "#4CAF50",
            "warning": "#FF9800",
            "danger": "#F44336",
            "success": "#4CAF50",
            "info": "#2196F3",
            "light": "#f8f9fa",  # Light gray
            "dark": "#ffffff",    # White background
            "white": "#ffffff",   # White
            "gray": "#6c757d",    # Dark gray for text
            "light_gray": "#e9ecef"  # Light gray
        }

if __name__ == "__main__":
    try:
        print("Starting Modern Utang Tracker...")
        app = ModernUtangTracker()
        print("Application initialized successfully")
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
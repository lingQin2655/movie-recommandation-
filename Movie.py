import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import json
import os

# Set global appearance and color theme
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class Movie:
    def __init__(self):
        # Initialize the main window
        self.root = ctk.CTk()
        self.root.title("Movie Recommendation System")
        self.root.geometry("1200x850")
        self.root.resizable(False, False)

        # Outer background color for the main window
        self.root.configure(fg_color="#F0F2F5")
        
        # Load users from file storage instead of hardcoded dictionary
        self.users_file = "users_db.json"
        self.users = self.load_users()
        
        # Start by showing the login screen
        self.show_login_screen()
        
        # Run the application loop
        self.root.mainloop()

    def load_users(self):
        """Loads users from a JSON file and ensures default admins always exist."""
        default_users = {
            "simjy": {"password": "JySim1192", "role": "admin"},
            "limxq": {"password": "Limxq0089", "role": "admin"},
        }
        
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, "r") as file:
                    users = json.load(file)
                    # Ensure default admins exist even if file exists
                    for k, v in default_users.items():
                        if k not in users:
                            users[k] = v
                    return users
            except Exception:
                return default_users
        else:
            self.save_users(default_users)
            return default_users

    def save_users(self, users_data):
        """Saves the current user dictionary to the JSON file."""
        with open(self.users_file, "w") as file:
            json.dump(users_data, file, indent=4)

    def clear_window(self):
        """Removes all widgets from the current window."""
        for widget in self.root.winfo_children():
            widget.destroy()




    #login screen
    def show_login_screen(self):
        """Displays the modern login form card with an image."""
        self.clear_window()
        self.root.title("Movie Recommendation - Login")

        card = ctk.CTkFrame(
            self.root, width=500, height=600, corner_radius=50,  # Made card slightly taller to fit the image
            fg_color="#AECFFB", border_width=1, border_color="#ABCDF9"
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

       #Import logo image 
        try:
            pil_image = Image.open("logo.png")  # Ensure 'logo.png' is in your folder
            self.logo_img = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(120, 100))
            
            logo_label = ctk.CTkLabel(card, text="", image=self.logo_img)
            logo_label.place(relx=0.5, y=50, anchor="center")
        except Exception as e:
            print("Could not load image. Make sure 'logo.png' is in the folder.")

        # Title & Subtitle (Adjusted 'y' coordinates down slightly to make room for the image)
        ctk.CTkLabel(
            card, text="System Login", font=("Segoe UI", 26, "bold"), text_color="#1A1A1A"
        ).place(relx=0.5, y=100, anchor="center")

        ctk.CTkLabel(
            card, text="Enter your credentials to continue", font=("Segoe UI", 13), text_color="#6E7781"
        ).place(relx=0.5, y=140, anchor="center")

        # Username Field
        ctk.CTkLabel(
            card, text="Username", font=("Segoe UI", 13, "bold"), text_color="#333333"
        ).place(x=60, y=180)
        
        self.username_entry = ctk.CTkEntry(
            card, width=360, height=42, corner_radius=10, 
            placeholder_text="Enter your username", font=("Segoe UI", 13)
        )
        self.username_entry.place(x=60, y=210)

        # Password Field
        ctk.CTkLabel(
            card, text="Password", font=("Segoe UI", 13, "bold"), text_color="#333333"
        ).place(x=60, y=270)
        
        self.password_entry = ctk.CTkEntry(
            card, width=360, height=42, corner_radius=10, 
            placeholder_text="Enter your password", show="•", font=("Segoe UI", 13)
        )
        self.password_entry.place(x=60, y=300)

        # Login Button
        ctk.CTkButton(
            card, text="Login", width=360, height=45, corner_radius=10,
            font=("Segoe UI", 15, "bold"), fg_color="#2563EB", hover_color="#1D4ED8",
            cursor="hand2", command=self.verify_login
        ).place(x=60, y=380)

        # Sign Up Navigation Button
        ctk.CTkButton(
            card, text="Don't have an account? Sign Up", font=("Segoe UI", 12, "underline"),
            fg_color="transparent", text_color="#2563EB", hover_color="#F3F4F6",
            cursor="hand2", command=self.show_signup_screen
        ).place(relx=0.5, y=470, anchor="center")

   
    #sign up screen
    def show_signup_screen(self):
        """Displays the Sign Up (Registration) form card."""
        self.clear_window()
        self.root.title("Movie Recommendation - Sign Up")

        card = ctk.CTkFrame(
            self.root, width=480, height=520, corner_radius=20, 
            fg_color="#AECFFB", border_width=1, border_color="#ABCDF9"
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            card, text="Create New Account", font=("Segoe UI", 26, "bold"), text_color="#1A1A1A"
        ).place(relx=0.5, y=55, anchor="center")

        ctk.CTkLabel(
            card, text="Sign up to explore recommendations", font=("Segoe UI", 13), text_color="#6E7781"
        ).place(relx=0.5, y=95, anchor="center")

        ctk.CTkLabel(
            card, text="Choose Username", font=("Segoe UI", 13, "bold"), text_color="#333333"
        ).place(x=60, y=145)
        
        self.new_username_entry = ctk.CTkEntry(
            card, width=360, height=42, corner_radius=10, 
            placeholder_text="Choose a unique username", font=("Segoe UI", 13)
        )
        self.new_username_entry.place(x=60, y=175)

        ctk.CTkLabel(
            card, text="Choose Password", font=("Segoe UI", 13, "bold"), text_color="#333333"
        ).place(x=60, y=235)
        
        self.new_password_entry = ctk.CTkEntry(
            card, width=360, height=42, corner_radius=10, 
            placeholder_text="Choose a password", show="•", font=("Segoe UI", 13)
        )
        self.new_password_entry.place(x=60, y=265)

        ctk.CTkButton(
            card, text="Sign Up", width=360, height=45, corner_radius=10,
            font=("Segoe UI", 15, "bold"), fg_color="#16A34A", hover_color="#15803D",
            cursor="hand2", command=self.register_user
        ).place(x=60, y=345)

        ctk.CTkButton(
            card, text="Back to Login", font=("Segoe UI", 12, "underline"),
            fg_color="transparent", text_color="#2563EB", hover_color="#F3F4F6",
            cursor="hand2", command=self.show_login_screen
        ).place(relx=0.5, y=430, anchor="center")



    #register screen
    def register_user(self):
        """Validates input, registers user, and writes to file."""
        username = self.new_username_entry.get().strip()
        password = self.new_password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        if username in self.users:
            messagebox.showerror("Error", "Username already exists. Please choose another.")
            return

        # Add new user and save to file permanently
        self.users[username] = {"password": password, "role": "customer"}
        self.save_users(self.users)
        
        messagebox.showinfo("Success", "Account created successfully! Please log in.")
        self.show_login_screen()

    #verify login screen
    def verify_login(self):
        username = self.username_entry.get().strip().lower() # Convert to lowercase
        password = self.password_entry.get().strip()

        if username in self.users and self.users[username]["password"] == password:
            role = self.users[username]["role"]
            messagebox.showinfo("Success", f"Logged in successfully as {role.capitalize()}!")
            
            if role == "admin":
                self.show_admin_dashboard(username)
            elif role == "customer":
                self.show_customer_dashboard(username)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    # ADMIN PORTAL
    def show_admin_dashboard(self, username):
        self.clear_window()
        self.root.title("Admin Portal - Movie Management")

# Main container filling the window
        main_container = ctk.CTkFrame(self.root, fg_color="#E5E7EB")
        main_container.pack(fill="both", expand=True)

        # --- 1. TOP HEADER FRAME (Logo, Search, Wishlist, Profile) ---
        header_frame = ctk.CTkFrame(main_container, height=80, fg_color="#89B5F8", corner_radius=0)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        # Logo on the left (Displays image if loaded, otherwise falls back to placeholder)
        if hasattr(self, 'logo_img') and self.logo_img:
            logo_label = ctk.CTkLabel(header_frame, text="", image=self.logo_img)
            logo_label.pack(side="left", padx=30)
        else:
            logo_box = ctk.CTkFrame(header_frame, width=110, height=45, fg_color="#E5E7EB", corner_radius=8)
            logo_box.pack(side="left", padx=30)
            ctk.CTkLabel(logo_box, text="logo", font=("Segoe UI", 14, "bold"), text_color="#374151").place(relx=0.5, rely=0.5, anchor="center")

        # Search bar in the center
        search_entry = ctk.CTkEntry(
            header_frame, width=380, height=40, 
            placeholder_text="search movies...", corner_radius=8, font=("Segoe UI", 13)
        )
        search_entry.pack(side="left", padx=60)

        # Right side items: Logout, Wishlist (Heart), and Profile icon
        logout_btn = ctk.CTkButton(
            header_frame, text="Logout", width=80, height=38, 
            font=("Segoe UI", 12, "bold"), fg_color="#DC2626", hover_color="#B91C1C", 
            corner_radius=8, command=self.show_login_screen
        )
        logout_btn.pack(side="right", padx=25)


        profile_icon_btn = ctk.CTkButton(
            header_frame, text="👤", width=45, height=38, 
            font=("Segoe UI", 16), fg_color="#F3F4F6", text_color="#1F2937", 
            hover_color="#E5E7EB", corner_radius=8,
            command=lambda: messagebox.showinfo("Profile", f"Logged in as: {username}\nRole: Customer")
        )
        profile_icon_btn.pack(side="right", padx=5)

        portal_label = ctk.CTkLabel(header_frame, text="Admin portal", font=("Segoe UI", 13, "bold"), text_color="#F0F2F5")
        portal_label.pack(side="right", padx=15)

        # --- 2. SCROLLABLE CONTENT AREA ---
        scroll_content = ctk.CTkScrollableFrame(main_container, fg_color="#C1D7F9", width=1140, height=730)
        scroll_content.pack(fill="both", expand=True, padx=20, pady=15)

        # --- 3. TODAY RECOMMENDATION SECTION ---
        rec_title = ctk.CTkLabel(scroll_content, text="Today recommendation:", font=("Segoe UI", 16, "bold"), text_color="#1F2937")
        rec_title.pack(anchor="w", padx=10, pady=(10, 8))

        banner_card = ctk.CTkFrame(scroll_content, width=1100, height=220, fg_color="#FDFDFD", corner_radius=15, border_width=1, border_color="#E5E7EB")
        banner_card.pack(padx=10, pady=5)
        banner_card.pack_propagate(False)

        ctk.CTkLabel(banner_card, text="recommendation movie", font=("Segoe UI", 26, "bold"), text_color="#1A1A1A").place(relx=0.5, rely=0.45, anchor="center")
        ctk.CTkLabel(banner_card, text="Explore today's hand-picked top trending movie feature!", font=("Segoe UI", 13), text_color="#6E7781").place(relx=0.5, rely=0.62, anchor="center")


        
    def save_new_movie(self):
        title = self.movie_title_entry.get().strip()
        genre = self.movie_genre_entry.get().strip()
        year = self.movie_year_entry.get().strip()
        desc = self.movie_desc_entry.get().strip()

        if not title or not genre:
            messagebox.showerror("Error", "Title and Genre are required!")
            return

        self.movies[title] = {"genre": genre, "year": year, "description": desc}
        self.save_movies(self.movies)
        messagebox.showinfo("Success", f"Movie '{title}' added successfully!")
        self.show_admin_dashboard("admin_user")

    def show_admin_movie_list(self):
        """Admin catalog view with ability to delete movies."""
        self.clear_window()
        self.root.title("Admin - Manage Movies")

        card = ctk.CTkFrame(self.root, width=750, height=650, corner_radius=20, fg_color="#FFFFFF", border_width=1, border_color="#E1E4E8")
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="Movie Catalog Management", font=("Segoe UI", 22, "bold"), text_color="#1A1A1A").place(relx=0.5, y=40, anchor="center")

        scroll_frame = ctk.CTkScrollableFrame(card, width=670, height=430, fg_color="#F9FAFB")
        scroll_frame.place(relx=0.5, y=90, anchor="n")

        if not self.movies:
            ctk.CTkLabel(scroll_frame, text="No movies available.", font=("Segoe UI", 14), text_color="#6E7781").pack(pady=30)
        else:
            for title, data in self.movies.items():
                row = ctk.CTkFrame(scroll_frame, fg_color="#FFFFFF", corner_radius=10, border_width=1, border_color="#E5E7EB")
                row.pack(fill="x", pady=5, padx=5)

                info_text = f"🎬 {title} ({data.get('year', 'N/A')}) - Genre: {data.get('genre', 'N/A')}"
                ctk.CTkLabel(row, text=info_text, font=("Segoe UI", 13, "bold"), text_color="#111827").pack(side="left", padx=15, pady=12)

                # Admin delete capability button
                del_btn = ctk.CTkButton(row, text="Delete", width=80, height=30, fg_color="#DC2626", hover_color="#B91C1C", font=("Segoe UI", 11, "bold"), command=lambda t=title: self.delete_movie(t))
                del_btn.pack(side="right", padx=15, pady=12)

        ctk.CTkButton(card, text="Back to Dashboard", width=200, height=40, fg_color="#6B7280", hover_color="#4B5563", font=("Segoe UI", 13, "bold"), command=lambda: self.show_admin_dashboard("admin_user")).place(relx=0.5, y=580, anchor="center")

    def delete_movie(self, title):
        if title in self.movies:
            del self.movies[title]
            self.save_movies(self.movies)
            messagebox.showinfo("Deleted", f"Movie '{title}' has been removed.")
            self.show_admin_movie_list()

    #CUSTOMER / USER PORTAL
    def show_customer_dashboard(self, username):
        """Displays the Customer Portal matching your custom wireframe design."""
        self.clear_window()
        self.root.title("Customer Portal - Movie Recommendation")

        # Main container filling the window
        main_container = ctk.CTkFrame(self.root, fg_color="#E5E7EB")
        main_container.pack(fill="both", expand=True)

        # --- 1. TOP HEADER FRAME (Logo, Search, Wishlist, Profile) ---
        header_frame = ctk.CTkFrame(main_container, height=80, fg_color="#89B5F8", corner_radius=0)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        # Logo on the left (Displays image if loaded, otherwise falls back to placeholder)
        if hasattr(self, 'logo_img') and self.logo_img:
            logo_label = ctk.CTkLabel(header_frame, text="", image=self.logo_img)
            logo_label.pack(side="left", padx=30)
        else:
            logo_box = ctk.CTkFrame(header_frame, width=110, height=45, fg_color="#E5E7EB", corner_radius=8)
            logo_box.pack(side="left", padx=30)
            ctk.CTkLabel(logo_box, text="logo", font=("Segoe UI", 14, "bold"), text_color="#374151").place(relx=0.5, rely=0.5, anchor="center")

        # Search bar in the center
        search_entry = ctk.CTkEntry(
            header_frame, width=380, height=40, 
            placeholder_text="search movies...", corner_radius=8, font=("Segoe UI", 13)
        )
        search_entry.pack(side="left", padx=60)

        # Right side items: Logout, Wishlist (Heart), and Profile icon
        logout_btn = ctk.CTkButton(
            header_frame, text="Logout", width=80, height=38, 
            font=("Segoe UI", 12, "bold"), fg_color="#DC2626", hover_color="#B91C1C", 
            corner_radius=8, command=self.show_login_screen
        )
        logout_btn.pack(side="right", padx=25)

        heart_btn = ctk.CTkButton(
            header_frame, text="♡", width=45, height=38, 
            font=("Segoe UI", 18), fg_color="#F3F4F6", text_color="#1F2937", 
            hover_color="#E5E7EB", corner_radius=8
        )
        heart_btn.pack(side="right", padx=5)

        profile_icon_btn = ctk.CTkButton(
            header_frame, text="👤", width=45, height=38, 
            font=("Segoe UI", 16), fg_color="#F3F4F6", text_color="#1F2937", 
            hover_color="#E5E7EB", corner_radius=8,
            command=lambda: messagebox.showinfo("Profile", f"Logged in as: {username}\nRole: Customer")
        )
        profile_icon_btn.pack(side="right", padx=5)

        portal_label = ctk.CTkLabel(header_frame, text="Customer portal", font=("Segoe UI", 13, "bold"), text_color="#F0F2F5")
        portal_label.pack(side="right", padx=15)

        # --- 2. SCROLLABLE CONTENT AREA ---
        scroll_content = ctk.CTkScrollableFrame(main_container, fg_color="#C1D7F9", width=1140, height=730)
        scroll_content.pack(fill="both", expand=True, padx=20, pady=15)

        # --- 3. TODAY RECOMMENDATION SECTION ---
        rec_title = ctk.CTkLabel(scroll_content, text="Today recommendation:", font=("Segoe UI", 16, "bold"), text_color="#1F2937")
        rec_title.pack(anchor="w", padx=10, pady=(10, 8))

        banner_card = ctk.CTkFrame(scroll_content, width=1100, height=220, fg_color="#FDFDFD", corner_radius=15, border_width=1, border_color="#E5E7EB")
        banner_card.pack(padx=10, pady=5)
        banner_card.pack_propagate(False)

        ctk.CTkLabel(banner_card, text="recommendation movie", font=("Segoe UI", 26, "bold"), text_color="#1A1A1A").place(relx=0.5, rely=0.45, anchor="center")
        ctk.CTkLabel(banner_card, text="Explore today's hand-picked top trending movie feature!", font=("Segoe UI", 13), text_color="#6E7781").place(relx=0.5, rely=0.62, anchor="center")

        # --- 4. MOVIE GENRE SECTION ---
        genre_container = ctk.CTkFrame(scroll_content, fg_color="#89B5F8", height=60, corner_radius=10, border_width=1, border_color="#E5E7EB")
        genre_container.pack(fill="x", padx=10, pady=15)
        genre_container.pack_propagate(False)

        genre_label = ctk.CTkLabel(genre_container, text="movie genre", font=("Segoe UI", 13, "bold"), text_color="#333333")
        genre_label.pack(side="left", padx=20)

        genres = ["romantic", "action", "comedy", "sci-fi", "horror", "drama"]
        for g in genres:
            g_btn = ctk.CTkButton(
                genre_container, text=g, width=95, height=32, corner_radius=16, 
                fg_color="#F3F4F6", text_color="#374151", hover_color="#E5E7EB", 
                font=("Segoe UI", 12), border_width=1, border_color="#D1D5DB"
            )
            g_btn.pack(side="left", padx=6)

        # --- 5. MOVIE GRID SECTION (3 Columns Grid matching sketch) ---
        grid_label = ctk.CTkLabel(scroll_content, text="Popular Catalog", font=("Segoe UI", 16, "bold"), text_color="#1F2937")
        grid_label.pack(anchor="w", padx=10, pady=(10, 5))

        grid_frame = ctk.CTkFrame(scroll_content, fg_color="transparent")
        grid_frame.pack(fill="x", padx=10, pady=5)

        # Sample movies to display in the 6 grid cards from your sketch
        sample_movies = [
            ("Inception", "Sci-Fi | 2010"),
            ("The Dark Knight", "Action | 2008"),
            ("Interstellar", "Sci-Fi | 2014"),
            ("Titanic", "Romantic | 1997"),
            ("The Notebook", "Romantic | 2004"),
            ("Avengers", "Action | 2012")
        ]

        # Organize into 2 rows of 3 columns
        for row_idx in range(2):
            row_box = ctk.CTkFrame(grid_frame, fg_color="transparent")
            row_box.pack(fill="x", pady=10)

            for col_idx in range(3):
                item_index = row_idx * 3 + col_idx
                if item_index < len(sample_movies):
                    m_title, m_info = sample_movies[item_index]

                    # Individual movie card container
                    card_item = ctk.CTkFrame(
                        row_box, width=350, height=240, fg_color="#FFFFFF", 
                        corner_radius=12, border_width=1, border_color="#E5E7EB"
                    )
                    card_item.pack(side="left", padx=12, expand=True)
                    card_item.pack_propagate(False)

                    # Placeholder box for "movie image"
                    img_box = ctk.CTkFrame(card_item, width=310, height=145, fg_color="#E5E7EB", corner_radius=8)
                    img_box.pack(pady=12)
                    ctk.CTkLabel(img_box, text="movie image", font=("Segoe UI", 13, "italic"), text_color="#6B7280").place(relx=0.5, rely=0.5, anchor="center")

                    # Movie text details under the image box
                    ctk.CTkLabel(card_item, text=m_title, font=("Segoe UI", 13, "bold"), text_color="#111827").pack(anchor="w", padx=20)
                    ctk.CTkLabel(card_item, text=m_info, font=("Segoe UI", 11), text_color="#6B7280").pack(anchor="w", padx=20)

    def show_customer_movie_catalog(self, username):
        """Read-only view for customers to explore movie recommendations."""
        self.clear_window()
        self.root.title("Browse Movies - Recommendations")

        card = ctk.CTkFrame(self.root, width=750, height=650, corner_radius=20, fg_color="#FFFFFF", border_width=1, border_color="#E1E4E8")
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text="Recommended Movies For You", font=("Segoe UI", 22, "bold"), text_color="#1A1A1A").place(relx=0.5, y=40, anchor="center")

        scroll_frame = ctk.CTkScrollableFrame(card, width=670, height=430, fg_color="#F9FAFB")
        scroll_frame.place(relx=0.5, y=90, anchor="n")

        if not self.movies:
            ctk.CTkLabel(scroll_frame, text="No recommendations available right now.", font=("Segoe UI", 14), text_color="#6E7781").pack(pady=30)
        else:
            for title, data in self.movies.items():
                row = ctk.CTkFrame(scroll_frame, fg_color="#FFFFFF", corner_radius=10, border_width=1, border_color="#E5E7EB")
                row.pack(fill="x", pady=6, padx=5)

                ctk.CTkLabel(row, text=f"🎬 {title} ({data.get('year', 'N/A')})", font=("Segoe UI", 13, "bold"), text_color="#111827").pack(anchor="w", padx=15, pady=(10, 2))
                ctk.CTkLabel(row, text=f"Genre: {data.get('genre', 'N/A')} | {data.get('description', '')}", font=("Segoe UI", 11), text_color="#4B5563").pack(anchor="w", padx=15, pady=(0, 10))

        ctk.CTkButton(card, text="Back to Dashboard", width=200, height=40, fg_color="#6B7280", hover_color="#4B5563", font=("Segoe UI", 13, "bold"), command=lambda: self.show_customer_dashboard(username)).place(relx=0.5, y=580, anchor="center")

if __name__ == "__main__":
    Movie()
from tkinter import messagebox, filedialog
from PIL import Image
import customtkinter as ctk
import json
import os
import shutil
import uuid

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

        self.movies_file = "movies_db.json"
        self.movies = self.load_movies() 
        
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

    def load_movies(self):
        if os.path.exists(self.movies_file):
            try:
                with open(self.movies_file, "r") as file:
                    return json.load(file)
            except Exception:
                return {}
        else:
            return {}

    def save_movies(self, movies_data):
        with open(self.movies_file, "w") as file:
            json.dump(movies_data, file, indent=4)

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
            self.current_username = username #Save current logged in username
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
            header_frame, 
            text="👤", 
            width=45, 
            height=38, 
            font=("Segoe UI", 16), 
            fg_color="#F3F4F6", 
            text_color="#1F2937", 
            hover_color="#E5E7EB", 
            corner_radius=8,
            command=lambda: messagebox.showinfo("Profile", f"Logged in as: {self.current_username}\nRole: Admin")
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

        banner_card = ctk.CTkFrame(
            scroll_content, 
            width=1100, height=220, 
            fg_color="#FDFDFD", 
            corner_radius=15, 
            border_width=1, border_color="#E5E7EB")
        banner_card.pack(padx=10, pady=5)
        banner_card.pack_propagate(False)

        ctk.CTkLabel(
            banner_card, 
            text="recommendation movie", 
            font=("Segoe UI", 26, "bold"), 
            text_color="#1A1A1A").place(relx=0.5, rely=0.45, anchor="center")
        
        ctk.CTkLabel(
            banner_card, 
            text="Explore today's hand-picked top trending movie feature!", 
            font=("Segoe UI", 13), text_color="#6E7781").place(relx=0.5, rely=0.62, anchor="center")
        
        grid_label = ctk.CTkLabel(
            scroll_content,
            text="Movie Catalog",
            font=("Segoe UI", 16, "bold"),
            text_color="#1F2937"
        )
        grid_label.pack(anchor="w", padx=10, pady=(15, 5))

        grid_frame = ctk.CTkFrame(
            scroll_content,
            fg_color="transparent"
        )
        grid_frame.pack(fill="x", padx=10, pady=5)

        movie_list = list(self.movies.items())

        # Keep poster image references
        self.movie_poster_images = []

        if not movie_list:
            ctk.CTkLabel(
                grid_frame,
                text="No movies available. Add a new movie to get started!",
                font=("Segoe UI", 13),
                text_color="#6B7280"
            ).pack(pady=20)

        else:
            for row_idx in range((len(movie_list) + 2) // 3):
                row_box = ctk.CTkFrame(
                    grid_frame,
                    fg_color="transparent"
                )
                row_box.pack(fill="x", pady=10)

                for col_idx in range(3):
                    item_index = row_idx * 3 + col_idx

                    if item_index < len(movie_list):
                        m_title, m_data = movie_list[item_index]

                        card_item = ctk.CTkFrame(
                            row_box,
                            width=350,
                            height=240,
                            fg_color="#FFFFFF",
                            corner_radius=12,
                            border_width=1,
                            border_color="#E5E7EB"
                        )
                        card_item.pack(
                            side="left",
                            padx=12,
                            expand=True
                        )
                        card_item.pack_propagate(False)

                        # Movie Poster
                        poster_path = m_data.get("poster", "")

                        if poster_path and os.path.exists(poster_path):
                            try:
                                poster_image = Image.open(poster_path)

                                poster_ctk_image = ctk.CTkImage(
                                    light_image=poster_image,
                                    dark_image=poster_image,
                                    size=(110, 145)
                                )

                                self.movie_poster_images.append(
                                    poster_ctk_image
                                )

                                ctk.CTkLabel(
                                    card_item,
                                    text="",
                                    image=poster_ctk_image
                                ).pack(pady=12)

                            except Exception:
                                img_box = ctk.CTkFrame(
                                    card_item,
                                    width=110,
                                    height=145,
                                    fg_color="#E5E7EB",
                                    corner_radius=8
                                )
                                img_box.pack(pady=12)

                                ctk.CTkLabel(
                                    img_box,
                                    text="Poster unavailable",
                                    font=("Segoe UI", 13, "italic"),
                                    text_color="#6B7280"
                                ).place(
                                    relx=0.5,
                                    rely=0.5,
                                    anchor="center"
                                )

                        else:
                            img_box = ctk.CTkFrame(
                                card_item,
                                width=110,
                                height=145,
                                fg_color="#E5E7EB",
                                corner_radius=8
                            )
                            img_box.pack(pady=12)

                            ctk.CTkLabel(
                                img_box,
                                text="movie image",
                                font=("Segoe UI", 13, "italic"),
                                text_color="#6B7280"
                            ).place(
                                relx=0.5,
                                rely=0.5,
                                anchor="center"
                            )

                        # Movie Title
                        ctk.CTkLabel(
                            card_item,
                            text=m_title,
                            font=("Segoe UI", 13, "bold"),
                            text_color="#111827"
                        ).pack(anchor="w", padx=20)

                        # Genre and Year
                        m_info = (
                            f"{m_data.get('genre', 'N/A')} | "
                            f"{m_data.get('year', 'N/A')}"
                        )

                        ctk.CTkLabel(
                            card_item,
                            text=m_info,
                            font=("Segoe UI", 11),
                            text_color="#6B7280"
                        ).pack(anchor="w", padx=20)


        #Admin movie management buttons
        button_frame = ctk.CTkFrame(scroll_content, fg_color="transparent")
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            text="Add New Movie",
            width = 200,
            height = 45,
            command = self.show_add_movie_screen
        ).pack(side = "left", padx = 15)

        ctk.CTkButton(
            button_frame,
            text = "Manage Movies",
            width = 200, 
            height = 45,
            fg_color = "#2563EB",
            hover_color = "#1D4ED8",
            command = self.show_admin_movie_list
        ).pack(side = "left", padx = 15)


    #admin dashboard    
    def show_add_movie_screen(self):
        self.clear_window()
        self.root.title("Admin - Add Movie")

        card = ctk.CTkFrame(
            self.root,
            width=600,
            height=720,
            corner_radius=20,
            fg_color="#FFFFFF"
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Page Title
        ctk.CTkLabel(
            card,
            text="Add New Movie",
            font=("Segoe UI", 24, "bold")
        ).place(relx=0.5, y=40, anchor="center")

        # Movie Title
        ctk.CTkLabel(
            card,
            text="Movie Title",
            font=("Segoe UI", 13, "bold")
        ).place(x=50, y=90)

        self.movie_title_entry = ctk.CTkEntry(
            card,
            width=500,
            height=40,
            placeholder_text="Enter movie title"
        )
        self.movie_title_entry.place(x=50, y=120)

        # Genre
        ctk.CTkLabel(
            card,
            text="Genre",
            font=("Segoe UI", 13, "bold")
        ).place(x=50, y=175)

        self.movie_genre_entry = ctk.CTkEntry(
            card,
            width=500,
            height=40,
            placeholder_text="Enter movie genre"
        )
        self.movie_genre_entry.place(x=50, y=205)

        # Release Year
        ctk.CTkLabel(
            card,
            text="Year",
            font=("Segoe UI", 13, "bold")
        ).place(x=50, y=260)

        self.movie_year_entry = ctk.CTkEntry(
            card,
            width=500,
            height=40,
            placeholder_text="Enter release year"
        )
        self.movie_year_entry.place(x=50, y=290)

        # Description
        ctk.CTkLabel(
            card,
            text="Description",
            font=("Segoe UI", 13, "bold")
        ).place(x=50, y=345)

        self.movie_desc_entry = ctk.CTkTextbox(
            card,
            width=500,
            height=100
        )
        self.movie_desc_entry.place(x=50, y=375)

        # Movie Poster
        ctk.CTkLabel(
            card,
            text="Movie Poster",
            font=("Segoe UI", 13, "bold")
        ).place(x=50, y=495)

        self.poster_path = None

        self.poster_label = ctk.CTkLabel(
            card,
            text="No poster selected",
            width=200,
            height=65,
            fg_color="#E5E7EB",
            corner_radius=10
        )
        self.poster_label.place(x=50, y=525)

        # Choose Poster Button
        ctk.CTkButton(
            card,
            text="Choose Poster",
            width=180,
            height=40,
            command=self.select_poster
        ).place(x=300, y=537)

        # Add Movie Button
        ctk.CTkButton(
            card,
            text="Add Movie",
            width=500,
            height=40,
            fg_color="#2563EB",
            command=self.save_new_movie
        ).place(x=50, y=615)

        # Back to Dashboard Button
        ctk.CTkButton(
            card,
            text="Back to Dashboard",
            width=500,
            height=35,
            fg_color="#6B7280",
            command=lambda: self.show_admin_dashboard(self.current_username)
        ).place(x=50, y=665)

    def save_new_movie(self):
        # Get movie details
        title = self.movie_title_entry.get().strip()
        genre = self.movie_genre_entry.get().strip()
        year = self.movie_year_entry.get().strip()
        desc = self.movie_desc_entry.get("1.0", "end").strip()

        # Check required fields
        if not title or not genre or not year or not desc:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Check duplicate movie title
        if title in self.movies:
            messagebox.showerror(
                "Error",
                "Movie already exists in the catalog."
            )
            return

        # Check poster selection
        if not self.poster_path or not os.path.isfile(self.poster_path):
            messagebox.showerror(
                "Error",
                "Please select a valid movie poster."
            )
            return

        # Create movie_posters folder
        os.makedirs("movie_posters", exist_ok=True)

        # Get poster extension
        extension = os.path.splitext(self.poster_path)[1].lower()

        # Clean movie title for filename
        safe_title = "".join(
            char for char in title
            if char not in '<>:"/\\|?*'
        ).strip().rstrip(".")

        if not safe_title:
            messagebox.showerror(
                "Error",
                "Movie title cannot be used as a poster filename."
            )
            return

        # Use movie title as poster filename
        poster_filename = f"{safe_title}{extension}"
        poster_dest = os.path.join("movie_posters", poster_filename)

        # Avoid overwriting an existing poster
        if os.path.exists(poster_dest):
            messagebox.showerror(
                "Error",
                "A poster with this filename already exists. Please use another movie title."
            )
            return

        # Copy poster into project folder
        try:
            shutil.copy2(self.poster_path, poster_dest)

            # Save movie details
            self.movies[title] = {
                "year": year,
                "genre": genre,
                "description": desc,
                "poster": poster_dest
            }

            self.save_movies(self.movies)

        except Exception as e:
            # Remove copied poster if saving fails
            if os.path.exists(poster_dest):
                os.remove(poster_dest)

            self.movies.pop(title, None)

            messagebox.showerror(
                "Error",
                f"Unable to save movie:\n{e}"
            )
            return

        messagebox.showinfo(
            "Success",
            f"Movie '{title}' added successfully!"
        )

        self.show_admin_movie_list()

    def select_poster(self):
        file_path = filedialog.askopenfilename(
            title="Select Movie Poster",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")
            ]
        )

        if file_path:
            self.poster_path = file_path

            self.poster_label.configure(
                text=os.path.basename(file_path)
            )

    def show_admin_movie_list(self):
        """Admin catalog view with ability to delete movies."""
        self.clear_window()
        self.root.title("Admin - Manage Movies")

        card = ctk.CTkFrame(
            self.root, width=750, height=650, 
            corner_radius=20, 
            fg_color="#FFFFFF", 
            border_width=1, border_color="#E1E4E8")
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            card, 
            text="Movie Catalog Management", 
            font=("Segoe UI", 22, "bold"), 
            text_color="#1A1A1A"
        ).place(relx=0.5, y=40, anchor="center")

        scroll_frame = ctk.CTkScrollableFrame(card, width=670, height=430, fg_color="#F9FAFB")
        scroll_frame.place(relx=0.5, y=90, anchor="n")

        if not self.movies:
            ctk.CTkLabel(
                scroll_frame, 
                text="No movies available.", 
                font=("Segoe UI", 14), 
                text_color="#6E7781").pack(pady=30)
        else:
            for title, data in self.movies.items():
                row = ctk.CTkFrame(
                    scroll_frame, 
                    fg_color="#FFFFFF", 
                    corner_radius=10, 
                    border_width=1, border_color="#E5E7EB")
                row.pack(fill="x", pady=5, padx=5)

                info_text = f"🎬 {title} ({data.get('year', 'N/A')}) - Genre: {data.get('genre', 'N/A')}"
                ctk.CTkLabel(
                    row, 
                    text=info_text, 
                    font=("Segoe UI", 13, "bold"), 
                    text_color="#111827").pack(side="left", padx=15, pady=12)

                # Admin delete capability button
                del_btn = ctk.CTkButton(
                    row, 
                    text="Delete", 
                    width=80, 
                    height=30, 
                    fg_color="#DC2626", hover_color="#B91C1C", 
                    font=("Segoe UI", 11, "bold"), 
                    command=lambda t=title: self.delete_movie(t))
                del_btn.pack(side="right", padx=15, pady=12)

        ctk.CTkButton(
            card, 
            text="Back to Dashboard", 
            width=200, height=40, 
            fg_color="#6B7280", hover_color="#4B5563", 
            font=("Segoe UI", 13, "bold"), 
            command=lambda: self.show_admin_dashboard(self.current_username)
        ).place(relx=0.5, y=580, anchor="center")

    def delete_movie(self, title):
        if title not in self.movies:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete '{title}'?"
        )

        if confirm:
            #Get poster path 
            poster_path = self.movies[title].get("poster")

            #Delete movie details
            del self.movies[title]
            self.save_movies(self.movies)

            if poster_path and os.path.exists(poster_path):
                try:
                    os.remove(poster_path)
                except Exception as e:
                    messagebox.showwarning(
                        "Warning",
                        f"Movie deleted but failed to remove poster:\n{e}"
                    )

            messagebox.showinfo(
                "Deleted",
                f"Movie '{title}' has been deleted."
            )
            self.show_admin_movie_list()



    def bind_click_recursive(self, widget, callback):
        widget.bind("<Button-1>", callback)

        for child in widget.winfo_children():
            self.bind_click_recursive(child, callback)

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

        
        # Display movies added by Admin
        movie_list = list(self.movies.items())

        # Keep movie poster references
        self.movie_poster_images = []

        for row_idx in range((len(movie_list) + 2) // 3):
            row_box = ctk.CTkFrame(grid_frame, fg_color="transparent")
            row_box.pack(fill="x", pady=10)

            for col_idx in range(3):
                item_index = row_idx * 3 + col_idx

                if item_index < len(movie_list):
                    m_title, m_data = movie_list[item_index]

                    # Individual movie card container
                    card_item = ctk.CTkFrame(
                        row_box, width=350, height=240, fg_color="#FFFFFF",
                        corner_radius=12, border_width=1, border_color="#E5E7EB"
                    )
                    card_item.pack(side="left", padx=12, expand=True)
                    card_item.pack_propagate(False)

                    # Movie Poster
                    poster_path = m_data.get("poster", "")

                    if poster_path and os.path.exists(poster_path):
                        try:
                            poster_image = Image.open(poster_path)

                            poster_ctk_image = ctk.CTkImage(
                                light_image=poster_image,
                                dark_image=poster_image,
                                size=(110, 145)
                            )

                            self.movie_poster_images.append(poster_ctk_image)

                            ctk.CTkLabel(
                                card_item,
                                text="",
                                image = poster_ctk_image
                            ).pack(pady=12)

                        except Exception:
                            img_box = ctk.CTkFrame(
                                card_item, width=110, height=145,
                                fg_color="#E5E7EB", corner_radius=8
                            )
                            img_box.pack(pady=12)

                            ctk.CTkLabel(
                                img_box,
                                text="Poster unavailable",
                                font=("Segoe UI", 13, "italic"),
                                text_color="#6B7280"
                            ).place(relx=0.5, rely=0.5, anchor="center")

                    else:
                        img_box = ctk.CTkFrame(
                            card_item, width=110, 
                            height=145,
                            fg_color="#E5E7EB",
                            corner_radius=8
                        )
                        img_box.pack(pady=12)

                        ctk.CTkLabel(
                            img_box,
                            text="movie image",
                            font=("Segoe UI", 13, "italic"),
                            text_color="#6B7280"
                        ).place(relx=0.5, rely=0.5, anchor="center")

                    # Movie text details under the image box
                    ctk.CTkLabel(
                        card_item,
                        text=m_title,
                        font=("Segoe UI", 13, "bold"),
                        text_color="#111827"
                    ).pack(anchor="w", padx=20)
                    
                    m_info = f"{m_data.get('genre', 'N/A')} | {m_data.get('year', 'N/A')}"

                    ctk.CTkLabel(
                        card_item,
                        text=m_info,
                        font=("Segoe UI", 11),
                        text_color="#6B7280"
                    ).pack(anchor="w", padx=20)

                    #make the entire card clickable to show movie details
                    click_command = lambda e, t=m_title, d=m_data:(
                        self.show_movie_details(t, d, username)
                    )

                    self.bind_click_recursive(card_item, click_command)

    def show_movie_details(self, title, data, username):
        """Display full details of a selected movie."""
        self.clear_window()
        self.root.title("Movie Details")

        card = ctk.CTkFrame(
            self.root,
            width=750,
            height=650,
            corner_radius=20,
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#E1E4E8"
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Movie Title
        ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 24, "bold"),
            text_color="#111827"
        ).place(relx=0.5, y=50, anchor="center")

        # Genre and Year
        info_text = (
            f"Genre: {data.get('genre', 'N/A')}  |  "
            f"Year: {data.get('year', 'N/A')}"
        )

        ctk.CTkLabel(
            card,
            text=info_text,
            font=("Segoe UI", 13),
            text_color="#6B7280"
        ).place(relx=0.5, y=100, anchor="center")

        # Description
        ctk.CTkLabel(
            card,
            text="Description",
            font=("Segoe UI", 15, "bold"),
            text_color="#111827"
        ).place(x=40, y=150)

        description = ctk.CTkTextbox(
            card,
            width=670,
            height=300,
            font=("Segoe UI", 13),
            wrap="word"
        )
        description.place(x=40, y=185)

        description.insert(
            "1.0",
            data.get("description", "No description available.")
        )
        description.configure(state="disabled")

        # Back Button
        ctk.CTkButton(
            card,
            text="Back to Dashboard",
            width=200,
            height=40,
            fg_color="#6B7280",
            hover_color="#4B5563",
            command=lambda: self.show_customer_dashboard(username)
        ).place(relx=0.5, y=570, anchor="center")

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

                ctk.CTkLabel(
                    row, 
                    text=f"🎬 {title} {data.get('year', 'N/A')}", 
                    font=("Segoe UI", 13, "bold"), 
                    text_color="#111827").pack(anchor="w", padx=15, pady=(10, 2))
                
                ctk.CTkLabel(
                    row, 
                    text=f"Genre: {data.get('genre', 'N/A')}", 
                    font=("Segoe UI", 11), text_color="#4B5563").pack(anchor="w", padx=15, pady=(0, 10))

        ctk.CTkButton(
            card, 
            text="Back to Dashboard", 
            width=200, height=40, 
            fg_color="#6B7280", hover_color="#4B5563", 
            font=("Segoe UI", 13, "bold"), 
            command=lambda: self.show_customer_dashboard(username)
        ).place(relx=0.5, y=580, anchor="center")

    def open_movie_details(event, title, data):
        self.show_movie_details(title, data, self.current_username)

if __name__ == "__main__":
    Movie()
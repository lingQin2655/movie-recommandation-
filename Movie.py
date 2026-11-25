import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
import json
import os
import shutil


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

        self.current_username = None

        # Load users from JSON file
        self.users_file = "users_db.json"
        self.users = self.load_users()

        # Load movies from JSON file
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
                with open(self.users_file, "r", encoding="utf-8") as file:
                    users = json.load(file)
                    for k, v in default_users.items():
                        if k not in users:
                            users[k] = v
                    return users
            except Exception:
                return default_users
        else:
            self.save_users(default_users)
            return default_users

    def validate_credentials(self, username, password, require_password=True):
        """
        Validates username and password rules:
        - Username: must contain both letters (alphabet) and numbers (digits), no spaces.
        - Password: 9 to 12 characters (more than 8, max 12), containing both letters and digits.
        Returns (True, "") if valid, or (False, error_message) if invalid.
        """
        if not username:
            return False, "Username cannot be empty."

        if not username.isalnum():
            return False, "Username can only contain letters and numbers (no spaces or symbols)."

        if not (any(c.isalpha() for c in username) and any(c.isdigit() for c in username)):
            return False, "Username must contain both alphabet letters and numbers (e.g., user123)."

        if require_password or password:
            if not password:
                return False, "Password cannot be empty."

            if not password.isalnum():
                return False, "Password can only contain letters and numbers (no spaces or symbols)."

            if not (9 <= len(password) <= 12):
                return False, "Password must be more than 8 characters and at most 12 characters (9–12 chars)."

            if not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
                return False, "Password must contain both alphabet letters and digits (e.g., Pass12345)."

        return True, ""
    
    def save_users(self, users_data):
        """Saves the current user dictionary to the JSON file."""
        with open(self.users_file, "w", encoding="utf-8") as file:
            json.dump(users_data, file, indent=4)

    def load_movies(self):
        """Loads movies from movies_db.json, seeding defaults if the file does not exist."""
        default_movies = {
            "Inception": {
                "year": "2010",
                "genre": "sci-fi",
                "description": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                "poster": "",
                "rating": 8.8,
                "total_votes": 1250,
            },
            "The Dark Knight": {
                "year": "2008",
                "genre": "action",
                "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological tests.",
                "poster": "",
                "rating": 9.0,
                "total_votes": 2100,
            },
            "Interstellar": {
                "year": "2014",
                "genre": "sci-fi",
                "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                "poster": "",
                "rating": 8.7,
                "total_votes": 980,
            },
            "Titanic": {
                "year": "1997",
                "genre": "romantic",
                "description": "A seventeen-year-old aristocrat falls in love with a kind, poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
                "poster": "",
                "rating": 7.9,
                "total_votes": 1400,
            },
            "The Notebook": {
                "year": "2004",
                "genre": "romantic",
                "description": "A poor yet passionate young man falls in love with a rich young woman, giving her a sense of freedom.",
                "poster": "",
                "rating": 7.8,
                "total_votes": 750,
            },
            "Avengers": {
                "year": "2012",
                "genre": "action",
                "description": "Earth's mightiest heroes must come together and learn to fight as a team against Loki.",
                "poster": "",
                "rating": 8.0,
                "total_votes": 1600,
            },
        }

        if os.path.exists(self.movies_file):
            try:
                with open(self.movies_file, "r", encoding="utf-8") as file:
                    return json.load(file)
            except Exception:
                return default_movies
        else:
            self.save_movies(default_movies)
            return default_movies

    def save_movies(self, movies_data):
        """Saves the movies dictionary to movies_db.json."""
        with open(self.movies_file, "w", encoding="utf-8") as file:
            json.dump(movies_data, file, indent=4)

    def _movies_as_list(self):
        """Converts self.movies dict into a list of movie dicts for UI views."""
        return [
            {
                "title": title,
                "genre": data.get("genre", "N/A"),
                "year": data.get("year", "N/A"),
                "info": f"{data.get('genre', 'N/A').capitalize()} | {data.get('year', 'N/A')}",
                "rating": data.get("rating", 0.0),
                "total_votes": data.get("total_votes", 0),
                "description": data.get("description", "No description available."),
                "poster": data.get("poster", ""),
            }
            for title, data in self.movies.items()
        ]

    def clear_window(self):
        """Removes all widgets from the current window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- LOGIN SCREEN ---
    def show_login_screen(self):
        """Displays the modern login form card with an image."""
        self.clear_window()
        self.root.title("Movie Recommendation - Login")

        card = ctk.CTkFrame(
            self.root, width=500, height=600, corner_radius=50,
            fg_color="#AECFFB", border_width=1, border_color="#ABCDF9"
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        try:
            pil_image = Image.open("logo.png")
            self.logo_img = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(120, 100))
            logo_label = ctk.CTkLabel(card, text="", image=self.logo_img)
            logo_label.place(relx=0.5, y=50, anchor="center")
        except Exception:
            print("Could not load image. Make sure 'logo.png' is in the folder.")

        ctk.CTkLabel(
            card, text="System Login", font=("Segoe UI", 26, "bold"), text_color="#1A1A1A"
        ).place(relx=0.5, y=100, anchor="center")

        ctk.CTkLabel(
            card, text="Enter your credentials to continue", font=("Segoe UI", 13), text_color="#6E7781"
        ).place(relx=0.5, y=140, anchor="center")

        ctk.CTkLabel(
            card, text="Username", font=("Segoe UI", 13, "bold"), text_color="#333333"
        ).place(x=60, y=180)

        self.username_entry = ctk.CTkEntry(
            card, width=360, height=42, corner_radius=10,
            placeholder_text="Enter your username", font=("Segoe UI", 13)
        )
        self.username_entry.place(x=60, y=210)

        ctk.CTkLabel(
            card, text="Password", font=("Segoe UI", 13, "bold"), text_color="#333333"
        ).place(x=60, y=270)

        self.password_entry = ctk.CTkEntry(
            card, width=360, height=42, corner_radius=10,
            placeholder_text="Enter your password", show="•", font=("Segoe UI", 13)
        )
        self.password_entry.place(x=60, y=300)

        ctk.CTkButton(
            card, text="Login", width=360, height=45, corner_radius=10,
            font=("Segoe UI", 15, "bold"), fg_color="#2563EB", hover_color="#1D4ED8",
            cursor="hand2", command=self.verify_login
        ).place(x=60, y=380)

        ctk.CTkButton(
            card, text="Don't have an account? Sign Up", font=("Segoe UI", 12, "underline"),
            fg_color="transparent", text_color="#2563EB", hover_color="#F3F4F6",
            cursor="hand2", command=self.show_signup_screen
        ).place(relx=0.5, y=470, anchor="center")

    # --- SIGN UP SCREEN ---
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

    def register_user(self):
        """Validates input, registers user, and writes to file."""
        username = self.new_username_entry.get().strip().lower()
        password = self.new_password_entry.get().strip()

        is_valid, error_msg = self.validate_credentials(username, password, require_password=True)
        if not is_valid:
            messagebox.showerror("Validation Error", error_msg)
            return

        if username in self.users:
            messagebox.showerror("Error", "Username already exists. Please choose another.")
            return

        self.users[username] = {"password": password, "role": "customer"}
        self.save_users(self.users)

        messagebox.showinfo("Success", "Account created successfully! Please log in.")
        self.show_login_screen()

    def verify_login(self):
        username = self.username_entry.get().strip().lower()
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

    # --- ADMIN PORTAL ---
    def show_admin_dashboard(self, username):
        self.current_username = username
        self.clear_window()
        self.root.title("Admin Portal - Movie Management")

        main_container = ctk.CTkFrame(self.root, fg_color="#E5E7EB")
        main_container.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(main_container, height=80, fg_color="#89B5F8", corner_radius=0)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        if hasattr(self, "logo_img") and self.logo_img:
            logo_label = ctk.CTkLabel(header_frame, text="", image=self.logo_img)
            logo_label.pack(side="left", padx=30)
        else:
            logo_box = ctk.CTkFrame(header_frame, width=110, height=45, fg_color="#E5E7EB", corner_radius=8)
            logo_box.pack(side="left", padx=30)
            ctk.CTkLabel(logo_box, text="logo", font=("Segoe UI", 14, "bold"), text_color="#374151").place(relx=0.5, rely=0.5, anchor="center")
 
        search_entry = ctk.CTkEntry(
            header_frame, width=380, height=40,
            placeholder_text="search movies or genre...", corner_radius=8, font=("Segoe UI", 13)
        )
        search_entry.pack(side="left", padx=60)

        logout_btn = ctk.CTkButton(
            header_frame, text="Logout", width=80, height=38,
            font=("Segoe UI", 12, "bold"), fg_color="#DC2626", hover_color="#B91C1C",
            corner_radius=8, command=self.show_login_screen
        )
        logout_btn.pack(side="right", padx=25)

        profile_icon_btn = ctk.CTkButton(
            header_frame, text="👤", 
            width=45, height=38,
            font=("Segoe UI", 16), 
            fg_color="#F3F4F6", 
            text_color="#1F2937",
            hover_color="#E5E7EB", 
            corner_radius=8,
            command=lambda: self.show_admin_profile(username)
        )
        profile_icon_btn.pack(side="right", padx=5)

        portal_label = ctk.CTkLabel(header_frame, text="Admin portal", font=("Segoe UI", 13, "bold"), text_color="#F0F2F5")
        portal_label.pack(side="right", padx=15)

        scroll_content = ctk.CTkScrollableFrame(main_container, fg_color="#C1D7F9", width=1140, height=730)
        scroll_content.pack(fill="both", expand=True, padx=20, pady=15)

        rec_title = ctk.CTkLabel(scroll_content, text="Today recommendation:", font=("Segoe UI", 16, "bold"), text_color="#1F2937")
        rec_title.pack(anchor="w", padx=10, pady=(10, 8))

        banner_card = ctk.CTkFrame(
            scroll_content, 
            width=1100, 
            height=220,
            fg_color="#FDFDFD", 
            corner_radius=15,
            border_width=1, 
            border_color="#E5E7EB"
        )
        banner_card.pack(padx=10, pady=5)
        banner_card.pack_propagate(False)

        ctk.CTkLabel(
            banner_card, 
            text="recommendation movie",
            font=("Segoe UI", 26, "bold"), 
            text_color="#1A1A1A"
        ).place(relx=0.5, rely=0.45, anchor="center")

        ctk.CTkLabel(
            banner_card, 
            text="Explore today's hand-picked top trending movie feature!",
            font=("Segoe UI", 13), 
            text_color="#6E7781"
        ).place(relx=0.5, rely=0.62, anchor="center")

        self.movie_poster_images = []
        current_genre = ["all"] 
        
        def populate_grid(selected_genre="all"):
            if selected_genre is not None:
                current_genre[0] = selected_genre

            for widget in grid_frame.winfo_children():
                widget.destroy()

            query = search_entry.get().strip().lower()
            active_genre = current_genre[0].lower()
            all_movies = self._movies_as_list()

            # 1. Filter by genre button selection
            if active_genre != "all":
                filtered_movies = [m for m in all_movies if m["genre"].lower() == active_genre]
            else:
                filtered_movies = all_movies

            # 2. Filter by search query (matches movie title OR genre)
            if query:
                filtered_movies = [
                    m for m in filtered_movies
                    if query in m["title"].lower() or query in m["genre"].lower()
                ]

            # Update section title dynamically
            if query and active_genre != "all":
                grid_label.configure(text=f"Search Results for '{query}' in {active_genre.capitalize()}")
            elif query:
                grid_label.configure(text=f"Search Results for '{query}'")
            elif active_genre != "all":
                grid_label.configure(text=f"Popular Catalog — {active_genre.capitalize()} Movies")
            else:
                grid_label.configure(text="Popular Catalog")

            if not filtered_movies:
                msg = f"No movies found matching '{query}'." if query else f"No movies found for '{active_genre}' genre."
                ctk.CTkLabel(
                    grid_frame, text=msg,
                    font=("Segoe UI", 13), text_color="#4B5563"
                ).pack(pady=20)
                return
            
            num_rows = (len(filtered_movies) + 2) // 3
            for row_idx in range(num_rows):
                row_box = ctk.CTkFrame(grid_frame, fg_color="transparent")
                row_box.pack(fill="x", pady=10)

                for col_idx in range(3):
                    item_index = row_idx * 3 + col_idx
                    if item_index < len(filtered_movies):
                        movie = filtered_movies[item_index]
                        m_title, m_info = movie["title"], movie["info"]

                        card_item = ctk.CTkFrame(
                            row_box, width=320, height=495, fg_color="#FFFFFF", #change size
                            corner_radius=12, border_width=1, border_color="#E5E7EB"
                        )
                        card_item.pack(side="left", padx=12, expand=True)
                        card_item.pack_propagate(False)

                        poster_path = movie.get("poster", "")
                        if poster_path and os.path.exists(poster_path):
                            try:
                                poster_image = Image.open(poster_path)
                                poster_ctk_image = ctk.CTkImage( #change size
                                    light_image=poster_image, dark_image=poster_image, size=(270, 400)
                                )
                                self.movie_poster_images.append(poster_ctk_image)
                                img_widget = ctk.CTkLabel(card_item, text="", image=poster_ctk_image)
                                img_widget.pack(pady=12)
                                clickable_widgets = (card_item, img_widget)
                            except Exception:
                                img_box = ctk.CTkFrame(card_item, width=110, height=145, fg_color="#E5E7EB", corner_radius=8)
                                img_box.pack(pady=12)
                                img_label = ctk.CTkLabel(img_box, text="Poster unavailable", font=("Segoe UI", 13, "italic"), text_color="#6B7280")
                                img_label.place(relx=0.5, rely=0.5, anchor="center")
                                clickable_widgets = (card_item, img_box, img_label)
                        else:
                            img_box = ctk.CTkFrame(card_item, width=110, height=145, fg_color="#E5E7EB", corner_radius=8)
                            img_box.pack(pady=12)
                            img_label = ctk.CTkLabel(img_box, text="movie image", font=("Segoe UI", 13, "italic"), text_color="#6B7280")
                            img_label.place(relx=0.5, rely=0.5, anchor="center")
                            clickable_widgets = (card_item, img_box, img_label)

                        title_label = ctk.CTkLabel(card_item, text=m_title, font=("Segoe UI", 13, "bold"), text_color="#111827")
                        title_label.pack(anchor="w", padx=20)

                        info_label = ctk.CTkLabel(card_item, text=m_info, font=("Segoe UI", 11), text_color="#6B7280")
                        info_label.pack(anchor="w", padx=20)

                        for widget in (*clickable_widgets, title_label, info_label):
                            widget.bind("<Button-1>", lambda e, mov=movie: self.show_movie_introduction_admin(mov, username))
                            widget.configure(cursor="hand2")

        # Trigger live search whenever user types
        search_entry.bind("<KeyRelease>", lambda event: populate_grid())
        genre_container = ctk.CTkFrame(scroll_content, fg_color="#89B5F8", height=60, corner_radius=10, border_width=1, border_color="#E5E7EB")
        genre_container.pack(fill="x", padx=10, pady=15)
        genre_container.pack_propagate(False)

        ctk.CTkLabel(genre_container, text="movie genre", font=("Segoe UI", 13, "bold"), text_color="#333333").pack(side="left", padx=20)

        genres = ["all", "romantic", "action", "comedy", "sci-fi", "horror", "drama"]
        for g in genres:
            g_btn = ctk.CTkButton(
                genre_container, text=g, width=85, height=32, corner_radius=16,
                fg_color="#759EF1", text_color="#374151", hover_color="#3E75E3",
                font=("Segoe UI", 12), border_width=1, border_color="#D1D5DB",
                command=lambda genre=g: populate_grid(genre)
            )
            g_btn.pack(side="left", padx=5)

        grid_label = ctk.CTkLabel(scroll_content, text="Popular Catalog", font=("Segoe UI", 16, "bold"), text_color="#1F2937")
        grid_label.pack(anchor="w", padx=10, pady=(10, 5))

        grid_frame = ctk.CTkFrame(scroll_content, fg_color="transparent")
        grid_frame.pack(fill="x", padx=10, pady=5)

        populate_grid("all")

        button_frame = ctk.CTkFrame(scroll_content, fg_color="transparent")
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame, 
            text="Add New Movie", 
            width=200, height=45,
            command=self.show_add_movie_screen
        ).pack(side="left", padx=15)

        ctk.CTkButton(
            button_frame, 
            text="Manage Movies", 
            width=200, height=45,
            fg_color="#2563EB", 
            hover_color="#1D4ED8",
            command=self.show_admin_movie_list
        ).pack(side="left", padx=15)

    def show_movie_introduction_admin(self, movie_data, username):
        """Displays full movie introduction page with rating slider and JSON persistence."""
        self.clear_window()
        self.root.title(f"{movie_data['title']} - Movie Introduction")

        main_container = ctk.CTkFrame(self.root, fg_color="#E5E7EB")
        main_container.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(main_container, height=80, fg_color="#89B5F8", corner_radius=0)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        back_btn = ctk.CTkButton(
            header_frame, text="← Back to Main Page", width=160, height=38,
            font=("Segoe UI", 13, "bold"), fg_color="#3E75E3", hover_color="#2563EB",
            corner_radius=8, command=lambda: self.show_admin_dashboard(username)
        )
        back_btn.pack(side="left", padx=30)

        ctk.CTkLabel(
            header_frame, text=f"Movie Details: {movie_data['title']}",
            font=("Segoe UI", 18, "bold"), text_color="#1F2937"
        ).pack(side="left", padx=20)

        intro_scroll = ctk.CTkScrollableFrame(main_container, fg_color="#C1D7F9", width=1140, height=730)
        intro_scroll.pack(fill="both", expand=True, padx=20, pady=15)

        detail_card = ctk.CTkFrame(intro_scroll, width=850, fg_color="#FFFFFF", corner_radius=15, border_width=1, border_color="#E5E7EB")
        detail_card.pack(padx=20, pady=20, expand=True)

        img_box = ctk.CTkFrame(detail_card, width=770, height=240, fg_color="#E5E7EB", corner_radius=10)
        img_box.pack(pady=20)
        img_box.pack_propagate(False)

        poster_path = movie_data.get("poster", "")
        if poster_path and os.path.exists(poster_path):
            try:
                poster_image = Image.open(poster_path)
                self.detail_poster_img = ctk.CTkImage(light_image=poster_image, dark_image=poster_image, size=(150, 210))
                ctk.CTkLabel(img_box, text="", image=self.detail_poster_img).place(relx=0.5, rely=0.5, anchor="center")
            except Exception:
                ctk.CTkLabel(img_box, text=f"[{movie_data['title']} Movie Image]", font=("Segoe UI", 15, "italic"), text_color="#6B7280").place(relx=0.5, rely=0.5, anchor="center")
        else:
            ctk.CTkLabel(img_box, text=f"[{movie_data['title']} Movie Image]", font=("Segoe UI", 15, "italic"), text_color="#6B7280").place(relx=0.5, rely=0.5, anchor="center")

        info_frame = ctk.CTkFrame(detail_card, fg_color="transparent")
        info_frame.pack(fill="x", padx=40, pady=5)

        title_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        title_row.pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(title_row, text=movie_data["title"], font=("Segoe UI", 24, "bold"), text_color="#111827").pack(side="left")

        if not hasattr(self, "user_favorites"):
            self.user_favorites = {}
        if username not in self.user_favorites:
            self.user_favorites[username] = set()

        is_favorite = movie_data["title"] in self.user_favorites[username]

        

        ctk.CTkLabel(
            info_frame,
            text=f"Genre Type: {movie_data['genre'].capitalize()}   |   Release Year: {movie_data['year']}",
            font=("Segoe UI", 13, "bold"), text_color="#4B5563"
        ).pack(anchor="w", pady=(0, 10))


        ctk.CTkLabel(info_frame, text="Description", font=("Segoe UI", 15, "bold"), text_color="#1F2937").pack(anchor="w", pady=(15, 5))
        ctk.CTkLabel(info_frame, text=movie_data["description"], font=("Segoe UI", 13), text_color="#4B5563", wraplength=750, justify="left").pack(anchor="w")



    def show_add_movie_screen(self):
        self.clear_window()
        self.root.title("Admin - Add Movie")

        card = ctk.CTkFrame(self.root, 
                            width=600, 
                            height=720, 
                            corner_radius=20, 
                            fg_color="#FFFFFF")
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, 
                     text="Add New Movie", 
                     font=("Segoe UI", 24, "bold")
                     ).place(relx=0.5, y=40, anchor="center")

        ctk.CTkLabel(card, 
                     text="Movie Title", 
                     font=("Segoe UI", 13, "bold")
                     ).place(x=50, y=90)
        self.movie_title_entry = ctk.CTkEntry(card, 
                                              width=500, 
                                              height=40, 
                                              placeholder_text="Enter movie title")
        self.movie_title_entry.place(x=50, y=120)

        ctk.CTkLabel(card, 
                     text="Genre", 
                     font=("Segoe UI", 13, "bold")
                     ).place(x=50, y=175)
        self.movie_genre_entry = ctk.CTkEntry(card, 
                                              width=500, 
                                              height=40, 
                                              placeholder_text="Enter movie genre")
        self.movie_genre_entry.place(x=50, y=205)

        ctk.CTkLabel(card, 
                     text="Year", 
                     font=("Segoe UI", 13, "bold")
                     ).place(x=50, y=260)
        self.movie_year_entry = ctk.CTkEntry(card, 
                                             width=500, 
                                             height=40, 
                                             placeholder_text="Enter release year")
        self.movie_year_entry.place(x=50, y=290)

        ctk.CTkLabel(card, 
                     text="Description", 
                     font=("Segoe UI", 13, "bold")
                     ).place(x=50, y=345)
        self.movie_desc_entry = ctk.CTkTextbox(card, 
                                               width=500, 
                                               height=100)
        self.movie_desc_entry.place(x=50, y=375)

        ctk.CTkLabel(card, 
                     text="Movie Poster", 
                     font=("Segoe UI", 13, "bold")
                     ).place(x=50, y=495)
        self.poster_path = None

        self.poster_label = ctk.CTkLabel(
            card, 
            text="No poster selected", 
            width=200,  
            height=65,
            fg_color="#E5E7EB", corner_radius=10
        )
        self.poster_label.place(x=50, y=525)

        ctk.CTkButton(card, 
                      text="Choose Poster", 
                      width=180, 
                      height=40, 
                      command=self.select_poster
                      ).place(x=300, y=537)

        ctk.CTkButton(card, 
                      text="Add Movie", 
                      width=500, 
                      height=40, 
                      fg_color="#2563EB", 
                      command=self.save_new_movie
                      ).place(x=50, y=615)

        ctk.CTkButton(
            card, 
            text="Back to Dashboard", 
            width=500, 
            height=35, 
            fg_color="#6B7280",
            command=lambda: self.show_admin_dashboard(self.current_username)
        ).place(x=50, y=665)

    def save_new_movie(self):
        title = self.movie_title_entry.get().strip()
        genre = self.movie_genre_entry.get().strip().lower()
        year = self.movie_year_entry.get().strip()
        desc = self.movie_desc_entry.get("1.0", "end").strip()

        if not title or not genre or not year or not desc:
            messagebox.showerror("Error", "All fields are required!")
            return

        if title in self.movies:
            messagebox.showerror("Error", "Movie already exists in the catalog.")
            return

        if not self.poster_path or not os.path.isfile(self.poster_path):
            messagebox.showerror("Error", "Please select a valid movie poster.")
            return

        os.makedirs("movie_posters", exist_ok=True)
        extension = os.path.splitext(self.poster_path)[1].lower()
        safe_title = "".join(char for char in title if char not in '<>:"/\\|?*').strip().rstrip(".")

        if not safe_title:
            messagebox.showerror("Error", "Movie title cannot be used as a poster filename.")
            return

        poster_filename = f"{safe_title}{extension}"
        poster_dest = os.path.join("movie_posters", poster_filename)

        if os.path.exists(poster_dest):
            messagebox.showerror("Error", "A poster with this filename already exists. Please use another movie title.")
            return

        try:
            shutil.copy2(self.poster_path, poster_dest)
            self.movies[title] = {
                "year": year,
                "genre": genre,
                "description": desc,
                "poster": poster_dest,
                "rating": 0.0,
                "total_votes": 0,
            }
            self.save_movies(self.movies)
        except Exception as e:
            if os.path.exists(poster_dest):
                os.remove(poster_dest)
            self.movies.pop(title, None)
            messagebox.showerror("Error", f"Unable to save movie:\n{e}")
            return

        messagebox.showinfo("Success", f"Movie '{title}' added successfully!")
        self.show_admin_movie_list()

    def select_poster(self):
        file_path = filedialog.askopenfilename(
            title="Select Movie Poster",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if file_path:
            self.poster_path = file_path
            self.poster_label.configure(text=os.path.basename(file_path))

    def show_admin_movie_list(self):
        """Admin catalog view with ability to delete movies."""
        self.clear_window()
        self.root.title("Admin - Manage Movies")

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

        ctk.CTkLabel(
            card, text="Movie Catalog Management",
            font=("Segoe UI", 22, "bold"), 
            text_color="#1A1A1A"
        ).place(relx=0.5, y=40, anchor="center")

        scroll_frame = ctk.CTkScrollableFrame(card, 
                                              width=670, 
                                              height=430, 
                                              fg_color="#F9FAFB")
        scroll_frame.place(relx=0.5, y=90, anchor="n")

        if not self.movies:
            ctk.CTkLabel(
                scroll_frame, 
                text="No movies available.",
                font=("Segoe UI", 14), 
                text_color="#6E7781"
            ).pack(pady=30)
        else:
            for title, data in self.movies.items():
                row = ctk.CTkFrame(
                    scroll_frame, 
                    fg_color="#FFFFFF",
                    corner_radius=10, 
                    border_width=1, 
                    border_color="#E5E7EB"
                )
                row.pack(fill="x", pady=5, padx=5)

                info_text = f"🎬 {title} ({data.get('year', 'N/A')}) - Genre: {data.get('genre', 'N/A')}"
                ctk.CTkLabel(
                    row, 
                    text=info_text,
                    font=("Segoe UI", 13, "bold"), 
                    text_color="#111827"
                ).pack(side="left", padx=15, pady=12)

                del_btn = ctk.CTkButton(
                    row, 
                    text="Delete", 
                    width=80, 
                    height=30,
                    fg_color="#DC2626", 
                    hover_color="#B91C1C",
                    font=("Segoe UI", 11, "bold"),
                    command=lambda t=title: self.delete_movie(t)
                )
                del_btn.pack(side="right", padx=15, pady=12)

        ctk.CTkButton(
            card, text="Back to Dashboard", 
            width=200, 
            height=40,
            fg_color="#6B7280", 
            hover_color="#4B5563",
            font=("Segoe UI", 13, "bold"),
            command=lambda: self.show_admin_dashboard(self.current_username)
        ).place(relx=0.5, y=580, anchor="center")

    def delete_movie(self, title):
        if title not in self.movies:
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{title}'?")
        if confirm:
            poster_path = self.movies[title].get("poster")
            del self.movies[title]
            self.save_movies(self.movies)

            if poster_path and os.path.exists(poster_path):
                try:
                    os.remove(poster_path)
                except Exception as e:
                    messagebox.showwarning("Warning", f"Movie deleted but failed to remove poster:\n{e}")

            messagebox.showinfo("Deleted", f"Movie '{title}' has been deleted.")
            self.show_admin_movie_list()

    def show_admin_profile(self,username):
        self.clear_window()
        self.root.title("Admin Profile - Movie Recommendation")

        main_container = ctk.CTkFrame(self.root, fg_color="#E5E7EB")
        main_container.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(main_container, height=80, fg_color="#89B5F8", corner_radius=0)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        ctk.CTkLabel(header_frame, text="Admin Profile", font=("Segoe UI", 20, "bold"), text_color="#1F2937").pack(side="left", padx=30)

        content_area = ctk.CTkFrame(main_container, fg_color="#C1D7F9", corner_radius=12)
        content_area.pack(fill="both", expand=True, padx=20, pady=15)

        profile_card = ctk.CTkFrame(
            content_area, width=480, height=340, fg_color="#FFFFFF",
            corner_radius=15, border_width=1, border_color="#E5E7EB"
        )
        profile_card.place(relx=0.5, rely=0.5, anchor="center")
        profile_card.pack_propagate(False)

        ctk.CTkLabel(profile_card, text="👤", font=("Segoe UI", 54)).pack(pady=(30, 10))
        ctk.CTkLabel(profile_card, text="Account Information", font=("Segoe UI", 18, "bold"), text_color="#1F2937").pack(pady=(0, 15))

        info_box = ctk.CTkFrame(profile_card, fg_color="#F3F4F6", corner_radius=8, width=360, height=50)
        info_box.pack(pady=5)
        info_box.pack_propagate(False)
        ctk.CTkLabel(info_box, text=f"Username:  {username}", font=("Segoe UI", 14, "bold"), text_color="#374151").place(relx=0.5, rely=0.5, anchor="center")

        btn_frame = ctk.CTkFrame(profile_card, fg_color="transparent")
        btn_frame.pack(side="bottom", pady=30)

        back_btn = ctk.CTkButton(
            btn_frame, text="Back to Main Page", width=160, height=40,
            font=("Segoe UI", 13, "bold"), fg_color="#6B7280", hover_color="#4B5563",
            corner_radius=8, command=lambda: self.show_admin_dashboard(username)
        )
        back_btn.pack(side="left", padx=10)

        edit_btn = ctk.CTkButton(
            btn_frame, text="Edit Profile", width=160, height=40,
            font=("Segoe UI", 13, "bold"), fg_color="#3E75E3", hover_color="#2563EB",
            corner_radius=8, command=lambda: self.show_admin_edit_profile(username)
        )
        edit_btn.pack(side="left", padx=10)

    def show_admin_edit_profile(self, username):
        self.clear_window()
        self.root.title("Edit Profile - Movie Recommendation")

        main_container = ctk.CTkFrame(self.root, fg_color="#E5E7EB")
        main_container.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(main_container, height=80, fg_color="#89B5F8", corner_radius=0)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        ctk.CTkLabel(header_frame, text="Edit Profile", font=("Segoe UI", 20, "bold"), text_color="#1F2937").pack(side="left", padx=30)

        content_area = ctk.CTkFrame(main_container, fg_color="#C1D7F9", corner_radius=12)
        content_area.pack(fill="both", expand=True, padx=20, pady=15)

        edit_card = ctk.CTkFrame(
            content_area, width=500, height=460, fg_color="#FFFFFF",
            corner_radius=15, border_width=1, border_color="#E5E7EB"
        )
        edit_card.place(relx=0.5, rely=0.5, anchor="center")
        edit_card.pack_propagate(False)

        ctk.CTkLabel(edit_card, text="Update Account Details", font=("Segoe UI", 18, "bold"), text_color="#1F2937").pack(pady=(25, 15))

        ctk.CTkLabel(edit_card, text="Username:", font=("Segoe UI", 13, "bold"), text_color="#374151").pack(anchor="w", padx=60)
        username_entry = ctk.CTkEntry(edit_card, width=380, height=38, font=("Segoe UI", 13), corner_radius=8)
        username_entry.insert(0, username)
        username_entry.pack(pady=(5, 15))

        ctk.CTkLabel(edit_card, text="New Password (leave blank to keep current):", font=("Segoe UI", 13, "bold"), text_color="#374151").pack(anchor="w", padx=60)
        new_pass_entry = ctk.CTkEntry(edit_card, width=380, height=38, show="*", placeholder_text="Enter new password", font=("Segoe UI", 13), corner_radius=8)
        new_pass_entry.pack(pady=(5, 15))

        ctk.CTkLabel(edit_card, text="Confirm New Password:", font=("Segoe UI", 13, "bold"), text_color="#374151").pack(anchor="w", padx=60)
        confirm_pass_entry = ctk.CTkEntry(edit_card, width=380, height=38, show="*", placeholder_text="Confirm new password", font=("Segoe UI", 13), corner_radius=8)
        confirm_pass_entry.pack(pady=(5, 10))

        status_label = ctk.CTkLabel(edit_card, text="", font=("Segoe UI", 12, "bold"), text_color="#DC2626")
        status_label.pack(pady=5)

        def save_changes():
                new_user = username_entry.get().strip().lower()
                new_pw = new_pass_entry.get().strip()
                confirm_pw = confirm_pass_entry.get().strip()
    
                if not new_user:
                    status_label.configure(text="Username cannot be empty.", text_color="#DC2626")
                    return
    
                if new_pw or confirm_pw:
                    if new_pw != confirm_pw:
                        status_label.configure(text="Passwords do not match!", text_color="#DC2626")
                        return
    
                is_valid, error_msg = self.validate_credentials(new_user, new_pw, require_password=False)
                if not is_valid:
                    status_label.configure(text=error_msg, text_color="#DC2626")
                    return
    
                if new_user != username:
                    if new_user in self.users:
                        status_label.configure(text="Username already taken!", text_color="#DC2626")
                        return
                    user_record = self.users.pop(username, {"password": new_pw, "role": "admin"})
                    if new_pw:
                        user_record["password"] = new_pw
                    self.users[new_user] = user_record
                    if hasattr(self, "user_favorites") and username in self.user_favorites:
                        self.user_favorites[new_user] = self.user_favorites.pop(username)
                elif new_pw and username in self.users:
                    self.users[username]["password"] = new_pw
    
                self.save_users(self.users)
                self.show_admin_profile(new_user)
    
        btn_frame = ctk.CTkFrame(edit_card, fg_color="transparent")
        btn_frame.pack(side="bottom", pady=25)
    
        cancel_btn = ctk.CTkButton(
                btn_frame, text="Cancel", width=160, height=40,
                font=("Segoe UI", 13, "bold"), fg_color="#6B7280", hover_color="#4B5563",
                corner_radius=8, command=lambda: self.show_admin_profile(username)
            )
        cancel_btn.pack(side="left", padx=10)
    
        save_btn = ctk.CTkButton(
                btn_frame, text="Save Changes", width=160, height=40,
                font=("Segoe UI", 13, "bold"), fg_color="#16A34A", hover_color="#15803D",
                corner_radius=8, command=save_changes
            )
        save_btn.pack(side="left", padx=10)
        

    # --- CUSTOMER / USER PORTAL --- #ohyeah
    def show_customer_dashboard(self, username):
        """Displays the Customer Portal backed by movies_db.json with genre filtering."""
        self.current_username = username
        self.clear_window()
        self.root.title("Customer Portal - Movie Recommendation")

        main_container = ctk.CTkFrame(self.root, fg_color="#E5E7EB")
        main_container.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(main_container, height=80, fg_color="#89B5F8", corner_radius=0)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        if hasattr(self, "logo_img") and self.logo_img:
            logo_label = ctk.CTkLabel(header_frame, text="", image=self.logo_img)
            logo_label.pack(side="left", padx=30)
        else:
            logo_box = ctk.CTkFrame(header_frame, width=110, height=45, fg_color="#E5E7EB", corner_radius=8)
            logo_box.pack(side="left", padx=30)
            ctk.CTkLabel(logo_box, text="logo", font=("Segoe UI", 14, "bold"), text_color="#374151").place(relx=0.5, rely=0.5, anchor="center")

        search_entry = ctk.CTkEntry(
            header_frame, width=380, height=40,
            placeholder_text="search movies or genre...", corner_radius=8, font=("Segoe UI", 13)
        )
        search_entry.pack(side="left", padx=60)

        logout_btn = ctk.CTkButton(
            header_frame, text="Logout", width=80, height=38,
            font=("Segoe UI", 12, "bold"), fg_color="#DC2626", hover_color="#B91C1C",
            corner_radius=8, command=self.show_login_screen
        )
        logout_btn.pack(side="right", padx=25)

        heart_btn = ctk.CTkButton(
            header_frame, text="♡", width=45, height=38,
            font=("Segoe UI", 18), fg_color="#F3F4F6", text_color="#1F2937",
            hover_color="#E5E7EB", corner_radius=8,
            command=lambda: self.show_favourite_heart(username)
        )
        heart_btn.pack(side="right", padx=5)

        profile_icon_btn = ctk.CTkButton(
            header_frame, text="👤", width=45, height=38,
            font=("Segoe UI", 16), fg_color="#F3F4F6", text_color="#1F2937",
            hover_color="#E5E7EB", corner_radius=8,
            command=lambda: self.show_customer_profile(username)
        )
        profile_icon_btn.pack(side="right", padx=5)

        portal_label = ctk.CTkLabel(header_frame, text="Customer portal", font=("Segoe UI", 13, "bold"), text_color="#F0F2F5")
        portal_label.pack(side="right", padx=15)

        scroll_content = ctk.CTkScrollableFrame(main_container, fg_color="#C1D7F9", width=1140, height=730)
        scroll_content.pack(fill="both", expand=True, padx=20, pady=15)

        rec_title = ctk.CTkLabel(scroll_content, text="Today recommendation:", font=("Segoe UI", 16, "bold"), text_color="#1F2937")
        rec_title.pack(anchor="w", padx=10, pady=(10, 8))

        banner_card = ctk.CTkFrame(scroll_content, width=1100, height=220, fg_color="#FDFDFD", corner_radius=15, border_width=1, border_color="#E5E7EB")
        banner_card.pack(padx=10, pady=5)
        banner_card.pack_propagate(False)

        ctk.CTkLabel(banner_card, text="recommendation movie", font=("Segoe UI", 26, "bold"), text_color="#1A1A1A").place(relx=0.5, rely=0.45, anchor="center")
        ctk.CTkLabel(banner_card, text="Explore today's hand-picked top trending movie feature!", font=("Segoe UI", 13), text_color="#6E7781").place(relx=0.5, rely=0.62, anchor="center")

        self.movie_poster_images = []
        current_genre = ["all"] 

        def populate_grid(selected_genre="all"):
            if selected_genre is not None:
                current_genre[0] = selected_genre

            for widget in grid_frame.winfo_children():
                widget.destroy()

            query = search_entry.get().strip().lower()
            active_genre = current_genre[0].lower()
            all_movies = self._movies_as_list()

            # 1. Filter by genre button selection
            if active_genre != "all":
                filtered_movies = [m for m in all_movies if m["genre"].lower() == active_genre]
            else:
                filtered_movies = all_movies

            # 2. Filter by search query (matches movie title OR genre)
            if query:
                filtered_movies = [
                    m for m in filtered_movies
                    if query in m["title"].lower() or query in m["genre"].lower()
                ]

            # Update section title dynamically
            if query and active_genre != "all":
                grid_label.configure(text=f"Search Results for '{query}' in {active_genre.capitalize()}")
            elif query:
                grid_label.configure(text=f"Search Results for '{query}'")
            elif active_genre != "all":
                grid_label.configure(text=f"Popular Catalog — {active_genre.capitalize()} Movies")
            else:
                grid_label.configure(text="Popular Catalog")

            if not filtered_movies:
                msg = f"No movies found matching '{query}'." if query else f"No movies found for '{active_genre}' genre."
                ctk.CTkLabel(
                    grid_frame, text=msg,
                    font=("Segoe UI", 13), text_color="#4B5563"
                ).pack(pady=20)
                return
            
            num_rows = (len(filtered_movies) + 2) // 3
            for row_idx in range(num_rows):
                row_box = ctk.CTkFrame(grid_frame, fg_color="transparent")
                row_box.pack(fill="x", pady=10)

                for col_idx in range(3):
                    item_index = row_idx * 3 + col_idx
                    if item_index < len(filtered_movies):
                        movie = filtered_movies[item_index]
                        m_title, m_info = movie["title"], movie["info"]

                        card_item = ctk.CTkFrame(
                            row_box, width=320, height=495, fg_color="#FFFFFF", #change size
                            corner_radius=12, border_width=1, border_color="#E5E7EB"
                        )
                        card_item.pack(side="left", padx=12, expand=True)
                        card_item.pack_propagate(False)

                        poster_path = movie.get("poster", "")
                        if poster_path and os.path.exists(poster_path):
                            try:
                                poster_image = Image.open(poster_path)
                                poster_ctk_image = ctk.CTkImage( #change size
                                    light_image=poster_image, dark_image=poster_image, size=(270, 400)
                                )
                                self.movie_poster_images.append(poster_ctk_image)
                                img_widget = ctk.CTkLabel(card_item, text="", image=poster_ctk_image)
                                img_widget.pack(pady=12)
                                clickable_widgets = (card_item, img_widget)
                            except Exception:
                                img_box = ctk.CTkFrame(card_item, width=110, height=145, fg_color="#E5E7EB", corner_radius=8)
                                img_box.pack(pady=12)
                                img_label = ctk.CTkLabel(img_box, text="Poster unavailable", font=("Segoe UI", 13, "italic"), text_color="#6B7280")
                                img_label.place(relx=0.5, rely=0.5, anchor="center")
                                clickable_widgets = (card_item, img_box, img_label)
                        else:
                            img_box = ctk.CTkFrame(card_item, width=110, height=145, fg_color="#E5E7EB", corner_radius=8)
                            img_box.pack(pady=12)
                            img_label = ctk.CTkLabel(img_box, text="movie image", font=("Segoe UI", 13, "italic"), text_color="#6B7280")
                            img_label.place(relx=0.5, rely=0.5, anchor="center")
                            clickable_widgets = (card_item, img_box, img_label)

                        title_label = ctk.CTkLabel(card_item, text=m_title, font=("Segoe UI", 13, "bold"), text_color="#111827")
                        title_label.pack(anchor="w", padx=20)

                        info_label = ctk.CTkLabel(card_item, text=m_info, font=("Segoe UI", 11), text_color="#6B7280")
                        info_label.pack(anchor="w", padx=20)

                        for widget in (*clickable_widgets, title_label, info_label):
                            widget.bind("<Button-1>", lambda e, mov=movie: self.show_movie_introduction_customer(mov, username))
                            widget.configure(cursor="hand2")

        # Trigger live search whenever user types
        search_entry.bind("<KeyRelease>", lambda event: populate_grid())
        genre_container = ctk.CTkFrame(scroll_content, fg_color="#89B5F8", height=60, corner_radius=10, border_width=1, border_color="#E5E7EB")
        genre_container.pack(fill="x", padx=10, pady=15)
        genre_container.pack_propagate(False)

        ctk.CTkLabel(genre_container, text="movie genre", font=("Segoe UI", 13, "bold"), text_color="#333333").pack(side="left", padx=20)

        genres = ["all", "romantic", "action", "comedy", "sci-fi", "horror", "drama"]
        for g in genres:
            g_btn = ctk.CTkButton(
                genre_container, text=g, width=85, height=32, corner_radius=16,
                fg_color="#759EF1", text_color="#374151", hover_color="#3E75E3",
                font=("Segoe UI", 12), border_width=1, border_color="#D1D5DB",
                command=lambda genre=g: populate_grid(genre)
            )
            g_btn.pack(side="left", padx=5)

        grid_label = ctk.CTkLabel(scroll_content, text="Popular Catalog", font=("Segoe UI", 16, "bold"), text_color="#1F2937")
        grid_label.pack(anchor="w", padx=10, pady=(10, 5))

        grid_frame = ctk.CTkFrame(scroll_content, fg_color="transparent")
        grid_frame.pack(fill="x", padx=10, pady=5)

        populate_grid("all")

    def show_movie_introduction_customer(self, movie_data, username):
        """Displays full movie introduction page with rating slider and JSON persistence."""
        self.clear_window()
        self.root.title(f"{movie_data['title']} - Movie Introduction")

        main_container = ctk.CTkFrame(self.root, fg_color="#E5E7EB")
        main_container.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(main_container, height=80, fg_color="#89B5F8", corner_radius=0)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        back_btn = ctk.CTkButton(
            header_frame, text="← Back to Main Page", width=160, height=38,
            font=("Segoe UI", 13, "bold"), fg_color="#3E75E3", hover_color="#2563EB",
            corner_radius=8, command=lambda: self.show_customer_dashboard(username)
        )
        back_btn.pack(side="left", padx=30)

        ctk.CTkLabel(
            header_frame, text=f"Movie Details: {movie_data['title']}",
            font=("Segoe UI", 18, "bold"), text_color="#1F2937"
        ).pack(side="left", padx=20)

        intro_scroll = ctk.CTkScrollableFrame(main_container, fg_color="#C1D7F9", width=1140, height=730)
        intro_scroll.pack(fill="both", expand=True, padx=20, pady=15)

        detail_card = ctk.CTkFrame(intro_scroll, width=850, fg_color="#FFFFFF", corner_radius=15, border_width=1, border_color="#E5E7EB")
        detail_card.pack(padx=20, pady=20, expand=True)

        img_box = ctk.CTkFrame(detail_card, width=770, height=240, fg_color="#E5E7EB", corner_radius=10)
        img_box.pack(pady=20)
        img_box.pack_propagate(False)

        poster_path = movie_data.get("poster", "")
        if poster_path and os.path.exists(poster_path):
            try:
                poster_image = Image.open(poster_path)
                self.detail_poster_img = ctk.CTkImage(light_image=poster_image, dark_image=poster_image, size=(150, 210))
                ctk.CTkLabel(img_box, text="", image=self.detail_poster_img).place(relx=0.5, rely=0.5, anchor="center")
            except Exception:
                ctk.CTkLabel(img_box, text=f"[{movie_data['title']} Movie Image]", font=("Segoe UI", 15, "italic"), text_color="#6B7280").place(relx=0.5, rely=0.5, anchor="center")
        else:
            ctk.CTkLabel(img_box, text=f"[{movie_data['title']} Movie Image]", font=("Segoe UI", 15, "italic"), text_color="#6B7280").place(relx=0.5, rely=0.5, anchor="center")

        info_frame = ctk.CTkFrame(detail_card, fg_color="transparent")
        info_frame.pack(fill="x", padx=40, pady=5)

        title_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        title_row.pack(fill="x", pady=(0, 5))

        ctk.CTkLabel(title_row, text=movie_data["title"], font=("Segoe UI", 24, "bold"), text_color="#111827").pack(side="left")

        if not hasattr(self, "user_favorites"):
            self.user_favorites = {}
        if username not in self.user_favorites:
            self.user_favorites[username] = set()

        is_favorite = movie_data["title"] in self.user_favorites[username]

        def toggle_favorite():
            if movie_data["title"] in self.user_favorites[username]:
                self.user_favorites[username].remove(movie_data["title"])
                fav_btn.configure(
                    text="♡ Add to Favorites",
                    fg_color="#F3F4F6", text_color="#1F2937", hover_color="#E5E7EB"
                )
            else:
                self.user_favorites[username].add(movie_data["title"])
                fav_btn.configure(
                    text="❤️ In Favorites",
                    fg_color="#FEE2E2", text_color="#DC2626", hover_color="#FECACA"
                )

        fav_btn = ctk.CTkButton(
            title_row,
            text="❤️ In Favorites" if is_favorite else "♡ Add to Favorites",
            width=160, height=36,
            font=("Segoe UI", 12, "bold"),
            fg_color="#FEE2E2" if is_favorite else "#F3F4F6",
            text_color="#DC2626" if is_favorite else "#1F2937",
            hover_color="#FECACA" if is_favorite else "#E5E7EB",
            corner_radius=8,
            command=toggle_favorite
        )
        fav_btn.pack(side="right")

        ctk.CTkLabel(
            info_frame,
            text=f"Genre Type: {movie_data['genre'].capitalize()}   |   Release Year: {movie_data['year']}",
            font=("Segoe UI", 13, "bold"), text_color="#4B5563"
        ).pack(anchor="w", pady=(0, 10))

        rating_box = ctk.CTkFrame(info_frame, fg_color="#FEF3C7", corner_radius=6)
        rating_box.pack(anchor="w", pady=5)

        rating_display_lbl = ctk.CTkLabel(
            rating_box,
            text=f"Rating: {movie_data['rating']} / 10 ⭐ ({movie_data['total_votes']} votes)",
            font=("Segoe UI", 13, "bold"), text_color="#D97706"
        )
        rating_display_lbl.pack(padx=12, pady=6)

        ctk.CTkLabel(info_frame, text="Description", font=("Segoe UI", 15, "bold"), text_color="#1F2937").pack(anchor="w", pady=(15, 5))
        ctk.CTkLabel(info_frame, text=movie_data["description"], font=("Segoe UI", 13), text_color="#4B5563", wraplength=750, justify="left").pack(anchor="w")

        ctk.CTkLabel(info_frame, text="Rate this Movie", font=("Segoe UI", 16, "bold"), text_color="#1F2937").pack(anchor="w", pady=(25, 5))

        rating_box_frame = ctk.CTkFrame(info_frame, fg_color="#F3F4F6", corner_radius=10)
        rating_box_frame.pack(fill="x", pady=5)

        slider_label = ctk.CTkLabel(rating_box_frame, text="Select Rating: 8 / 10", font=("Segoe UI", 12, "bold"), text_color="#374151")
        slider_label.pack(anchor="w", padx=20, pady=(15, 5))

        def slider_event(val):
            slider_label.configure(text=f"Select Rating: {int(val)} / 10")

        rating_slider = ctk.CTkSlider(rating_box_frame, from_=1, to=10, number_of_steps=9, command=slider_event)
        rating_slider.set(8)
        rating_slider.pack(fill="x", padx=20, pady=5)

        status_lbl = ctk.CTkLabel(rating_box_frame, text="", font=("Segoe UI", 11), text_color="#059669")
        status_lbl.pack(pady=2)

        def submit_rating():
            user_rating = int(rating_slider.get())
            old_avg = movie_data["rating"]
            old_votes = movie_data["total_votes"]
            new_votes = old_votes + 1
            new_avg = round(((old_avg * old_votes) + user_rating) / new_votes, 1)

            movie_data["rating"] = new_avg
            movie_data["total_votes"] = new_votes

            if movie_data["title"] in self.movies:
                self.movies[movie_data["title"]]["rating"] = new_avg
                self.movies[movie_data["title"]]["total_votes"] = new_votes
                self.save_movies(self.movies)

            rating_display_lbl.configure(text=f"Rating: {new_avg} / 10 ⭐ ({new_votes} votes)")
            status_lbl.configure(text=f"✅ Successfully submitted your {user_rating}/10 rating!")

        submit_btn = ctk.CTkButton(
            rating_box_frame, text="Submit Rating", width=140, height=38,
            font=("Segoe UI", 12, "bold"), fg_color="#3E75E3", hover_color="#2563EB",
            corner_radius=8, command=submit_rating
        )
        submit_btn.pack(anchor="e", padx=20, pady=(5, 15))

    def show_customer_profile(self, username):
        self.clear_window()
        self.root.title("Customer Profile - Movie Recommendation")

        main_container = ctk.CTkFrame(self.root, fg_color="#E5E7EB")
        main_container.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(main_container, height=80, fg_color="#89B5F8", corner_radius=0)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        ctk.CTkLabel(header_frame, text="Customer Profile", font=("Segoe UI", 20, "bold"), text_color="#1F2937").pack(side="left", padx=30)

        content_area = ctk.CTkFrame(main_container, fg_color="#C1D7F9", corner_radius=12)
        content_area.pack(fill="both", expand=True, padx=20, pady=15)

        profile_card = ctk.CTkFrame(
            content_area, width=480, height=340, fg_color="#FFFFFF",
            corner_radius=15, border_width=1, border_color="#E5E7EB"
        )
        profile_card.place(relx=0.5, rely=0.5, anchor="center")
        profile_card.pack_propagate(False)

        ctk.CTkLabel(profile_card, text="👤", font=("Segoe UI", 54)).pack(pady=(30, 10))
        ctk.CTkLabel(profile_card, text="Account Information", font=("Segoe UI", 18, "bold"), text_color="#1F2937").pack(pady=(0, 15))

        info_box = ctk.CTkFrame(profile_card, fg_color="#F3F4F6", corner_radius=8, width=360, height=50)
        info_box.pack(pady=5)
        info_box.pack_propagate(False)
        ctk.CTkLabel(info_box, text=f"Username:  {username}", font=("Segoe UI", 14, "bold"), text_color="#374151").place(relx=0.5, rely=0.5, anchor="center")

        btn_frame = ctk.CTkFrame(profile_card, fg_color="transparent")
        btn_frame.pack(side="bottom", pady=30)

        back_btn = ctk.CTkButton(
            btn_frame, text="Back to Main Page", width=160, height=40,
            font=("Segoe UI", 13, "bold"), fg_color="#6B7280", hover_color="#4B5563",
            corner_radius=8, command=lambda: self.show_customer_dashboard(username)
        )
        back_btn.pack(side="left", padx=10)

        edit_btn = ctk.CTkButton(
            btn_frame, text="Edit Profile", width=160, height=40,
            font=("Segoe UI", 13, "bold"), fg_color="#3E75E3", hover_color="#2563EB",
            corner_radius=8, command=lambda: self.show_customer_edit_profile(username)
        )
        edit_btn.pack(side="left", padx=10)

    def show_customer_edit_profile(self, username):
        self.clear_window()
        self.root.title("Edit Profile - Movie Recommendation")

        main_container = ctk.CTkFrame(self.root, fg_color="#E5E7EB")
        main_container.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(main_container, height=80, fg_color="#89B5F8", corner_radius=0)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)
        ctk.CTkLabel(header_frame, text="Edit Profile", font=("Segoe UI", 20, "bold"), text_color="#1F2937").pack(side="left", padx=30)

        content_area = ctk.CTkFrame(main_container, fg_color="#C1D7F9", corner_radius=12)
        content_area.pack(fill="both", expand=True, padx=20, pady=15)

        edit_card = ctk.CTkFrame(
            content_area, width=500, height=460, fg_color="#FFFFFF",
            corner_radius=15, border_width=1, border_color="#E5E7EB"
        )
        edit_card.place(relx=0.5, rely=0.5, anchor="center")
        edit_card.pack_propagate(False)

        ctk.CTkLabel(edit_card, text="Update Account Details", font=("Segoe UI", 18, "bold"), text_color="#1F2937").pack(pady=(25, 15))

        ctk.CTkLabel(edit_card, text="Username:", font=("Segoe UI", 13, "bold"), text_color="#374151").pack(anchor="w", padx=60)
        username_entry = ctk.CTkEntry(edit_card, width=380, height=38, font=("Segoe UI", 13), corner_radius=8)
        username_entry.insert(0, username)
        username_entry.pack(pady=(5, 15))

        ctk.CTkLabel(edit_card, text="New Password (leave blank to keep current):", font=("Segoe UI", 13, "bold"), text_color="#374151").pack(anchor="w", padx=60)
        new_pass_entry = ctk.CTkEntry(edit_card, width=380, height=38, show="*", placeholder_text="Enter new password", font=("Segoe UI", 13), corner_radius=8)
        new_pass_entry.pack(pady=(5, 15))

        ctk.CTkLabel(edit_card, text="Confirm New Password:", font=("Segoe UI", 13, "bold"), text_color="#374151").pack(anchor="w", padx=60)
        confirm_pass_entry = ctk.CTkEntry(edit_card, width=380, height=38, show="*", placeholder_text="Confirm new password", font=("Segoe UI", 13), corner_radius=8)
        confirm_pass_entry.pack(pady=(5, 10))

        status_label = ctk.CTkLabel(edit_card, text="", font=("Segoe UI", 12, "bold"), text_color="#DC2626")
        status_label.pack(pady=5)

        def save_changes():
            new_user = username_entry.get().strip().lower()
            new_pw = new_pass_entry.get().strip()
            confirm_pw = confirm_pass_entry.get().strip()

            if not new_user:
                status_label.configure(text="Username cannot be empty.", text_color="#DC2626")
                return

            if new_pw or confirm_pw:
                if new_pw != confirm_pw:
                    status_label.configure(text="Passwords do not match!", text_color="#DC2626")
                    return

            is_valid, error_msg = self.validate_credentials(new_user, new_pw, require_password=False)
            if not is_valid:
                status_label.configure(text=error_msg, text_color="#DC2626")
                return

            if new_user != username:
                if new_user in self.users:
                    status_label.configure(text="Username already taken!", text_color="#DC2626")
                    return
                user_record = self.users.pop(username, {"password": new_pw, "role": "customer"})
                if new_pw:
                    user_record["password"] = new_pw
                self.users[new_user] = user_record
                if hasattr(self, "user_favorites") and username in self.user_favorites:
                    self.user_favorites[new_user] = self.user_favorites.pop(username)
            elif new_pw and username in self.users:
                self.users[username]["password"] = new_pw

            self.save_users(self.users)
            self.show_customer_profile(new_user)

        btn_frame = ctk.CTkFrame(edit_card, fg_color="transparent")
        btn_frame.pack(side="bottom", pady=25)

        cancel_btn = ctk.CTkButton(
            btn_frame, text="Cancel", width=160, height=40,
            font=("Segoe UI", 13, "bold"), fg_color="#6B7280", hover_color="#4B5563",
            corner_radius=8, command=lambda: self.show_customer_profile(username)
        )
        cancel_btn.pack(side="left", padx=10)

        save_btn = ctk.CTkButton(
            btn_frame, text="Save Changes", width=160, height=40,
            font=("Segoe UI", 13, "bold"), fg_color="#16A34A", hover_color="#15803D",
            corner_radius=8, command=save_changes
        )
        save_btn.pack(side="left", padx=10)

    def show_favourite_heart(self, username):
        """Displays the user's favorite movies watchlist page."""
        self.clear_window()
        self.root.title(f"{username}'s Favorite Movies - Watchlist")

        main_container = ctk.CTkFrame(self.root, fg_color="#E5E7EB")
        main_container.pack(fill="both", expand=True)

        header_frame = ctk.CTkFrame(main_container, height=80, fg_color="#89B5F8", corner_radius=0)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        back_btn = ctk.CTkButton(
            header_frame, text="← Back to Main Page", width=160, height=38,
            font=("Segoe UI", 13, "bold"), fg_color="#3E75E3", hover_color="#2563EB",
            corner_radius=8, command=lambda: self.show_customer_dashboard(username)
        )
        back_btn.pack(side="left", padx=30)

        ctk.CTkLabel(
            header_frame, text=f"❤️ {username}'s Watchlist",
            font=("Segoe UI", 18, "bold"), text_color="#1F2937"
        ).pack(side="left", padx=20)

        scroll_content = ctk.CTkScrollableFrame(main_container, fg_color="#C1D7F9", width=1140, height=730)
        scroll_content.pack(fill="both", expand=True, padx=20, pady=15)

        grid_label = ctk.CTkLabel(scroll_content, text="Saved Favorite Movies", font=("Segoe UI", 16, "bold"), text_color="#1F2937")
        grid_label.pack(anchor="w", padx=10, pady=(10, 5))

        grid_frame = ctk.CTkFrame(scroll_content, fg_color="transparent")
        grid_frame.pack(fill="x", padx=10, pady=5)

        if not hasattr(self, "user_favorites"):
            self.user_favorites = {}
        fav_titles = self.user_favorites.get(username, set())

        all_movies = self._movies_as_list()
        favorite_movies = [m for m in all_movies if m["title"] in fav_titles]

        if not favorite_movies:
            no_fav_card = ctk.CTkFrame(grid_frame, fg_color="#FFFFFF", corner_radius=12, width=800, height=200)
            no_fav_card.pack(pady=40, padx=20)
            no_fav_card.pack_propagate(False)

            ctk.CTkLabel(
                no_fav_card, text="Your watchlist is empty! 💔",
                font=("Segoe UI", 20, "bold"), text_color="#1F2937"
            ).place(relx=0.5, rely=0.35, anchor="center")

            ctk.CTkLabel(
                no_fav_card, text="Click 'Add to Favorites' on any movie introduction page to save it here.",
                font=("Segoe UI", 13), text_color="#6B7280"
            ).place(relx=0.5, rely=0.55, anchor="center")
            return

        num_rows = (len(favorite_movies) + 2) // 3
        for row_idx in range(num_rows):
            row_box = ctk.CTkFrame(grid_frame, fg_color="transparent")
            row_box.pack(fill="x", pady=10)

            for col_idx in range(3):
                item_index = row_idx * 3 + col_idx
                if item_index < len(favorite_movies):
                    movie = favorite_movies[item_index]
                    m_title, m_info = movie["title"], movie["info"]

                    card_item = ctk.CTkFrame(
                        row_box, width=350, height=260, fg_color="#FFFFFF",
                        corner_radius=12, border_width=1, border_color="#E5E7EB"
                    )
                    card_item.pack(side="left", padx=12, expand=True)
                    card_item.pack_propagate(False)

                    img_box = ctk.CTkFrame(card_item, width=110, height=145, fg_color="#E5E7EB", corner_radius=8)
                    img_box.pack(pady=12)
                    img_label = ctk.CTkLabel(img_box, text="movie image", font=("Segoe UI", 13, "italic"), text_color="#6B7280")
                    img_label.place(relx=0.5, rely=0.5, anchor="center")

                    title_label = ctk.CTkLabel(card_item, text=m_title, font=("Segoe UI", 13, "bold"), text_color="#111827")
                    title_label.pack(anchor="w", padx=20)

                    info_label = ctk.CTkLabel(card_item, text=m_info, font=("Segoe UI", 11), text_color="#6B7280")
                    info_label.pack(anchor="w", padx=20)

                    for widget in (card_item, img_box, img_label, title_label, info_label):
                        widget.bind("<Button-1>", lambda e, mov=movie: self.show_movie_introduction_customer(mov, username))
                        widget.configure(cursor="hand2")


if __name__ == "__main__":
    Movie()
from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
from pandas import *
from tkinter import messagebox

# Load data for 18+ movies
data_18_plus = read_csv("IMDb_All.csv")
data_18_plus.columns = data_18_plus.columns.str.lower()

# Load data for movies under 18
data_under_18 = read_csv("IMDb_Under_18.csv")
data_under_18.columns = data_under_18.columns.str.lower()



def show_results(data, search_window, error_msg=None):
    if data.empty or error_msg:
        # Handle error or empty data situation
        error_message = error_msg if error_msg else "No results found. Please try different search criteria."
        messagebox.showerror("Error", error_message)
        return  # Exit the function early, preventing the results window from opening

    # Close the search window before opening the results window
    search_window.destroy()

    # Proceed with creating the results window if data is not empty and no error message
    result_window = Toplevel()
    result_window.title("Search Results")
    
    # Create a treeview with columns based on the DataFrame columns
    tree = ttk.Treeview(result_window)
    tree["columns"] = data.columns.tolist()
    tree["show"] = "headings"  # Hide the first column with the tree lines

    # Setup the columns and headings with dynamically adjusted widths
    column_widths = {col: max((len(col), data[col].astype(str).map(len).max())) for col in data.columns}
    for column in data.columns:
        tree.heading(column, text=column.replace("_", " ").title())
        tree.column(column, width=min(300, max(100, column_widths[column] * 7)))
    
    # Insert data into the treeview
    for index, row in data.iterrows():
        tree.insert("", END, values=row.tolist())
        
    # Add scrollbars
    h_scrollbar = ttk.Scrollbar(result_window, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=h_scrollbar.set)
    h_scrollbar.pack(side="bottom", fill="x")
    
    v_scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=v_scrollbar.set)
    v_scrollbar.pack(side="right", fill="y")
    
    tree.pack(side="left", fill="both", expand=True)



def search_data(data, title_entry, genre_entry, release_date_entry, rating_entry, actor_entry, director_entry, search_window, search_button):
    # Disable the search button to prevent multiple searches
    search_button.config(state="disabled")

    title_query = title_entry.get().strip()
    genre_query = genre_entry.get().strip()
    release_date_query = release_date_entry.get().strip()
    rating_query = rating_entry.get().strip()
    actor_query = actor_entry.get().strip()
    director_query = director_entry.get().strip()

    # Check if all fields are empty
    if not any([title_query, genre_query, release_date_query, rating_query, actor_query, director_query]):
        messagebox.showerror("Input Required", "Please enter search criteria in at least one field.")
        search_button.config(state="normal")  # Re-enable the search button
        return  # Exit the function to prevent further processing

    filtered_data = data
    error_msgs = []  # List to collect error messages

    # Apply filters
    if title_query:
        filtered_data = filtered_data[filtered_data["title"].str.contains(title_query, case=False, na=False)]
    if genre_query:
        filtered_data = filtered_data[filtered_data["genre"].str.contains(genre_query, case=False, na=False)]
    if release_date_query:
        try:
            release_year = int(release_date_query)
            if not 1920 <= release_year <= 2022:
                error_msgs.append("Invalid year. Please enter a year between 1920 and 2022.")
            else:
                filtered_data = filtered_data[filtered_data["year"] == release_year]
        except ValueError:
            error_msgs.append("Release year must be an integer between 1920 and 2022.")
    if rating_query:
        try:
            rating_num = float(rating_query)
            if not 1 <= rating_num <= 10:
                error_msgs.append("Rating should be between 1 and 10.")
            else:
                filtered_data = filtered_data[filtered_data["rating"] >= rating_num]
        except ValueError:
            error_msgs.append("Invalid rating. Please enter a number between 1 and 10.")
    if actor_query:
        filtered_data = filtered_data[filtered_data["actors"].str.contains(actor_query, case=False, na=False)]
    if director_query:
        filtered_data = filtered_data[filtered_data["director"].str.contains(director_query, case=False, na=False)]

    # Handle errors or no results
    if error_msgs or filtered_data.empty:
        if not error_msgs:  # If there are no specific error messages, assume no results were found
            error_msgs.append("No results found. Please adjust your search criteria.")
        error_message = "\n".join(error_msgs)
        messagebox.showerror("Search Error", error_message)
        search_button.config(state="normal")  # Re-enable the search button after error handling
    else:
        # Close the search window before showing the results
        search_window.destroy()
        show_results(filtered_data, search_window)



def create_search_window(data):
    search_window = Toplevel()
    search_window.title("Movie Explorer")
    
    def confirm_exit():
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
            search_window.quit()
            
    def confirm_and_go_back():
        if messagebox.askyesno("Confirm", "Are you sure you want to go back?"):
            search_window.destroy()

    # Labels
    title_label = Label(search_window, text="Movie Title:", font=("Aptos", 12, "bold"))
    title_label.grid(row=0, column=0, sticky=W, padx=(20,0), pady=(20,20))
    genre_label = Label(search_window, text="Genre:", font=("Aptos", 12, "bold"))
    genre_label.grid(row=3, column=0, sticky=W, padx=(20,0))
    release_date_label = Label(search_window, text="Release Date:", font=("Aptos", 12, "bold"))
    release_date_label.grid(row=5, column=0, sticky=W, padx=(20,0))
    rating_label = Label(search_window, text="Rating:", font=("Aptos", 12, "bold"))
    rating_label.grid(row=7, column=0, sticky=W, padx=(20,0))
    actor_label = Label(search_window, text="Actor:", font=("Aptos", 12, "bold"))
    actor_label.grid(row=9, column=0, sticky=W, padx=(20,0))
    director_label = Label(search_window, text="Director:", font=("Aptos", 12, "bold"))
    director_label.grid(row=11, column=0, sticky=W, padx=(20,0))

    # Entry widgets
    title_entry = Entry(search_window, width=50)
    title_entry.grid(row=0, column=1, padx=(5,0), pady=(20,20))
    genre_entry = Entry(search_window, width=50)
    genre_entry.grid(row=3, column=1, padx=(20,20))
    release_date_entry = Entry(search_window, width=50)
    release_date_entry.grid(row=5, column=1, padx=(20,20))
    rating_entry = Entry(search_window, width=50)
    rating_entry.grid(row=7, column=1, padx=(20,20))
    actor_entry = Entry(search_window, width=50)
    actor_entry.grid(row=9, column=1, padx=(20,20))
    director_entry = Entry(search_window, width=50)
    director_entry.grid(row=11, column=1, padx=(20,20))

    # Back button
    back_button = Button(search_window, text="Back", font=("Aptos", 12, "bold"), bg="black", fg="white", command=confirm_and_go_back)
    back_button.grid(row=13, column=0, pady=(20,20))
    
    # Search button will search the data_under_18 or the data_18_plus file depending on which button is clicked  
    search_button = Button(search_window, text="Search", font=("Aptos", 12, "bold"), bg="black", fg="white",
    command=lambda: search_data(
        data, title_entry, genre_entry, release_date_entry, rating_entry, actor_entry, director_entry, search_window, search_button))
    search_button.grid(row=13, column=1, pady=(20,20))
    
    # Exit button
    exit_button = Button(search_window, text="Exit", font=("Aptos", 12, "bold"), bg="black", fg="white", 
                         command=confirm_exit)
    exit_button.grid(row=13, column=2, padx=(20,40), pady=(20,20))
    
    
# Initialize the main window
root = Tk()
root.title("Movie Explorer")

# Load and resize images for the age selection buttons using Pillow
under_18_img = Image.open("Not 18 Minor Image.png")
under_18_img = under_18_img.resize((100, 100))  # Resizing to 100x100 pixels
under_18_photo = ImageTk.PhotoImage(under_18_img)

adult_img = Image.open("18 Adult Image.png")
adult_img = adult_img.resize((100, 100))  # Resizing to 100x100 pixels
adult_photo = ImageTk.PhotoImage(adult_img)

# Create the frame to hold the age selection images and buttons
selection_frame = Frame(root)
selection_frame.grid(pady=20, padx=20, row=0, column=0)

# Create labels for the age selection images
under_18_label = Label(selection_frame, image=under_18_photo)
under_18_label.grid(row=0, column=0, padx=20)

adult_label = Label(selection_frame, image=adult_photo)
adult_label.grid(row=0, column=1, padx=20)

# Create buttons and place them under the images
under_18_button = Button(root, text="Under 18", font=("Aptos", 12, "bold"), bg="black", fg="white",
                         command=lambda: create_search_window(data_under_18))
under_18_button.grid(row=1, column=0, padx=20, pady=10, sticky="w")

adult_button = Button(root, text="Adult 18+", font=("Aptos", 12, "bold"), bg="black", fg="white",
                      command=lambda: create_search_window(data_18_plus))
adult_button.grid(row=1, column=0, padx=20, pady=10, sticky="e")

# Start the main loop
root.mainloop()

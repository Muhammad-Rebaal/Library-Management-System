import datetime

class Book:
    def __init__(self, title, author, category, available=True, count=1):
        # Initialize book attributes
        self.title = title
        self.author = author
        self.category = category
        self.available = available
        self.count = count  # Number of copies of the book

    def increment_count(self):
        # Increment the count of book copies
        self.count += 1

class User:
    def __init__(self, username, password):
        # Initialize user attributes
        self.username = username
        self.password = password
        self.borrowed_books = []  # List to store borrowed books

class Library:
    def __init__(self):
        # Initialize library with books and users
        self.books = []  # List to store books
        self.users = []  # List to store users
        self.load_books_from_file()  # Load books from file
        self.load_users_from_file()  # Load users from file

    def load_books_from_file(self):
        try:
            # Read book data from file and populate the library
            with open("library.txt", "r") as file:
                for line in file:
                    # Parse book data from each line
                    data = line.strip().split(',')
                    title, author, category, available, count = data[0], data[1], data[2], bool(data[3]), int(data[4])
                    book = Book(title, author, category, available, count)
                    self.books.append(book)
        except FileNotFoundError:
            print("Library file not found. Starting with an empty library.")

    def save_books_to_file(self):
        # Save books data to file
        with open("library.txt", "w") as file:
            for book in self.books:
                file.write(f"{book.title},{book.author},{book.category},{book.available},{book.count}\n")

    def load_users_from_file(self):
        try:
            # Read user data from file and populate the user list
            with open("user.txt", "r") as file:
                for line in file:
                    data = line.strip().split(',')
                    username, password = data[0], data[1]
                    user = User(username, password)
                    self.users.append(user)
        except FileNotFoundError:
            print("User file not found. Starting with an empty user list.")

    def save_users_to_file(self):
        # Save user data to file
        with open("user.txt", "w") as file:
            for user in self.users:
                file.write(f"{user.username},{user.password}\n")

    # Function to add a new book to the library
    def add_book(self, title, author, category):
        existing_book = next((book for book in self.books if book.title.lower() == title.lower()), None)
        if existing_book:
            existing_book.increment_count()
            print(f"Another copy of '{title}' added to the library. Total: {existing_book.count}")
        else:
            book = Book(title, author, category)
            self.books.append(book)
            print(f"Book '{title}' by {author} added to the library.")

        self.save_books_to_file()

    # Function to display all books in the library
    def display_books(self):
        if not self.books:
            print("No books in the library.")
        else:
            print("Books available in the library:")
            for idx, book in enumerate(self.books, 1):
                status = "Available" if book.available else "Not Available"
                print(f"{idx}. {book.title} by {book.author} - Category: {book.category} - {status} - Copies: {book.count}")

    # Function to register a new user
    def register_user(self, username, password):
        user = User(username, password)
        self.users.append(user)
        print(f"User '{username}' registered successfully.")
        self.save_users_to_file()  # Save users after registration

    # Function to authenticate user login
    def authenticate_user(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

    # Function to allow a user to borrow a book
    def borrow_book(self, user, title):
        for book in self.books:
            if book.title.lower() == title.lower() and book.available:
                book.available = False
                user.borrowed_books.append(book)
                due_date = datetime.datetime.now() + datetime.timedelta(days=14)  # Due date is 14 days from now
                print(f"You have borrowed '{book.title}' by {book.author}. Please return by {due_date.strftime('%Y-%m-%d')}.")
                return
        print(f"Book '{title}' is either not available or does not exist in the library.")

    # Function to allow a user to return a book
    def return_book(self, user, title):
        for book in user.borrowed_books:
            if book.title.lower() == title.lower() and not book.available:
                book.available = True
                user.borrowed_books.remove(book)
                print(f"Thank you for returning '{book.title}' by {book.author}.")
                return
        print("Either the book was not borrowed or does not exist in your borrowed books.")

    # Function to display all registered users
    def display_users(self):
        if not self.users:
            print("No users in the system.")
        else:
            print("Users registered in the system:")
            for idx, user in enumerate(self.users, 1):
                print(f"{idx}. Username: {user.username}")

def main():
    # Main function to run the Library Management System
    library = Library()
    while True:
        print("\nLibrary Management System")
        print("1. Add a book")
        print("2. Display all books")
        print("3. Register a new user")
        print("4. Borrow a book")
        print("5. Return a book")
        print("6. Display all users")
        print("7. Quit")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            category = input("Enter book category: ")
            library.add_book(title, author, category)
        elif choice == "2":
            library.display_books()
        elif choice == "3":
            username = input("Enter username: ")
            password = input("Enter password: ")
            library.register_user(username, password)
        elif choice == "4":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user = library.authenticate_user(username, password)
            if user:
                title = input("Enter the title of the book you want to borrow: ")
                library.borrow_book(user, title)
            else:
                print("Invalid username or password.")
        elif choice == "5":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user = library.authenticate_user(username, password)
            if user:
                title = input("Enter the title of the book you want to return: ")
                library.return_book(user, title)
            else:
                print("Invalid username or password.")
        elif choice == "6":
            library.display_users()
        elif choice == "7":
            print("Thank you for using the Library Management System.")
            library.save_books_to_file()
            library.save_users_to_file()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()

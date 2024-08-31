import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import re

class Contact:
    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def __str__(self):
        return f"Name: {self.name}\nPhone: {self.phone}\nEmail: {self.email}\nAddress: {self.address}"

class ContactBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name, phone, email, address):
        contact = Contact(name, phone, email, address)
        self.contacts.append(contact)

    def view_contacts(self):
        return self.contacts

    def search_contact(self, search_term):
        results = [contact for contact in self.contacts if search_term.lower() in contact.name.lower() or search_term in contact.phone]
        return results

    def update_contact(self, old_name, new_name=None, new_phone=None, new_email=None, new_address=None):
        for contact in self.contacts:
            if contact.name.lower() == old_name.lower():
                if new_name:
                    contact.name = new_name
                if new_phone:
                    contact.phone = new_phone
                if new_email:
                    contact.email = new_email
                if new_address:
                    contact.address = new_address
                return f"Updated contact: {contact}"
        return "Contact not found"

    def delete_contact(self, name):
        for contact in self.contacts:
            if contact.name.lower() == name.lower():
                self.contacts.remove(contact)
                return f"Deleted contact: {name}"
        return "Contact not found"

class ContactBookApp:
    def __init__(self, root):
        self.contact_book = ContactBook()
        self.root = root
        self.root.title("Contact Book")
        self.root.configure(bg='lightblue')

        font_large = ("Arial", 14)

        self.title_label = tk.Label(root, text="Contact Book", font=("Arial", 24), bg='lightblue')
        self.title_label.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Contact", bg='lightpink', font=font_large, command=self.open_add_contact_window)
        self.add_button.pack(pady=10)

        self.search_button = tk.Button(root, text="Search Contact", bg='lightpink', font=font_large, command=self.open_search_contact_window)
        self.search_button.pack(pady=10)

        self.tree_frame = tk.Frame(root, bg='lightblue')
        self.tree_frame.pack(pady=10)

        self.tree = ttk.Treeview(self.tree_frame, columns=('No', 'Name', 'Phone', 'Email', 'Address', 'Actions'), show='headings')
        self.tree.heading('No', text='No')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Phone', text='Phone')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Address', text='Address')
        self.tree.heading('Actions', text='Actions')
        self.tree.column('No', width=30, anchor='center')
        self.tree.column('Name', width=100, anchor='center')
        self.tree.column('Phone', width=100, anchor='center')
        self.tree.column('Email', width=150, anchor='center')
        self.tree.column('Address', width=200, anchor='center')
        self.tree.column('Actions', width=200, anchor='center')

        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')

        self.no_contacts_label = tk.Label(self.tree_frame, text="No Contacts Added Yet!", font=font_large, bg='lightblue')

        self.update_contacts_list()

    def open_add_contact_window(self):
        self.open_contact_window("Add Contact", self.add_contact)

    def open_update_contact_window(self, contact):
        self.open_contact_window("Update Contact", self.update_contact, contact)

    def open_search_contact_window(self):
        search_term = simpledialog.askstring("Input", "Enter name or phone number to search:", parent=self.root)
        if search_term:
            results = self.contact_book.search_contact(search_term)
            self.display_search_results(results)

    def open_contact_window(self, title, action, contact=None):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("300x400")
        window.configure(bg='lightblue')

        font_large = ("Arial", 14)

        tk.Label(window, text="Name:", bg='lightblue', font=font_large).pack(pady=5)
        name_entry = tk.Entry(window, font=font_large)
        name_entry.pack(pady=5)
        if contact:
            name_entry.insert(0, contact.name)

        tk.Label(window, text="Phone:", bg='lightblue', font=font_large).pack(pady=5)
        phone_entry = tk.Entry(window, font=font_large)
        phone_entry.pack(pady=5)
        if contact:
            phone_entry.insert(0, contact.phone)

        tk.Label(window, text="Email:", bg='lightblue', font=font_large).pack(pady=5)
        email_entry = tk.Entry(window, font=font_large)
        email_entry.pack(pady=5)
        if contact:
            email_entry.insert(0, contact.email)

        tk.Label(window, text="Address:", bg='lightblue', font=font_large).pack(pady=5)
        address_entry = tk.Entry(window, font=font_large)
        address_entry.pack(pady=5)
        if contact:
            address_entry.insert(0, contact.address)

        def on_submit():
            name = name_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            address = address_entry.get()

            if not re.match(r'^\d{10}$', phone):
                messagebox.showerror("Error", "Phone number must be 10 digits.", parent=window)
                return

            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                messagebox.showerror("Error", "Invalid email address.", parent=window)
                return

            if title == "Add Contact":
                action(name, phone, email, address)
            else:
                action(contact.name, name, phone, email, address)

            self.update_contacts_list()
            window.destroy()

        submit_button = tk.Button(window, text="Submit", command=on_submit, font=font_large)
        submit_button.pack(pady=20)

    def add_contact(self, name, phone, email, address):
        self.contact_book.add_contact(name, phone, email, address)
        messagebox.showinfo("Success", "Contact added successfully!", parent=self.root)

    def update_contact(self, old_name, new_name, new_phone, new_email, new_address):
        result = self.contact_book.update_contact(old_name, new_name, new_phone, new_email, new_address)
        messagebox.showinfo("Update Contact", result, parent=self.root)

    def delete_contact(self, contact):
        result = self.contact_book.delete_contact(contact.name)
        messagebox.showinfo("Delete Contact", result, parent=self.root)
        self.update_contacts_list()

    def update_contacts_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        contacts = self.contact_book.view_contacts()
        if not contacts:
            self.tree.pack_forget()
            self.scrollbar.pack_forget()
            self.no_contacts_label.pack()
        else:
            self.no_contacts_label.pack_forget()
            self.tree.pack(side=tk.LEFT)
            self.scrollbar.pack(side=tk.RIGHT, fill='y')
            for idx, contact in enumerate(contacts, start=1):
                self.tree.insert('', 'end', values=(idx, contact.name, contact.phone, contact.email, contact.address))
                self.add_action_buttons(idx, contact)

    def add_action_buttons(self, idx, contact):
        tree_id = self.tree.get_children()[-1]
        edit_button = tk.Button(self.tree_frame, text="Edit", command=lambda c=contact: self.open_update_contact_window(c))
        delete_button = tk.Button(self.tree_frame, text="Delete", command=lambda c=contact: self.delete_contact(c))
        self.tree.set(tree_id, column="Actions", value="")
        self.tree_frame.update_idletasks()
        bbox = self.tree.bbox(tree_id, column="Actions")
        if bbox:
            edit_button.place(x=bbox[0], y=bbox[1])
            delete_button.place(x=bbox[0] + 60, y=bbox[1])

    def display_search_results(self, results):
        result_window = tk.Toplevel(self.root)
        result_window.title("Search Results")
        result_window.geometry("800x600")
        result_window.configure(bg='lightblue')

        # Create a style
        style = ttk.Style()

        # Set the theme to default
        style.theme_use('default')

        # Create the Treeview widget
        tree = ttk.Treeview(result_window, columns=('No', 'Name', 'Phone', 'Email', 'Address', 'Actions'), show='headings')
        tree.heading('No', text='No')
        tree.heading('Name', text='Name')
        tree.heading('Phone', text='Phone')
        tree.heading('Email', text='Email')
        tree.heading('Address', text='Address')
        # tree.heading('Actions', text='Actions')

        tree.column('No', width=30, anchor='center')
        tree.column('Name', width=100, anchor='center')
        tree.column('Phone', width=100, anchor='center')
        tree.column('Email', width=150, anchor='center')
        tree.column('Address', width=200, anchor='center')
        # tree.column('Actions', width=200, anchor='center')

        # Set the Treeview style before packing it
        tree.tag_configure('gray', background='#D3D3D3')
        tree.pack(fill='both', expand=True)


        for idx, contact in enumerate(results, start=1):
            tree.insert('', 'end', values=(idx, contact.name, contact.phone, contact.email, contact.address))

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()

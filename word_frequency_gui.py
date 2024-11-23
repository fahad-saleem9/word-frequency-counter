import tkinter as tk

class Node:    #linked list node
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    #function to insert at begining
    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
    #function to insert at end
    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = new_node
    #function to insert at any position
    def insert_at_position(self, data, position):
        new_node = Node(data)
        if position == 0:
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        for _ in range(position - 1):
            if current is None:
                raise ValueError("Position exceeds the length of the linked list")
            current = current.next

        new_node.next = current.next
        current.next = new_node
    #function of deletion
    #corner case 1: if list is empty
    def delete(self, data):
        if not self.head:
            return
        
        if self.head.data == data:
            self.head = self.head.next
            return

        current = self.head
        while current.next and current.next.data != data:
            current = current.next

        if current.next:
            current.next = current.next.next
            
    #function to display
    def display(self):
        current = self.head
        result = []
        while current:
            result.append(current.data)
            current = current.next
        return result
    #function to search 
    def search(self, data):
        current = self.head
        positions = []
        position = 0
        while current:
            position += 1
            if current.data == data:
                positions.append(position)
            current = current.next
        return positions

    #function to display word count(frequency)
    def word_frequency(self):
        frequency = {}
        current = self.head
        while current:
            word = current.data
            if word in frequency:
                frequency[word] += 1
            else:
                frequency[word] = 1
            current = current.next
        return frequency
    
    #making gui using tkinter
class WordFrequencyCounterApp:
    def __init__(self, master):
        self.master = master
        master.title("Word Frequency Counter")
        master.configure(bg="#0F1035")

        self.word_list = LinkedList()
        self.inserted_words = []
        self.deleted_words = []
        self.searched_positions = []

        self.paragraph_label = tk.Label(master, text="\tEnter the paragraph: \t", font=("Arial", 14), fg="white", bg="#0F1035", anchor='w')
        self.paragraph_label.pack(padx=5, pady=5, anchor='w')

        self.paragraph_entry = tk.Text(master, width=50, height=5, font=("Arial", 12), bg='#DCF2F1')
        self.paragraph_entry.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=True)

        scrollbar = tk.Scrollbar(master, command=self.paragraph_entry.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.paragraph_entry.config(yscrollcommand=scrollbar.set)

        self.word_label = tk.Label(master, text="Enter the word:", font=("Arial", 14), fg="white",bg="#0F1035")
        self.word_label.pack()

        self.word_entry = tk.Entry(master, width=50, font=("Arial", 12), bg='#DCF2F1')
        self.word_entry.pack()

        self.operation_label = tk.Label(master, text="Select operation:", font=("Arial", 14), fg="white",bg="#0F1035")
        self.operation_label.pack()

        self.operation_options = ["Insert", "Delete", "Search", "Display Frequency", "Total Words"]
        self.operation_var = tk.StringVar(master)
        self.operation_var.set(self.operation_options[0])

        self.operation_menu = tk.OptionMenu(master, self.operation_var, *self.operation_options)
        self.operation_menu.pack()

        self.position_label = tk.Label(master, text="Enter position (if applicable):", font=("Arial", 14), fg="white",bg="#0F1035")
        self.position_label.pack()

        self.position_entry = tk.Entry(master, width=50, font=("Arial", 12), bg='#DCF2F1')
        self.position_entry.pack()

        self.execute_button = tk.Button(master, text="Execute Operation", command=self.execute_operation, font=("Arial", 12), bg='green', fg='white')
        self.execute_button.pack()

        self.result_text = tk.Text(master, height=18, width=70, font=("Arial", 12), bg='#DCF2F1', fg='black')
        self.result_text.pack()

    def update_gui(self, text):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)

    def execute_operation(self):
        paragraph = self.paragraph_entry.get("1.0", tk.END) 

        self.word_list = LinkedList()
        words = paragraph.split()
        for word in words:
            self.word_list.insert_at_end(word)

        word_to_process = self.word_entry.get()
        operation = self.operation_var.get()
        position_entry = self.position_entry.get()

        try:
            position = int(position_entry)
        except ValueError:
            position = None

        updated_paragraph = ""  
        frequency_info = ""  

        if operation == "Insert":
            if position is not None:
                self.word_list.insert_at_position(word_to_process, position)
            else:
                self.word_list.insert_at_end(word_to_process)
            self.inserted_words.append((word_to_process, position))
            updated_paragraph = " ".join(map(str, self.word_list.display()))
        elif operation == "Delete":
            self.word_list.delete(word_to_process)
            self.deleted_words.append((word_to_process, -1)) 
            updated_paragraph = " ".join(map(str, self.word_list.display()))
        elif operation == "Search":
            positions = self.word_list.search(word_to_process)
            self.searched_positions.extend(positions)
            search_result = f"Word '{word_to_process}' found at positions: {', '.join(map(str, positions))}\n"
            self.update_gui(search_result)
            return  
        elif operation == "Display Frequency":
            frequency = self.word_list.word_frequency()
            updated_paragraph = " ".join(map(str, self.word_list.display()))
            operation_info = f"{operation}ed: {word_to_process}.\n"
            frequency_info = f"Inserted Words (with location): {self.inserted_words}\n"
            frequency_info += f"Deleted words (with position): {self.deleted_words}\n"
            frequency_info += f"Searched Words (with location): {self.searched_positions}\n"
            frequency_info += "Word Frequencies:\n"
            for word, count in frequency.items():
                frequency_info += f"{word}: {count}\n"
        elif operation == "Total Words":
            total_words = len(self.word_list.display())
            frequency_info = f"Total number of words: {total_words}\n"
        else:
            self.update_gui("Invalid operation selected")

        self.update_gui("Updated Paragraph: " + updated_paragraph + "\n" + frequency_info)

if __name__ == "__main__":
    root = tk.Tk()
    app = WordFrequencyCounterApp(root)
     #window size
    root.geometry("800x600")  
    root.mainloop()
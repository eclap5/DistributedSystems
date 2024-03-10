import xmlrpc.client

class NotebookClient:
    def __init__(self) -> None:
        try:
            self.server = xmlrpc.client.ServerProxy('http://localhost:8000')
        except ConnectionRefusedError:
            print('Server not running')
            exit(1)

    def addNote(self):
        topic = input('Enter topic: ')
        noteName = input('Enter note name: ')
        noteText = input('Enter note text: ')
        print(self.server.addNote(topic, noteName, noteText))

    def getNotes(self):
        topic = input('Enter topic: ')
        notes = self.server.getNotes(topic)
        for note in notes:
            print()
            print(f"Name: {note['name']}")
            print(f"Note: {note['text']}")
            print(f"Time: {note['timestamp']}")
    
    def searchWikipedia(self):
        searchTerm = input('Enter search term: ')
        topic = input('Enter topic for data to be added: ')
        data = self.server.getWikipediaData(searchTerm)
        if len(data) == 0:
            print('No data found')
        else:
            print(self.server.addNote(topic, 'Link to Wikipedia', data[3][0]))
    
if __name__ == '__main__':
    client = NotebookClient()
    
    while True:
        print('1. Add note')
        print('2. Get notes')
        print('3. Search Wikipedia')
        print('4. Exit')
        choice = input('Enter choice: ')
        
        if choice == '1':
            client.addNote()

        elif choice == '2':
            client.getNotes()

        elif choice == '3':
            client.searchWikipedia()

        elif choice == '4':
            break
        else:
            print('Invalid choice')
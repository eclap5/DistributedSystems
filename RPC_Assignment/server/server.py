import xmlrpc.server
import xml.etree.ElementTree as ET
import requests
import datetime

class NotebookServer:
    def __init__(self) -> None:
        self.database = 'notebook.xml'
        try:
            self.tree = ET.parse(self.database)
            self.root = self.tree.getroot()
        except (FileNotFoundError, ET.ParseError):
            self.root = ET.Element('notebook')
            self.tree = ET.ElementTree(self.root)
            self.tree.write(self.database)

    def findTopic(self, topic):
        for child in self.root.findall('topic'):
            if child.get('name') == topic:
                return child
        return ''

    def createNote(self, topic, noteName, noteText):
        newNote = ET.SubElement(topic, 'note', {'name': noteName})
        ET.SubElement(newNote, 'text').text = noteText
        ET.SubElement(newNote, 'timestamp').text = str(datetime.datetime.now().replace(microsecond=0))

    def addNote(self, topicName, noteName, noteText):
        topic = self.findTopic(topicName)
        if len(topic) == 0:
            topic = ET.SubElement(self.root, 'topic', {'name': topicName})

        self.createNote(topic, noteName, noteText)
        self.tree.write(self.database)
        return 'Note added successfully'

    def getNotes(self, topicName):
        notes = []
        topic = self.findTopic(topicName)
        if len(topic) == 0:
            return notes
        
        for note in topic.findall('note'):
            notes.append({
                'name': note.get('name'),
                'text': note.find('text').text,
                'timestamp': note.find('timestamp').text
            })

        return notes

    def getWikipediaData(self, searchTerm):
        url = 'https://en.wikipedia.org/w/api.php'
        params = {
            'action': 'opensearch',
            'format': 'json',
            'search': searchTerm,
            'namespace': 0,
            'limit': 1
        }
        try:
            response = requests.get(url, params=params)
            data = response.json()
            return data
        except requests.RequestException:
            print('Error fetching data from Wikipedia')
            return []


if __name__ == '__main__':
    port = 8000
    server = xmlrpc.server.SimpleXMLRPCServer(('localhost', port))
    server.register_instance(NotebookServer())
    server.serve_forever()
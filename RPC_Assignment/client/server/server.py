import xmlrpc.server
import xml.etree.ElementTree as ET
import datetime
import requests

class NotebookServer:
    def __init__(self) -> None:
        self.database = 'notebook.xml'

        self.tree = ET.parse(self.database)
        self.root = self.tree.getroot()

    def findTopic(self, topic):
        for child in self.root.findall('topic'):
            if child.get('name') == topic:
                return child
        return None

    def createNote(self, topic, name, note):
        newNote = ET.SubElement(topic, 'note', {'name': name})
        ET.SubElement(newNote, 'text').text = note
        ET.SubElement(newNote, 'timestamp').text = str(datetime.datetime.now().replace(microsecond=0))

    def addNote(self, topic, note):
        topic = self.findTopic(topic)
        if topic is None:
            topic = ET.SubElement(self.root, 'topic', {'name': topic})

        self.createNote(topic, note['name'], note['text'])
        self.tree.write(self.database)

    def getNotes(self, topic):
        notes = []
        topic = self.findTopic(topic)
        if topic is None:
            return notes
        
        for note in topic.findall('note'):
            notes.append({
                'name': note.get('name'),
                'text': note.find('text').text,
                'timestamp': note.find('timestamp').text
            })

        return notes
    
if __name__ == '__main__':
    server = xmlrpc.server.SimpleXMLRPCServer(('localhost', 8000))
    server.register_instance(NotebookServer())
    server.serve_forever()
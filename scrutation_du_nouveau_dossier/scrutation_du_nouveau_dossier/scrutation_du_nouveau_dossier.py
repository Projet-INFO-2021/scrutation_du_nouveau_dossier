import sys
import time
import logging
import watchdog
import nouveau_module
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import PatternMatchingEventHandler

def enlever_caractere(string):
    res = '' 
    for i in range(0, len(string)): 
        if i>= 2: 
            res = res + string[i] 
    return res

class MyHandler(PatternMatchingEventHandler):
    def process(self, event):

        with open(event.src_path, 'r') as xml_source:
            xml_string = xml_source.read()
            parsed = xmltodict.parse(xml_string)
            element = parsed.get('Pulsar', {}).get('OnAir', {}).get('media')
            if not element:
                return

            media = Media(
                title=element.get('title1'),
                description=element.get('title3'),
                media_id=element.get('media_id1'),
                hour=magicdate(element.get('hour')),
                length=element.get('title4')
            )
            media.save()

    def on_modified(self, event):
        print(event.src_path)

    def on_created(self, event):
        print(event.src_path)
        nouveau_module.ajout_module(enlever_caractere(event.src_path))
        

if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
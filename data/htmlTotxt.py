import html2text
import os

for filename in os.listdir('data/data'):
    if filename.endswith('.txt'):
        with open('data/data/' + filename, 'r', encoding='utf-8') as html:    
            w = open('data/results/plain_' + filename, 'w+', encoding='utf-8')
            lines = html.readlines()
            for line in lines:
                w.write(str(html2text.html2text(line))) #.encode('utf-8')
            html.close()
            w.close()



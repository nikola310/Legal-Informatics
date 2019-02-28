#!/usr/bin/python
from reldi.ner_tagger import NERTagger
from getpass import getpass
import Tkinter, tkFileDialog
import json
import io
import argparse
import os
user = 'igor_trpovski'
passwd = 'SifrazaIgoraSIAPreldi!2018'
coding ='utf8'

def write(result, file, judgement_id, directory):
    final=set()
    tokenID_to_ner={}

    with io.open(directory + os.path.sep + 'out' + os.path.sep + 'presuda_json_' + judgement_id + '.json','w',encoding="utf-8") as outfile:
        outfile.write(unicode(json.dumps(result, indent=2, ensure_ascii=False)))
    for ner_entity in result['namedEntities']['entity']:
        for tokenID in ner_entity["tokenIDs"].split(" "):
            tokenID_to_ner[tokenID]=ner_entity["value"]
    for sentence in result['sentences']['sentence']:
        token_array = sentence['tokenIDs'].split(' ')
        for tokenID in token_array:
            for token in result['tokens']['token']:
                if token['ID'] == tokenID:
                    token["sentenceID"] = sentence["ID"]
        final.add(sentence['tokenIDs'].split(' ')[-1])
        

    for token,lemma,tag, in zip(result['tokens']['token'],result['lemmas']['lemma'],result['POStags']['tag']):
        ner_entity=tokenID_to_ner.get(token["ID"],"O")
        file.write((judgement_id+'~'+token['sentenceID']+'~'+token['ID']+'\t'+token['text']+'\t'+lemma['text']+'\t'+tag['text']+'\t'+ner_entity+'\n').encode(coding))
        if token['ID'] in final:
            file.write('\n')
    file.close()

if __name__ == "__main__":

    directory = tkFileDialog.askdirectory()
    ner_tagger = NERTagger('sr')
    ner_tagger.authorize(user, passwd)

    if not os.path.exists(directory + os.path.sep + 'out'):
        os.mkdir(directory + os.path.sep + 'out')

    files=[e for e in os.listdir(directory) if e.endswith('.txt')]
    for index,file in enumerate(files):
        print 'Processing',index+1,'/',len(files) 
        judgement_id = file.split('_')[-1][:-4]
        if os.path.exists(directory + os.path.sep + 'out' + os.path.sep + 'presuda_one_line_' + judgement_id + '.txt.tagNERlem'):
            print 'Skipped'
            continue 
        write(json.loads(ner_tagger.tag(open(os.path.join(directory, file)).read().decode(coding).encode('utf8'))), open(os.path.join(directory + os.path.sep + 'out', file) + '.tagNERlem', 'w'), judgement_id, directory)
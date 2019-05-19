# coding=UTF-8
'''
Created on 7 May 2015

@author: Nikola Milosevic

Created at the University of Manchester, School of Computer Science
Licence GNU/GPL 3.0
'''
from tokeniser import tokenize_text, generate_tokenizer, process
rules = {
'ovnicxki':'',
'ovnicxka':'',
'ovnika':'',
'ovniku':'',
'ovnicxe':'',
'kujemo':'',
'ovacyu':'',
'ivacyu':'',
'isacyu':'',
'dosmo':'',
'ujemo':'',
'ijemo':'',
'ovski':'',
'ajucxi':'',
'icizma':'',
'ovima':'',
'ovnik':'',
'ognu':'',
'inju':'',
'enju':'',
'cxicyu':'',
'sxtva':'',
'ivao':'',
'ivala':'',
'ivalo':'',
'skog':'',
'ucxit':'',
'ujesx':'',
'ucyesx':'',
'ocyesx':'',
'osmo':'',
'ovao':'',
'ovala':'',
'ovali':'',
'ismo':'',
'ujem':'',
'esmo':'',
'asmo':'', #pravi gresku kod pevasmo
'zxemo':'',
'cyemo':'',
'cyemo':'',
'bemo':'',
'ovan':'',
'ivan':'',
'isan':'',
'uvsxi':'',
'ivsxi':'',
'evsxi':'',
'avsxi':'',
'sxucyi':'',
'uste':'',
'icxe':'i',#bilo ik
'acxe':'ak',
'uzxe':'ug',
'azxe':'ag',# mozda treba az, pokazati, pokazxe
'aci':'ak',
'oste':'',
'aca':'',
'enu':'',
'enom':'',
'enima':'',
'eta':'',
'etu':'',
'etom':'',
'adi':'',
'alja':'',
'nju':'nj',
'lju':'',
'lja':'',
'lji':'',
'lje':'',
'ljom':'',
'ljama':'',
'zi':'g',
'etima':'',
'ac':'',
'becyi':'beg',
'nem':'',
'nesx':'',
'ne':'',
'nemo':'',
'nimo':'',
'nite':'',
'nete':'',
'nu':'',
'ce':'',
'ci':'',
'cu':'',
'ca':'',
'cem':'',
'cima':'',
'sxcyu':'s',
'ara':'r',
'iste':'',
'este':'',
'aste':'',
'ujte':'',
'jete':'',
'jemo':'',
'jem':'',
'jesx':'',
'ijte':'',
'inje':'',
'anje':'',
'acxki':'',
'anje':'',
'inja':'',
'cima':'',
'alja':'',
'etu':'',
'nog':'',
'omu':'',
'emu':'',
'uju':'',
'iju':'',
'sko':'',
'eju':'',
'ahu':'',
'ucyu':'',
'icyu':'',
'ecyu':'',
'acyu':'',
'ocu':'',
'izi':'ig',
'ici':'ik',
'tko':'d',
'tka':'d',
'ast':'',
'tit':'',
'nusx':'',
'cyesx':'',
'cxno':'',
'cxni':'',
'cxna':'',
'uto':'',
'oro':'',
'eno':'',
'ano':'',
'umo':'',
'smo':'',
'imo':'',
'emo':'',
'ulo':'',
'sxlo':'',
'slo':'',
'ila':'',
'ilo':'',
'ski':'',
'ska':'',
'elo':'',
'njo':'',
'ovi':'',
'evi':'',
'uti':'',
'iti':'',
'eti':'',
'ati':'',
'vsxi':'',
'vsxi':'',
'ili':'',
'eli':'',
'ali':'',
'uji':'',
'nji':'',
'ucyi':'',
'sxcyi':'',
'ecyi':'',
'ucxi':'',
'oci':'',
'ove':'',
'eve':'',
'ute':'',
'ste':'',
'nte':'',
'kte':'',
'jte':'',
'ite':'',
'ete':'',
'cyi':'',
'usxe':'',
'esxe':'',
'asxe':'',
'une':'',
'ene':'',
'ule':'',
'ile':'',
'ele':'',
'ale':'',
'uke':'',
'tke':'',
'ske':'',
'uje':'',
'tje':'',
'ucye':'',
'sxcye':'',
'icye':'',
'ecye':'',
'ucxe':'',
'oce':'',
'ova':'',
'eva':'',
'ava':'av',
'uta':'',
'ata':'',
'ena':'',
'ima':'',
'ama':'',
'ela':'',
'ala':'',
'aka':'',
'aja':'',
'jmo':'',
'oga':'',
'ega':'',
'aća':'',
'oca':'',
'aba':'',
'cxki':'',
'ju':'',
'hu':'',
'cyu':'',
'cu':'',
'ut':'',
'it':'',
'et':'',
'at':'',
'usx':'',
'isx':'',
'esx':'',
'esx':'',
'uo':'',
'no':'',
'mo':'',
'mo':'',
'lo':'',
'ko':'',
'io':'',
'eo':'',
'ao':'',
'un':'',
'an':'',
'om':'',
'ni':'',
'im':'',
'em':'',
'uk':'',
'uj':'',
'oj':'',
'li':'',
'ci':'',
'uh':'',
'oh':'',
'ih':'',
'eh':'',
'ah':'',
'og':'',
'eg':'',
'te':'',
'sxe':'',
'le':'',
'ke':'',
'ko':'',
'ka':'',
'ti':'',
'he':'',
'cye':'',
'cxe':'',
'ad':'',
'ecy':'',
'ac':'',
'na':'',
'ma':'',
'ul':'',
'ku':'',
'la':'',
'nj':'nj',
'lj':'lj',
'ha':'',
'a':'',
'e':'',
'u':'',
'sx':'',
'o':'',
'i':'',
'j':'',
'i':''
         }
dictionary = {
#biti glagol
'bih':'biti',
'bi':'biti',
'bismo':'biti',
'biste':'biti',
'bisxe':'biti',
'budem':'biti',
'budesx':'biti',
'bude':'biti',
'budemo':'biti',
'budete':'biti',
'budu':'biti',
'bio':'biti',
'bila':'biti',
'bili':'biti',
'bile':'biti',
'biti':'biti',
'bijah':'biti',
'bijasxe':'biti',
'bijasmo':'biti',
'bijaste':'biti',
'bijahu':'biti',
'besxe':'biti',
#jesam
'sam':'jesam',
'si':'jesam',
'je':'jesam',
'smo':'jesam',
'ste':'jesam',
'su':'jesam',
'jesam':'jesam',
'jesi':'jesam',
'jeste':'jesam',
'jesmo':'jesam',
'jeste':'jesam',
'jesu':'jesam',
# glagol hteti
'cyu':'hteti',
'cyesx':'hteti',
'cye':'hteti',
'cyemo':'hteti',
'cyete':'hteti',
'hocyu':'hteti',
'hocyesx':'hteti',
'hocye':'hteti',
'hocyemo':'hteti',
'hocyete':'hteti',
'hocye':'hteti',
'hteo':'hteti',
'htela':'hteti',
'hteli':'hteti',
'htelo':'hteti',
'htele':'hteti',
'htedoh':'hteti',
'htede':'hteti',
'htede':'hteti',
'htedosmo':'hteti',
'htedoste':'hteti',
'htedosxe':'hteti',
'hteh':'hteti',
'hteti':'hteti',
'htejucyi':'hteti',
'htevsxi':'hteti',
# glagol moći
'mogu':'mocyi',
'možeš':'mocyi',
'može':'mocyi',
'možemo':'mocyi',
'možete':'mocyi',
'mogao':'mocyi',
'mogli':'mocyi',
'moći':'mocyi'
}

stop_words = ["biti", "ne", 
"jesam", "sam", "jesi", "si", "je", "jesmo", "smo", "jeste", "ste", "jesu", "su", "sa",
"nijesam", "nisam", "nijesi", "nisi", "nije", "nijesmo", "nismo", "nijeste", "niste", "nijesu", "nisu",
"budem", "budeš", "bude", "budemo", "budete", "budu", "budes",
"bih",  "bi", "bismo", "biste", "biše", "bise",
"bio", "bili", "budimo", "budite", "bila", "bilo", "bile", 
"cu", "ces", "ce", "cemo", "cete", "ceš",
"necu", "neces", "nece", "necemo", "necete", "neceš",
"mogu", "možeš", "može", "možemo", "možete",
"mozes", "moze", "mozemo", "mozete",
"i", "a", "ili", "ali", "pa", "te", "da", "u", "po", "na",
".", ",", "-", ";", ":", "?", "!", "+"]

def stem_arr(str):
    str = str.lower()
    str = str.replace("š", "sx")
    str = str.replace("č", "cx")
    str = str.replace("ć", "cy")
    str = str.replace("đ", "dx")
    str = str.replace("ž", "zx")
    lang = 'sr'
    mode = 'standard'
    tokenizer=generate_tokenizer(lang)
    lam = remove_stop_words(tokenize_text(process[mode](tokenizer,str,lang)))
    i = 0
    for word in lam:
        for key in dictionary:
            if key == word:
                lam[i]= dictionary[key]
                break
        for key in rules:
            if(word.endswith(key) and len(word)-len(key)>2):
                lam[i] = word[:-len(key)]+rules[key]
                break
        i = i+1
    return lam

def stem_str(str):
    str = str.lower()
    str = str.replace("š", "sx")
    str = str.replace("č", "cx")
    str = str.replace("ć", "cy")
    str = str.replace("đ", "dx")
    str = str.replace("ž", "zx")
    str = str.replace("Š", "sx")
    str = str.replace("Č", "cx")
    str = str.replace("Ć", "cy")
    str = str.replace("Đ", "dx")
    str = str.replace("Ž", "zx")
    str = str.replace("“","\"")
    str = str.replace("\"","")
    str = str.replace("”","\"")
    str = str.replace("'","\"")
    str = str.replace("’","\"")
    str = str.replace("€","eur")
    str = str.replace("„","\"")
    lang = 'sr'
    mode = 'standard'
    tokenizer=generate_tokenizer(lang)
    lam = remove_stop_words(tokenize_text(process[mode](tokenizer,str,lang)))
    i = 0
    for word in lam:
        for key in dictionary:
            if key == word:
                lam[i]= dictionary[key]
                break
        for key in rules:
            # Tokenize only words larger than 2 characters, apart from modal verbs
            if(word.endswith(key) and len(word)-len(key)>2):
                lam[i] = word[:-len(key)]+rules[key]
                break
        i = i+1
    end_str = "" 
    for word in lam:
        end_str = end_str+" "+word
    return end_str

def remove_stop_words(token_arr):
    retVal = []
    for token in token_arr:
        contains = False
        for stop_word in stop_words:
            if token == stop_word:
                contains = True
                break
        if not contains:
            retVal.append(token)

    return retVal




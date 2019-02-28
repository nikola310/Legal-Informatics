import Tkinter, tkFileDialog
import io
import os

directory = tkFileDialog.askdirectory()
files=[e for e in os.listdir(directory) if e.endswith('.txt')]
if not os.path.exists(directory + os.path.sep + 'out'):
    os.mkdir(directory + os.path.sep + 'out')

for index,fl in enumerate(files):
    print 'Processing',index+1,'/',len(files)

    judgement_id = fl.split('_')[-1][:-4]    
    with io.open(directory + os.path.sep + 'out' + os.path.sep + 'presuda_one_line_' + judgement_id + '.txt', "w+", encoding = "UTF-8") as no_spaces:
        with io.open(os.path.join(directory, fl), 'r', encoding = "UTF-8") as spaces:
            data = spaces.read().replace('\n', ' ')
            no_spaces.write(data)

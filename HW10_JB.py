#   line 45 to change the directory that this code works from/in
#   line 37 change exp to fullscreen w/ bool

import os, random 
from psychopy import visual, event, gui, core

instructions = 'Welcome to the Brinegar lab! \n\nFor this experiment, you will \
be completing 100 trials in which you will be presented with two images \
simultaneously. Your job is to determine if the two images are the same or \
different. If they are the same, type \'e\'. If they are different, type \
\'i\'. \n\nThere is an equal chance that each trial will be a \'same\' trial or \
a \'different\' trial. If you type an incorrect response, you will be shown \
feedback that lasts 2 seconds, but if you are correct, you will be able to \
proceed to the next trial. In that way, the more mistakes you make, the \
longer the experiment will take, so try to be as accurate as possible! \
\n\nHowever, we want you to be as quick as possible, too. Please keep your \
fingers on the keyboard so that you can make a quick decision. \
\n\nPlease let the researcher know if you have any questions. When you are \
ready to begin, press the spacebar.'

#   According to https://github.com/psychopy/psychopy/issues/4412 : 
#   "it is not currently possible to mark fields [in gui.Dlg] as required 
#   for locally run experiments". No known follow-up on this issue. 

#   Collect subject ID & demographics
demo_gui = gui.Dlg(title='Participant Demographics') # dialog box
demo_gui.addText('Please provide the following information before hitting \'OK\':')
demo_gui.addField('Subject number: ')
demo_gui.addField('Age: ')
demo_gui.addField('Gender: ', choices=['female','male','nonbinary','prefer not to say'])
demo_gui.show()
subj_num = demo_gui.data[0] #gui.data creates list of input ; call index 
age = demo_gui.data[1]
gender = demo_gui.data[2]

if demo_gui.OK: #if user presses ok, they will proceed to the experiment
    win = visual.Window(size=[800,800],color=[1,1,1],fullscr=False, units='pix')
    instructions = visual.TextStim(win=win,text=instructions,units='pix',color=[-1,-1,-1])
    instructions.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

#   add .png file names of a specified folder to a list of strings
    stim_list = []
    for file in os.listdir('/Users/jessicabrinegar/Desktop/HW10_JB'):
        if file.endswith(".png"):
           stim_list.append(file)
     
    keys = ['e', 'i'] # allowed input
    trial_types = ['same', 'different']
    
#   'Get ready' screen
    ready = visual.TextStim(win, 'Get Ready!', color=[-1, -1, -1], units='pix')
    ready.draw()
    win.flip()
    core.wait(2.0) # show the textstim for 2 seconds b4 proceeding
    
    clock = core.Clock() # clock will allow RT to be recorded
    
#   define some functions to be used in the loop
    def present_feedback():
        visual.TextStim(win=win, text=accuracy, color=[-1,-1,-1]).draw()
        win.flip()
        core.wait(2.0)
    def show_images(): 
        image.draw()
        image2.draw()
        win.flip()
        stim_list.remove(secondimage) #sample w/o replacement

#   experiment begins -- write all data to a file named 'Subj_{#}.csv'
    with open('Subj_' + str(subj_num) + '.csv', 'w') as datafile:
        datafile.write('Demos\n , SubjectID = ' + subj_num + ', Age = ' + age + ', Gender = ' + gender + '\nTrial, TrialType, Image1, Image2, CorrectResp, ActualResp, Accuracy, RT\n')
        for i in range(4): # 100 trials
            #   random.choice gives equal weights to each instance
            #   You can use random.choices if you want to set weights
            trial_key = random.choice(trial_types) # choose same or diff trial type
            clock.reset() # set the timer
            if trial_key == 'different':
                firstimage = random.choice(stim_list)
                image = visual.ImageStim(win, image=firstimage, units='pix', pos=(-200,0))
                #image = visual.ImageStim(win, image=firstimage,units='pix', pos=(-200,0))
                #   remove first image so it can't be chosen again
                stim_list.remove(firstimage)
                secondimage = random.choice(stim_list)
                image2 = visual.ImageStim(win=win, image=secondimage,units='pix', pos=(200,0))
                corrResp = 'i'
            else:
                firstimage = random.choice(stim_list)
                image = visual.ImageStim(win, image=firstimage, units='pix', pos=(-200,0))
                secondimage = firstimage
                image2 = visual.ImageStim(win, image=secondimage,units='pix', pos=(200,0))
                corrResp = 'e'
            show_images() # show images w/o replacing
            key = event.waitKeys(keyList=keys) # wait for 'e' or 'i' press
            RT = clock.getTime() # stop timer
            if 'e' in key:
                if trial_key == 'different':
                    accuracy = 'Incorrect'
                    present_feedback()
                else:
                    accuracy = 'Correct'
            elif 'i' in key:
                if trial_key == 'different':
                    accuracy = 'Correct'
                else:
                    accuracy = 'Incorrect'
                    present_feedback()
            datafile.write(str(i) + ',' + trial_key + ',' + firstimage + ',' + secondimage + ',' + corrResp + ',' + str(key[0]) + ',' + accuracy + ',' + str(RT) + '\n')
    thanks = visual.TextStim(win, 'Thank you for participating! Please let the researcher know you are finished. \n\n*Researcher presses q to exit*', color=[-1, -1, -1], units='pix')
    thanks.draw()
else: # if user pressed 'cancel', the exp will not run
    win = visual.Window(size=[800,800],color=[1,1,1],fullscr=False, units='pix')
    cancel = visual.TextStim(win=win,text='You have cancelled the experiment. Please inform the researcher. \n\n*Researcher presses q to exit*',units='pix',color=[-1,-1,-1])
    cancel.draw()
win.flip()
event.waitKeys(keyList=['q']) #press q to exit
win.close()

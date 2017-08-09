# BOB404

Manifest: 
The idea is to make an virtual assistant that looks like BOB from tv series dimension 404. The BOB ( in future can be called BOB404 or BOB ) is planed to be written in pure python, and is to be able to transmit coded "emotions" ( angry/sad when task is not done, judgy when you postponed, but all that in cute manner ). The overall language the BOB will be written is closly tied to speed and performance of python, if python is shown to be slow, there is possibility that some parts of BOB app will be coded in low level language. 

BOB is in its infancy, the idea is still fluid and aspects of his assistancy can change over time. 

The idea:
One window a bit sassy assistant, that can schedule your work, track your progress and give loving push when needed. 

Current workflow:
An browser based SVG GUI - abandoned
App/program based GUI - python > still on this idea

GUI:
- showing an emotion described by emotions.pdf
- alternating over emotions if condition is met
- overall dynamic presence 

-> additional info:
  Decided to go with hexadecimal limit for color system, so in future animation can go easly by defining steping variants of color, current lowest common denominator is 5 , since lcd(230,240) is 10 (2*5 ) with 23 and 24 steps respectfully. I personally belive that this will make my life easier when it becomes neccesery to implement color change animation by defining duration and steps needed for that duration. The duration of each change will influence the smoothness of transition so defining a time constant is next step when animating. So with base 5 , I can estimate that lcd can be 5,10,15,20,25 ... each defining number of steps.
  When talking about color, I am talking about RGB values in tuple based data type, so there are 3 places with each containing values from 0 - 255 (0xff) so by that definition i accepted functional oriented programming paradigm. 
  
Actions and control:
  GUI control, idea to control the gui is based upon command line and/or IP socket with BOB described port ( some free port ) to compensate for the long run time for future actions, BOB should have some "loading animation" emotion, or "working class" as i like to call it. 
  
-> currently leaning over IP socket

USER-BOB comunication:
 Comunication based upon USER/BOB will be in first on additional "console" of sort, simple text input editor with some refresh rate, but in final version BOB should have a VOICE. I am strictly against using robot vocie bank ( perhaps something cool and unexpected like Russel Brand or some other posh english dude ) and synthesis of speach should be AI, aka BOB should analize in its free time users speech modulation/cros faders and etc and implement them in his own speech. My background in audio engienieering should help with this issue.
 
-> Currently leaning on, data base of flat sounds of letters and then building mp3 file in bynary form and playing inside hidden python player. Pitch and modulation will be a problem that needs to be solved. 

-> Currently leaning on apearing console, for times when BOB is "confused" by pronuanciation so console will be permanent part of BOB404 but it will aper when needed ( or can be activated if person is mute/deaf ).

FREEDOM / NOT FREEDOM:
  Actual pressence of BOB404 in your computer is still to be established. I am currently not sure how deep BOB app should be allowed to go. Perpahs only fetching and tracking files, it would be start, but i am still not sure if BOB should be allowed to have acces to the system. 

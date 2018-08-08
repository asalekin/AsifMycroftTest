from mycroft.skills.core import FallbackSkill
from mycroft.skills.core import MycroftSkill, intent_handler
import nltk
from nltk.stem.porter import *
import json, socket
#from websocket import create_connection, WebSocket

class MeaningFallback(FallbackSkill):
    """
        A Fallback skill to answer the question about the
        meaning of life, the universe and everything.
    """

    #host = '10.12.101.149'
    #port = 7423


    fly_list=['aerial', 'aeriform', 'drone', 'astral', 'aero', 'aeri', 'bird', 'ether']
    launch_list=['fli', 'air', 'up', 'high', 'loft', 'sky', 'elev', 'altitud', 'atmosph', 'takeoff', 'off', 'launch']
    land_list=['down', 'put', 'drop', 'land', 'dock', 'settl']
    inspect_list=['surveil', 'monitor', 'inspect', 'accid', 'leak', 'gas', 'fire', 'examin', 'check', 'investig', 'scan', 'survey', 'inquir', 'scout']
    move_list=['go', 'move', 'take', 'park', 'depart', 'send', 'fli', 'spin', 'turn', 'rotat','bring', 'back', 'come']  # bring
    video_list=['view', 'video', 'look', 'see', 'observ', 'watch', 'show', 'display', 'bird', 'outlook', 'pictur', 'broadcast', 'record', 'eye', 'peek']
    location_list=['area', 'arena', 'block', 'build', 'circuit', 'corner', 'spot', 'divis', 'dominion', 'field', 'ground', 'hous', 'plot', 'place', 'provinc', 'point', 'region', 'section', 'station', 'space', 'sector', 'slot', 'territori', 'track', 'tract', 'turf', 'ward', 'zone', 'factori', 'locat', 'factori', 'laboratori', 'mill', 'warehous', 'lot', 'parkinglot', 'garag', 'anchorag', 'dock', 'harbor', 'pier', 'dock', 'port', 'berth', 'citi']

    pick_list=['deliv', 'pick', 'carri', 'transport', 'ferri', 'import', 'transfer', 'lift', 'fetch', 'ship', 'drop', 'put', 'set', 'situat']
    pickntake_list=['pick', 'take', 'import', 'lift', 'fetch']
    put_list=['drop', 'put', 'set', 'place', 'situat']
    package_list=['good', 'materi', 'shipment', 'object','packag', 'payload', 'box', 'cargo', 'load', 'product', 'packet', 'item', 'body']

    match_words=fly_list+launch_list+land_list+inspect_list+move_list+video_list+location_list+pick_list+pickntake_list+put_list+package_list

    machine_location_dict={}
    machine_type_dict={}

    machine_type_dict["shannon"]="ground"
    machine_location_dict["shannon"]=["base"]
    machine_type_dict["alexander"]="aerial"
    machine_location_dict["alexander"]=["base"]
    machine_type_dict["richie"]="ground"
    machine_location_dict["richie"]=["base"]

    Last_location=""
    Last_name=""
    stemmer = PorterStemmer()
    
    def __init__(self):
        super(MeaningFallback, self).__init__(name='Meaning Fallback')
        self.stemmer = PorterStemmer()

    def initialize(self):
        """
            Registers the fallback skill
        """
        self.register_fallback(self.handle_fallback, 1)

    def handle_fallback(self, message):
        """
            Answers question about the meaning of life, the universe
            and everything.
        """
        allwords = message.data.get("utterance")

        allwords=allwords.lower()
        allwords_words=allwords.split(" ")

        richie_sst_fix=['ritchi', 'richie', 'vici', 'ricci']
        ##################################################################################################################### for the demmo
        if any([a in richie_sst_fix for a in allwords_words]):
            allwords_words[[a in richie_sst_fix for a in allwords_words].index(True)]='richie'


        allwords_token=nltk.word_tokenize(allwords)

        if any([a in richie_sst_fix for a in allwords_token]):
            allwords_token[[a in richie_sst_fix for a in allwords_token].index(True)]='richie'
        word_stemmed = [self.stemmer.stem(plural) for plural in allwords_token]


        

        if any(s in self.match_words for s in word_stemmed):
 
            self.speak(message.data.get("utterance"))   #ricci  vici   channel  [ritchi,richie, vici, ricci]

            TASK=""
            LOCATION=[]
            Machine_Type="ground"
            Machine_NAME=""
            Location_index=[]

            
            posTagged=nltk.pos_tag(allwords_token)

            drone_flag=False
            drone_index=None

            if any(s in self.fly_list for s in word_stemmed):
                drone_index=[i for i, e in enumerate([s in self.fly_list for s in word_stemmed]) if e == True]
                drone_flag=True

            launch_flag=False
            launch_index=None

            if any(s in self.launch_list for s in word_stemmed):
                launch_index=[i for i, e in enumerate([s in self.launch_list for s in word_stemmed]) if e == True]
                launch_flag=True

            land_flag=False
            land_index=None
            if any(s in self.land_list for s in word_stemmed):
                land_index=[i for i, e in enumerate([s in self.land_list for s in word_stemmed]) if e == True]
                land_flag=True

            if drone_flag==True or launch_flag==True or land_flag==True:
                Machine_Type="aerial"

            ################################ get inspect info
            inspect_flag=False
            inspect_index=None

            if any(s in self.inspect_list for s in word_stemmed):
                inspect_index=[i for i, e in enumerate([s in self.inspect_list for s in word_stemmed]) if e == True]
                inspect_flag=True

            ################################ get move info
            move_flag=False
            move_index=None
            
            if any(s in self.move_list for s in word_stemmed):
                move_index=[i for i, e in enumerate([s in self.move_list for s in word_stemmed]) if e == True]
                move_flag=True

            ############################### get video info
            video_flag=False
            video_index=None
            
            if any(s in self.video_list for s in word_stemmed):
                video_index=[i for i, e in enumerate([s in self.video_list for s in word_stemmed]) if e == True]
                video_flag=True


            ################################ get area info
            location_flag=False
            location_index=None
            
            if any(s in self.location_list for s in word_stemmed):
                location_index=[i for i, e in enumerate([s in self.location_list for s in word_stemmed]) if e == True]
                location_flag=True

            ################################ get pick and deliver info
            pick_flag=False
            pick_index=None
          
            if any(s in self.pick_list for s in word_stemmed):
                pick_index=[i for i, e in enumerate([s in self.pick_list for s in word_stemmed]) if e == True]
                pick_flag=True

            pickntake_flag=False
            pickntake_index=None
            

            if any(s in self.pickntake_list for s in word_stemmed):
                pickntake_index=[i for i, e in enumerate([s in self.pickntake_list for s in word_stemmed]) if e == True]
                pickntake_flag=True

            ### 'drop', 'put', 'set', 'place', 'situat'
            put_flag=False
            put_index=None
            
            if any(s in self.put_list for s in word_stemmed):
                put_index=[i for i, e in enumerate([s in self.put_list for s in word_stemmed]) if e == True]
                put_flag=True

            ################################ get package info
            package_flag=False
            package_index=None
            
            if any(s in self.package_list for s in word_stemmed):
                package_index=[i for i, e in enumerate([s in self.package_list for s in word_stemmed]) if e == True]
                package_flag=True

            ################################ get robotname info
            MachineName_flag=False
            amachine=['robot', 'machine']
            if any(s in amachine for s in word_stemmed):
                amachine_index=[i for i, e in enumerate([s in amachine for s in word_stemmed]) if e == True]
                #print(amachine_index[0])
                if 'a' == allwords_words[amachine_index[0]-1]:
                    Machine_NAME=''
                    self.Last_name=''
                elif (len(posTagged)>(amachine_index[0]+1)) and ('NN' in posTagged[amachine_index[0]+1][1]):
                    Machine_NAME=allwords_words[amachine_index[0]+1]
                    MachineName_flag=True

                elif (len(posTagged)>(amachine_index[0]+2)) and ('VB' in posTagged[amachine_index[0]+1][1]) and ('NN' in posTagged[amachine_index[0]+2][1]):
                    Machine_NAME=allwords_words[amachine_index[0]+2]
                    MachineName_flag=True

                #elif ((amachine_index[0]-1)>=0) and ('NN' in posTagged[amachine_index[0]-1][1]):
                #    Machine_NAME=allwords_words[amachine_index[0]-1]
                #    MachineName_flag=True

                #elif ((amachine_index[0]-2)>=0) and ('VB' in posTagged[amachine_index[0]-1][1]) and ('NN' in posTagged[amachine_index[0]-2][1]):
                #    Machine_NAME=allwords_words[amachine_index[0]-2]
                #    MachineName_flag=True

            elif 'drone' in word_stemmed:
                Machine_NAME='alexander'
                MachineName_flag=True


            # machine_location_dict[Machine_NAME]
            if MachineName_flag==False:
                for keys in self.machine_location_dict.keys():
                    if keys in allwords:
                        Machine_NAME=keys
                        MachineName_flag=True

                        Machine_Type=self.machine_type_dict[keys]   ############ retrieve the machines type from dictionary


            ########################## launch or land logic

            if launch_flag==True and location_flag==False:
                TASK="takeoff"
            elif launch_flag==True:
                TASK="move"   # if drone move to the same place it already is, launch or land
            elif land_flag==True:
                TASK="landAt"
            elif move_flag==True:
                TASK="move"

            if inspect_flag==True:
                TASK="surveillance"
            elif video_flag==True:
                TASK="view"
            ##################################################################################### for the demo
            if Machine_Type=='aerial':
                Machine_NAME='alexander'
            elif Machine_Type=='ground' and Machine_NAME=='alexander':
                Machine_NAME=''

            ####################################### machine name resolve
            if MachineName_flag==True:
                self.Last_name=Machine_NAME
            else:
                if ('camera' in allwords) and (location_flag==True):
                    Machine_NAME="static"
                    Machine_Type="static"
                else:
                    if self.Last_name!="":
                        Machine_NAME=self.Last_name
                        #Machine_Type=self.machine_type_dict[Machine_NAME]

                MachineName_flag=True

            if TASK=='view' and 'citi' in word_stemmed:
                Machine_NAME="static"
                Machine_Type="static"

            ###################################################################### pick and place

            if TASK=="" and (MachineName_flag==True or (self.Last_name != "")) and (location_flag==True or (self.Last_location != "")): ###################################### default task move
                TASK="move"

            ###### hand back/return
            back_word=['back', 'return']
            temp_LOCATION=[]

            ################################################################################################## for the demo when some location names are defined
            parking_lot_defined_locations=['parking', 'lot', 'parkinglot', 'garag']
            harbor_defined_locations=['anchorag', 'dock', 'harbor', 'pier', 'port', 'berth']
            warehouse_defined_locations=['warehous', 'white', 'house']

            if location_flag==True:
                for i in range(len(location_index)):
                    if (location_index[i]-1)>=0  and posTagged[location_index[i]-1][1]=='CD':
                        LOCATION.append(allwords_words[location_index[i]-1])
                        Location_index.append(location_index[i])

                    elif (len(posTagged)>(location_index[i]+1)) and posTagged[location_index[i]+1][1]=='CD':
                        LOCATION.append(allwords_words[location_index[i]+1])
                        Location_index.append(location_index[i])

                    elif (len(posTagged)>(location_index[i]+2)) and ('VB' in posTagged[location_index[i]+1][1]) and posTagged[location_index[i]+2][1]=='CD':
                        LOCATION.append(allwords_words[location_index[i]+2])
                        Location_index.append(location_index[i])

                    elif (location_index[i]-2)>=0  and ('VB' in posTagged[location_index[i]-1][1]) and posTagged[location_index[i]-2][1]=='CD':
                        LOCATION.append(allwords_words[location_index[i]-2])
                        Location_index.append(location_index[i])

                    else:
                        #temp_LOCATION.append(allwords_words[location_index[i]])   word_stemmed[location_index[i]]

                        if 'factori' in word_stemmed[location_index[i]]:
                            LOCATION.append("factory")
                            Location_index.append(location_index[i])
                            #warehouse_defined_locations

                        elif word_stemmed[location_index[i]] in warehouse_defined_locations:        #            'warehous' in word_stemmed[location_index[i]]:
                            LOCATION.append("warehouse")
                            Location_index.append(location_index[i])

                        elif allwords_token[location_index[i]] in parking_lot_defined_locations and ("parkinglot" not in LOCATION):
                            LOCATION.append("parkinglot")
                        elif word_stemmed[location_index[i]] in harbor_defined_locations:
                            LOCATION.append("harbor")
                            Location_index.append(location_index[i])
                            Location_index.append(location_index[i])


            else:
                if any(i in allwords for i in back_word) and MachineName_flag==True:  ############## handle back here
                    if Machine_NAME in self.machine_location_dict:
                        #######################################################################LOCATION=machine_location_dict[Machine_NAME]
                        temp_l=self.machine_location_dict[Machine_NAME]

                        if len(temp_l)<2:
                            LOCATION=['base']
                        else:
                            LOCATION=temp_l[len(temp_l)-2]
                    else:
                        LOCATION=self.Last_location
                else:
                    LOCATION=self.Last_location

            #if TASK=="PnP":                                                    ################ area na deowa thakle ki hbe ahnlde kora hoy nai
            if len(LOCATION)>1:
                if 'in' in word_stemmed:   #put_flag

                    if len(LOCATION)==1:
                        if put_flag==True:
                            LOCATION[0]='destination '+LOCATION[0]
                        else:
                            LOCATION[0]='source '+LOCATION[0]
                    else:
                        temp_min=1000
                        temp_min_index=1000
                        temp_index=word_stemmed.index('in')

                        for i in range(len(LOCATION)):
                            temp_l_index=Location_index[i]
                            if temp_l_index > temp_index:
                                if (temp_l_index - temp_index) < temp_min:
                                    temp_min=temp_l_index - temp_index
                                    temp_min_index=i

                        if temp_min<1000:
                            if put_flag==True:
                                LOCATION[temp_min_index]='destination '+LOCATION[temp_min_index]
                            else:
                                LOCATION[temp_min_index]='source '+LOCATION[temp_min_index]

                if 'on' in word_stemmed:   #put_flag

                    if len(LOCATION)==1:
                        if put_flag==True:
                            LOCATION[0]='destination '+LOCATION[0]
                        else:
                            LOCATION[0]='source '+LOCATION[0]
                    else:
                        temp_min=1000
                        temp_min_index=1000
                        temp_index=word_stemmed.index('on')

                        for i in range(len(LOCATION)):
                            temp_l_index=Location_index[i]
                            if temp_l_index > temp_index:
                                if (temp_l_index - temp_index) < temp_min:
                                    temp_min=temp_l_index - temp_index
                                    temp_min_index=i

                        if temp_min<1000:
                            if put_flag==True:
                                LOCATION[temp_min_index]='destination '+LOCATION[temp_min_index]
                            else:
                                LOCATION[temp_min_index]='source '+LOCATION[temp_min_index]

                if 'to' in word_stemmed:
                    if len(LOCATION)==1:
                        LOCATION[0]='destination '+LOCATION[0]

                    else:
                        temp_min=1000
                        temp_min_index=1000
                        #temp_index=word_stemmed.index('to')
                        temp_index=len(word_stemmed)-word_stemmed[::-1].index('to')-1


                        for i in range(len(LOCATION)):
                            temp_l_index=Location_index[i]
                            if temp_l_index > temp_index:
                                if (temp_l_index - temp_index) < temp_min:
                                    temp_min=temp_l_index - temp_index
                                    temp_min_index=i

                        if temp_min<1000:
                            LOCATION[temp_min_index]='destination '+LOCATION[temp_min_index]

                if 'from' in word_stemmed:

                    if len(LOCATION)==1:
                        LOCATION[0]='source '+LOCATION[0]

                    else:
                        temp_min=1000
                        temp_min_index=1000
                        #temp_index=word_stemmed.index('from')
                        temp_index=len(word_stemmed)-word_stemmed[::-1].index('from')-1

                        for i in range(len(LOCATION)):
                            temp_l_index=Location_index[i]
                            if temp_l_index > temp_index:
                                if (temp_l_index - temp_index) < temp_min:
                                    temp_min=temp_l_index - temp_index
                                    temp_min_index=i

                        if temp_min<1000:
                            LOCATION[temp_min_index]='source '+LOCATION[temp_min_index]

            if pick_flag==True or package_flag==True:  #pickntake_flag  put_flag
                TASK="pickAndPlace"
                #self.speak(str(len(LOCATION)))
                if len(LOCATION)==1:
                    if pickntake_flag ==True:
                        TASK="pick"
                        #LOCATION[0]='source '+LOCATION[0]
                    elif put_flag ==True:
                        TASK="place"
                        #LOCATION[0]='destination '+LOCATION[0]

            elif TASK=='move' and 'home' in word_stemmed:
                LOCATION=['base']
            ######################################## save machine location
            if len(LOCATION)==1:
                #Last_location=LOCATION
                if 'destination' in LOCATION[0]:
                    self.Last_location=LOCATION[0].split('destination ')[1]
                elif 'source' in LOCATION[0]:
                    self.Last_location=LOCATION[0].split('source ')[1]
                else:
                    self.Last_location=LOCATION

                ########################################################### saving individual machine location
                if Machine_NAME in self.machine_location_dict:
                    temp_l=self.machine_location_dict[Machine_NAME]
                    temp_l.append(self.Last_location)
                    if len(temp_l)>2:
                        del temp_l[0]
                    self.machine_location_dict[Machine_NAME]=temp_l
                elif Machine_NAME !="":
                    temp_l=[]
                    temp_l.append(self.Last_location)
                    self.machine_type_dict[Machine_NAME]=Machine_Type
                    self.machine_location_dict[Machine_NAME]=temp_l

            elif len(LOCATION)>1:
                for i in range(len(LOCATION)):
                    if 'destination' in LOCATION[i]:
                        self.Last_location=LOCATION[i].split('destination ')[1]

                        ########################################################### saving individual machine location
                        if Machine_NAME in self.machine_location_dict:
                            temp_l=self.machine_location_dict[Machine_NAME]
                            temp_l.append(self.Last_location)
                            if len(temp_l)>2:
                                del temp_l[0]
                            self.machine_location_dict[Machine_NAME]=temp_l
                        elif Machine_NAME !="":
                            temp_l=[]
                            temp_l.append(self.Last_location)
                            self.machine_type_dict[Machine_NAME]=Machine_Type
                            self.machine_location_dict[Machine_NAME]=temp_l

 
            serialized=json.dumps({'task':TASK, 'nickname':Machine_NAME, 'type':Machine_Type, 'destination':LOCATION}).encode('utf-8')
            self.speak("TASK "+TASK+ " Machine Name "+Machine_NAME+"  "+str(LOCATION).strip('[]'))

            #serialized=json.dumps({'Task': 'move', 'Nickname':'shannon', 'Type':'3', 'Location':'area 3'}).encode('utf-8')
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #clientsocket.connect(('10.12.100.22', 7423))  #'localhost', 9099
            clientsocket.connect(('localhost', 9011))
            clientsocket.sendall(serialized)
            clientsocket.close()

            """
            host = '10.12.101.149'
            port = 7423
            socket = socket.socket()
            serialized=json.dumps({'Task': 'move', 'Nickname':'shannon', 'Type':'3', 'Location':'area 3'}).encode('utf-8')
            socket.connect((host, port))

            socket.sendall(serialized)
            socket.close()

            try
                self.socket.connect((self.host, self.port))            
                self.socket.send('%d\n' % len(serialized))
                self.socket.sendall(serialized)
                self.socket.close()
                self.speak("TASK "+TASK+ " Machine Name "+Machine_NAME+"  "+str(LOCATION).strip('[]'))
            except (TypeError, ValueError), e:
                self.speak("Connection error")
            """

            return True # Indicate that the utterance was handled

        else:

            self.speak("Skill not matched and Speaker said "+utterance)
            return False

    def shutdown(self):
        """
            Remove this skill from list of fallback skills.
        """
        self.remove_fallback(self.handle_fallback)
        super(MeaningFallback, self).shutdown()


def create_skill():
    return MeaningFallback()

import dataCollection as data
import pandas as pd
import tbapy
import operator

class Team:
    def checkNull(self, x):
        if x == '':
            return(0)
        else:
            return(x)

    def average_list(self, input):
        holder = 0
        for num in input:
            holder += float(self.checkNull(num))
        return(round(holder / len(input), 1))

    def numberToLetters(self, q):
        q = q - 1
        result = ''
        while q >= 0:
            remain = q % 26
            result = chr(remain+65) + result;
            q = q//26 - 1
        return(result)

    def percent(self, input):
        x = round(input*100, 1)
        try:
            return(str(int(x))+'%')
        except:
            return(str(x)+'%')

    def combine_points(self, input1, input2):
        add = []
        if len(input1) > len(input2):
            smallest = input2
        else:
            smallest = input1
        
        for i in range(len(smallest)):
            add.append(int(self.checkNull(input1[i]))+int(self.checkNull(input2[i])))
        return(self.average_list(add))

    def four_comp(self, dict, inputs):
        largest = {'Names': [], 'Val': 0}
        output = ''
        for key in inputs:
            if (dict[key] - 3) > largest['Val']:
                largest = {'Names': [key+' Main'], 'Val': dict[key]}
            elif dict[key] > largest['Val']:
                largest = {'Names': [key], 'Val': dict[key]}
            elif dict[key] == largest['Val']:
                largest['Names'].append(key)
        for i in range(len(largest['Names'])):
            try:
                largest['Names'][i+1]
                output += largest['Names'][i]+' & '
            except:
                output += largest['Names'][i]
        return(output)


    def long_string(self, input1, input2, input3):
        #'Overall: '+str(averages['OHatch'])+' | Rocket Hatches: '+str(averages['Rocket Hatch'])+' | Rover Hatches: '+str(averages['Rover Hatch'])
        #0: String | 1: Val
        output = ''
        for curr in [input1, input2, input3]:
            if float(curr[1]) > 0:
                output += curr[0] + str(curr[1]) + ' | '
            else:
                if curr[0] == 'Overall: ':
                    output += 'Overall: 0(%)'
        return(output)


    def find_data(self):
        dependent_vars, raw_team_data = data.getSheet('B1:R1')[0], data.getSheet('B2:R')
        dlen, tlen, hlen = len(dependent_vars), len(raw_team_data), 0
        BLACK_LIST = ['the', 'they', '&', 'and', 'I', 'it', 'robot', 'team', '', ' ', 'a', 'is', 'to', 'N/A', 'an', 'match', 'not', 'their', 'too', 'only', 'on', 'was', 'off', 'of', 'for', 'as', 'by', 'other', 'Their']
        QT = {
            'ID': dependent_vars.index('ID of the Team'),
            'TLHatch': dependent_vars.index('# of ROCKET HATCHES'), #Rocket Hatches
            'TLCargo': dependent_vars.index('# of ROCKET CARGO'), #Rocket Cargo
            'TSHATCH': dependent_vars.index('# of ROVER HATCHES'), #Rover Hatches
            'TSCARGO': dependent_vars.index('# of ROVER CARGO'), #Rover Cargo
            'SHATCH': dependent_vars.index('How many S:Hatches?'), 
            'SCARGO': dependent_vars.index('How many S:Cargo?'),
            'lineCross': dependent_vars.index('Crossed HAB Line?'), 
            'startPos': dependent_vars.index('Starting Position'),
            'climb': dependent_vars.index('HAB Climbing'),
            'high': dependent_vars.index('How many times did the robot place a hatch or cargo level 2+ in the rocket?'),
            'playStyle': dependent_vars.index('What was the robot\'s play style?'),
            'help': dependent_vars.index('How much did the robot contribute to the team?'),
            'driving': dependent_vars.index('How would you rate the team\'s driving?'),
            'free': dependent_vars.index('Free Response (No more than a sentence or two)')
        }
        team_list = []
        for team in raw_team_data:
            if team[0] not in team_list:
                team_list.append(str(team[0]))
        df = pd.DataFrame(index=team_list)
        df['ID'] = None
        print("Analyzing data... ", end="\r", flush=True)
        for team_mod in team_list:
            output, actionDict = {}, {}
            for n in raw_team_data:
                if n[0] == team_mod:
                    for key, val in QT.items():
                        try:
                            try:
                                actionDict[key] += [n[val]]
                            except KeyError:
                                actionDict[key] = [n[val]]
                        except IndexError:
                            try:
                                actionDict[key] += ['']
                            except KeyError:
                                actionDict[key] = ['']
            #-----Averages
            averages = {
                'SHATCH': self.average_list(actionDict['SHATCH']),
                'SCARGO': self.average_list(actionDict['SCARGO']),
                'Rocket Hatch': self.average_list(actionDict['TLHatch']),
                'Rocket Cargo': self.average_list(actionDict['TLCargo']),
                'Rover Hatch': self.average_list(actionDict['TSHATCH']),
                'Rover Cargo': self.average_list(actionDict['TSCARGO']),
                'OHatch': self.combine_points(actionDict['TLHatch'], actionDict['TSHATCH']),
                'OCargo': self.combine_points(actionDict['TLCargo'], actionDict['TSCARGO'])
            }
            output['Tele Hatch'] = self.long_string(['Overall: ' , averages['OHatch']], ['Rocket Hatches: ', averages['Rocket Hatch']], ['Rover Hatches: ', averages['Rover Hatch']])
            output['Tele Cargo'] = self.long_string(['Overall: ' , averages['OCargo']], ['Rocket Cargo: ', averages['Rocket Cargo']], ['Rover Cargo: ', averages['Rover Cargo']])
            output['Sand Hatch'] = averages['SHATCH']
            output['Sand Cargo'] = averages['SCARGO']
            output['Driving'] = self.average_list(actionDict['driving'])
            output['Contribute'] = self.average_list(actionDict['help'])
            #----Teleop Phase
            output['type'] = self.four_comp(averages, ['Rocket Hatch', 'Rocket Cargo', 'Rover Hatch', 'Rover Cargo'])
            if averages['OCargo'] <= 0:
                if averages['OHatch'] <= 0:
                    output['type'] = 'Vegetable'
            #---Sandstorm Phase
            if averages['SCARGO'] < 0.4:
                if averages['SHATCH'] < 0.4:
                    output['start_type'] = 'No Plays'
            elif averages['SHATCH'] == averages['SCARGO']:
                output['start_type'] = 'Mixed'
            elif averages['SHATCH'] > averages['SCARGO']:
                output['start_type'] = 'Goes for Hatch'
            elif averages['SCARGO'] > averages['SHATCH']:
                output['start_type'] = 'Goes for Cargo'
            else:
                output['start_type'] = 'No Plays'
            #---Start Position
            output['startPos'] = 'No Pref'
            if actionDict['startPos'].count('L') - 1> actionDict['startPos'].count('R'):
                if actionDict['startPos'].count('L') - 1> actionDict['startPos'].count('M'):
                    output['startPos'] = 'Left'
            elif actionDict['startPos'].count('R') - 1> actionDict['startPos'].count('L'):
                if actionDict['startPos'].count('R') - 1> actionDict['startPos'].count('M'):
                    output['startPos'] = 'Right'
            elif actionDict['startPos'].count('M') - 1> actionDict['startPos'].count('L'):
                if actionDict['startPos'].count('M') - 1> actionDict['startPos'].count('M'):
                    output['startPos'] = 'Middle'
                
            #---Line Cross
            output['Line Cross'] = ('Overall: '+(self.percent((actionDict['lineCross'].count('Level 1') + actionDict['lineCross'].count('Level 2'))/len(actionDict['lineCross'])))+' | Level 2: '+self.percent(actionDict['lineCross'].count('Level 2')/len(actionDict['lineCross']))+' | Level 1: '+self.percent(actionDict['lineCross'].count('Level 1')/len(actionDict['lineCross'])))
            #---Climb 2+
            l2, l3 = self.percent((actionDict['climb'].count('Level 2')) / len(actionDict['climb'])), self.percent((actionDict['climb'].count('Level 3')) / len(actionDict['climb']))
            output['Climbs >2'] = ('Overall: '+(self.percent((actionDict['climb'].count('Level 2') + actionDict['climb'].count('Level 3'))/ len(actionDict['climb'])))+(' | L2: '+l2+' | L3: '+l3))
            climb_assist = actionDict['climb'].count('They helped another team climb')
            output['Climb Assists'] = (str(climb_assist)+' | '+self.percent(climb_assist / len(actionDict['climb'])))
            #---Playstyle
            if actionDict['playStyle'].count('Defensive') > actionDict['playStyle'].count('Aggressive'):
                if actionDict['playStyle'].count('Defensive') > actionDict['playStyle'].count('Both'):
                    output['playStyle'] = 'Defensive'
            elif actionDict['playStyle'].count('Aggressive') > actionDict['playStyle'].count('Defensive'):
                if actionDict['playStyle'].count('Aggressive') > actionDict['playStyle'].count('Both'):
                    output['playStyle'] = 'Agressive'
            elif actionDict['playStyle'].count('Both') > actionDict['playStyle'].count('Defensive'):
                if actionDict['playStyle'].count('Both') > actionDict['playStyle'].count('Aggressive'):
                    output['playStyle'] = 'Mixed'
            else:
                output['playStyle'] = 'Mixed'
            #output['Rocket Above 2+ Scores'] = '1-2: ' + str(actionDict['high'].count('1 - 2') / len(actionDict['high']) + '3+: ' + str(actionDict['high'].count('3+') / len(actionDict['high'])))
            
            #---Free Response
            word_list, checked, output['Key Words'] = [], [], {}
            for response in actionDict['free']:
                word_list += response.split(' ')
            for word in word_list:
                if word not in checked:
                    if word not in BLACK_LIST:
                        output['Key Words'][str(word)] = word_list.count(word)
                        checked.append(word)
            sorted_by_value, add = sorted(output['Key Words'].items(), key=lambda kv: kv[1]), {} #Sorts the similarity of each person by least to greatest
            sorted_by_value.reverse() #Reveres the order to greatest to least
            for n in sorted_by_value[:5]: #Removes anything after the 5th position
                add[n[0]] = n[1]
            output['Key Words'] = add
            
            output['Responses'] = actionDict['free']
            #--Final
            df.loc[team_mod]['ID'] = actionDict['ID'][0]
            for key, val in output.items():
                try:
                    df[key]
                except:
                    df[key] = None
                df.loc[team_mod][key] = str(val)
            holder = ['ID']
            for key, val in output.items():
                holder.append(str(key))
            if len(holder) > hlen:
                header, hlen = holder, len(holder)

            #Output
            print('Analyzing data... '+self.percent(team_list.index(team_mod)/len(team_list))+' | '+str(team_list.index(team_mod)+1)+'/'+str(len(team_list)), end="\t\r")
        print('Analyzing data... DONE!           ')
        df.to_excel("output.xlsx")
        listDf = df.values.tolist()
        data.update_values('1dYGGIlULMGon1FZJ3vn0u29EQvL7sjt-Wbo10JV9E7s', 'A:'+self.numberToLetters(dlen), 'RAW', [header]+listDf)
        return(df)

if __name__ == '__main__':
   Team().find_data()

import dataCollection as data
import pandas as pd
import tbapy
import operator


#print("Creating Dataframe... ", end="", flush=True)
#df.set_index(['ID of the Team'])
# print('DONE')
'''

Scout 
 - Data averaging 
 - just split it up

Data Collection 
 - get the data from the spread sheet
 
Runtime 
  - Runs the code base every match  

Worker 
 - IDEA (probaly not)
   Split the data into parts so that each worker can do it on its own thread 
'''

class Scout:

    def _check_null(self, x):
        if x == '':
            return(0)
        else:
            return(x)

    def average_list(self, input):
        holder = 0
        for num in input:
            holder += float(self._check_null(num))
        return(round(holder / len(input), 1))

    def numberToLetters(self, q):
        q = q - 1
        result = ''
        while q >= 0:
            remain = q % 26
            result = chr(remain+65) + result
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
            if dict[key] > largest['Val']:
                largest = {'Names': [key], 'Val': dict[key]}
            if dict[key] - 4 > largest['Val']:
                largest = {'Names': [key+' Speical'], 'Val': dict[key]}
            if dict[key] == largest['Val']:
                largest['Names'].append(key)
        for i in range(len(largest['Names'])):
            try:
                largest['Names'][i+1]
                output += largest['Names'][i]+' & '
            except:
                output += largest['Names'][i]
        return(output)


    def find_data(self):
        dependent_vars, raw_team_data = data.getSheet('B1:R1')[0], data.getSheet('B2:R')
        dlen, tlen = len(dependent_vars), len(raw_team_data)
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
            'high': dependent_vars.index('Did the robot constantly reach level 2+ on the rocket?'),
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
            # Split this up into little parts 
            output, actionDict = {'Line Cross': ''}, {}
            for n in raw_team_data:
                if n[0] == team_mod:
                    for key, val in QT.items():
                        try:
                            actionDict[key] += [n[val]]
                        except KeyError:
                            actionDict[key] = [n[val]]
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
            output['Tele Hatch'] = 'Overall: '+str(averages['OHatch'])+' | Rocket Hatches: '+str(averages['Rocket Hatch'])+' | Rover Hatches: '+str(averages['Rover Hatch'])
            output['Tele Cargo'] = 'Overall: '+str(averages['OCargo'])+' | Rocket Cargo: '+str(averages['Rocket Cargo'])+' | Rover Cargo: '+str(averages['Rover Cargo'])
            output['Sand Hatch'] = averages['SHATCH']
            output['Sand Cargo'] = averages['SCARGO']
            output['Driving'] = self.average_list(actionDict['driving'])
            output['Contribute'] = self.average_list(actionDict['help'])
            #----Teleop Phase
            output['type'] = self.four_comp(averages, ['Rocket Hatch', 'Rocket Cargo', 'Rover Hatch', 'Rover Cargo'])
            if averages['OCargo'] < 1:
                if averages['OHatch'] < 1:
                    output['type'] += 'Vegetable'
            #---Sandstorm Phase
            if averages['SHATCH'] == averages['SCARGO']:
                output['start_type'] = 'Mixed'
            elif averages['SHATCH'] > averages['SCARGO']:
                output['start_type'] = 'Goes for Hatch'
            elif averages['SCARGO'] > averages['SHATCH']:
                output['start_type'] = 'Goes for Cargo'
            elif averages['SCARGO'] < 1:
                if averages['SHATCH'] < 1:
                    output['start_type'] = 'No Plays'
            else:
                output['start_type'] = 'No Plays'
            # ---Start Position
            if actionDict['startPos'].count('L') > actionDict['startPos'].count('R'):
                if actionDict['startPos'].count('L') > actionDict['startPos'].count('M'):
                    output['startPos'] = 'Left'
            elif actionDict['startPos'].count('R') > actionDict['startPos'].count('L'):
                if actionDict['startPos'].count('R') > actionDict['startPos'].count('M'):
                    output['startPos'] = 'Right'
            elif actionDict['startPos'].count('M') > actionDict['startPos'].count('L'):
                if actionDict['startPos'].count('M') > actionDict['startPos'].count('M'):
                    output['startPos'] = 'Middle'
            else:
                output['startPos'] = 'Mixed'
            # ---Line Cross
            output['Line Cross'] = ('Overall: '+(self.percent((actionDict['lineCross'].count('Level 1') + actionDict['lineCross'].count('Level 2'))/len(actionDict['lineCross'])))+' | Level 2: '+self.percent(
                actionDict['lineCross'].count('Level 2')/len(actionDict['lineCross']))+' | Level 1: '+self.percent(actionDict['lineCross'].count('Level 1')/len(actionDict['lineCross'])))
            # ---Climb 2+
            l2, l3 = self.percent((actionDict['climb'].count('Level 2')) / len(actionDict['climb'])), self.percent(
                (actionDict['climb'].count('Level 3')) / len(actionDict['climb']))
            output['Climbs >2'] = ('Overall: '+(self.percent((actionDict['climb'].count('Level 2') +
                                                              actionDict['climb'].count('Level 3')) / len(actionDict['climb'])))+(' | L2: '+l2+' | L3: '+l3))
            climb_assist = actionDict['climb'].count(
                'They helped another team climb')
            output['Climb Assists'] = (
                str(climb_assist)+' | '+self.percent(climb_assist / len(actionDict['climb'])))
            # ---Playstyle
            if actionDict['playStyle'].count('Defensive') > actionDict['playStyle'].count('Aggressive'):
                if actionDict['playStyle'].count('Defensive') > actionDict['playStyle'].count('MBoth'):
                    output['startPos'] = 'Defensive'
            elif actionDict['playStyle'].count('Aggressive') > actionDict['playStyle'].count('Defensive'):
                if actionDict['playStyle'].count('Aggressive') > actionDict['playStyle'].count('Both'):
                    output['startPos'] = 'Agressive'
            elif actionDict['playStyle'].count('Both') > actionDict['playStyle'].count('Defensive'):
                if actionDict['playStyle'].count('Both') > actionDict['playStyle'].count('Aggressive'):
                    output['startPos'] = 'Both'
            else:
                output['startPos'] = 'Mixed'
            output['Rocket Above 2+ Scores'] = actionDict['high'].count('Yes') / len(actionDict['high'])
            #---Free Response
            word_list, checked, output['Key Words'] = [], [], {}
            for response in actionDict['free']:
                word_list += response.split(' ')
            for word in word_list:
                if word not in checked:
                    output['Key Words'][str(word)] = word_list.count(word)
                    checked.append(word)
            sorted_by_value, add = sorted(output['Key Words'].items(), key=lambda kv: kv[1]), {
            }  # Sorts the similarity of each person by least to greatest
            sorted_by_value.reverse()  # Reveres the order to greatest to least
            # Removes anything after the 5th position
            for n in sorted_by_value[:5]:
                add[n[0]] = n[1]
            output['Key Words'] = add
            # --Final
            header = ['ID']
            df.loc[team_mod]['ID'] = actionDict['ID'][0]
            for key, val in output.items():
                try:
                    df[key]
                except:
                    df[key] = None
                df.loc[team_mod][key] = str(val)
                header.append(key)
            # Output
            print('Analyzing data... '+self.percent(team_list.index(team_mod)/len(team_list)) +
                  ' | '+str(team_list.index(team_mod)+1)+'/'+str(len(team_list)), end="%\t\r")
        print('Analyzing data... DONE!           ')
        df.to_excel("output.xlsx")
        listDf = df.values.tolist()
        data.update_values('1dYGGIlULMGon1FZJ3vn0u29EQvL7sjt-Wbo10JV9E7s',
                           'A:'+self.number_to_letters(dlen), 'RAW', [header]+listDf)
        return(df)


if __name__ == '__main__':
    print(Scout().find_data())

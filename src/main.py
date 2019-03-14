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

    def number_to_letters(self, q):
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

    def find_data(self):
        '''
        Gets data from the sheets 
        get the length of them 
        Creates a dict that holds the items names and then goes through dv to find the correlating part
        creates a team_list array 
        goes through the teams in the spread sheet and adds them to an array if they are not there already
        creates a panda data frame
        Goes through each team and goes through data 
        '''
        dependent_vars, raw_team_data = data.getSheet(
            'B1:O1')[0], data.getSheet('B2:O')
        dlen, tlen = len(dependent_vars), len(raw_team_data)
        QT = {
            'ID': dependent_vars.index('ID of the Team'),
            'THatch': dependent_vars.index('How many hatches did they mount?'),
            'TCargo': dependent_vars.index('How much cargo did they secure?'),
            'SHatch': dependent_vars.index('How many S:Hatches?'),
            'SCargo': dependent_vars.index('How many S:Cargo?'),
            'lineCross': dependent_vars.index('Crossed HAB Line?'),
            'startPos': dependent_vars.index('Starting Position'),
            'climb': dependent_vars.index('HAB Climbing'),
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
            # -----Averages
            hatch_avg = self.average_list(actionDict['THatch'])
            ball_avg = self.average_list(actionDict['TCargo'])
            sHatch_avg = self.average_list(actionDict['SHatch'])
            sBall_avg = self.average_list(actionDict['SCargo'])
            output['Tele Hatch'] = hatch_avg
            output['Tele Cargo'] = ball_avg
            output['Sand Hatch'] = sHatch_avg
            output['Sand Cargo'] = sBall_avg
            output['Driving'] = self.average_list(actionDict['driving'])
            output['Contribute'] = self.average_list(actionDict['help'])
            # ----Teleop Phase
            if hatch_avg == ball_avg:
                output['type'] = 'Mixed'
            elif hatch_avg > ball_avg:
                output['type'] = 'Hatch Main'
            elif ball_avg > hatch_avg:
                output['type'] = 'Ball Main'
            elif hatch_avg - ball_avg > 4:
                output['type'] = 'Hard Hatch Main'
            elif ball_avg - hatch_avg > 4:
                output['type'] = 'Hard Ball Main'
            elif ball_avg < 1:
                if hatch_avg < 1:
                    output['type'] = 'Vegetable'
            else:
                output['type'] = 'No Plays'
            # ---Sandstorm Phase
            if sHatch_avg == sBall_avg:
                output['start_type'] = 'Mixed'
            elif sHatch_avg > sBall_avg:
                output['start_type'] = 'Goes for Hatch'
            elif sBall_avg > sHatch_avg:
                output['start_type'] = 'Goes for Cargo'
            elif sBall_avg < 1:
                if sHatch_avg < 1:
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
            # ---Free Response
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

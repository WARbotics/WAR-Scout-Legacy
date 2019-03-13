import dataCollection as data
import pandas as pd
import tbapy
import operator

dependent_vars, raw_team_data = data.getSheet('B1:O1')[0], data.getSheet('B2:O')
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

df = pd.DataFrame(team_list, index=team_list, columns=['ID'])
#print("Creating Dataframe... ", end="", flush=True)
#df.set_index(['ID of the Team'])
#print('DONE')

class Team:
    def average_list(self, input):
        holder = 0
        for num in input:
            holder += float(num)
        return(round(holder / len(list), 1))

    def find_data(self):
        print("Finding Types... ", end="\r", flush=True)
        df['Type'], df['Ball Avg'], df['Hatch Avg'] = None, None, None
        for team_mod in team_list:
            output, actionDict = {'type': 'Uknown', 'start_type': 'Uknown'}, {}
            for n in raw_team_data:
                if n[0] == team_mod:
                    for key, val in QT:
                        actionDict[key] = n[val]
            #-----Averages
            hatch_avg = self.average_list(actionDict['THatch'])
            ball_avg = self.average_list(actionDict['TCargo'])
            sHatch_avg = self.average_list(actionDict['SHatch'])
            sBall_avg = self.average_list(actionDict['SCargo'])
            #----Teleop Phase
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
            #---Sandstorm Phase
            if sHatch_avg == sBall_avg:
                output['start_type'] = 'Mixed'
            elif sHatch_avg > sBall_avg:
                output['start_type'] = 'Goes for Hatch'
            elif sBall_avg > sHatch_avg:
                output['start_type'] = 'Goes for Cargo'
            elif sBall_avg < 1:
                if sHatch_avg < 1:
                    output['start_type'] = 'No Plays'
            #---Start Position
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
            print('Finding Types... '+str(team_list.index(team_mod)/len(team_list)), end="%\r")
            df.loc[team_mod]['Type'], df.loc[team_mod]['Ball Avg'], df.loc[team_mod]['Hatch Avg'] = type, ball_avg, hatch_avg
        print('Finding Types... DONE!')

    

        
        

if __name__ == '__main__':
    Team().find_data()
    #df.loc['6925'].append('Hello')
    #print(df)
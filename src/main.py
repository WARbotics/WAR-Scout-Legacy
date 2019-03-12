import dataCollection as data
import pandas as pd
import tbapy
import operator

dependent_vars, raw_team_data = data.getSheet('B1:O1')[0], data.getSheet('B2:O')
dlen, tlen = len(dependent_vars), len(raw_team_data)
QT = {
    'THatch': dependent_vars.index('How many hatches did they mount?'), 
    'TCargo': dependent_vars.index('How much cargo did they secure?'), 
    'SHatch': dependent_vars.index('How many S:Hatches?'), 
    'lineCross': dependent_vars.index('Crossed HAB Line?'), 
    'startPos': dependent_vars.index('Starting Position'),
    'ID': dependent_vars.index('ID of the Team'),
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
            type_list, ball_list, hatch_list, sball_list, shatch_list, holder = [], [], [], [], [], 0
            #----Averages
            for n in raw_team_data:
                if n[0] == team_mod:
                    ball_list.append(n[QT['TCargo']])
                    hatch_list.append(n[QT['THatch']])
                    sball_list.append(n[QT['SCargo']])
                    shatch_list.append
            hatch_avg = self.average_list(hatch_list)
            ball_avg = self.average_list(ball_list)
            #----Types
            if hatch_avg == ball_avg:
                holder = 'Mixed'
            elif hatch_avg > ball_avg:
                holder = 'Hatch Main'
            elif ball_avg > hatch_avg:
                holder = 'Ball Main'
            elif hatch_avg - ball_avg > 4:
                holder = 'Hard Hatch Main'
            elif ball_avg - hatch_avg > 4:
                holder = 'Hard Ball Main'
            elif ball_avg == 0:
                if hatch_avg == 0:
                    holder = 'Vegetable'
            
            print('Finding Types... '+str(team_list.index(team_mod)/len(team_list)), end="%\r")
            df.loc[team_mod]['Type'], df.loc[team_mod]['Ball Avg'], df.loc[team_mod]['Hatch Avg'] = holder, ball_avg, hatch_avg
        print('Finding Types... DONE!')

    

        
        

if __name__ == '__main__':
    Team().find_data()
    #df.loc['6925'].append('Hello')
    print(df)
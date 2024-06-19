
from typing import List
import pandas as pd
from glob import glob


class Polla:
    def __init__(
            self, 
            master_file: str = 'master_plan.csv', 
            finalists_file: str = 'finalists.csv', 
            predictions_files: str = './predictions/*.txt', 
            scoreboard_file = 'scoreboard.csv'):
        self.master_file = master_file
        self.finalists_file = finalists_file
        self.predictions_files = predictions_files
        self.scoreboard_file = scoreboard_file
        self.master_plan, self.finalists = self.load()
        self.participants = []
        self.load_predictions()
    
    def load_predictions(self):
        for file in glob(self.predictions_files):
            data, last_four = self._parser_file(file)
            participant_name = file.split('\\')[-1].split('.txt')[0]
            self.participants.append(participant_name)
            self.master_plan[participant_name] = data
            self.finalists[participant_name] = last_four
        

    def load(self):
        master = pd.read_csv(self.master_file, index_col='Match')
        finalists = pd.read_csv(self.finalists_file, index_col='Position')
        return master, finalists

    
    def _parser_file(self, filename) -> List:
        with open(filename) as f:
            data = f.readlines()

        clean_data = [line.strip() for line in data]
        all_data_clean = []
        last_four = []

        i = 0
        for line in clean_data:
            if i < 24:
                all_data_clean.append(line)
            elif (
                (i >= 54 and i < 58) or
                (i >= 66 and i < 68) or
                (i >= 78 and i < 79) or
                (i >= 81 and i < 82)):
                all_data_clean.append(line[-5:])
            elif (i >= 84 and i < 88):
                last_four.append(line)
            
            i += 1
        return all_data_clean, last_four



    def _get_tendencia(self, row):
        if row['Status'] == 'pendiente':
            return '-'
        if row['goal_local'] == row['goal_visita']:
            return f"X|{int(row['goal_local'])}-{int(row['goal_visita'])}"
        elif row['goal_local'] > row['goal_visita']:
            return f"1|{int(row['goal_local'])}-{int(row['goal_visita'])}"
        else:
            return f"2|{int(row['goal_local'])}-{int(row['goal_visita'])}"


    def compute_results(self):
        self.master_plan['results'] = self.master_plan.apply(lambda row: self._get_tendencia(row), axis=1)


    def save(self):
        self.master_plan.to_csv(self.master_file)
        self.finalists.to_csv(self.finalists_file)
        self.scoreboard.to_csv(self.scoreboard_file)
        print('All saved!')


    def build_scoreboard(self):
        scoreboard = {k: self._get_points(k, self.master_plan) + self._get_points_finalists(k, self.finalists) for k in self.participants}
        scoreboard =  {k: v for k, v in sorted(scoreboard.items(), key=lambda item: item[1], reverse=True)}
        self.scoreboard = pd.DataFrame({'Position': [ x for x in range(1,len(self.participants)+1)], 'Participante':scoreboard.keys(), 'Points': scoreboard.values() }).set_index('Position')
        return self.scoreboard

    def _get_points_finalists(self, participant, df):
        total_score = 0
        for index, row in df[df.Status == 'jugado'].iterrows():
            if row.Results == row[participant]:
                total_score += 3
            elif row[participant] in df.Results:
                total_score += 1
        return total_score

    def _get_points(self, participant, df):
        total_score = 0
        for index, row in df[df.Status == 'jugado'].iterrows():
            if row.results == row[participant]:
                total_score += 3
            elif row.results[0:1] == row[participant][0:1]:
                total_score += 1
        return total_score
    
    def _write_scoreboard(self):
        output_markdown = [
            '# Copa America 2024\n',
            '\n',
            'This is a repo with a piece of code to keep track of the fantasy game with my friends',
            ' for the Copa America 2024.\n\n',
            '## Predicciones y resultados parciales\n',
            '- [Pronosticos y resultados](https://github.com/dasoto/polla/blob/main/master_plan.csv)\n'
            '## Scoreboard\n\n'
            '| Position | Nombre | Score |\n',
            '| -------- | ------ | ----- |\n',
            
            ]
        for index, row in self.scoreboard.iterrows():
            print(row)
            output_markdown.append(f'|{index}. | {row.Participante} | {row.Points} |\n')
        with open('README.md', 'w') as md:
            md.writelines(output_markdown)


if __name__ == '__main__':
    polla = Polla()
    polla.compute_results()
    scoreboard = polla.build_scoreboard()
    print(scoreboard)
    polla.save()

    polla._write_scoreboard()




# group_phase = clean_data[0:24]
# quarters = clean_data[54:58]
# semifinals = clean_data[66:68]
# third_fourth = clean_data[78:79]
# final = clean_data[81:82]
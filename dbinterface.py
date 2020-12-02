import csv
from pymongo import MongoClient

if __name__ == '__main__':
    input('Please, run the main program file.')


class DataBase:
    def __init__(self, name: str, auth_data: dict):
        db_name = auth_data['questionnaire'][name]
        user = auth_data['user']
        password = auth_data['password']

        appeal = f'mongodb+srv://{user}:{password}@cluster0.sonqc.mongodb.net/{db_name}?retryWrites=true&w=majority'

        self.db = MongoClient(appeal)['questionnaire'][db_name]
        self.__lambda_fun()

    def __lambda_fun(self):
        self._get_last_id = lambda: len(list(self.db.find())) - 1
        self.get_list_data = lambda: list(self.db.find())
        self.get_questions_ids = lambda: [el['_id'] for el in self.get_list_data()]
        self.remove_all_data = lambda: self.db.delete_many({})
        self.remove_questions = lambda *ids: [self.db.delete_one({'_id': id_}) for id_ in ids]

        self._remove_arg = lambda question_id, arg: self.db.update_one({
            '_id': question_id
        }, {
            '$pull': {'answers': arg}
        })

    def add(self, data: str, question_id: int = None):
        if question_id is None:
            last_id = self._get_last_id()
            post = {'_id': last_id + 1, 'question': data, 'answers': []}

            self.db.insert_one(post)
            return

        self.db.update_one({'_id': question_id}, {'$push': {'answers': data}})

    def show_all(self, file_name: str):
        rows = self.get_list_data()
        columns = [*rows[0].keys()] if rows else []

        with open(f'{file_name}.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, delimiter=';', fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)

    def show_ans(self, question_id: int):
        file_name = str(question_id)

        columns = ['answer_id', 'answer']
        rows = enumerate(self.db.find_one({'_id': question_id})['answers'])

        with open(f'{file_name}.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(columns)
            writer.writerows(rows)

    def remove_answers(self, question_id: int, *ids: int):
        questions = self.get_list_data()

        for question in questions:
            if question['_id'] == question_id:
                answers = question['answers']
                break
        else:
            return

        for id_ in ids:
            answer = answers[id_]
            self._remove_arg(question_id, answer)

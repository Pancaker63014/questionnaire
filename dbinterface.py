import json
import csv
import pymongo
from pymongo import MongoClient

if __name__ == '__main__':
    print('Please, run the main program file.')
    input()
    exit()


class DataBase:
    def __init__(self, name: str):
        """ TODO
        :param name:
        """

        with open('auth.json') as file:
            auth = json.load(file)

        db_name = auth['questionnaire'][name]
        user = auth['user']
        password = auth['password']

        appeal = f'mongodb+srv://{user}:{password}@cluster0.sonqc.mongodb.net/{db_name}?retryWrites=true&w=majority'

        self.db = MongoClient(appeal)['questionnaire'][db_name]
        self.__lambda_fun()

    def __lambda_fun(self):
        """
        Create self lambda functions for class.
        """

        self._get_last_id = lambda: len(list(self.db.find())) - 1
        self._get_list_data = lambda: list(self.db.find())
        self.remove_all_data = lambda: self.db.delete_many({})
        self.remove_questions = lambda *ids: [self.db.delete_one({'_id': id_}) for id_ in ids]

    def add(self, data: str, question_id: int = None):

        if question_id is None:
            last_id = self._get_last_id()
            post = {'_id': last_id + 1, 'question': data, 'answers': []}

            self.db.insert_one(post)
            return

        self.db.update_one({'_id': question_id}, {'$push': {'answers': data}})

    def show_all(self, file_name: str):
        """
        TODO
        :param file_name:
        :return:
        """

        rows = self._get_list_data()
        columns = [*rows[0].keys()] if rows else []

        with open(f'{file_name}.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, delimiter=';', fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)

    def show_ans(self, question_id: int):
        """
        TODO
        :param question_id:
        :return:
        """

        file_name = str(question_id)

        columns = ['answer_id', 'answer']
        rows = enumerate(self.db.find_one({'_id': question_id})['answers'])

        with open(f'{file_name}.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(columns)
            writer.writerows(rows)


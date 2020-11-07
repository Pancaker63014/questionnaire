from dbinterface import DataBase


def main():
    # auth.json
    db_result = DataBase(name='collection_name_results')
    db_request = DataBase(name='collection_name_questions')

    db_result.add('dsfg', question_id=1)

    # while True:
    #     question()
    #     result = input()
    #     save_res(result)


def question():
    pass


def save_res(result: str):
    pass


if __name__ == '__main__':
    main()

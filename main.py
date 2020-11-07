from dbinterface import DataBase


def main():
    """
    :return:
    """
    # auth.json
    db_result = DataBase(name='collection_name_results')
    db_request = DataBase(name='collection_name_questions')

    # while True:
    #     question()
    #     result = input()
    #     save_res(result)


def question():
    """
    :return:
    """
    pass


def save_res(result: str):
    """
    :param result:
    :return:
    """
    pass


if __name__ == '__main__':
    main()

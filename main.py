import json
from dbinterface import DataBase
from colorama import Fore, Style, init


def assistance():
    response('https://github.com/gitDev-ms/questionnaire#readme - use this to learn more')


def login(user: str = None, password: str = None):
    if user is None or password is None:
        user = INTERFACE['AUTH']['user']
        password = INTERFACE['AUTH']['password']

    INTERFACE['PROXY'] = (user == request(appeal='Username') and password == request(appeal='Password'))

    if INTERFACE['PROXY']:
        response('Success')
        return

    response(INTERFACE['ERRORS'][401])


def logout():
    if not INTERFACE['PROXY']:
        response(INTERFACE['ERRORS'][430])
        return

    INTERFACE['PROXY'] = False
    response('Success')


def report_all():
    if not INTERFACE['PROXY']:
        response(INTERFACE['ERRORS'][407])
        return

    try:
        INTERFACE['DB'].show_all(request(appeal='File name'))
        response('Success')
    except PermissionError:
        response('You are trying to modify an open file')


def report():
    if not INTERFACE['PROXY']:
        response(INTERFACE['ERRORS'][407])
        return

    input_data = request(appeal='Question ID').lower()
    if input_data == '-1' or input_data == 'all':
        report_all()
        return

    try:
        INTERFACE['DB'].show_ans(question_id=int(input_data))
        response('Success')
    except PermissionError:
        response(INTERFACE['ERRORS'][600])
    except TypeError:
        response(INTERFACE['ERRORS'][432])


def poll():
    for el in INTERFACE['DB'].get_list_data():
        id_, question, _ = el.values()
        response(question)
        INTERFACE['DB'].add(request(), id_)

    response('Thank for your responses')


def remove_data():
    if not INTERFACE['PROXY']:
        response(INTERFACE['ERRORS'][407])
        return

    response('What do you want to remove (q/a/all)?')
    input_data = request().lower()

    if input_data in ('a', 'answer', 'answers'):
        response('Enter the question id')
        question_id = int(request())

        if question_id not in INTERFACE['DB'].get_questions_ids():
            response(INTERFACE['ERRORS'][432])
            return
        
        response('Enter ids of answers separated by space')

        try:
            INTERFACE['DB'].remove_answers(question_id, *map(int, request().split()))
            response('Success')
        except IndexError:
            response(INTERFACE['ERRORS'][432])

        return

    if input_data in ('q', 'question', 'questions'):
        response('Enter ids of questions separated by space')
        INTERFACE['DB'].remove_questions(*map(int, request().split()))
        response('Success')
        return

    if input_data == 'all':
        INTERFACE['DB'].remove_all_data()
        response('Success')
        return

    response(INTERFACE['ERRORS'][400])


# ------------------------------------------------------------------------------------------------------------ #


def check(function):
    try:
        function()
    except Exception as e:
        response(str(e))


def auth():
    with open('auth.json') as file:
        return json.load(file)


def request(appeal: str = 'User'):
    print(Fore.GREEN, end='')
    return input(f'{appeal}: ')


def response(message: str): print(Fore.RED, 'Program: ' + message, Style.RESET_ALL, sep='')


INTERFACE = {
    'PREFIX': '/',
    'PROXY': False,
    'AUTH': auth(),
    'DB': DataBase(name='collection_name', auth_data=auth()),
    'COMMANDS': {
        'help': assistance,
        'exit': exit,
        'login': login,
        'logout': logout,
        'report all': report_all,
        'report': report,
        'start': poll,
        'remove': remove_data
    },
    'ERRORS': {
        400: 'Invalid request',
        401: 'Incorrect username or password',
        404: 'Command not found',
        407: 'Authentication required',
        418: 'I’m a teapot',
        430: 'Already done',
        432: 'No such data',
        520: 'Unknown Error',
        600: 'You are trying to modify an open file'
    }
}


def main():
    init()
    mainloop()


def mainloop():
    while True:
        input_data = request()

        if input_data.startswith(INTERFACE['PREFIX']):
            command = input_data[1:]

            if command in INTERFACE['COMMANDS']:
                check(INTERFACE['COMMANDS'][command])
                continue

            msg = INTERFACE['ERRORS'][404]

        else:
            msg = INTERFACE['ERRORS'][400]

        response(msg)


if __name__ == '__main__':
    main()

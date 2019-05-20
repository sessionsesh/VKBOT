import json

def get_button(label, color, payload=''):
    return {
        'action': {
            'type': 'text',
            'payload': json.dumps(payload),
            'label': label
        },
        'color': color
    }

def get_keyboard(keyboard):
    res = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    return str(res.decode('utf-8'))

# keyboard = {
#     'one_time': True,
#     'buttons': [
#         [get_button(label='На сегодня', color='positive')],
#         [get_button(label='На завтра', color='negative')],
#         [get_button(label='На эту неделю', color='primary')],
#         [get_button(label='На следующую неделю', color='default')],
#         [get_button(label='Какая группа?', color='default')],
#         [get_button(label='Какая неделя?', color='default')]
#
#     ]
# }





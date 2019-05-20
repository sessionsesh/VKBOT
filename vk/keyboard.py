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


keyboard = {
    'one_time': True,
    'buttons': [
        [get_button(label='На сегодня', color='positive')],
        [get_button(label='На завтра', color='negative')],
        [get_button(label='На эту неделю', color='primary')],
        [get_button(label='На следующую неделю', color='default')],
        [get_button(label='Какая группа?', color='default')],
        [get_button(label='Какая неделя?', color='default')]

    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

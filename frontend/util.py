import json
import sys
import threading


def write_filters_to_file(key, value):
    with open('filters.json') as f:
        text = f.read()
        if not text:
            text = '{}'
        filters = json.loads(text)

    filters[key] = value
    with open('filters.json', 'w') as f:
        f.write(filters)


def start_script(d, app):
    print('starting...')
    write_dict_to_file(d)
    sys.path.insert(0, './')
    import main
    t1 = threading.Thread(target = lambda: main.main(app))
    t1.start()


def write_dict_to_file(d):
    with open('filters.json', 'w') as f:
        f.write(json.dumps(d, indent = 4))



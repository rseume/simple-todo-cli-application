import click
import colorama
colorama.just_fix_windows_console()
colorama.init(autoreset=True)
from datetime import date
import os
from pathlib import Path
import json
from tabulate import tabulate

SETTINGS_FILE_NAME:     str = 'settings.json'
DEFAULT_SAVE_FILE_NAME: str = 'todos.json'

PRIORITIES = {
    'o': ('OPTIONAL', colorama.Fore.WHITE,  10),
    'l': ('LOW',      colorama.Fore.CYAN,   20),
    'm': ('MEDIUM',   colorama.Fore.GREEN,  30),
    'h': ('HIGH',     colorama.Fore.YELLOW, 40),
    'c': ('CRUCIAL',  colorama.Fore.RED,    50),
}


@click.group()
def _mycommands():
    pass


@click.command('add')
@click.argument('name', type=click.STRING, required=False)
@click.option('-n', '--name', 'name', type=click.STRING,
              required=True, default='new', show_default=True,
              prompt='Name', help='The name of the todo note you want to create.')
@click.option('-d', '--desc', 'desc', type=click.STRING,
              required=False, default='', show_default=False,
              prompt='Description', help='The description of the todo note you want to create.')
@click.option('-p', '--prio', 'prio', type=click.Choice(PRIORITIES.keys()),
              required=True, default='m', show_default=True,
              prompt='Priotiry', help='The priority of the todo note you want to create.')
def create_todo(name: str, desc: str, prio: int) -> None:
    """Create a new todo note and save it to the active file."""
    todo_list = _get_todo_list()
    name = _get_valid_name(name, todo_list)
    item = {
        'name': name,
        'desc': desc,
        'prio': prio,
        'date': str(date.today()),
    }
    todo_list.append(item)
    _save_todo_list(todo_list)
    click.echo('Todo note has been created successfully.')


@click.command('read')
@click.argument('idx', type=click.INT, required=True)
def read_todo(idx: int) -> None:
    """Displays all the info of the todo note with the given index."""
    todo_list = _get_todo_list()
    item = _get_todo_item(idx, todo_list)
    if item is not None:
        _print_todo(idx-1, item)


@click.command('readn')
@click.argument('name', type=click.STRING, required=True)
def read_todo_by_name(name: str) -> None:
    """Displays all the info of the todo note with the given name."""
    todo_list = _get_todo_list()
    # idx, item = _get_todo_item_by_name(name, todo_list)
    # if item is not None:
    #     _print_todo(idx, item)
    entry = _get_todo_item_by_name(name, todo_list)
    if entry is not None:
        _print_todo(entry[0], entry[1])


@click.command('read-all')
def read_all() -> None:
    """Display the full information of all todo notes in the active file."""
    todo_list = _get_todo_list()
    for i, x in enumerate(todo_list):
        _print_todo(i, x)


@click.command('edit')
@click.argument('idx', type=click.INT, required=True)
def update_todo(idx: int) -> None:
    """Edit the todo note with the given index."""
    todo_list = _get_todo_list()
    item = _get_todo_item(idx, todo_list)
    if item is None:
        return
    _update_todo(item)
    _save_todo_list(todo_list)
    click.echo('Todo not updated successfully.')


@click.command('editn')
@click.argument('name', type=click.STRING, required=True)
def update_todo_by_name(name: str) -> None:
    """Edit the todo note with the given name."""
    todo_list = _get_todo_list()
    # _, item = _get_todo_item_by_name(name, todo_list)
    # if item is None:
    #     return
    # _update_todo(item)
    entry = _get_todo_item_by_name(name, todo_list)
    if entry is None:
        return
    _update_todo(entry[1])
    _save_todo_list(todo_list)
    click.echo('Todo not updated successfully.')


@click.command('del')
@click.argument('idx', type=click.INT, required=True)
def delete_todo(idx: int) -> None:
    """Delete the todo note with the given index."""
    todo_list = _get_todo_list()
    if not _is_index_valid(idx, len(todo_list)):
        return
    del todo_list[idx-1]
    _save_todo_list(todo_list)
    click.echo('Todo note deleted successfully.')


@click.command('deln')
@click.argument('name', type=click.STRING, required=True)
def delete_todo_by_name(name: str) -> None:
    """Delete the todo note with the given name."""
    todo_list = _get_todo_list()
    idx, item = _get_todo_item_by_name(name, todo_list)
    if item is None:
        return
    # todo_list.remove(item)
    del todo_list[idx]
    _save_todo_list(todo_list)
    click.echo('Todo note deleted successfully.')


@click.command('list')
def list_todos() -> None:
    """List all todo notes in the active file."""
    todo_list = _get_todo_list()
    if len(todo_list) == 0:
        click.echo('No todo notes yet.')
        return
    # _print_todo_table(todo_list)
    _print_todo_table(((i, x) for i, x in enumerate(todo_list)))


@click.command('sort')
@click.argument('args', required=True, nargs=-1)
def sort_todos(args: tuple[str]) -> None:
    args = tuple(x.lower() for x in args)
    todo_list = _get_todo_list()
    if 'a' in args:
        todo_list.sort(key=lambda x: x['name'], reverse=False)
        click.echo('Notes sorted ascending alphabetical.')
    elif 'na' in args:
        todo_list.sort(key=lambda x: x['name'], reverse=True)
        click.echo('Notes sorted descending alphabetical.')
    if 'p' in args:
        todo_list.sort(key=lambda x: PRIORITIES[x['prio']][2], reverse=True)
        click.echo('Notes sorted ascending priority.')
    elif 'np' in args:
        todo_list.sort(key=lambda x: PRIORITIES[x['prio']][2], reverse=False)
        click.echo('Notes sorted descending priority.')
    if 'd' in args:
        todo_list.sort(key=lambda x: x['date'], reverse=True)
        click.echo('Notes sorted ascending creation date.')
    elif 'nd' in args:
        todo_list.sort(key=lambda x: x['date'], reverse=False)
        click.echo('Notes sorted descending creation date.')
    _save_todo_list(todo_list)


@click.command('clear')
def clear_todos() -> None:
    """Clear all todo notes in the active file."""
    if _confirm('Are you sure? Deleting all todo notes is not reversable?'):
        # if len(_get_todo_list()) == 0:
        #     click.echo('No notes to delete.')
        #     return
        _save_todo_list([])
        click.echo('All todo notes have been deleted successfully.')


@click.command('set-file')
@click.argument('filename')
def set_file(filename: str) -> None:
    _set_file(filename)


@click.command('add-file')
@click.argument('filename', type=str, required=1)
def create_file(filename: str) -> None:
    filename = _append_extension(filename, '.json')
    file_path = _get_env_path(('saves', filename))
    if os.path.exists(file_path):
        click.echo('The specified filename already exists. Not able to create it.')
        if not _confirm('Should it be overriden?'):
            return
    _create_save_file(file_path)
    click.echo(f'{filename} created successfully.')
    if _confirm('Should this file be used for storage?'):
        _set_file(filename)


@click.command('rename-file')
@click.argument('filename', type=str, required=1)
@click.argument('new_name', type=str, required=1)
def rename_file(filename: str, new_name: str) -> None:
    filename = _append_extension(filename, '.json')
    file_path = os.path.join(_get_env_path(('saves/', filename)))
    if not os.path.exists(file_path):
        click.echo('The specified filename does not exists. Please check your spelling.')
        return
    new_name = _append_extension(new_name, 'json')
    new_path = os.path.join(_get_env_path(('saves/', new_name)))
    os.rename(file_path, new_path)
    click.echo(f'Filename {filename} has been successfully renamed to {new_name}')


@click.command('del-file')
@click.argument('filename', type=str, required=1)
def delete_file(filename: str) -> None:
    # TODO: If active file is deleted ask the user to set a valid one.
    if not filename.lower().endswith('.json'):
        filename += '.json'
    file_path = os.path.join(_get_env_path(('saves/', filename)))
    if not os.path.exists(file_path):
        click.echo('The specified filename does not exists. Please check your spelling.')
        return
    os.remove(file_path)
    click.echo(f'{filename} has been removed successfully.')


@click.command('list-files')
def list_files() -> None:
    """Lists all files in the save directory."""
    file_list = os.listdir(_get_env_path(('saves/', )))
    for file in file_list:
        click.echo(Path(file).stem)


@click.command('clear-files')
def clear_files() -> None:
    if not _confirm('Are you sure? Delete all save files? This action is not reversable!'):
        return
    path = _get_env_path(('saves/', ))
    file_list = os.listdir(path)
    for file in file_list:
        os.remove(os.path.join(path, file))
    click.echo('All files cleared successfully.')
    # TODO: Reset saving file to default.


@click.command('info')
def display_info() -> None:
    settings = _get_settings()
    click.echo(f'Filename: {settings.get("filename")}')
    click.echo(f'Directory: {_get_env_path()}')


def _append_extension(filename: str, extension: str) -> None:
    if not filename.lower().endswith(extension):
        filename += extension
    return filename


def _set_file(filename: str) -> None:
    filename = _append_extension(filename, '.json')
    file_path = _get_env_path(('saves/', ))
    file_path = os.path.join(file_path, filename)
    if not os.path.exists(file_path):
        click.echo('A file with the specified name does not exist.')
        inp = click.prompt('Should it be create? [Y/n]')
        if not 'y' in inp.lower():
            return
        _create_save_file(file_path)
    settings = _get_settings()
    settings['filename'] = filename
    _save_settings(settings)
    click.echo(f'Active file is {filename}')


def _create_save_file(file_path: str) -> str:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w+') as f:
        json.dump([], f)


def _update_todo(item: dict) -> dict:
    item['name'] = click.prompt('New name', item['name'])
    item['desc'] = click.prompt('New description', item['desc'])
    item['prio'] = click.prompt('New priority', item['prio'])
    item['date'] = str(date.today())
    return item


def _print_todo_simple(idx: int, item: dict) -> None:
    # click.echo(f'({idx}) {item["name"]}\t{PRIORITIES[prio]}\t{item["date"]}')
    print(f'({idx})', f'{item["name"]}\t', _get_priority_as_text(item), f'{item["date"]}')


def _print_todo(idx: int, item: dict) -> None:
    # _print_todo_simple(idx, item)
    _print_todo_table(((idx, item), ))
    desc = item.get('desc')
    if desc is not None and desc.strip():
        click.echo(desc)


def _print_todo_table(notes: tuple[tuple[int, dict]]) -> None:
    table = tabulate(
        (
            (
                f'({i + 1})',
                x.get('name'),
                _get_priority_as_text(x),
                x.get('date'),
            ) for i, x in notes
        ),
        headers=(
            'Index',
            'Name',
            'Priority',
            'Date',
        )
    )
    click.echo(table)


def _confirm(msg: str) -> bool:
    inp = click.prompt(f'{msg} [Y/n]')
    if 'y' in inp.lower():
        return True
    click.echo('Aborted!')
    return False


def _is_index_valid(idx: int, lenght: int) -> bool:
    if idx < 1:
        click.echo('Index should not be less then 1!')
        return False
    if idx > lenght:
        click.echo(f'Input out of range. The list has maximal {lenght} item/s.')
        return False
    return True


def _get_valid_name(name: str, items: list[dict]) -> str:
    while True:
        while not name.strip():
            click.echo('Name must not be blank!')
            name = click.prompt('Please input a valid name')
        while any(x.get('name') == name for x in items):
            click.echo('The given name already exists in the file!')
            name = click.prompt('Please input a valid name')
        if not name.strip():
            continue
        return name.strip()


def _get_todo_item(idx: int, todo_list: list[dict]) -> dict:
    if _is_index_valid(idx, len(todo_list)):
        # We idx - 1 because the user should input indecies from 1 to len(count).
        return todo_list[idx-1]
    return None


def _get_todo_item_by_name(name: str, todo_list: list[dict]) -> tuple[int, dict]:
    try:
        idx, item = next((i, x) for i, x in enumerate(todo_list) if x.get('name') == name)
    except StopIteration:
        click.echo('No todo note with such name exists it this file! Please check your spelling.')
    else:
        return (idx, item)


def _get_priority_as_text(item: dict) -> str:
    prio = item.get('prio', 'm')
    if prio is None or prio not in PRIORITIES.keys():
        prio = 'm'
    prio = PRIORITIES[prio]
    return prio[1] + prio[0] + colorama.Style.RESET_ALL


def _get_todo_list() -> list[dict]:
    file_path = _get_save_file_path()
    try:
        with open(file_path, 'r') as f:
            todo_list = json.load(f)
    except json.decoder.JSONDecodeError as e:
        pass
    return todo_list


def _save_todo_list(todo_list: list[dict]) -> None:
    file_path = _get_save_file_path()
    with open(file_path, 'w') as f:
        json.dump(todo_list, f, indent=4)


def _get_save_file_path() -> str:
    filename = _get_settings()['filename']
    file_path = _get_env_path(('saves', filename))
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w+') as f:
            json.dump([], f)
    return file_path


def _get_settings() -> dict:
    file_path = _get_env_path((SETTINGS_FILE_NAME, ))
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w+') as f:
            data = {
                'filename': DEFAULT_SAVE_FILE_NAME,
            }
            json.dump(data, f)
        return data
    with open(file_path, 'r') as f:
        data: dict = json.load(f)
        if 'filename' not in data.keys():
            data['filename'] = DEFAULT_SAVE_FILE_NAME
    return data


def _save_settings(settings: dict) -> None:
    file_path = _get_env_path((SETTINGS_FILE_NAME, ))
    with open(file_path, 'w') as f:
        json.dump(settings, f)


def _get_env_path(dirs: tuple[str] = ()) -> str:
    local_appdata_path = os.getenv('LOCALAPPDATA')
    return os.path.join(local_appdata_path, 'Heisenbug', 'Todo', *dirs)


def _main() -> None:
    _mycommands.add_command(create_todo)
    _mycommands.add_command(read_todo)
    _mycommands.add_command(read_todo_by_name)
    _mycommands.add_command(read_all)
    _mycommands.add_command(update_todo)
    _mycommands.add_command(update_todo_by_name)
    _mycommands.add_command(delete_todo)
    _mycommands.add_command(delete_todo_by_name)
    _mycommands.add_command(list_todos)
    _mycommands.add_command(sort_todos)
    _mycommands.add_command(clear_todos)
    _mycommands.add_command(set_file)
    _mycommands.add_command(create_file)
    _mycommands.add_command(rename_file)
    _mycommands.add_command(delete_file)
    _mycommands.add_command(list_files)
    _mycommands.add_command(clear_files)
    _mycommands.add_command(display_info)
    _mycommands()


if __name__ == '__main__':
    _main()
    try:
        pass
    except click.exceptions.Abort:
        pass
    except Exception as e:
        print('Unexpected error occured. Please send the error log to us.')
        import logging
        import requests

        logging.basicConfig(level=logging.INFO, filename='log.log', filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s')

        logger = logging.getLogger(__name__)
        handler = logging.FileHandler(__name__ + '.log')
        formatter = logging.Formatter(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logger.exception(e)

        # TODO: Update the way the URL and the form is being handled
        url = 'https://docs.google.com/forms/d/e/1FAIpQLSfRpt2YNBeUfxc5ZhvetXl2VQ0zj6gjtcse0HUIU3jH6JiZmQ/'
        data = {
            'log_file': logger,
        }

        response = requests.post(url, data=data)
        if not response.ok:
            click.echo(
                f'something went wrong. You can visit this link and provide the log file at {handler.baseFilename} manualy'
            )

        exit(-1)
    else:
        import sys
        sys.exit(0)
    finally:
        pass

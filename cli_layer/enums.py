from enum import Enum
from rich import print

import typer

from db_layer.database import SqliteDb


class CategoryEnum(str, Enum):
    """
    Class for prompting the user to select from a list of choices.
    """
    @classmethod
    def from_category_list(cls, list_data):
        print(list_data)
        enum_values = [(name.upper(), name) for name in list_data]  # enum class attributes
        return cls("CategoryEnum", enum_values)


def load_category_enum():
    """
    Reads the database for list of category names and convert that into a CategoryEnum object.
    :return: CategoryEnum object instance
    """
    db = SqliteDb('ledger.db')
    category_names = db.get_category_names()
    db.close()
    if not category_names:
        result = CategoryEnum.from_category_list(['Assets', 'Liabilities'])
    else:
        result = CategoryEnum.from_category_list(category_names)
    return result


def load_accounts(enabled=True):
    db = SqliteDb('ledger.db')
    result = db.get_accounts(enabled=enabled)
    db.close()
    return result


CategoryChoice = load_category_enum()
enabled_accounts = load_accounts(enabled=True)
disabled_accounts = load_accounts(enabled=False)


def prompt_selected_choice(choices, matching_items=None):
    """
    Turns a list of strings into numbered choices for prompt, indenting matching items if provided.
    :param choices: list
    :param matching_items: list (optional)
    :return: str
    """
    tab_choices = []
    for index, choice in enumerate(choices):
        if matching_items and choice in matching_items:
            tab_choices.append(f"\t{index + 1}. {choice}")
        else:
            tab_choices.append(f"{index + 1}. {choice}")
    numbered_choices = "\n".join(tab_choices)

    choice = typer.prompt(f"Enter number to select:\n{numbered_choices}\t")
    try:
        index = int(choice) - 1
        selected_choice = choices[index]
        typer.echo(f"{selected_choice} selected.")
        return selected_choice
    except (ValueError, IndexError):
        typer.echo("Invalid choice. Please try again.")
        return prompt_selected_choice(choices)
        return prompt_selected_choice(choices, matching_items)


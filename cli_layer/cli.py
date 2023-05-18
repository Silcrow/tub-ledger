import typer

from cli_layer.enums import CategoryChoice
from models.accounting import Category, Account
from db_layer.database import SqliteDb

app = typer.Typer()

BLUE = "\033[94m"
RESET = "\033[0m"


@app.command()
def save_category(
        use_test_db: bool = False,
        name: str = typer.Option(..., prompt="What's the category name?"),
        parent: CategoryChoice = typer.Option(default=None, prompt="Select a parent category:",
                                              show_choices=True,
                                              case_sensitive=False),
        description: str = typer.Option("", prompt="Description?")
):
    kwargs = locals()
    del kwargs['use_test_db']
    # convert CategoryChoice obj to Category obj
    category_choice = kwargs['parent']
    category = Category.from_enum(category_choice)
    kwargs['parent'] = category

    category = Category.from_dict(kwargs)
    if use_test_db:
        db = SqliteDb('ledger.db', test=use_test_db)
        db.upsert_category(category)
        print(f"Saved {category.name} under {category.parent.name}.")
        db.close()
    else:
        if typer.confirm("Do you want to save?", default=True):
            db = SqliteDb('ledger.db', test=use_test_db)
            db.upsert_category(category)
            print(f"Saved {category.name} under {category.parent.name}.")
            db.close()
            typer.run(start_menu)
        else:
            typer.run(start_menu)
    return kwargs


@app.command()
def save_account(
        use_test_db: bool = False,
        name: str = typer.Option(..., prompt="What's the account name?"),
        value: float = typer.Option(0.0, prompt="What's the account balance?"),
        category: CategoryChoice = typer.Option(default=None, prompt="Select a category:",
                                                show_choices=True,
                                                case_sensitive=False),
        remarks: str = typer.Option("", prompt="Any remarks?")
):
    if category is None:
        category = CategoryChoice.Assets  # Set default value

    kwargs = locals()
    del kwargs['use_test_db']
    # convert CategoryChoice obj to Category obj
    category_choice = kwargs['category']
    category = Category.from_enum(category_choice)
    kwargs['category'] = category

    account = Account.from_dict(kwargs)
    if use_test_db:
        db = SqliteDb('ledger.db', test=use_test_db)
        db.upsert_account(account)
        print(f"Saved {account.name}: {account.value:.2f} under {account.category.name}.")
        db.close()
    else:
        if typer.confirm("Do you want to save?", default=True):
            db = SqliteDb('ledger.db', test=use_test_db)
            db.upsert_account(account)
            print(f"Saved {account.name}: {account.value:.2f} under {account.category.name}.")
            db.close()
            typer.run(start_menu)
        else:
            typer.run(start_menu)
    return kwargs


@app.command()
def exit_menu():
    raise typer.Exit


@app.command()
def start_menu():
    """
    List all commands the user can select.
    :return: string of selected choice.
    """
    print(BLUE + "Main menu" + RESET)
    commands_dict = {command.callback.__name__: command.callback for command in app.registered_commands}
    choices = list(commands_dict.keys())
    choices.remove('start_menu')
    numbered_choices = "\n".join(f"{index + 1}. {choice}" for index, choice in enumerate(choices))
    choice = typer.prompt(f"Enter number to select:\n{numbered_choices}\t")
    try:
        index = int(choice) - 1
        selected_choice = choices[index]
        typer.echo(f"{selected_choice} selected.")
        command_func = commands_dict[selected_choice]
        typer.run(command_func)
    except (ValueError, IndexError, KeyError):
        typer.echo("Invalid choice. Please try again.")
        start_menu()
    return selected_choice


if __name__ == "__main__":
    typer.run(start_menu)

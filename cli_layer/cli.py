import typer

from cli_layer.enums import CategoryChoice
from models.accounting import Category, Account
from db_layer.database import SqliteDb

app = typer.Typer()


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
    db = SqliteDb('ledger.db', test=use_test_db)
    db.upsert_account(account)
    print(f"Saved {account.name}: {account.value:.2f} under {account.category.name}.")
    db.close()
    return kwargs


if __name__ == "__main__":
    app()

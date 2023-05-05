import typer
from models.accounting import Category, Account
from database import SqliteDb
from enum import Enum

app = typer.Typer()
db = SqliteDb('ledger.db')


class CategoryEnum(str, Enum):
    # did not grok
    @classmethod
    def from_category_names(cls):
        category_names = db.get_category_names()
        enum_values = [(name.upper(), name) for name in category_names]
        return cls("CategoryEnum", enum_values)


CategoryEnum = CategoryEnum.from_category_names()
VALID_CATEGORIES = [category.value for category in CategoryEnum]

# consider displaying the hierarchy of the categories to the user when they are selecting a category


@app.command()
def save_account(
        name: str = typer.Option(..., prompt="What's the account name?"),
        value: float = typer.Option(0.0, prompt="What's the account balance?"),
        category: CategoryEnum = typer.Option(None, prompt="Select a category:",
                                              show_choices=True,
                                              case_sensitive=False,
                                              help="Valid categories: food, rent, transportation"),
        remarks: str = typer.Option("", prompt="What's the account description?")
):
    kwargs = locals()
    kwargs['category'] = category.value
    print(kwargs)

    account = Account(**kwargs)  # BUG the class expects category as obj not string
    # db.upsert_account(account)
    print(account.to_dict())

    print(f"Account {name} with balance {value:.2f} created.")
    return kwargs


if __name__ == "__main__":
    app()

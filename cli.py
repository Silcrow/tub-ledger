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


@app.command()
def save_account(
        name: str = typer.Option(..., prompt="What's the account name?"),
        value: float = typer.Option(0.0, prompt="What's the account balance?"),
        category: CategoryEnum = typer.Option(None, prompt="Select a category:",
                                              show_choices=True,
                                              case_sensitive=False),
        remarks: str = typer.Option("", prompt="Any remarks?")
):
    kwargs = locals()

    # convert CategoryEnum obj to Category obj
    category_enum = kwargs['category']
    category_obj = Category.from_enum(category_enum)
    kwargs['category'] = category_obj

    account_obj = Account.from_dict(kwargs)
    print('acc_obj', account_obj)
    print(account_obj.__dict__)
    # db.upsert_account(account)

    print(f"Saved {name} = {value:.2f} under {category}.")
    return kwargs


if __name__ == "__main__":
    app()

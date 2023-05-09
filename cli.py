import typer
from models.accounting import Category, Account
from database import SqliteDb
from enum import Enum

app = typer.Typer()
real_db = SqliteDb('ledger.db')

category_names = real_db.get_category_names()


class CategoryEnum(str, Enum):
    @classmethod
    def from_category_list(cls, list_data):
        enum_values = [(name.upper(), name) for name in list_data]  # enum class attributes
        return cls("CategoryEnum", enum_values)


CategoryChoice = CategoryEnum.from_category_list(category_names)


@app.command()
def save_account(
        name: str = typer.Option(..., prompt="What's the account name?"),
        value: float = typer.Option(0.0, prompt="What's the account balance?"),
        category: CategoryChoice = typer.Option(None, prompt="Select a category:",
                                                show_choices=True,
                                                case_sensitive=False),
        remarks: str = typer.Option("", prompt="Any remarks?")
):
    kwargs = locals()

    # convert CategoryChoice obj to Category obj
    category_choice = kwargs['category']
    category = Category.from_enum(category_choice)
    kwargs['category'] = category

    account = Account.from_dict(kwargs)
    real_db.upsert_account(account)

    print(f"Saved {account.name}: {account.value:.2f} under {account.category.name}.")
    return kwargs


if __name__ == "__main__":
    app()

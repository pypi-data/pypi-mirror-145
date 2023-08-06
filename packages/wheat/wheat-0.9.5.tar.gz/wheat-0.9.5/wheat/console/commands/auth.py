from cleo.helpers import argument
from wheat.console.commands.command import Command
from wheat.factory import Factory


class AuthCommand(Command):

    name = "auth"

    description = (
        "Authenticate with <c1>Harvest</c1> by providing a personal access token and"
        " account id."
    )

    arguments = [
        argument("account_id", "The account id of the Harvest account.", optional=True),
        argument(
            "token", "The personal access token of the harvest account.", optional=True
        ),
    ]

    def handle(self) -> None:
        id = self.argument("account_id")
        token = self.argument("token")
        if id and not token or token and not id:
            self.line(
                "You must provide both an Account ID and a Personal Access Token.",
                style="e",
            )
            self.line('  (use "wheat auth" to enter them interactively)')
            self.line(
                '  (use "wheat auth <account_id> <token>" to provide them as arguments)'
            )
            return 1

        if id and token:
            return self.authenticate(id, token)

        # Interactive.
        self.line(
            "You must provide both an <c2>Account ID</c2> and a <c2>Personal Access"
            " Token</c2>"
        )
        self.line(
            "Refer to the <c1>Harvest</c1> developer documentation for more information"
        )

        link = "https://id.getharvest.com/oauth2/access_tokens/new"
        self.line("")
        self.line(f"You can create new credentials here: {link}")

        self.line("")
        question = self.create_question("Account ID:")
        account_id = str(self.ask(question))

        question = self.create_question("Personal Access Token:")
        token = str(self.ask(question))

        return self.authenticate(account_id, token)

    def authenticate(self, account_id: str, token: str) -> int:
        factory = Factory(self.io)

        path = factory.create_harvest_credentials(account_id, token)

        self.line("")
        self.line(f'Credentials saved to "{path!s}"', style="w")

        try:
            harvest = factory.create_harvest()
        except AttributeError as e:
            self.line_error("Failed to authenticate with the Harvest API.")

            self.line("")
            raise e

        self.line("")
        self.line(
            f"Welcome to Wheat, {harvest.api.first_name}. <success>You're ready to log"
            " some hours!</success>"
        )

        return 0

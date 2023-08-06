

class CleanCommand:
    def __init__(self, client):
        self._client = client


    def _clean(self, args):
        res = self._client.query(
            """
        mutation cleanEnv {
          cleanCommand {
            ok
          }
        }
        """
        )
        print(res)

    def register_subparser(self, subparsers):
        parser = subparsers.add_parser('clean', help="Clean all your models.")
        parser.set_defaults(func=self._clean)

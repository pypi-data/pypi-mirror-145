import sys
from os.path import expanduser

import yaml


class AuthTokenManager:
    CONFIG_FILE = ".fentik"
    TOKEN_KEY = "authtoken"
    SERVICE_URI = "service_uri"
    DEFAULT_SERVICE_URI = "https://api.fentik.com/api/graphql"

    def _config_file(self):
        home = expanduser("~")
        return f'{home}/{self.CONFIG_FILE}'

    def get_token(self):
        try:
            with open(self._config_file(), 'r') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                return data[self.TOKEN_KEY]
        except Exception as e:
            print("Unable to read authtoken: " + str(e))
            sys.exit(1)

    def put_token(self, token):
        with open(self._config_file(), 'w') as f:
            yaml.dump({self.TOKEN_KEY: token}, f)

    def get_service_uri(self):
        try:
            with open(self._config_file(), 'r') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                return data[self.SERVICE_URI]
        except Exception:
            return self.DEFAULT_SERVICE_URI

    def _authtoken(self, args):
        token = args.token[0]
        self.put_token(token)
        print("token saved")

    def register_subparser(self, subparsers):
        parser = subparsers.add_parser(
            'authtoken',
            help="Configure authtoken to user for your development environment.",
        )
        parser.add_argument('token', nargs=1, help='your authtoken string')
        parser.set_defaults(func=self._authtoken)

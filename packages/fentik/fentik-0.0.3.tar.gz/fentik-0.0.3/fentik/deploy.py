import json
import sys
from pathlib import Path


class DeployCommand:
    def __init__(self, client):
        self._client = client

    def _file_contents(self, path):
        with open(path, 'r') as f:
            return f.read()

    def _deploy(self, args):
        models = {}
        deployment_config = {"model_sources": models}
        for path in Path('models/').rglob('*.sql'):
            model_file = str(path)
            model_name = path.name[:-4]
            content = self._file_contents(path)
            if model_name in models:
                print(
                    f"error: {model_name} from file {model_file} already defined in {models[model_name]['path']}"
                )
                sys.exit(1)
            models[model_name] = {"path": model_file, "content": content}

        for target in args.target_models:
            if target not in models:
                print(f"Target model '{target}' not found.")
                sys.exit(1)

        deployment_config['target_models'] = args.target_models

        config = json.dumps(json.dumps(deployment_config))
        res = self._client.query(
            """
        mutation DeployConfig {
          deployCommand(config: %s) {
            ok
          }
        }
        """
            % config
        )
        print(res)

    def register_subparser(self, subparsers):
        parser = subparsers.add_parser('deploy', help="Deploy local models.")
        parser.add_argument("target_models", nargs='+')
        parser.set_defaults(func=self._deploy)

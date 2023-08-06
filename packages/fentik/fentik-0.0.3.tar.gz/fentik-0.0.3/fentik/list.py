import json

from prettytable import PrettyTable


class ListCommand:
    def __init__(self, client):
        self._client = client

    def _sources(self):
        result = self._client.query(
            """
query GetSourceConfigs {
  sourceConfigs {
    name
    sourceType
    database
    tableIncludeList
    tableExcludeList
  }
}
        """
        )
        result = json.loads(result)
        result = result['data']['sourceConfigs']
        if not result:
            result = []
        pt = PrettyTable()
        pt.field_names = ['Name', 'Databases', 'Type']
        pt.add_rows([[r['name'], r['database'], r['sourceType']]
                    for r in result])
        return (
            pt.get_string()
            + "\n"
            + f"({len(result)} row{'s' if len(result) != 1 else ''})"
        )

    def _list(self, args):
        result = self._sources()
        print(result)

    def register_subparser(self, subparsers):
        parser = subparsers.add_parser(
            'list', help="List resources in Fentik.")
        parser.set_defaults(func=self._list)

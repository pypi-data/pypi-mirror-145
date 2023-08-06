import click
from mlops.api.datasource import commands as ds_group
from mlops.tools import commands as tools_group

@click.group()
def main():
    pass

def run():
    main.add_command(ds_group.datasource)
    main.add_command(tools_group.tools)
    main()
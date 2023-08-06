import click

@click.group(name="datasource")
def datasource():
    pass

@datasource.command(name="create", help="a test help")
@click.option('--type', type=click.Choice(['redshift', 'bigquery', 'csv']), required=True, help="The type of datasource to create")
@click.option('--credentials', type=str, help="The path to the file containing the credentials (usually ~/.aws or any folder where you stored your google credentials). Not necessary when type is csv")
@click.option('--csv-file', type=str, help="The path of the csv file to be used as data source, not necessary when type is redshift or gcp")
@click.argument('description', type=str, required=True)
def create(type, credentials, csv_file, description):
    """Create a new datasource
        TYPE - the type of datasource being created. Supported values are [redshift, bigquery, csv]
        DESCRIPTION - a brief description of the datasource, no white-spaces and use only letters ([a-Z]) and hyphen (-) 
    """
    if type == 'csv':
        if credentials and credentials != "":
            click.echo("Ignoring credentials file. The type specified was csv")
        if not csv_file or csv_file == "":
            click.echo("FAILED. Missing csv-file option")
            return -1
    elif type == 'redshift':
        # do redshift stuff
        if csv_file and csv_file != "":
            click.echo("Ignoring csv file. This option is invalid for redshift.")
    elif type == 'bigquery':
        if csv_file and csv_file != "":
            click.echo("Ignoring csv file. This option is invalid for bigquery.")
    #TODO call create datasource endpoint

def create_bigquery():
    pass

if __name__ == '__main__':
    datasource()
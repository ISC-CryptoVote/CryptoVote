import click
import requests

@click.group()
def cli():
    pass

@cli.command()
@click.argument('token')
def fill_ballot(token):
    url = 'http://localhost:8000/request-ballot'
    response = requests.get(url, headers={"Token": token})

    # validate signed ballot
    
    click.echo(response.json())

if __name__ == '__main__':
    cli()
import click
from magniv.build import build as m_build
from magniv.export import export as m_export
from magniv.run import run as m_run


@click.group()
def cli():
    pass


@cli.command()
def build():
    return m_build()


@cli.command()
@click.option('--gcp', is_flag=True) # GCP creeates the dockerfiles and cloubuild.yaml
def export(gcp):
    return m_export(gcp)


@cli.command()
@click.argument("filepath")
@click.argument("function_name")
def run(filepath, function_name):
    return m_run(filepath, function_name)

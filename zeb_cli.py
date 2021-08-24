import click
from flask.cli import FlaskGroup
from passlib.hash import bcrypt

from app import db
from app.models import ZbUser
from app.models.role import Role

cli = FlaskGroup()


@cli.command('create_role')
@click.argument("role_name")
def create_role(role_name):
    role = Role(name=role_name)
    db.session.add(role)
    db.session.commit()


@cli.command('init_roles')
def init_roles():
    role_admin = Role(name='Admin', id=1)
    role_client = Role(name='Client', id=2)
    role_anon = Role(name='Anonymous', id=0)
    db.session.bulk_save_objects([role_admin, role_anon, role_client])
    db.session.commit()


@cli.command('create_superadmin')
@click.option('-f', '--first-name', 'first_name')
@click.option('-e', '--email', 'email')
@click.option('-l', '--last-name', 'last_name')
@click.option('-p', '--password', 'password')
def create_superadmin(first_name, last_name, email, password):
    """
        method to create first user
    """
    assert all((first_name, last_name, email, password))
    password = bcrypt.hash(str(password))
    super_user = ZbUser(first_name=first_name, last_name=last_name, email=email, password=password, role_id=1)
    db.session.add(super_user)
    db.session.commit()
    print(f"User Created: {super_user.id} -> {super_user.email}")


if __name__ == '__main__':
    cli()

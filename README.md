# Technician Test 

**requirements**

- docker: https://docs.docker.com/install/

- docker-compose: https://docs.docker.com/compose/install/

First you need to clone your project.

inside the project directory run:

`docker-compose up -d`

after docker-compose was finished is needed to execute this commands

`docker exec -ti test_api python zeb_cli.py init_roles`

once the roles have been created it's time to create our first superuser

`docker exec -ti test_api python zeb_cli.py create_superadmin -f [first-name] -l [last-name] -e [email] -p [password]`

and now the project is ready to use!

## Important Info

url web is http://0.0.0.0:5000

url web is http://0.0.0.0:5000/docs


to see the log api

`docker logs -f test_api`

to see the log psql

`docker logs -f test_psql`


to run unit test

`docker exec -ti test_api pytest`

### API DOC: 

[![Run in Postman](https://run.pstmn.io/button.svg)](https://documenter.getpostman.com/view/148100/TzzEoZya)

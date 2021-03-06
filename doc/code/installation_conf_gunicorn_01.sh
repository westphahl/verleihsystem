# Verleihsystem Web Application - Gunicorn
description	"Gunicorn - Verleihsystem Web Application"

start on runlevel [2345]
stop on runlevel [!2345]

respawn
script
    WEBAPP=/usr/webapps/verleihsystem/mount/prj/verleihsystem
    GUNICORN=/usr/webapps/verleihsystem/environment/bin/gunicorn_django
    USER=www-data
    GROUP=www-data
    BIND=127.0.0.1:8001

    cd $WEBAPP
    exec $GUNICORN --user $USER --group $GROUP --bind $BIND
end script

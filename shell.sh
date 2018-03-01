#!/bin/bash

# Configurable variables
[ -z "$SERVER_HOST" ] && SERVER_HOST="0.0.0.0" || SERVER_HOST=$SERVER_HOST
[ -z "$SERVER_PORT" ] && SERVER_PORT="8000" || SERVER_PORT=$SERVER_PORT

# Constant variables
SCRIPT=$(basename "$0")
[ -z "$VENV" ] && VENV=./venv || VENV=$VENV

# Binary executable
PYTHON=$VENV/bin/python
PIP=$VENV/bin/pip
WEBPACKDEV=./node_modules/.bin/webpack
WEBPACKDEVSERVER=./node_modules/.bin/webpack-dev-server
GULP=./node_modules/.bin/gulp

# Build your environment for you to start development
setupenv() {
    # Create virtual environment
    virtualenv --no-site-packages --python=`which python3` $VENV

    # Upgrade your virtual env pip to latest version
    $PYTHON -m pip install -U pip

    $PIP install -r requirements.txt
    npm install

    printf "\n"
    print "Setup successful!"
    print "Run 'source $VENV/bin/activate' to active virtual env and 'deactivate' to deactivate it"
}

# Compile our app sources using webpack
build() {
    if [ "$1" == "--dev" ]; then
        $WEBPACKDEV --progress
    else
        NODE_ENV=production \
        $WEBPACKDEV -p --progress --devtool=cheap-module-source-map
        $GULP build
    fi

    $PYTHON manage.py migrate
    $PYTHON manage.py collectstatic --noinput
}

# Start django development server
runserver() {
    build
    
    if [ -z "$1" ]; then
        $PYTHON manage.py runserver $SERVER_HOST:$SERVER_PORT
    else
        $PYTHON manage.py runserver $1
    fi
}

# Start webpack (JS bundler) dev server
# Explain arguments
# --inline --hot: enable browser auto reload when we make changes to files
runwebpack() {
    # Passing the dev server url to webpack config. It is used there for
    # doing proxy redirection
    SERVER_URL="http://$SERVER_HOST:$SERVER_PORT" \
    $WEBPACKDEVSERVER --progress --inline --hot --host 0.0.0.0
}

mysqldb() {
    # Check if is using mysql first
    engine=`$PYTHON manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default']['ENGINE'].split('.')[-1])"`
    if [ "$engine" != "mysql" ]; then
        print "Error: You not using mysql"
        exit 1;
    fi;

    config=(`$PYTHON manage.py shell -c "from django.conf import settings; db=settings.DATABASES['default']; print(db['HOST']); print(db['NAME']); print(db['USER']); print(db['PASSWORD'])"`)
    host=${config[0]}
    name=${config[1]}
    user=${config[2]}
    pass=${config[3]}

    command=$1
    if [ "$command" == "dump" ]; then
        mysqldump -h "$host" -u "$user" -p"$pass" "$name"

    elif [ "$command" == "drop" ]; then
        read -p "Are you sure you want to drop $name [y/n]?" -n 1 sure
        if [ "$sure" == "y" ]; then
            echo "DROP DATABASE $name" | mysql -h "$host" -u "$user" -p"$pass" "$name"
            printf "\n"
        fi

    elif [ "$command" == "create" ]; then
         echo "CREATE DATABASE $name" | mysql -h "$host" -u "$user" -p"$pass"

    elif [ "$command" == "import" ]; then
        if [ -z "$2" ]; then
            cat | mysql -h "$host" -u "$user" -p"$pass" "$name" && print "Import complete."
        else
            mysql -h "$host" -u "$user" -p"$pass" "$name" < $2 && print "Import complete."
        fi

    else
        print "Run either mysqldb dump/create/drop"
    fi
}

print() {
    printf "($SCRIPT) $1"
    printf "\n"
}

# Make sure script only run at script location
if [ ! -f $(basename $0) ]; then
    echo "$(basename $0) not found here" 1>&2
    exit 1
fi

# Call function from argument
$@

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd ${DIR}
mkdir backend
cd backend
pip3 install virtualenv
python3 -m venv ./venv
source venv/bin/activate
pip3 install -r ../requirements.txt
cd ..
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver


export ENV='Deploy'

export FLASK_APP='app'

export FLASK_DEBUG=True

export DATABASE_URL='postgres://omhesvoeovnphm:43e439582d233bd204be64e005b04254276ff746707e7f075f198b274316f080@ec2-23-20-168-40.compute-1.amazonaws.com:5432/dc4alsk53pf8nn'

flask db upgrade

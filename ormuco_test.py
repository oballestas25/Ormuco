from os import name
from flask import Flask
from flask import request
from flask import jsonify
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
from novaclient import client as clientnova
from glanceclient import Client as clientglance
###
### Authenticating - Keystone
### 

auth = v3.Password(auth_url='https://api-acloud.ormuco.com:5000/v3',
                    username='utb@ormuco.com',
                    password='ILOVEUTB2021',
                    project_id='2ee7b627f154414f83ffdbbf6c78999f')
sess = session.Session(auth=auth)
keystone = client.Client(session=sess)
#print(sess)

###
### Novaclient compute service
###

nova = clientnova.Client('2.1',session=sess)
server_list=nova.servers.list()
flavor_list=nova.flavors.list()

print('\n Server List\n')
print(server_list)
#print('\n Flavor List\n')
#print(flavor_list)


###
### Glanceclient image service  
###

glance = clientglance('2', session=sess)
image_list=glance.images.list()


#print('\nImage List\n')
#for image in glance.images.list():
#   print (image)

###
### Create Instance
###
image='294eeb80-ce67-459d-8447-7dad67241dd0'
flavor=100
#instance = nova.servers.create(name="Oscar-test", image=image,flavor=flavor, key_name='oballestas2')


###
### To Json
###
servers = []

for server in server_list:
    servers.append(server.__dict__["_info"])
    print(server.__dict__["_info"])
    print("\n")



app = Flask(__name__)
@app.route("/list_instances", methods=['GET'])
def to_json():
    
    return jsonify(servers)

@app.route("/create_instances",methods=['POST'])

def create_server():
    
    request_data = request.get_json()
    #print(request_data)
    name_instance= request_data ['server_name']
    image_instance= request_data ['image']
    flavor_instance= request_data ['flavor']
    key_name_instance= request_data ['key_name']
    instance = nova.servers.create(name=name_instance, image=image_instance,flavor=flavor_instance, key_name=key_name_instance)
    return request_data


#@app.route('/')
#export FLASK_APP=ormuco_test
#export FLASK_ENV=development

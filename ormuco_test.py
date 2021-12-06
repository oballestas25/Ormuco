from os import error, name
from flask import Flask, request, render_template, url_for
from werkzeug.utils import redirect
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
from novaclient import client as clientnova
from glanceclient import Client as clientglance

app = Flask(__name__)

########## Nova Client #########

auth = v3.Password(auth_url='https://api-acloud.ormuco.com:5000/v3',username='utb@ormuco.com',password='ILOVEUTB2021',
project_id='2ee7b627f154414f83ffdbbf6c78999f')
sess = session.Session(auth=auth)
keystone = client.Client(session=sess)
nova = clientnova.Client('2.1',session=sess)


######### Images-Glance #######
def images ():
    sess = session.Session(auth=auth)
    glance = clientglance('2', session=sess)
    image_list=glance.images.list()
    images_list_dict=[]

    for image in image_list:
        images_list_dict.append([image["id"],image["name"],image["status"]])

    return images_list_dict

########## Flavor ##########
def flavors():
    flavor_list=nova.flavors.list()
    flavor_list_dict=[]
    for flavor in range(len(flavor_list)):
        flavor_list_dict.append([flavor_list[flavor].__dict__["id"],flavor_list[flavor].__dict__["name"],flavor_list[flavor].__dict__["ram"], 
        flavor_list[flavor].__dict__["disk"], flavor_list[flavor].__dict__["OS-FLV-EXT-DATA:ephemeral"],
        flavor_list[flavor].__dict__["vcpus"],flavor_list[flavor].__dict__["os-flavor-access:is_public"]])

    return flavor_list_dict

######## Servers #########
def servers():
    server_list=nova.servers.list()
    server_list_dict=[]
    for server in range(len(server_list)):

        image_addr=server_list[server].__dict__["image"]["id"]
        flavor_addr=server_list[server].__dict__["flavor"]["id"]


        server_list_dict.append([server_list[server].__dict__["id"],server_list[server].__dict__["name"],server_list[server].__dict__["status"], 
        server_list[server].__dict__["addresses"]["default-network"][0]["addr"], server_list[server].__dict__["image"]["id"],
        server_list[server].__dict__["flavor"]["id"]])

    return server_list_dict

############## Index ###################
@app.route("/",methods=['POST','GET'])
def index():

    return render_template("index.html")

########## Login ###########

@app.route("/login",methods=['POST','GET'])
def login():

    if request.method == 'POST':
        user_name=request.form['user_name']  
        password=request.form['pw']

        if (user_name=="utb@ormuco.com" and password=="ILOVEUTB2021"):
            return redirect(url_for("index"))

        else:
            return render_template("login.html")

    else:
        return render_template("login.html")

############## Create an Instance ############

@app.route("/create_instance",methods=['POST','GET'])
def create_instance():

    if request.method == 'POST':
        name_instance=request.form['server_name']  
        image_instance=request.form['image'] 
        flavor_instance= request.form['flavor']
        key_name_instance= request.form['key_name']
        instance = nova.servers.create(name=name_instance, image=image_instance,flavor=flavor_instance, key_name=key_name_instance)
    
    return render_template("create_instance.html")

############## Images List ############
@app.route("/images_list",methods=['POST','GET'])
def images_list():
    headings_i=["ID","Name","Status"]
    images_list=images()
    
    return render_template("list.html",headings=headings_i,data=images_list)

######## Flavor List ##############
@app.route("/flavors_list",methods=['POST','GET'])
def flavors_list():
    headings_f=["ID","Name","Ram","Disk","Ephemeral","VCPUs","Is Public"]
    flavors_list=flavors()

    return render_template("list.html",headings=headings_f,data=flavors_list)

######## Servers List ##############
@app.route("/instances_list",methods=['POST','GET'])
def instances_list():
    headings_s=["ID","Name","Status", "Networks","Image", "Flavor"]
    server_list=servers()
    return render_template("list.html",headings=headings_s,data=server_list)

#export FLASK_APP=ormuco_test
#export FLASK_ENV=development
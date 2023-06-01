import json
from flask import Flask
from flask import request, jsonify,session

from neo4j import GraphDatabase
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity

from flask_jwt_extended import jwt_required,verify_jwt_in_request
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS,cross_origin
import os
from datetime import timedelta




app = Flask(__name__)


app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)




SECRET_KEY="poBB61kAN1l91QRHJK98p794iaPI654jpjoiHIpiH_tyDTRXte49846_5"

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})




print("\n\n\n\n\n\n")

app.config["JWT_SECRET_KEY"] = SECRET_KEY

bcrypt = Bcrypt(app)


jwt = JWTManager(app)

# app.config["JWT_ALGORITHM"] = "HS256"

print(bcrypt.generate_password_hash("test").decode('UTF-8'))

driver = GraphDatabase.driver("bolt://127.0.0.1:7687",auth=('neo4j','1234'))


# print(driver.verify_connectivity())


#TODO
# recommended events [####------] 50%
# recommended teams [####------] 50%
# search events with keyword [########--] 80%
# search teams with keyword [########--]80%
# *( search events with tag and keyword [] )* DEPRECATED
# login [#######---] 70%
# register [#######---] 70%
# create team [##--------] 20%
# join team [####------] 40%
# team participate in event []



session = driver.session()

# res = session.run()

# print('it worked')




# match events where someone i know is in that event

# union all

# match events

# return data  to python

#
# add coefeicent based on manhatan distance to each user

# sort and limit results to 6

#   s

# event with someone i know has bigger coeffecient than who i dont know

# first list ( events with teammate i am close to ) coeff==1

# second list (events close to me == have something in common with me whether it is a skill or technologie or topics) coeff == 0.85

# third list ( events with manhatan distance of zero) coeff == 0.7

# final result (union and we sum coeffecients of the same id events then we sort and limit number of events to 6 )

# what to be done in cypher :

# 1-  a query for getting the events with members i know

# 2- get events with members i don't know


# for the team recommendations we filter


def calculate_manhatan_distance(interest1, interest2):

    interest1 = list(set(interest1))

    interest2 = list(set(interest2))

    li1 = len(interest1)

    li2 = len(interest2)


    while li1 > li2:
        interest2.append(-1)
        li2 += 1

    while li2 > li1:
        interest1.append(-1)
        li1 += 1


    print("reached")

    # the -1 is a padding to ensure that we add 0 later on
    result = 0
    while len(interest1) > 0:
        temp = interest1[0]
        if temp in interest2:
            result += 1
        interest1.pop(0)

    return result


















@app.route('/',methods=['GET'])
def home():
    return jsonify({
        'message':'Started Sucessfully',
    })


def get_user_or_none(tx,user_email):

    result = tx.run("""
        MATCH (u:user)WHERE u.email = $email
        RETURN u
        """, email=user_email)  # Anthor query :         MATCH (u:User{email : eamil})  RETURN p

    try:

        result.peek()
        return list(result)[0]  # return a list of Record objects

    except:

        return None






@app.route('/login',methods=['POST'])
@cross_origin()
def login():
    # email = request.json.get('email')
    email = request.json.get("email",None)
    password = request.json.get("password",None)
    print('executed! \n\n\n')
    user = session.execute_read(get_user_or_none,email)
    # user = user.data()
    if user:
        print(json.loads(user.data()['u']['prefrences'].replace("'",'"')))
        # print(user.data()['u']['password'])
        # pass_temp = bcrypt.generate_password_hash(password).decode('utf-8')
        # print(pass_temp.__str__())

        if ((password is not None) and bcrypt.check_password_hash(pw_hash=user.data()['u']['password'],password=password)):
            access_token = create_access_token(identity=email)
            # print((user.get("prefrences")))
            return jsonify(access_token=access_token),  200

        return jsonify({'msg':'wrong password'}),    401

    return jsonify({'msg':'user does not exist'}),      401



@app.route("/email-exists",methods=['POST'])
@cross_origin()
def email_exists():

    email = request.json.get("email",None)
    print("this is email : ")
    print(email)
    user = session.execute_read(get_user_or_none,email)
    print(user)

    if user is not None:
        return jsonify({'msg':'user already exists'}),  200

    else:

        return jsonify({'msg':'user does not exist'}),  445



def register_new_user(tx,user_info):
    result = tx.run("""
    create (n:user{f_name:$first_name, l_name:$last_name,email:$email,
    password:$password,location:$location,prefrences:$prefrences})
    """,
        first_name=user_info['first_name'],
        last_name=user_info['last_name'],
        email=user_info['email'],
        password=user_info['password'],
        location=user_info['location'],
        prefrences=user_info['prefrences']
        )

    return result.data()



@app.route("/register",methods=['POST'])
@cross_origin()
def register():

    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")

    password = request.json.get("password")

    location = request.json.get("location")


    skills = request.json.get("skills")

    topics = request.json.get("topics")

    for i in range(len(topics)):
        topics[i] = topics[i].upper()


    technologies = request.json.get("technologies")
    temp = {
        'skills':skills,
        'topics':topics,
        'technologies':technologies
    }


    prefrences= json.dumps(temp)

    #
    # user = get_user_or_none(email=email)
    #
    #
    # if user:
    #
    #     return jsonify({"msg":"email already exists"}),     401

    user_info = {'first_name':first_name,
                 'last_name':last_name,
                 'email':email,
                 'password':bcrypt.generate_password_hash(password),
                 'location':location,
                 'prefrences':prefrences
                 }
    if (session.execute_read(get_user_or_none,email)) : return jsonify({"msg":"sorry the user exists"}), 405
    result = session.execute_write(register_new_user,user_info)
    print(result)
    print(user_info)
    print(f'prefrences\n\t {prefrences}')
    access_token = create_access_token(identity=email)

    return jsonify(access_token=access_token), 200

    return jsonify(access_token=access_token),200




@app.route('/get-current-user-data',methods=['POST'])
@jwt_required()
@cross_origin()
def get_current_user_data():
    email= get_jwt_identity()
    print(email)
    print('\n\n')
    user = None
    if email:
        user = session.execute_read(get_user_or_none,email)
        print('\n\n here comes the user  ? : ')
        print(user)
        if user:
            print(user)
            temp = user.data()['u']
            first_name = temp['f_name']
            last_name = temp['l_name']

            prefrences = json.loads(temp['prefrences'].replace("'",'"'))
            currentTeam= "HOmies"
            location = temp['location']

            context = {

                'first_name':first_name,
                'last_name': last_name,
                'location': location,
                'prefrences':prefrences,
                'currentTeam':currentTeam,
                'numberOfParticipants':76,
            }
            print(context)
            return jsonify(context), 200

        return jsonify({'msg':'user not exist'}), 401

    return jsonify({'msg':'invalid token'}), 401









@app.route("/protected",methods=['GET'])
@jwt_required()
@cross_origin()
def protected():

    return jsonify(logged_in_as=get_jwt_identity()), 200
















def get_events_of_teammates(tx,email):

    # we could replace the match expression with a regular expression but the simpler the better
    results = tx.run("""
    match (e:Event)-[:participate]-(:team)-[:memeber]-(u:user)-[:know]-(u1:user)
    where u1.email = $email and not (u1)-[:knows|member|participate*3]-(:Event) 
    return e
    """)


def normalize_events_data(results):
    temp = []

    for item in results:
        temp.append(item['e'])

    # print(temp)


    return temp


def get_friend_events(tx, email):
    results = tx.run("""

    match (e:Event)-[:participate]-(:team)-[:member]-(:user)-[:knows]-(u1:user)

    where u1.email=$email  and not (u1)-[:member]-(:team)-[:participate]->(e) 

    return e
    
    limit 6
    
    
    """,
    email=email)

    try:
        # print(results)
        results.peek()
        return results.data()

    except:

        return None




def get_rest_events(tx,email):
    results = tx.run("""
    match (e:Event),(u1:user)

    where u1.email=$email  and not (u1)-[:knows]-(:user)-[:member]->(:team)-[:participate]->(e)
     and not (u1)-[:member]->(:team)-[:participate]->(e)
    

    return e
    
    limit 6
    
    """,email=email)


    try:
        results.peek()
        return results.data()
    except:
        return None



def get_six_events(tx):
    results = tx.run("""
    match (e:Event)
    return e
    limit 6
    """)
    try:
        results.peek()

        return results.data()
    except:
        return None





@app.route('/recommended-events', methods=['GET'])
@cross_origin()
@jwt_required(optional=True)
def recommended_events():

    # email = get_jwt_identity()
    # # first we get if the user is logged in
    # if email :
    #
    #     user = get_user_or_none(email=get_jwt_identity())
    #     if user:
    #         i_know = session.execute_read(get_events_of_teammates,email)
    #         user_prefrences = json.loads(user.get("prefrences"))
    #
    #         for event in i_know:
    #
    #             prefrences= json.loads(event.get("prefrences"))
    #
    #             # technologies = json.loads(event.get("technologies"))
    #             # topics = json.loads(event.get("topics"))
    #             distance = sum([
    #                 calculate_manhatan_distance(user_prefrences.skills,prefrences.skills),
    #                 calculate_manhatan_distance(user_prefrences.technologies, prefrences.technologies),
    #                 calculate_manhatan_distance(user_prefrences.topics, prefrences.topics),
    #             ])
    #             print("----------------------------------------------------\n\n")
    #             print(distance)



    # second if not logged in
    # else:
    #     pass

    # loggedIn = True
    # if loggedIn :
    #     same_location_events_query = '''
    #     match (n:event)-[:hosted]->(:location{number:$wilaya})<-[:live]-(u:user{username:"$username"})
    #     order by n.participants_count DESC
    #     return n as events
    #     '''
    #     same_interest_query = '''
    #     match (n:event)-[:tagging]->(:tag)<-[:interested]-(:user{username:"$username"})
    #     order by n.participants_count DESC
    #     return n
    #     '''
    #
    #
    #     event_query_based_on_skill = '''
    #     match (n:event)-[:tagging]->(:tag)-[:related]-(:skill)<-[:skilled]-(:user{username:"$username"})
    #     order by n.participants_count DESC
    #     return n
    #     '''
    #
    #     event_query_based_on_teammmates = '''
    #     match (fr:user)-[j:teammate{team:"$team"}]-(u:user{username:"$username"})
    #     match (n:event)<-[:participate]-(t:team{name:j.team_name})
    #
    #     return n as events
    #
    #     '''
    #
    #
    #     # teammate === worked_with
    #
    # else :
    #     based_participants_count = '''
    #     match (n:event)
    #     order by n.participants_count DESC
    #     return n
    #     '''
    #
    #
    #
    #
    # result = list(session.run('match (n) return n'))
    # print(result)
    #
    #
    #
    # for r in result:
    #     print('\n\n\n\n\n')
    #     print(r)
    #     print('\n\n\n\n\n')


    email = get_jwt_identity()
    context = {}
    if(email):
        friends_events = session.execute_read(get_friend_events,email)
        friends_events = normalize_events_data(friends_events)
        print(friends_events)
        # print(friends_events)
        # print(friends_events)
        # print(len(friends_events))
        if friends_events and len(friends_events)<6:
            rest_events = session.execute_read(get_rest_events,email)
            rest_events = normalize_events_data(rest_events)
            i=0
            while i< 6- len(friends_events):
                friends_events.append(rest_events[i])
                i+=1
            context = {
                'data':friends_events
            }
        else:
            rest_events = session.execute_read(get_six_events)
            rest_events = normalize_events_data(rest_events)

            context = {
                'data': rest_events
            }


    else:

        rest_events = session.execute_read(get_six_events)
        rest_events= normalize_events_data(rest_events)

        context = {
            'data':rest_events
        }

    for item in context['data']:
        print(item['title'])

    return jsonify(context),    200

    #
    # context = {}
    # #context["info"] = result
    #
    # return jsonify(context)



@app.route('/recommended-teams', methods=['GET'])
@jwt_required(optional=True)
@cross_origin()
def recommended_teams():
    email = get_jwt_identity()

    if(email):
        friends_events = session.execute_read(get_friend_events,email)
        print(friends_events)


    context = {

    }

    return jsonify(context)


def get_event_list(tx, keyword):
    temp =  ""
    result = tx.run("""
        MATCH (e:Event) 
        WHERE toLOWER(e.title) CONTAINS toLOWER($keyword) 
        RETURN e
    """, keyword=keyword)
    return result.data()

@app.route('/search-events/<string:keyword>', methods=['GET'])
@cross_origin()
def search_events(keyword):
    if (keyword=='*') :
        keyword = 'a'
    # query = '''
    # match (e:Event)<-[:Host]-(u:User)
    # where e.name CONTAINS $keyword
    # OR e.description CONTAINS $keyword
    # OR u.name CONTAINS $keyword
    #
    # '''
    query = session.execute_read(get_event_list,keyword)
    # print(query)
    # print("\n\n\n")
    # print(query)

    list_of_events =[]
    for event in query:
        list_of_events.append(event['e'])
    msg = f'{len(query)} matching results'
    status = 200
    if len(query) == 0:
        msg = "false"
        # status = 404



    data_context = []
    for i in range(len(list_of_events)):
        data_context.append({
            'date':list_of_events[i]['date'],
            'prefrences': json.loads(list_of_events[i]['prefrences'].replace("'",'"')),
            'description': list_of_events[i]['description'],
            # 'topics': list_of_events[i]['topics'],
            # 'skills': list_of_events[i]['skills'],
            # 'technologies': list_of_events[i]['technologies'],
            'title': list_of_events[i]['title'],
            'prize': list_of_events[i]['prize'],
            'location': list_of_events[i]['location']
        })
        # print(data_context[i]['prefrences']['topics'])
    context = {
        "data":data_context,
        "msg":msg
    }

    return jsonify(context), status


def get_event_or_none(tx,title):
    result = tx.run("""
    match(e:Event)
    where toLower(e.title) = toLower($title)
    return e
    """,title=title)
    try:
        result.peek()
        return result.data()
    except:
        return None




def get_number_of_participants(tx,title):
    result = tx.run("""
    match (e:Event)-[:participate]-()-[l:memeber]-(:user)
    where e.title = $title
    return count(l) as nb
    """,title=title)
    return result.data()[0]




@app.route('/get-event-details/<string:title>',methods=['GET'])
@cross_origin()
def get_event_details(title):
    print(title)
    query = session.execute_read(get_event_or_none,title)
    number = session.execute_read(get_number_of_participants,title)
    print(query)
    print(number)
    if query:
        event = query[0]['e']
        event_context = {
            'title':event['title'],
            'description':event['description'],
            'prize': event['prize'],
            'location': event['location'],
            'date': event['date'],
            'prefrences': json.loads(event['prefrences'].replace("'",'"')),
            'numberOfParticipants':number['nb']
        }
        return jsonify(event_context), 200


    return jsonify({'msg':'Event not found'}),404





@app.route('/event-name/<string:title>',methods=['POST','GET'])
@jwt_required()
@cross_origin()
def event_name(title):
    query = session.execute_read(get_event_or_none,title)
    print(query)
    if len(query):
        return jsonify({"msg":'exists'}),   200
    return jsonify({"msg":'Does not exist'}), 201



def create_event_node(tx,event_info):
    result = tx.run("""
    create (e:Event{
    title:$title,
    date:$date,
    location:$location,
    prize:$prize,
    description:$description,
    prefrences:$prefrences
})


    """,
    title=event_info['title'],
    date=event_info['date'],
    location=event_info['location'],
    prize=event_info['prize'],
    description=event_info['description'],
    prefrences=event_info['prefrences'],
    email=event_info['email']
         )


    return result.data()




@app.route('/create-event',methods=['POST'])
@cross_origin()
@jwt_required()
def create_event():
    email = get_jwt_identity()
    title = request.json.get("title",None)
    description = request.json.get("description",None)
    location = request.json.get("location",None)
    date = request.json.get('date',None)
    prize = request.json.get('prize',None)
    skills = request.json.get('skills',None)
    technologies = request.json.get('technologies',None)
    topics = request.json.get('topics',None)
    prefrences = {
        "skills":skills,
        "technologies":technologies,
        "topics":topics
    }
    event_info = {
        'title':title,
        'description':description,
        'location':location,
        'date':date,
        'prize':prize,
        'prefrences':json.dumps(prefrences),
        'email':email
    }
    result = session.execute_write(create_event_node,event_info)
    # print('\n\n\nthis are the prefrences dict')
    # print(prefrences)
    # print('\n\n\nthis is the json.dumps')
    # print(json.dumps(prefrences))
    # # print(len(json.dumps(prefrences)['skills']))
    print(request.json)
    return jsonify(),200




#
#
# @app.route('/create-team',methods=['POST'])
# @cross_origin()
# @jwt_required()
# def create_team():
#
#     team_name= request.json.get('team_name',None)
#     team_secret_name=request.json.get("team_secret_name",None)
#     team_size = request.json.get('size',None)
#




def get_team_list(tx,name):

    results = tx.run("""
    match (t:team)
    where t.name CONTAINS $name 
    return t
    """,name=name)

    return results.data()




def get_all_team_list(tx):
    result = tx.run("""
    match (t:team)
    return t
    limit 12

    """)

    return result.data()





@app.route('/search-team/<string:keyword>', methods=['GET'])
@cross_origin()
def search_team(keyword):
    result = []
    if(keyword=="*"):
        result = session.execute_read(get_all_team_list)
    else:
        result  = session.execute_read(get_team_list,keyword)

    print()

    data = []
    for temp in result:
        data.append(temp['t'])


    print(data)
    context = {'data':data}
    print(context)
    return jsonify(context),    200



def check_param(tx,param):
    result = tx.run("""
    match (t:team)
    where t.secret_name = $param
    """,param=param)

    try :
        result.peek()
        return result.data()
    except:
        return None



def create_team_node(tx,context,email):

    result = tx.run("""
    
    match (u:user),
    
    create (t:team{
    name:$name,
    size:$size,
    description:$description,
    privacy:$privacy,
    })
    
    
    return u,t
    """,
    name=context['name'],
    size=context['size'],
    description=context['description'],
    privacy=context['privacy'],
    secret_name=context['secret_name'],
    email=email
    )

    return result

def create_leader(tx,email,secret_name):
    result = tx.run("""
    match (u:user),(t:team)
    where u.email = $email and t.secret_name = $secret_name
    create (u)-[:leader]->(t)
    """,
    email=email,
    secret_name=secret_name
    )

    try:

        result.peek()
        return result.data()

    except:

        return None



@app.route('/param-exists/<string:param>',methods=['POST'])
@jwt_required()
@cross_origin()
def param_exists(param):

    result = session.execute_read(check_param,param)
    if (not result )or (len(result)==0):
        return jsonify(),   445

    return jsonify(),200


@app.route('/create-team',methods=["POST"])
@jwt_required()
@cross_origin()
def create_team():
    email  = get_jwt_identity()
    if not email:
        return jsonify({'msg':'for some reason i couldnt get the email from the token'}),   445

    name = request.json.get('name', None)

    size = request.json.get('size', None)

    privacy = request.json.get('privacy', None)

    description = request.json.get('description', None)

    secret_name = request.json.get('secret_name', None)


    context = {
        'name':  name,
        'size': size,
        'privacy': privacy,
        'description': description,
        'secret_name': secret_name,
    }


    context = json.dumps(context)


    result = session.execute_write(create_team_node,context,email)

    result1 = session.execute_write(create_leader,email,secret_name)



    return jsonify(context),    200









# with driver.session(database="neo4j") as session:
#     people = session.execute_read(
#         match_search_event,
#         "Al",
#     )
#     for person in people:
#         print(person.data())  # obtain dict representation


























if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)

# session.close()
# driver.close()



#
# def join_Team(tx,email,team_id):
#     result = tx.run('''
#     match(t:Team{id:$team_id}) , (u:User{email:$email)
#     where (u)-[:member]->(t) is NULL
#     with count((:user)-[:member]->(t) as cp
#     case
#         when n.size > cp THEN  create (u)-[:member]->(t)
#
#     return
    
    # ''')



























# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/

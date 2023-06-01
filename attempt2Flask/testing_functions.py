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







# WAEL WORK

#def match_search_team(tx, name_filter):
#     result = tx.run("""
#         MATCH (p:Team)<-[:Member]-(u:User) WHERE p.name CONTAINS $filter or u.name CONTAINS $filter
#         RETURN p
#         """, filter=name_filter)
#     return list(result)  # return a list of Record objects
#
# with driver.session(database="neo4j") as session:
#     people = session.execute_read(
#         match_search_team,
#         "Al",
#
#     )
#     for person in people:
#         print(person.data())  # obtain dict representation
#
#
#
#
#
#
# def match_search_event(tx, name_filter):
#     result = tx.run("""
#         MATCH (p:Event)<-[:Particpate]-(t:Team) <-[:Member]-(u:User) WHERE p.name CONTAINS $filter or p.descreption CONTAINS $filter or u.name CONTAINS $filter or t.name CONTAINS $filter
#         RETURN p
#         """, filter=name_filter)
#     return list(result)  # return a list of Record objects
#
# with driver.session(database="neo4j") as session:
#     people = session.execute_read(
#         match_search_event,
#         "Al",
#     )
#     for person in people:
#         print(person.data())  # obtain dict representation
#
#
#
#
# def join_team(tx, team_id, user_email, membership_descreption):
#     #user has to know team id to join it , has to authontificate , the team has to not be full , if yes , we create a realtionship between the user and the team(Member), and between the user and the old users(Teammate)
#     # if there is an error, try to check the syntax in (WHERE t.id = $ID) and specially $ID if ID is a int
#     result = tx.run("""
#         MATCH (t:Team)<-[:Member]-(old_Users:User), (u:User) WHERE ID(t) = $ID and u.email = $email and t.size> count(old_Users)
#         merge (t)<-[:Member{descreption:$descreption}]-(u)
#         merge(u)-[:Know]-(old_Users)
#         RETURN t
#         """, ID = team_id,email=user_email, descreption = membership_descreption)
#         #Maybe we don't have to add this line (RETURN p)
#
#         #if this does not work try this :
#         # MATCH (t:Team)<-[:Member]-(old_Users:User), (u:User) WHERE t.id = $ID and u.email = $email #and t.size> count(old_Users)  merge (t)<-[m]-(u)  merge(u)-[:Teammate]-(old_Users)  merge(u)-[:Know]-(old_Users) RETURN p
#
#     return list(result)  # return a list of Record objects
#
# with driver.session(database="neo4j") as session:
#     people = session.execute_write(
#         join_team,
#         "Al",
#         "a@gmail.com",
#         "descreption",
#     )
#     for person in people:
#         print(person.data())  # obtain dict representation
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# def get_user_or_None(user_email):
#
#     result = tx.run("""
#         MATCH (u:User)WHERE u.email = $email
#         RETURN p
#         """,email=user_email)  # Anthor query :         MATCH (u:User{email : eamil})  RETURN p
#     try:
#          return list(result)  # return a list of Record objects
#     except:
#         return None
#
#
#
#
#
# with driver.session(database="neo4j") as session:
#     people = session.execute_read(
#         get_user_or_None,
#         "a@gmail.com",
#     )
#     for person in people:
#         print(person.data())  # obtain dict representation
#
#
#
#
#
#
#
#
# def Create_User(tx, user_name, user_email, user_location, user_password, user_prefereces):
#     #MERGE (p:User) set p.name=$name, merge p.email=$email, merge p.location=$location, merge p.preferences=$preferences return p
#     result = tx.run("""
#         MERGE (p:User{name:$name, email:$email, location:$location, password: preferences:$preferences})
#         RETURN p
#         """, name = user_name, email = user_email, location = user_location, preferences = user_prefereces)
#     return list(result)  # return a list of Record objects
#
# with driver.session(database="neo4j") as session:
#     people = session.execute_write(
#         Create_User,
#         "name",
#         "email",
#         "location",
#         "preferences",
#     )
#     for person in people:
#         print(person.data())  # obtain dict representation
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# def Create_Event(tx, event_name, event_descreption,event_type, event_tags, event_recommanded_skills, event_prize):
#
#     result = tx.run("""
#         MERGE (p:Event{name:$name, type:$type, descreption:$descreption,tags:$tags, recommanded_skills:$recommanded_skills, prize:$prize  })
#         RETURN p
#         """, name = event_name, type = event_type, tags = event_tags, descreption = event_descreption,recommanded_skills = event_recommanded_skills, prize = event_prize)
#     return list(result)  # return a list of Record objects
#
# with driver.session(database="neo4j") as session:
#     people = session.execute_write(
#         Create_Event,
#         "code_rally",
#         "hackathon",
#         "ai",
#         "lorem ipsum",
#         15000,
#
#     )
#     for person in people:
#         print(person.data())  # obtain dict representation
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# def Create_Team(tx, team_leader_email, event_ID,team_name, team_left_position, team_size):
#     #(t:Team)<-[:Member]-
#     result = tx.run("""
#         MERGE (t:Team{name:$name, left_position:$position, size:$size}), (u:User), (e:Event)
#         WHERE  u.email = $email and ID(e) = $event_id
#         merge (t)<-[:Member]-(u)  merge (t)<-[:Leader]-(u) merge (t)-[:Participate]->(e)
#         RETURN p
#         """, name = team_name, email=team_leader_email, event_id = event_ID, postition = team_left_position, size = team_size)
#     return list(result)  # return a list of Record objects
#
# with driver.session(database="neo4j") as session:
#     people = session.execute_write(
#         Create_Team,
#         "a@gmail.com",
#         5,
#         "team_name",
#         "team_left_position",
#         "team_size",
#     )
#     for person in people:
#         print(person.data())  # obtain dict representation
#































if __name__ == '__main__':
    temp1 = ['django','react','nodejs']
    temp2 = ['react','django']
    temp3 = ['hackathon']



    # temp2.pop(0)
    # print(temp2)
    # print(calculate_manhatan_distance(temp1,temp2))
import json

import falcon

PERSONS = [
    {'id': '1', 'name': 'Bob', 'hobbies': []},
    {'id': '2', 'name': 'Larry', 'hobbies': []},
    {'id': '3', 'name': 'Kate', 'hobbies': []},
    {'id': '4', 'name': 'Clara', 'hobbies': []},
    {'id': '5', 'name': 'Sam', 'hobbies': []},
]


class PersonBase:
    def get_persons(self):
        return PERSONS

    def get_person(self, id):
        persons = self.get_persons()
        for person in persons:
            if person['id'] == id:
                return person

        return None

    def create_person(self, data):
        PERSONS.append(data)
        return data

    def update_person(self, person, data):
        if 'name' in data:
            person['name'] = data['name']

        return person

    def delete_person(self, id):
        persons = self.get_persons()
        global PERSONS
        PERSONS = [p for p in persons if p['id'] != id]

        return True


class HobbyBase:
    def get_hobbies(self, person):
        return person['hobbies']

    def has_hobby(self, person, id):
        hobbies = self.get_hobbies(person)
        return bool([h for h in hobbies if h['id'] == id])

    def create_hobby(self, person, data):
        hobbies = self.get_hobbies(person)
        hobbies.append(data)

        return hobbies

    def delete_hobby(self, person, id):
        hobbies = self.get_hobbies(person)
        person['hobbies'] = [h for h in hobbies if h['id'] != id]

        return True


class PersonResource(PersonBase):
    def on_get(self, request, response):
        persons = self.get_persons()

        response.body = json.dumps(persons)

    def on_post(self, request, response):
        body = json.loads(request.stream.read())

        data = {
            'id': body.get('id'),
            'name': body.get('name'),
        }

        if not data['id'] or not data['name']:
            raise falcon.HTTPBadRequest('Missing id or name')

        if self.get_person(data['id']):
            raise falcon.HTTPBadRequest('Person with given ID already exist')

        person = self.create_person(data)

        response.body = json.dumps({
            'url': '/persons/{}/'.format(person['id']),
        })


class PersonDetailResource(PersonBase):
    def on_get(self, request, response, person_id):
        person = self.get_person(person_id)

        if not person:
            raise falcon.HTTPNotFound()

        response.body = json.dumps(person)

    def on_patch(self, request, response, person_id):
        body = json.loads(request.stream.read())
        person = self.get_person(person_id)

        if not person:
            raise falcon.HTTPNotFound()

        person = self.update_person(person, body)

        response.body = json.dumps({
            'url': '/persons/{}/'.format(person['id']),
        })

    def on_delete(self, request, response, person_id):
        person = self.get_person(person_id)

        if not person:
            raise falcon.HTTPNotFound()

        self.delete_person(person['id'])

        response.body = json.dumps({
            'deleted': True,
        })


class PersonHobbyResource(PersonBase, HobbyBase):
    def on_get(self, request, response, person_id):
        person = self.get_person(person_id)

        if not person:
            raise falcon.HTTPNotFound()

        response.body = json.dumps(self.get_hobbies(person))

    def on_post(self, request, response, person_id):
        body = json.loads(request.stream.read())

        person = self.get_person(person_id)
        if not person:
            raise falcon.HTTPNotFound()

        data = {
            'id': body.get('id'),
            'name': body.get('name'),
        }

        if not data['id'] or not data['name']:
            raise falcon.HTTPBadRequest('Missing id or name')

        if self.has_hobby(person, data['id']):
            raise falcon.HTTPBadRequest('Hobby already exist')

        self.create_hobby(person, data)

        response.body = json.dumps({
            'url': '/persons/{}/hobbies/'.format(person['id']),
        })


class PersonHobbyDetailResource(PersonBase, HobbyBase):
    def on_delete(self, request, response, person_id, hobby_id):
        person = self.get_person(person_id)

        if not person or not self.has_hobby(person, hobby_id):
            raise falcon.HTTPNotFound()

        self.delete_hobby(person, hobby_id)

        response.body = json.dumps({
            'deleted': True,
        })


person_resource = PersonResource()
person_detail_resource = PersonDetailResource()
person_hobby_resource = PersonHobbyResource()
person_hobby_detail_resource = PersonHobbyDetailResource()

api = falcon.API()
api.add_route('/persons', person_resource)
api.add_route('/persons/{person_id}', person_detail_resource)
api.add_route('/persons/{person_id}/hobbies', person_hobby_resource)
api.add_route('/persons/{person_id}/hobbies/{hobby_id}', person_hobby_detail_resource)

import json


def exchange(lender, borrower, amount):
    """
    always update balance
    check debt side
        if there is no outstanding debt - create record - return
    if debt balance was set to zero - delete debt records
    else if lender increased amount owed - increase balance
    else if lender was already borrower
        if lender only reduced debt - update values
        else if lender reverted debt side - delete previous record and add new debt
    return
    :param lender: dict - RestApi.get_user for lender
    :param borrower: dict - RestApi.get_user for borrower
    :param amount: positive int - exchange volume
    :return: tuple dict - lender, borrower
    """

    def update_global_balance():
        lender['balance'] += amount
        borrower['balance'] -= amount

    # check what is the outstanding debt between both parties from lender POV
    try:
        if borrower['name'] in lender['owes']:
            debt = -lender['owes'][borrower['name']]

        else:
            debt = lender['owed_by'][borrower['name']]

        balance = debt + amount

    # if there is no recorded debt, add one to each side and increment balance - return
    except KeyError:
        lender['owed_by'][borrower['name']] = amount
        borrower['owes'][lender['name']] = amount

        update_global_balance()

        return lender, borrower

    # if balance becomes 0, then remove debt record and done
    if balance == 0:
        if debt < 0:
            del lender['owes'][borrower['name']]
            del borrower['owed_by'][lender['name']]
        else:
            del lender['owed_by'][borrower['name']]
            del borrower['owes'][lender['name']]

    # if lender debt was owed, increment it and done
    elif debt > 0:
        lender['owed_by'][borrower['name']] += amount
        borrower['owes'][lender['name']] += amount

    # if lender owed and balance is still negative, reduce debt and done
    elif debt < 0 and balance < 0:
        lender['owes'][borrower['name']] -= amount
        borrower['owed_by'][lender['name']] -= amount

    # if lender owed and balanced turned positive, delete entries and add new debt record
    else:
        del lender['owes'][borrower['name']]
        del borrower['owed_by'][lender['name']]
        lender['owed_by'][borrower['name']] = amount + debt
        borrower['owes'][lender['name']] = amount + debt

    update_global_balance()
    return lender, borrower


class RestAPI:
    # todo: missing sort by name for get_user
    def __init__(self, database=None):

        self.database = database if database else {'users': []}

        pass

    def get(self, url, payload=None):

        if url == "/users":

            if payload:

                load = json.loads(payload)

                return json.dumps({'users': self.get_user(load['users'][0])})

            return json.dumps(self.database)

    def get_user(self, username):
        return [user for user in self.database['users'] if user['name'] in username]

    def post(self, url, payload=None):

        if payload:

            if url == '/add':
                return json.dumps(self.add_user(json.loads(payload)))

            elif url == '/iou':
                return json.dumps(self.add_iou(json.loads(payload)))

        pass

    def add_user(self, payload):

        if 'user' in payload:

            self.database['users'].append({"name": payload['user'], "owes": {}, "owed_by": {}, "balance": 0.0})

            return {"name": payload['user'], "owes": {}, "owed_by": {}, "balance": 0.0}

    def add_iou(self, payload):

        if all(user_type in payload for user_type in ['lender', 'borrower']):  # checks if the payload is complete

            # if user does not exist, create user
            lender_name, borrower_name, amount = payload.values()

            self.add_user({'user': lender_name}) if not self.get_user(lender_name) else None
            self.add_user({'user': borrower_name}) if not self.get_user(borrower_name) else None

            lender, borrower = exchange(self.get_user(lender_name)[0], self.get_user(borrower_name)[0], amount)

            self.database['users'] = [self.database['users'][i]
                                      for i, user in enumerate(self.database['users'])
                                      if self.database['users'][i]['name'] not in [lender_name, borrower_name]]

            self.database['users'] += [lender, borrower]

        return {'users': sorted([lender, borrower], key=lambda i: i['name'])}

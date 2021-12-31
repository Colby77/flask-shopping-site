"""Customers at Ubermelon."""


class Customer(object):
    """Ubermelon customer."""

    def __init__(self, fname, lname, email, password):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password

    def __repr__(self):
        return f'Customer: {self.fname} {self.lname} {self.email} {self.password}'


def get_customers(file):

    customers = {}

    file = open(file, 'r')
    for line in file:
        line = line.strip()
        line = line.split('|')
        email = line[2]

        customers[email] = Customer(fname=line[0], lname=line[1], email=line[2], password=line[3])
    
    return customers


def get_by_email(email):
    return customers.get(email)


customers = get_customers('customers.txt')
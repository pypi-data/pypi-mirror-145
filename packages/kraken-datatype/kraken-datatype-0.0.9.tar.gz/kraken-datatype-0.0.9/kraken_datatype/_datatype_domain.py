import email_normalize
import validators

"""Normalize email
"""



def validate(data):

    if validators.domain(data):
        return True
    else:
        return False



def normalize(data):

    #todo: this

    return data
from django.db import models


class Request2PokeAPI(models.Model):
    ''' Since PokeAPI contains all the data in it's own database,
        this model will not be used to storeitems in DB. The DB will not be
        queried. Instead it will be used for mapping incoming Twilio requests
        to the correct PokeAPI URI through its view and sending data back
        to client number.
    '''

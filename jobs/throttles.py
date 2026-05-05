from rest_framework.throttling import UserRateThrottle

class Brust(UserRateThrottle):
    ''' Short term '''
    scope = 'brust'

class SustainedRateThrottle(UserRateThrottle):
    """Long term — ek din mein max 500 requests"""
    scope = 'sustained'
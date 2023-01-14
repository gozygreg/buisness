
class Cart():
    def __init__(self, request):
        self.session = request.session

        # Returing user obtain his/her existing session
        cart = self.session.get('session_key')

        # Generate a session for new user
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart














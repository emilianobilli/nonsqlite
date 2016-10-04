from uuid import uuid4
from datetime import datetime, timedelta

from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict
from nonsqlite.Object import Object


class ObjectSession(CallbackDict, SessionMixin):
	def __init__(self, initial=None, sid=None):
		CallbackDict.__init__(self,initial)
		self.sid = sid
		self.modified = False

class Session(Object):
	_db_name = ''
	def __init__(self):
		self.sid		= None
		self.data		= None
		self.expiration = None
		
class ObjectSessionInterface(SessionInterface):
	def __init__(self, ObjClass):
		self.store = ObjClass
	
	def open_session(self,app,request):
		sid = request.cookies.get(app.session_cookie_name)
		if sid:
			stored_session = self.store.get({'sid':sid})
			if stored_session:
				if stored_session.expiration > datetime.utcnow():
					return ObjectSession(initial=stored_session.data,sid=stored_session.sid)
		sid = str(uuid4())
		return ObjectSession(sid=sid)
	
	def save_session(self,app,session,response):
		domain = self.get_cookie_domain(app)
		if not session:
			response.delete_cookie(app.session_cookie_name, domain=domain)
			return
		if self.get_expiration_time(app,session):
			expiration = self.get_expiration_time(app, session)
		else:
			expiration = datetime.utcnow() + timedelta(hours=1)
		
		s = self.store()
		s.sid = session.sid
		s.session = session
		s.expiration = expiration
		s.save()
		response.set_cookie(app.session_cookie_name, session.sid,expires=self.get_expiration_time(app,session),httponly=True,domain=domain)
		
		
app = Flask(__name__)
app.session_interface = ObjectSessionInterface(Session)

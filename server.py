from flask import Flask, render_template, request
from peewee import * 
from datetime import datetime
import vobject

db = SqliteDatabase('rooms.db')

app = Flask(__name__)

class BaseModel(Model):
	class Meta:
		database = db
		
class Room(BaseModel):
	name = CharField()
	
	def timeslots_today(self):
		return self.timeslots.select().where((TimeSlot.datetime >= datetime(2014, 3, 3)) & (TimeSlot.datetime < datetime(2014, 3, 4)))

	def last_reading(self):
		return self.readings.select().order_by(Reading.id.desc()).first()

	def __unicode__(self):
		return str(self.name)
	
        
class TimeSlot(BaseModel):
	room = ForeignKeyField(Room, related_name='timeslots')
	datetime = DateTimeField(null=True)
	avail= BooleanField(null=True)
	cap  = IntegerField(null=True)
	subj = CharField(null=True)
	
class User(BaseModel):
	name = CharField()
	
class TimeSlotUser(BaseModel):
	timeslot = ForeignKeyField(TimeSlot, related_name='timeslot_users')
	user = ForeignKeyField(User, related_name='timeslot_users')
	
class Reading(BaseModel):
	room = ForeignKeyField(Room, related_name='readings')
	temperature = FloatField()
	noise = FloatField()
	light_status = BooleanField()
	
@app.route('/create_database')
def create_database():
	for table in [User, Reading, TimeSlotUser, TimeSlot, Room]:
		table.drop_table()
		table.create_table()

@app.route('/check_availability')
def check_availability():
	create_database()
	
	data = open("calendar.ics").read()

	# parse the top-level event with vobject
	cal = vobject.readOne(data)

	for event in cal.vevent_list:
		# Get Summary
		print 'Summary: ', event.summary.valueRepr()
		# Get Description
		print 'Description: ', event.description.valueRepr()

		# Get Time
		print 'Time (as a datetime object): ', event.dtstart.value
		print 'Time (as a string): ', event.dtstart.valueRepr()
		
		# Get Location
		print 'Location (as a datetime object): ', event.location.value
		print 'Time (as a string): ', event.dtstart.valueRepr()

		# skip rooms with empty location
		if not event.location.value.strip():
			continue
		
		room = Room.select().where(Room.name == event.location.valueRepr()).first()

		if room is None:
			room = Room.create(name=event.location.valueRepr())
		
		TimeSlot.create(room=room,
		                subj=event.summary.valueRepr(),
		                datetime=event.dtstart.value
		                )

@app.route('/log')
def log():
	room_id = request.args.get('room_id', '')
	temp = request.args.get('temp', '') # ?temp=<?>
	noise = request.args.get('noise', '')
	light_status = request.args.get('light', '')

	room = Room.select().where(Room.id == int(room_id)).first()

	reading = Reading.create(room=room, temperature=float(temp), noise=float(noise), light_status=(light_status == 't'))

	return str(reading.id)


@app.route('/')
def hello_world():
	rooms = Room.select()
	return render_template('hello.html', rooms=rooms)
	
if __name__=='__main__':
	app.debug = True
	app.run()



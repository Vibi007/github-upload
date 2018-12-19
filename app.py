from flask import Flask, jsonify
import json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import mapper
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:vib-123@127.0.0.1:3306/Reports'
db=SQLAlchemy(app)
ma = Marshmallow(app)

metadata = db.MetaData(db.engine)
pend_south = db.Table('Pending_South',
db.Column("OBJECT_ID", db.Integer, primary_key=True),
db.Column("CONCATSTATUSER", db.String),
db.Column("FRANCHISE_CODE", db.Integer)
,extend_existing=True)

class pending(object):
    pass

mapper(pending, pend_south)
session = db.sessionmaker(bind=db.engine)
Session = session()



class pendingSchema(ma.Schema):
    class Meta:
        model = pending
        fields = (['OBJECT_ID','CONCATSTATUSER','FRANCHISE_CODE'])

Pending_Schema = pendingSchema(many=True)
@app.route('/api/v1.0/demos')
def get_tasks():
    
    Tickets = Session.query(pending).all()
    Tickets_all = Pending_Schema.dump(Tickets).data
    return jsonify({'Tickets':Tickets_all})

@app.route('/api/v1.0/demos/')
def get_task():
    fran = request.args.get('FRANCHISE_CODE')
    ticket = Session.query(pending).filter_by(FRANCHISE_CODE=fran).all()
    Ticket_one = Pending_Schema.dump(ticket).data
    return jsonify({'Ticket':Ticket_one})
if __name__ == '__main__':
    app.run(debug=True)
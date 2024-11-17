from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class cs_info(db.Model):
    __tablename__="cs_info"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    fullname=db.Column(db.String,nullable=False)
    address=db.Column(db.String,nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    phone=db.Column(db.String,nullable=False)
    role=db.Column(db.Integer,default=1) #0-->admin ,,1-->customer
    flag=db.Column(db.String,nullable=False,default="no")
    requests=db.relationship("service_request",cascade="all,delete",backref="cs_info",lazy=True)


class pf_info(db.Model):
    __tablename__="pf_info"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    fullname=db.Column(db.String,nullable=False)
    address=db.Column(db.String,nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    phone=db.Column(db.Integer,nullable=False)
    servicename=db.Column(db.String,nullable=False)
    experience=db.Column(db.Integer,nullable=False)
    Date=db.Column(db.String,nullable=False)
    role=db.Column(db.Integer,default=2)
    verified=db.Column(db.String,nullable=False,default="pending")
    flag=db.Column(db.String,nullable=False,default="no")
    requests=db.relationship("service_request",cascade="all,delete",backref="pf_info",lazy=True)

class rejected_requests(db.Model):
    __tablename__="rejected_requests"
    id=db.Column(db.Integer,primary_key=True)
    professionalid=db.Column(db.Integer,db.ForeignKey("pf_info.id"),nullable=False)
    servicerequestid=db.Column(db.Integer,db.ForeignKey("service_request.id"),nullable=False)


class service(db.Model):
    __tablename__="service"
    id=db.Column(db.Integer,primary_key=True)
    servicename=db.Column(db.String,nullable=False)
    servicess=db.relationship("services",cascade="all,delete",backref="service",lazy=True)


class services(db.Model):
    __tablename__="services"
    id=db.Column(db.Integer,primary_key=True)
    description=db.Column(db.String,nullable=False)
    baseprice=db.Column(db.Float,default=0.0)
    timerequire=db.Column(db.Integer,nullable=False)
    average_rating=db.Column(db.Integer,nullable=True,default=0)
    service_id=db.Column(db.Integer,db.ForeignKey("service.id"),nullable=False)
    servicesss=db.relationship("service",backref="services",lazy=True)
    servicereq=db.relationship("service_request",cascade="all,delete",backref="services",lazy=True)

class service_request(db.Model):
    __tablename__="service_request"
    id=db.Column(db.Integer,primary_key=True)
    date_of_request=db.Column(db.String,nullable=True)
    date_of_completion=db.Column(db.String,nullable=True)
    service_rating=db.Column(db.Integer,default=0)
    service_status=db.Column(db.String,nullable=False,default="requested")
    service_remarks=db.Column(db.String,nullable=True)
    customer_id=db.Column(db.Integer,db.ForeignKey("cs_info.id"),nullable=False)
    professional_id=db.Column(db.Integer,db.ForeignKey("pf_info.id"),nullable=True,default=0)
    serviceid=db.Column(db.Integer,db.ForeignKey("service.id"),nullable=False)
    service_id=db.Column(db.Integer,db.ForeignKey("services.id"),nullable=False)
    customers=db.relationship("cs_info",backref="service_request",lazy=True)
    servicee=db.relationship("service",backref="service_request",lazy=True)
    servicess=db.relationship("services",backref="service_request",lazy=True)
    rejected=db.relationship("rejected_requests",cascade="all,delete",backref="service_request",lazy=True)
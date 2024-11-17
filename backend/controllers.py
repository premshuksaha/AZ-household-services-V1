from flask import Flask,render_template,request,redirect,url_for
from.models import *
from flask import current_app as app
import datetime
from sqlalchemy.sql import func
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


matplotlib.use('Agg')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        usname=request.form.get("email")
        pword=request.form.get("password")
        user1=cs_info.query.filter_by(email=usname,password=pword).first()
        user2=pf_info.query.filter_by(email=usname,password=pword).first()
        if user1 and user1.role==0:
            return redirect(url_for("admin_home",name=usname))
        elif user1 and user1.role==1:
            if user1.flag=="no":
                customer=fetch_customer_info(user1.id)
                return redirect(url_for("cs_home",name=usname,id=customer.id))
            else:
                return ("You have been flagged. Contact the administrator for more details")
        elif user2:
            if user2.verified=="pending":
                return ("You are not verified yet")
            elif user2.verified=="rejected":
                return ("Your documents has been rejected !!")
            else:
                if user2.flag=="no":
                    professional=fetch_professional_info(user2.id)
                    return redirect(url_for("pf_home",name=usname,id=professional.id,service=professional.servicename))
                else:
                    return ("You have been flagged. Contact the administrator for more details")
        else:
            return render_template("login.html",msg="Invalid user credentials...")

    return render_template("login.html",msg="")

@app.route("/cs_signup",methods=["GET","POST"])
def cs_signup():
    if request.method=="POST":
        usname=request.form.get("email")
        pword=request.form.get("password")
        fullname=request.form.get("fullname")
        phone=request.form.get("phone")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        user1=cs_info.query.filter_by(email=usname).first()
        if user1:
            return render_template("cs_signup.html",msg="Sorry, this mail already registered!!!")
        newuser=cs_info(email=usname,password=pword,fullname=fullname,phone=phone,address=address,pincode=pincode)
        db.session.add(newuser)
        db.session.commit()
        return render_template("login.html",msg="Please login now to proceed")
    return render_template("cs_signup.html",msg="")


@app.route("/pf_signup",methods=["GET","POST"])
def pf_signup():
    if request.method=="POST":
        usname=request.form.get("email")
        pword=request.form.get("password")
        fullname=request.form.get("fullname")
        phone=request.form.get("phone")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        s_name=request.form.get("service")
        exp=request.form.get("experience")
        datee=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        newuser=pf_info(email=usname,password=pword,fullname=fullname,phone=phone,address=address,pincode=pincode,servicename=s_name,experience=exp,Date=datee)
        db.session.add(newuser)
        db.session.commit()
        return render_template("login.html",msg="Please login now to proceed")
    return render_template("pf_signup.html",msg="")

@app.route("/admin/<name>")
def admin_home(name):
    service=get_service()
    unverified_professionals=pf_info.query.filter_by(verified="pending").all()
    service_requests=get_all_service_requests()
    customers=cs_info.query.all()
    professional=pf_info.query.all()
    
    return render_template("admin_home.html",name=name,servicee=service,unverified_professionals=unverified_professionals,service_requests=service_requests,customers=customers,professionals=professional)
                           

@app.route("/cs_home/<name>/<id>")
def cs_home(name,id):
    cs=fetch_customer_info(id)
    name=cs.email
    service=get_service()
    servi=services.query.all()
    all_services=service_request.query.filter_by(customer_id=id).all()
    professional=pf_info.query.all()
    return render_template("cs_home.html",name=name,id=id,service=service,all_services=all_services,professionals=professional,serv=servi)

@app.route("/pf_home/<name>/<id>/<service>")
def pf_home(name,id,service):
    try:
        pf=fetch_professional_info(id)
        name=pf.email
        service=pf.servicename
        servicee=get_service_id(service)
        allrequests=service_request.query.filter_by(serviceid=servicee).all()
        allrequests1=service_request.query.filter_by(professional_id=id).all()
        rejection=rejected_requests.query.filter_by(professionalid=id).all()
        customers=cs_info.query.all()
        return render_template("pf_home.html",name=name,pf=pf,id=id,service=service,requests=allrequests,requests1=allrequests1,servise=servicee,rejected=rejection,customers=customers)
    except:
        return("The servicetype that you are registered for does not exist.Contact the administrator for more info")

def fetch_customer_info(id):
    customer_info=cs_info.query.filter_by(id=id).first()
    return customer_info

def fetch_professional_info(id):
    professional_info=pf_info.query.filter_by(id=id).first()
    return professional_info



@app.route("/addservice/<name>",methods=["POST","GET"])
def add_service(name):
    if request.method=="POST":
        sname=request.form.get("servicename")
        add_service=service(servicename=sname)
        db.session.add(add_service)
        db.session.commit()
        return redirect(url_for("admin_home",name=name))

  
@app.route("/editservice/<name>",methods=["POST","GET"])
def edit_service(name):
    if request.method=="POST":
        id=request.form.get("idservice")
        new_servicename=request.form.get("servicesname")
        listss=service.query.filter_by(id=id).first()
        listss.servicename=new_servicename
        db.session.commit()
        return redirect(url_for("admin_home",name=name))
    

@app.route("/deleteservice/<name>",methods=["POST","GET"])
def delete_service(name):
    if request.method=="POST":
        new_servicename=request.form.get("servicesname")
        listss=service.query.filter_by(servicename=new_servicename).first()
        db.session.delete(listss)
        db.session.commit()
        return redirect(url_for("admin_home",name=name))

@app.route("/editservice/<servicee_id>/<s_name>/<name>",methods=["POST","GET"])
def services_edit(servicee_id,s_name,name):
    if request.method=="POST":
        serviceid=request.form.get("serviceid")
        description=request.form.get("description")
        timerequire=request.form.get("timerequired")
        baseprice=request.form.get("baseprice")
        all=services_info(serviceid)
        all.timerequire=timerequire
        all.description=description
        all.baseprice=baseprice
        db.session.commit()
        return redirect(url_for("view_services",servicee_id=servicee_id,servicename=s_name,name=name))
    
@app.route("/deleteservice/<servicee_id>/<s_name>/<name>",methods=["POST","GET"])
def services_delete(servicee_id,s_name,name):
    if request.method=="POST":
        description=request.form.get("description")
        timerequire=request.form.get("timerequired")
        baseprice=request.form.get("baseprice")
        all=services.query.filter_by(description=description).first()
        all.description=description
        all.timerequire=timerequire
        all.baseprice=baseprice
        db.session.delete(all)
        db.session.commit()
        return redirect(url_for("view_services",servicee_id=servicee_id,servicename=s_name,name=name))


@app.route("/servicesadd/<sarvice_id>/<servicename>/<name>",methods=["POST","GET"])
def servicesadd(sarvice_id,servicename,name):
    if request.method=="POST":
        desc=request.form.get("description")
        time=request.form.get("timerequired")
        bprice=request.form.get("baseprice")
        new=services(description=desc,timerequire=time,baseprice=bprice,service_id=sarvice_id)
        db.session.add(new)
        db.session.commit()
        return redirect(url_for("view_services",servicee_id=sarvice_id,servicename=servicename,name=name))


@app.route("/viewservices/<servicee_id>/<servicename>/<name>")
def view_services(servicee_id,servicename,name):
    service=services.query.filter_by(service_id=servicee_id).all()
    return render_template("viewservice.html",s_name=servicename,servicer=service,servicee_id=servicee_id,name=name)



@app.route("/openservice/<serviceid>/<servicename>/<id>/<name>")
def open_service(serviceid,servicename,id,name):
    service=services.query.filter_by(service_id=serviceid).all()
    return render_template("open_service.html",serviceid=serviceid,servicename=servicename,id=id,services=service,name=name)
    

@app.route("/pf_signupp")
def pf_signupp():
    services=get_service()
    return render_template("pf_signup.html",serv=services)

@app.route("/cs_signupp")
def cs_signupp():
    return render_template("cs_signup.html")

@app.route("/accept_pf/<id>/<name>")
def accept_pf(id,name):
    pf=pf_info.query.get(id)
    pf.verified="yes"
    db.session.commit()
    return redirect(url_for("admin_home",name=name))

@app.route("/reject_pf/<id>/<name>")
def reject_pf(id,name):
    pf=pf_info.query.get(id)
    pf.verified="rejected"
    db.session.commit()
    return redirect(url_for("admin_home",name=name))

@app.route("/book/<serviceid>/<servicesid>/<customerid>/<name>")
def book(serviceid,servicesid,customerid,name):
    date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    booking=service_request(date_of_request=date,customer_id=customerid,serviceid=serviceid,service_id=servicesid)
    db.session.add(booking)
    db.session.commit()
    return redirect(url_for("cs_home",name=name,id=customerid))


@app.route("/edit_csprofile/<name>/<id>",methods=["POST","GET"])
def edit_cs_profile(name,id):
    cs=fetch_customer_info(id)
    if request.method=="POST":
        csemail=request.form.get("email")
        pword=request.form.get("password")
        fname=request.form.get("fullname")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        phone=request.form.get("phone")
        cs.email=csemail
        cs.password=pword
        cs.fullname=fname
        cs.address=address
        cs.pincode=pincode
        cs.phone=phone
        db.session.commit()
        return redirect(url_for("cs_home",name=name,id=id))
    return render_template ("cs_profileedit.html",name=name,id=id,customer=cs)

@app.route("/edit_pfprofile/<name>/<id>/<service>",methods=["POST","GET"])
def edit_pf_profile(name,id,service):
    pf=fetch_professional_info(id)
    if request.method=="POST":
        pfemail=request.form.get("email")
        pword=request.form.get("password")
        fname=request.form.get("fullname")
        servicename=request.form.get("servicename")
        experience=request.form.get("experience")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        phone=request.form.get("phone")
        pf.email=pfemail
        pf.password=pword
        pf.fullname=fname
        pf.servicename=servicename
        pf.experience=experience
        pf.address=address
        pf.pincode=pincode
        pf.phone=phone
        db.session.commit()
        return redirect(url_for("pf_home",name=name,id=id,service=service))
    return render_template ("pf_profileedit.html",name=name,id=id,professional=pf,service=service)

@app.route("/acceptservice/<name>/<id>/<service>/<requestid>")
def acceptservice(name,id,service,requestid):
    requestt=service_request.query.filter_by(id=requestid).first()
    requesst=id
    requestt.professional_id=requesst
    requestt.service_status="accepted"
    db.session.commit()
    return redirect(url_for("pf_home",name=name,id=id,service=service))

@app.route("/rejectservice/<name>/<id>/<service>/<requestid>")
def rejectservice(name,id,service,requestid):
    rejecting=rejected_requests(professionalid=id,servicerequestid=requestid)
    db.session.add(rejecting)
    db.session.commit()
    return redirect(url_for("pf_home",name=name,id=id,service=service))


@app.route("/closerequest/<name>/<id>/<servireqid>")
def closerequest(name,id,servireqid):
    servicees=service_request.query.filter_by(id=servireqid).first()
    serviceid=servicees.serviceid
    servicesid=servicees.service_id
    professionalid=servicees.professional_id
    professional=pf_info.query.filter_by(id=professionalid).first()
    servicee=service.query.filter_by(id=serviceid).first()
    servicess=services.query.filter_by(id=servicesid).first()
    return render_template("serviceremarks.html",name=name,id=id,servicesid=servireqid,servicename=servicee.servicename,
                           description=servicess.description,dateofreq=servicees.date_of_request,pid=professional.id,
                           pname=professional.fullname,phone=professional.phone)




@app.route("/serviceremarks/<name>/<id>/<servireqid>",methods=["POST","GET"])
def serviceremarks(name,id,servireqid):
    if request.method=="POST":
        ratingg=request.form.get("rating")
        remarkss=request.form.get("remarks")
        date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        serv_request=service_request.query.filter_by(id=servireqid).first()
        serv_request.service_rating=ratingg
        serv_request.service_remarks=remarkss
        serv_request.date_of_completion=date
        serv_request.service_status="closed"
        db.session.commit()
        a=services.query.filter_by(id=serv_request.service_id).first()
        avg_ratin = (db.session.query(func.avg(service_request.service_rating).label("avg_rating")).filter( service_request.service_id == serv_request.service_id).filter_by(service_status="closed").first())
        average_rating = avg_ratin.avg_rating
        a.average_rating=average_rating
        db.session.commit()
        return redirect(url_for("cs_home",name=name,id=id))
    return redirect(url_for("cs_home",name=name,id=id))

@app.route("/adminsearch/<name>")
def adminsearch(name):
    return render_template("adminsearch.html",name=name)

@app.route("/adminsummary/<name>")
def adminsummary(name):
    try:
        overall_customer_ratings()
        status_wise_requests_count()
        service_count=services.query.count()
        services_count=service_request.query.count()
        customers_count=cs_info.query.filter_by(role=1).count()
        professionals_count=pf_info.query.count()
        return render_template("adminsummary.html",name=name,services_count=service_count,services_request_count=services_count,customers_count=customers_count,professionals_count=professionals_count)
    except:
        return redirect(url_for("admin_home",name=name))

@app.route("/cs_search/<name>/<id>")
def cs_search(name,id):
    return render_template("cs_search.html",name=name,id=id)

@app.route("/cs_summary/<name>/<id>")
def cs_summary(name,id):
    cs_status_wise_requests_count(id)
    return render_template("cssummary.html",name=name,id=id)

@app.route("/pf_search/<name>/<id>/<service>")
def pf_search(name,id,service):
    return render_template("pf_search.html",name=name,id=id,service=service)

@app.route("/pf_summary/<name>/<id>/<service>")
def pf_summary(name,id,service):
    try:
        pf_status_wise_requests_count(id)
        pf_overall_customer_ratings(id)
        avg_ratin = (db.session.query(func.avg(service_request.service_rating).label("avg_rating")).filter_by(professional_id=id).filter_by(service_status="closed").first())
        average_rating = avg_ratin.avg_rating
        return render_template("pfsummary.html",name=name,id=id,service=service,average_rating=average_rating)
    except:
        return redirect(url_for("pf_home",name=name,id=id,service=service))

def get_service():
    servicee=service.query.all()
    return servicee ##to return the service table(servicename)

def get_services():
    servicess=services.query.all()
    return servicess  ##to return the services table(desc,baseprice,etc)

def get_pf_info():
    all_pf=pf_info.query.all()
    return all_pf

def get_all_service_requests():
    all_services=service_request.query.all()
    return all_services

def services_info(id):
    services_info=services.query.filter_by(id=id).first()
    return services_info

def get_service_id(name):
    servicee=service.query.filter_by(servicename=name).first()
    return servicee.id



@app.route("/adminsearch/<name>",methods=["POST","GET"])
def admin_search(name):
    if request.method=="POST":
        search_byy=request.form.get("search_by")
        search_textt=request.form.get("search_text")
        if search_textt=="" and search_byy=="services":
            services=service_request.query.all()
            customers=cs_info.query.all()
            professional=pf_info.query.all()
            return render_template("adminsearch.html",name=name,services=services,customers=customers,professionals=professional,msg="")
        elif search_textt!="" and search_byy=="services":
            services=service_request.query.filter(service_request.service_status.ilike(f"%{search_textt}%")).all()
            customers=cs_info.query.all()
            professional=pf_info.query.all()
            return render_template("adminsearch.html",name=name,services=services,customers=customers,professionals=professional,msg="")
        elif search_textt=="" and search_byy=="customers":
            custom=cs_info.query.filter_by(role=1).all()
            return render_template("adminsearch.html",name=name,customa=custom,msg="")
        elif search_textt!="" and search_byy=="customers":
            custom=cs_info.query.filter(cs_info.fullname.ilike(f"%{search_textt}%")).all()
            return render_template("adminsearch.html",name=name,customa=custom,msg="")
        elif search_textt=="" and search_byy=="professionals":
            professiona=pf_info.query.all()
            return render_template("adminsearch.html",name=name,profess=professiona,msg="")
        elif search_textt!="" and search_byy=="professionals":
            professiona=pf_info.query.filter(pf_info.fullname.ilike(f"%{search_textt}%")).all()
            return render_template("adminsearch.html",name=name,profess=professiona,msg="")
        else:
            return render_template("adminsearch.html",name=name,msg="No Search Results Found !!!")
        
        
@app.route("/pf_search/<name>/<id>/<service>",methods=["POST","GET"])
def pf_searchh(name,id,service):
    if request.method=="POST":
        search_textt=request.form.get("search_txt")
        by_location=search_by_location(search_textt)
        by_pincode=search_by_pincode(search_textt)
        by_status=search_by_status(search_textt)
        all_services=service_request.query.filter_by(professional_id=id).all()
        customers=cs_info.query.all()
        if by_location:
            return render_template("pf_search.html",name=name,id=id,service=service,requests=all_services,customers=by_location )
        elif by_pincode:
            return render_template("pf_search.html",name=name,id=id,service=service,requests=all_services,customers=by_pincode )
        elif by_status:
            return render_template("pf_search.html",name=name,id=id,service=service,requests=by_status,customers=customers )
    return render_template("pf_search.html",name=name,id=id,service=service,msg="No search results found!!" )


def search_by_location(search_txt):
    cs_location=cs_info.query.filter(cs_info.address.ilike(f"%{search_txt}%")).all()
    return cs_location

def search_by_pincode(search_txt):
    cs_pincode=cs_info.query.filter(cs_info.pincode.ilike(f"%{search_txt}%")).all()
    return cs_pincode

def search_by_status(search_txt):
    service_status=service_request.query.filter(service_request.service_status.ilike(f"%{search_txt}%")).all()
    return service_status
        
        
@app.route("/cs_search/<name>/<id>",methods=["POST","GET"])
def cs_searchh(name,id):
    if request.method=="POST":
        search_byy=request.form.get("search_by")
        search_textt=request.form.get("search_text")
        by_serice_name=search_by_servicename(search_textt)
        by_serice_status=search_by_status1(search_textt)
        if search_byy=="servicename":
            if by_serice_name:
                serviceee=services.query.filter_by(service_id=by_serice_name.id).all()
                return render_template("cs_search.html",id=id,services=serviceee,name=name,msg="")
            else:
                return render_template("cs_search.html",name=name,id=id,msg="No Search Results Found !!!")
        elif search_byy=="status":
            if by_serice_status:
                servicee=get_service()
                servi=services.query.all()
                professional=pf_info.query.all()
                service_status=service_request.query.filter_by(customer_id=id).filter(service_request.service_status.ilike(f"%{search_textt}%")).all()
                return render_template("cs_search.html",id=id,name=name,service=servicee,all_services=service_status,professionals=professional,serv=servi)
            else:
                return render_template("cs_search.html",name=name,id=id,msg="No Search Results Found !!!")
        
def search_by_servicename(search_txt):
    service_name=service.query.filter(service.servicename.ilike(f"%{search_txt}%")).first()
    return service_name

def search_by_status1(search_txt):
    service_status=service_request.query.filter(service_request.service_status.ilike(f"%{search_txt}%")).all()
    return service_status

def rawe(word):
    result=word.split()
    result1=''
    for word in result:
        result1 +=word.lower()
    return result1


@app.route("/customer_flag/<name>/<id>")
def customer_flag(name,id):
    customer=cs_info.query.filter_by(id=id).first()
    customer.flag="yes"
    db.session.commit()
    return redirect(url_for("admin_search",name=name))

@app.route("/customer_unflag/<name>/<id>")
def customer_unflag(name,id):
    customer=cs_info.query.filter_by(id=id).first()
    customer.flag="no"
    db.session.commit()
    return redirect(url_for("admin_search",name=name))

@app.route("/professional_flag/<name>/<id>")
def professional_flag(name,id):
    professional=pf_info.query.filter_by(id=id).first()
    professional.flag="yes"
    db.session.commit()
    return redirect(url_for("admin_search",name=name))

@app.route("/professional_unflag/<name>/<id>")
def professional_uflag(name,id):
    professional=pf_info.query.filter_by(id=id).first()
    professional.flag="no"
    db.session.commit()
    return redirect(url_for("admin_search",name=name))


def overall_customer_ratings():
    ratings = service_request.query.all()
    onestar = 0
    twostar = 0
    threestar = 0
    fourstar = 0
    fivestar = 0
    for rating in ratings:
        if rating.service_rating == 1:
            onestar += 1
        elif rating.service_rating == 2:
            twostar += 1
        elif rating.service_rating == 3:
            threestar += 1
        elif rating.service_rating == 4:
            fourstar += 1
        elif rating.service_rating == 5:
            fivestar += 1     
    labels = ['onestar', 'twostar', 'threestar', 'fourstar','fivestar']
    sizes = [onestar, twostar, threestar, fourstar,fivestar]
    
    plt.title('Overall Customer Rating')
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightgreen','lightblue']
    explode = (0, 0, 0, 0,0.1) # explode 5star
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda
    pct: format_pct_and_count(pct, sizes), shadow=True, startangle=140)
    plt.axis('equal')
    plt.savefig('static/graphs/overall_customer_ratings.png')
    plt.close()
    return 'static/graphs/overall_customer_ratings.png'


def pf_overall_customer_ratings(id):
    onestar = 0
    twostar = 0
    threestar = 0
    fourstar = 0
    fivestar = 0
    ratings = service_request.query.filter_by(professional_id=id).all()
    
    for rating in ratings:
        if rating.service_rating == 1:
            onestar += 1
        elif rating.service_rating == 2:
            twostar += 1
        elif rating.service_rating == 3:
            threestar += 1
        elif rating.service_rating == 4:
            fourstar += 1
        elif rating.service_rating == 5:
            fivestar += 1     
    labels = ['onestar', 'twostar', 'threestar', 'fourstar','fivestar']
    sizes = [onestar, twostar, threestar, fourstar,fivestar]
    
    plt.title('Overall Customer Rating')
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightblue','brown']
    explode = (0, 0, 0, 0, 0) 
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=lambda pct: format_pct_and_count(pct, sizes), shadow=True, startangle=140)
    plt.axis('equal')
    plt.savefig('static/graphs/pf_overall_customer_ratings.png')
    plt.close()
    return 'static/graphs/pf_overall_customer_ratings.png'


def format_pct_and_count(pct, allvals):
    absolute = int(pct / 100. * sum(allvals))
    return "{:.1f}%\n({:d})".format(pct, absolute)


def status_wise_requests_count():
    services_count=service_request.query.all()
    types=[]
    for services in services_count:
        types.append(services.service_status)
    plt.hist(types)
    plt.savefig('static/graphs/status_wise_requests_count.png')
    plt.close()
    return 'static/graphs/status_wise_requests_count.png'


def cs_status_wise_requests_count(id):
    services_count=service_request.query.filter_by(customer_id=id).all()
    types=[]
    for services in services_count:
        types.append(services.service_status)
    plt.hist(types)
    plt.savefig('static/graphs/cs_status_wise_requests_count.png')
    plt.close()
    return 'static/graphs/cs_status_wise_requests_count.png'

def pf_status_wise_requests_count(id):
    services_count=service_request.query.filter_by(professional_id=id).all()
    types=[]
    for services in services_count:
        types.append(services.service_status)
    plt.hist(types)
    plt.savefig('static/graphs/pf_status_wise_requests_count.png')
    plt.close()
    return 'static/graphs/pf_status_wise_requests_count.png'


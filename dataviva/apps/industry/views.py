# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g
from dataviva.apps.general.views import get_locale
from dataviva.api.attrs.models import Cnae, Cbo, Bra
from dataviva.api.rais.models import Yi , Ybi, Yio, Ybio
from dataviva import db
from sqlalchemy import func, desc


mod = Blueprint('industry', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/industry',
                static_folder='static')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/')
def index():
 
    bra_id = '4mg'
    cnae_id = 'g47113' #supermarkets
    industry = {}

    industry = { 
        'name': unicode('Supermercados', 'utf8'), 
        'location' : False , 
        'class' : False,
        'year' : 2010,
        'background_image':  unicode("'static/img/bg-profile-location.jpg'", 'utf8'),
        'portrait' : unicode('https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d7748245.803118934!2d-49.94643868147362!3d-18.514293729997753!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xa690a165324289%3A0x112170c9379de7b3!2sMinas+Gerais!5e0!3m2!1spt-BR!2sbr!4v1450524997110', 'utf8') ,
        
        'text_profile' : unicode('Texto de perfil para Supermercados.', 'utf8'),
        'text_salary_job' : unicode('Texto para Salários e empregos', 'utf8'),
        'text_economic_opportunity' : unicode('Texto para Oportunidades Econômicas', 'utf8'),
        'county' : False
    }

    if bra_id == None : 
        bra_id = ""

    if bra_id == "" :
        industry['location'] = False
    else : 
        industry['location'] = True    
     
    if len(bra_id) == 9 : 
        industry['county'] = True
    else :
        industry['county'] = True    

    if len(cnae_id) == 1 : 
        industry['class'] = True
    else : 
        industry['class'] = False

    ####EXTRACTY 
    industry['name'] = Cnae.query.filter_by(id=cnae_id).one().name()
      
    if bra_id == "" :

        yi_max_year = db.session.query(func.max(Yi.year)).filter_by(cnae_id=cnae_id)
        industry['year'] = yi_max_year.scalar() 

        yio_max_year = db.session.query(func.max(Yio.year)).filter_by(cnae_id=cnae_id)

        ybi_max_year = db.session.query(func.max(Ybi.year)).filter_by(cnae_id=cnae_id)

        headers_generator = Yi.query.filter(
            Yi.cnae_id == cnae_id,
            Yi.year == yi_max_year    
            ).values(Yi.wage, Yi.num_jobs, Yi.num_est, Yi.wage_avg )


        for  wage, num_jobs, num_est, wage_avg in headers_generator:        
            industry['average_monthly_income'] = wage_avg
            industry['salary_mass'] = wage
            industry['total_jobs'] = num_jobs
            industry['total_establishments'] = num_est

        occupation_jobs_generaitor = Yio.query.join(Cbo).filter(
            Yio.cbo_id == Cbo.id,
            Yio.cnae_id == cnae_id,
            Yio.cbo_id_len == 4,                
            Yio.year == yio_max_year 
            ).order_by(desc(Yio.num_jobs)).limit(1).values(Cbo.name_pt, Yio.num_jobs)

        for  name, value in occupation_jobs_generaitor:        
            industry['occupation_max_number_jobs_name'] = name
            industry['occupation_max_number_jobs_value'] = value

        occupation_wage_avg_generaitor = Yio.query.join(Cbo).filter(
            Yio.cbo_id == Cbo.id,
            Yio.cnae_id == cnae_id,
            Yio.cbo_id_len == 4,                 
            Yio.year == yio_max_year 
            ).order_by(desc(Yio.wage_avg)).limit(1).values(Cbo.name_pt, Yio.wage_avg)

        for  name, value in occupation_wage_avg_generaitor:        
            industry['occupation_max_monthly_income_name'] = name
            industry['occupation_max_monthly_income_value'] = value
           
        if len(bra_id) != 9 : 

            county_jobs_generaitor = Ybi.query.join(Bra).filter(
                Bra.id == Ybi.bra_id,
                Ybi.cnae_id == cnae_id,
                Ybi.bra_id_len == 9,
                Ybi.year == ybi_max_year,      
                ).order_by(desc(Ybi.num_jobs)).limit(1).values(Bra.name_pt, Ybi.num_jobs)
        
            for  name, value in county_jobs_generaitor:        
                industry['county_max_number_jobs_name'] = name
                industry['county_max_number_jobs_value'] = value
   
            county_wage_avg_generaitor = Ybi.query.join(Bra).filter(
                Bra.id == Ybi.bra_id,
                Ybi.cnae_id == cnae_id,
                Ybi.bra_id_len == 9,
                Ybi.year == ybi_max_year,    
                ).order_by(desc(Ybi.wage_avg)).limit(1).values(Bra.name_pt, Ybi.wage_avg)   
            
            for  name, value in county_wage_avg_generaitor:        
                industry['county_max_monthly_income_name'] = name
                industry['county_max_monthly_income_value'] = value    
    
    else : 
        # Max year, location diferent Brazil
        ybi_max_year_bra_id=db.session.query(
            func.max(Ybi.year)).filter_by(bra_id=bra_id, cnae_id=cnae_id)
        
        industry['year'] = ybi_max_year_bra_id.scalar()

        ybio_max_year_bra_id=db.session.query(
            func.max(Ybio.year)).filter_by(bra_id=bra_id, cnae_id=cnae_id)
          

        ##Get Headers 
        headers_generate = Ybi.query.filter(
            Ybi.cnae_id==cnae_id,
            Ybi.bra_id == bra_id,
            Ybi.year==ybi_max_year_bra_id).values(
                Ybi.wage, Ybi.num_jobs, 
                Ybi.num_est, Ybi.wage_avg, 
                Ybi.rca, Ybi.distance, 
                Ybi.opp_gain) 

        lista = []
        for wage, num_jobs, num_est, wage_avg, rca, distance, opp_gain in headers_generate:
           industry['average_monthly_income'] = wage
           industry['salary_mass'] =  num_jobs
           industry['total_jobs'] =  num_est
           industry['total_establishments'] =  wage_avg
           industry['rca_domestic'] =  rca
           industry['distance'] =  distance
           industry['opportunity_gain'] =  opp_gain 

        dic_names_cbo = {}
        dic_names_bra = {}

        cbo_generate = Cbo.query.values(Cbo.id, Cbo.name_en, Cbo.name_pt)
        bra_generate = Bra.query.values(Bra.id, Bra.name_en, Bra.name_pt)

        for id, name_en, name_pt in cbo_generate:
            dic_names_cbo[id] = [name_en, name_pt]

        for id, name_en, name_pt in bra_generate:
            dic_names_bra[id] = [name_en, name_pt]

        occ_jobs_generate = Ybio.query.filter(
            Ybio.cnae_id == cnae_id,
            Ybio.cbo_id_len == 4,
            Ybio.bra_id == bra_id,
            Ybio.year == ybio_max_year_bra_id
            ).order_by(desc(Ybio.num_jobs)).limit(1).values(Ybio.cbo_id, Ybio.num_jobs)  

        

        for cbo_id, num_jobs in occ_jobs_generate : 
            industry['occupation_max_number_jobs_value'] = num_jobs
            industry['occupation_max_number_jobs_name'] = dic_names_cbo[cbo_id][1]      

        occ_wage_avg_generate = Ybio.query.filter(
            Ybio.cnae_id == cnae_id,
            Ybio.cbo_id_len == 4,
            Ybio.bra_id == bra_id,
            Ybio.year == ybio_max_year_bra_id
            ).order_by(desc(Ybio.wage_avg)).limit(1).values(Ybio.cbo_id, Ybio.wage_avg)  

      
        for cbo_id, wage_avg in occ_wage_avg_generate : 
            industry['occupation_max_monthly_income_value'] = wage_avg
            industry['occupation_max_monthly_income_name'] = dic_names_cbo[cbo_id][1]         
            
            
        if len(bra_id) != 9 :

            county_jobs_generate = Ybi.query.filter(
                Ybi.cnae_id == cnae_id,
                Ybi.bra_id_len == 9,
                Ybi.bra_id.like(bra_id+'%'), 
                Ybi.year == ybi_max_year_bra_id     
                ).order_by(desc(Ybi.num_jobs)).limit(1).values(Ybi.bra_id, Ybi.num_jobs)
            
            for id, num_jobs in county_jobs_generate : 
                industry['county_max_number_jobs_value'] = num_jobs
                industry['county_max_number_jobs_name'] = dic_names_bra[id][1]

            county_wage_avg_generate = Ybi.query.filter(
                Ybi.cnae_id == cnae_id,
                Ybi.bra_id_len == 9,
                Ybi.bra_id.like(bra_id+'%'),
                Ybi.year == 2013 
                ).order_by(desc(Ybi.wage_avg)).limit(1).values(Ybi.bra_id, Ybi.wage_avg)
            

            for id, wage_avg in county_wage_avg_generate : 
                industry['county_max_monthly_income_value'] = wage_avg
                industry['county_max_monthly_income_name'] = dic_names_bra[id][1]           



    return render_template('industry/index.html', body_class='perfil-estado', industry=industry)





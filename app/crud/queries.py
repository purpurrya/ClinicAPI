from sqlalchemy.orm import Session
from sqlalchemy import func, case, and_, distinct, literal_column, over, cast, Integer, Float, select
from app.models import (
    Analysis,
    Clients,
    ClientsContraindications,
    Contraindications,
    Doctors,
    DoctorsSalary,
    Hospital,
    Payments,
    PrescribedAnalysis,
    Procedures,
    ProceduresContraindications,
    ProceduresSupplies,
    Staff,
    VisitsHistory,
    Wards
)


def top_5_doctors_revenue(db: Session):
    stmt = select(
        VisitsHistory.doctor_id,
        Doctors.name,
        func.sum(VisitsHistory.price).label('total_revenue')
    ).join(Doctors, VisitsHistory.doctor_id == Doctors.id)
    stmt = stmt.group_by(VisitsHistory.doctor_id, Doctors.name)
    stmt = stmt.order_by(func.sum(VisitsHistory.price).desc()).limit(5)
    result = db.execute(stmt).all()
    return [dict(zip(["doctor_id", "name", "total_revenue"], row)) for row in result]

def avg_stay_by_ward(db: Session):
    stmt = select(
        Wards.id.label('ward_id'),
        Wards.category,
        func.avg(func.julianday(Hospital.discharge_date) - func.julianday(Hospital.receipt_date)).label('avg_stay_days')
    ).join(Hospital, Hospital.ward_id == Wards.id)
    stmt = stmt.where(Hospital.discharge_date.isnot(None))
    stmt = stmt.group_by(Wards.id, Wards.category)
    result = db.execute(stmt).all()
    return [dict(zip(["ward_id", "category", "avg_stay_days"], row)) for row in result]

def clients_with_procedure_and_contra(db: Session):
    stmt = select(
        Clients.id.label('client_id'),
        Clients.name,
        Procedures.id.label('procedure_id'),
        Procedures.name.label('procedure_name'),
        Contraindications.name.label('contraindication')
    ).distinct()
    stmt = stmt.join(ClientsContraindications, Clients.id == ClientsContraindications.client_id)
    stmt = stmt.join(Contraindications, ClientsContraindications.contraindication_code == Contraindications.code)
    stmt = stmt.join(VisitsHistory, Clients.id == VisitsHistory.client_id)
    stmt = stmt.join(Procedures, VisitsHistory.procedure_id == Procedures.id)
    stmt = stmt.join(
        ProceduresContraindications,
        and_(
            Procedures.id == ProceduresContraindications.procedure_id,
            ProceduresContraindications.contraindication_code == ClientsContraindications.contraindication_code
        )
    )
    result = db.execute(stmt).all()
    return [dict(zip(["client_id", "name", "procedure_id", "procedure_name", "contraindication"], row)) for row in result]

def supplies_count_by_procedure(db: Session):
    stmt = select(
        Procedures.id.label('procedure_id'),
        Procedures.name.label('procedure_name'),
        func.count(ProceduresSupplies.supply_id).label('total_supplies_used')
    ).join(ProceduresSupplies, Procedures.id == ProceduresSupplies.procedure_id)
    stmt = stmt.group_by(Procedures.id, Procedures.name)
    stmt = stmt.order_by(func.count(ProceduresSupplies.supply_id).desc())
    result = db.execute(stmt).all()
    return [dict(zip(["procedure_id", "procedure_name", "total_supplies_used"], row)) for row in result]

def cumulative_revenue(db: Session):
    stmt = select(
        Payments.date_of_payment.label('payment_date'),
        func.sum(Payments.sum).over(order_by=Payments.date_of_payment).label('cumulative_revenue')
    ).order_by(Payments.date_of_payment)
    result = db.execute(stmt).all()
    return [dict(zip(["payment_date", "cumulative_revenue"], row)) for row in result]

def clients_with_analysis_no_payment(db: Session):
    stmt = select(
        Clients.id.label('client_id'),
        Clients.name
    ).distinct()
    stmt = stmt.join(PrescribedAnalysis, Clients.id == PrescribedAnalysis.client_id)
    stmt = stmt.outerjoin(Payments, 
                          and_(
                              Payments.client_id == Clients.id,
                              Payments.analysis_id == PrescribedAnalysis.analysis_id
                          ))
    stmt = stmt.where(Payments.id.is_(None))
    result = db.execute(stmt).all()
    return [dict(zip(["client_id", "name"], row)) for row in result]

def staff_salary_categorized(db: Session):
    salary = Staff.salary_per_hour * Staff.hours_worked * (1 + Staff.additional_payment)
    level = case(
        (salary >= 100000, 'Высокая'),
        (salary >= 50000, 'Средняя'),
        else_='Низкая'
    )
    stmt = select(Staff.name, Staff.post, salary.label('salary'), level.label('salary_level')).order_by(salary.desc())
    result = db.execute(stmt).all()
    return [dict(zip(["name", "post", "salary", "salary_level"], row)) for row in result]

def clients_glucose_level(db: Session):
    stmt = select(
        PrescribedAnalysis.client_id,
        Clients.name,
        func.json_extract(PrescribedAnalysis.results, '$.biochemistry_results.glucose').label('glucose_level')
    ).join(Clients, PrescribedAnalysis.client_id == Clients.id)
    stmt = stmt.where(func.json_extract(PrescribedAnalysis.results, '$.biochemistry_results.glucose') > 5.0)
    result = db.execute(stmt).all()
    return [dict(zip(["client_id", "name", "glucose_level"], row)) for row in result]

def top_10_procedures_by_visits(db: Session):
    stmt = select(
        Procedures.name.label('procedure_name'),
        func.count(VisitsHistory.procedure_id).label('times_assigned')
    ).join(VisitsHistory, Procedures.id == VisitsHistory.procedure_id)
    stmt = stmt.group_by(Procedures.id, Procedures.name).order_by(func.count().desc()).limit(10)
    result = db.execute(stmt).all()
    return [dict(zip(["procedure_name", "times_assigned"], row)) for row in result]

def top_doctors_by_analysis(db: Session):
    lv = select(
        VisitsHistory.client_id,
        VisitsHistory.doctor_id,
        func.max(func.concat(VisitsHistory.date, ' ', VisitsHistory.time)).label('last_visit')
    ).group_by(VisitsHistory.client_id).subquery()
    stmt = select(
        Doctors.id.label('doctor_id'),
        Doctors.name,
        func.count(PrescribedAnalysis.analysis_id).label('total_analysis_prescribed')
    ).join(lv, PrescribedAnalysis.client_id == lv.c.client_id).join(Doctors, lv.c.doctor_id == Doctors.id)
    stmt = stmt.group_by(Doctors.id, Doctors.name).order_by(func.count().desc())
    result = db.execute(stmt).all()
    return [dict(zip(["doctor_id", "name", "total_analysis_prescribed"], row)) for row in result]

def frequent_clients_last_3_months(db: Session):
    cutoff = func.date('now', '-3 month')
    stmt = select(
        Clients.id.label('client_id'),
        Clients.name,
        func.count(VisitsHistory.client_id).label('visits_count')
    ).join(VisitsHistory, Clients.id == VisitsHistory.client_id)
    stmt = stmt.where(VisitsHistory.date >= cutoff)
    stmt = stmt.group_by(Clients.id, Clients.name).having(func.count() >= 2)
    result = db.execute(stmt).all()
    return [dict(zip(["client_id", "name", "visits_count"], row)) for row in result]

def appointments_per_doctor(db: Session):
    stmt = select(
        Doctors.id.label('doctor_id'),
        Doctors.name,
        func.count(VisitsHistory.doctor_id).label('total_appointments')
    ).join(VisitsHistory, Doctors.id == VisitsHistory.doctor_id)
    stmt = stmt.group_by(Doctors.id).order_by(func.count().desc())
    result = db.execute(stmt).all()
    return [dict(zip(["doctor_id", "name", "total_appointments"], row)) for row in result]

def procedures_with_contra_clients(db: Session):
    stmt = select(
        Procedures.id,
        Procedures.name.label('procedure_name'),
        func.count(distinct(ClientsContraindications.client_id)).label('clients_with_contra')
    ).join(ProceduresContraindications, Procedures.id == ProceduresContraindications.procedure_id)
    stmt = stmt.join(ClientsContraindications, ProceduresContraindications.contraindication_code == ClientsContraindications.contraindication_code)
    stmt = stmt.group_by(Procedures.id).having(func.count(distinct(ClientsContraindications.client_id)) > 10)
    result = db.execute(stmt).all()
    return [dict(zip(["procedure_id", "procedure_name", "clients_with_contra"], row)) for row in result]

def top_3_procedures_by_avg_payment(db: Session):
    stmt = select(
        Procedures.name.label('procedure_name'),
        func.avg(Payments.sum).label('avg_price')
    ).join(VisitsHistory, Procedures.id == VisitsHistory.procedure_id)
    stmt = stmt.join(Payments, and_(Payments.client_id == VisitsHistory.client_id, Payments.procedure_id == VisitsHistory.procedure_id))
    stmt = stmt.group_by(Procedures.id).order_by(func.avg(Payments.sum).desc()).limit(3)
    result = db.execute(stmt).all()
    return [dict(zip(["procedure_name", "avg_price"], row)) for row in result]

def repeat_procedure_clients(db: Session):
    stmt = select(
        Clients.name.label('client_name'),
        Procedures.name.label('procedure_name'),
        func.count().label('times_done')
    ).join(VisitsHistory, VisitsHistory.client_id == Clients.id)
    stmt = stmt.join(Procedures, VisitsHistory.procedure_id == Procedures.id)
    stmt = stmt.group_by(Clients.id, Procedures.id).having(func.count() >= 2).order_by(func.count().desc())
    result = db.execute(stmt).all()
    return [dict(zip(["client_name", "procedure_name", "times_done"], row)) for row in result]

def contraindications_stats(db: Session):
    stmt = select(
        Contraindications.name,
        func.count(ClientsContraindications.client_id).label('total_clients')
    ).outerjoin(ClientsContraindications, Contraindications.code == ClientsContraindications.contraindication_code)
    stmt = stmt.group_by(Contraindications.code, Contraindications.name).order_by(func.count().desc())
    result = db.execute(stmt).all()
    return [dict(zip(["name", "total_clients"], row)) for row in result]

def doctors_unique_clients(db: Session):
    stmt = select(
        Doctors.id.label('doctor_id'),
        Doctors.name,
        func.count(distinct(VisitsHistory.client_id)).label('unique_clients')
    ).join(VisitsHistory, Doctors.id == VisitsHistory.doctor_id)
    stmt = stmt.group_by(Doctors.id).order_by(func.count(distinct(VisitsHistory.client_id)).desc())
    result = db.execute(stmt).all()
    return [dict(zip(["doctor_id", "name", "unique_clients"], row)) for row in result]

def inactive_clients_2_months(db: Session):
    cutoff = func.date('now', '-2 months')
    stmt = select(
        Clients.id.label('client_id'),
        Clients.name,
        func.max(VisitsHistory.date).label('last_visit')
    ).join(VisitsHistory, Clients.id == VisitsHistory.client_id)
    stmt = stmt.group_by(Clients.id).having(func.max(VisitsHistory.date) < cutoff)
    result = db.execute(stmt).all()
    return [dict(zip(["client_id", "name", "last_visit"], row)) for row in result]

def paid_unpaid_procedures_count(db: Session):
    stmt = select(
        Procedures.name.label('procedure'),
        func.count(case((and_(Payments.status == True, Payments.sum > 0), 1))).label('payed'),
        func.count(case((and_(Payments.status == False, Payments.sum > 0), 1))).label('not_payed')
    ).join(Procedures, Procedures.id == Payments.procedure_id)
    stmt = stmt.group_by(Procedures.id).order_by(literal_column('payed').desc())
    result = db.execute(stmt).all()
    return [dict(zip(["procedure", "payed", "not_payed"], row)) for row in result]

def avg_procedure_cost_per_doctor(db: Session):
    stmt = select(
        Doctors.name.label('doctor_name'),
        func.avg(Payments.sum).label('avg_procedure_cost')
    ).join(VisitsHistory, Doctors.id == VisitsHistory.doctor_id)
    stmt = stmt.join(Payments, and_(Payments.client_id == VisitsHistory.client_id, Payments.procedure_id == VisitsHistory.procedure_id))
    stmt = stmt.group_by(Doctors.id).order_by(func.avg(Payments.sum).desc())
    result = db.execute(stmt).all()
    return [dict(zip(["doctor_name", "avg_procedure_cost"], row)) for row in result]

def one_visit_clients(db: Session):
    stmt = select(
        Clients.id.label('client_id'),
        Clients.name,
        func.count(VisitsHistory.client_id).label('total_visits')
    ).outerjoin(VisitsHistory, Clients.id == VisitsHistory.client_id)
    stmt = stmt.group_by(Clients.id).having(func.count() == 1)
    result = db.execute(stmt).all()
    return [dict(zip(["client_id", "name", "total_visits"], row)) for row in result]

def monthly_new_clients_growth(db: Session):
    first_visits = select(
        VisitsHistory.client_id,
        func.min(VisitsHistory.date).label('first_visit')
    ).group_by(VisitsHistory.client_id).subquery()
    stmt = select(
        func.strftime('%Y-%m', first_visits.c.first_visit).label('cohort_month'),
        func.count().label('new_clients')
    ).group_by(literal_column('cohort_month')).order_by(literal_column('cohort_month'))
    result = db.execute(stmt).all()
    return [dict(zip(["cohort_month", "new_clients"], row)) for row in result]

def avg_payment_by_weekday(db: Session):
    stmt = select(
        func.strftime('%w', Payments.date_of_payment).label('weekday'),
        func.round(func.avg(Payments.sum), 2).label('avg_payment')
    ).group_by('weekday').order_by('weekday')
    result = db.execute(stmt).all()
    return [dict(zip(["weekday", "avg_payment"], row)) for row in result]

def busiest_hours(db: Session):
    stmt = select(
        func.cast(func.strftime('%H', VisitsHistory.time), Integer).label('hour'),
        func.count().label('cnt')
    ).group_by('hour').order_by(func.count().desc())
    result = db.execute(stmt).all()
    return [dict(zip(["hour", "cnt"], row)) for row in result]

def payment_method_distribution(db: Session):
    stmt = select(
        Payments.payment_method,
        func.count().label('payments_count'),
        func.sum(Payments.sum).label('total_amount')
    ).group_by(Payments.payment_method).order_by(func.sum(Payments.sum).desc())
    result = db.execute(stmt).all()
    return [dict(zip(["payment_method", "payments_count", "total_amount"], row)) for row in result]

def high_avg_paying_clients(db: Session):
    client_avg = select(
        VisitsHistory.client_id,
        func.avg(Payments.sum).label('avg_paid')
    ).join(Payments, and_(VisitsHistory.client_id == Payments.client_id, VisitsHistory.procedure_id == Payments.procedure_id)).group_by(VisitsHistory.client_id).subquery()
    overall_avg = select(func.avg(Payments.sum).label('overall_avg')).scalar_subquery()
    stmt = select(
        client_avg.c.client_id,
        Clients.name,
        client_avg.c.avg_paid
    ).join(Clients, client_avg.c.client_id == Clients.id).where(client_avg.c.avg_paid > overall_avg).order_by(client_avg.c.avg_paid.desc())
    result = db.execute(stmt).all()
    return [dict(zip(["client_id", "name", "avg_paid"], row)) for row in result]

def doctors_salary_calculation(db: Session):
    base = DoctorsSalary.salary_per_hour * DoctorsSalary.hours_worked + DoctorsSalary.category_allowance + DoctorsSalary.bonus
    stmt = select(
        Doctors.name,
        (case(
            (DoctorsSalary.sponsored_merch_sold.between(0,30), base * 1.01),
            (DoctorsSalary.sponsored_merch_sold.between(31,70), base * 1.03),
            (DoctorsSalary.sponsored_merch_sold.between(71,100), base * 1.04),
            else_=base * 1.05
        )).label('final_salary')
    ).join(Doctors, DoctorsSalary.doctor_id == Doctors.id).order_by(literal_column('final_salary').desc())
    result = db.execute(stmt).all()
    return [dict(zip(["name", "final_salary"], row)) for row in result]

def top_3_most_profitable_procedures(db: Session):
    total_visits = func.count(VisitsHistory.procedure_id)
    total_profit = Procedures.price * total_visits
    stmt = select(
        Procedures.name.label('procedure'),
        Procedures.price,
        total_visits.label('total_visits'),
        total_profit.label('total_profit')
    ).join(VisitsHistory).group_by(Procedures.id, Procedures.price).order_by(total_profit.desc()).limit(3)
    result = db.execute(stmt).all()
    return [dict(zip(["procedure", "price", "total_visits", "total_profit"], row)) for row in result]

def top_5_procedures_assigned(db: Session):
    stmt = select(
        Procedures.name.label('procedure_name'),
        func.count(PrescribedAnalysis.procedure_id).label('times_assigned')
    ).join(PrescribedAnalysis, Procedures.id == PrescribedAnalysis.procedure_id)
    stmt = stmt.group_by(Procedures.id).order_by(func.count().desc()).limit(5)
    result = db.execute(stmt).all()
    return [dict(zip(["procedure_name", "times_assigned"], row)) for row in result]

def avg_days_between_visits(db: Session):
    client_visits = select(
        VisitsHistory.client_id,
        VisitsHistory.date.label('visit_date'),
        func.lag(VisitsHistory.date).over(
            partition_by=VisitsHistory.client_id,
            order_by=VisitsHistory.date
        ).label('prev_visit')
    ).subquery()
    intervals = select(
        (func.julianday(client_visits.c.visit_date) - func.julianday(client_visits.c.prev_visit)).label("interval")
    ).where(client_visits.c.prev_visit.isnot(None)).subquery()
    stmt = select(func.round(func.avg(intervals.c.interval), 2).label('avg_days_between_visits'))
    result = db.execute(stmt).scalar()
    return {"avg_days_between_visits": result}

def top_10_peak_days(db: Session):
    stmt = select(
        VisitsHistory.date.label('visit_date'),
        func.count().label('visits_count')
    ).group_by(VisitsHistory.date).order_by(func.count().desc()).limit(10)
    result = db.execute(stmt).all()
    return [dict(zip(["visit_date", "visits_count"], row)) for row in result]

def clients_with_contra_count(db: Session):
    stmt = select(
        Clients.id.label('client_id'),
        Clients.name,
        func.count(distinct(ClientsContraindications.contraindication_code)).label('contraindications_count')
    ).join(ClientsContraindications, Clients.id == ClientsContraindications.client_id)
    stmt = stmt.group_by(Clients.id).having(func.count(distinct(ClientsContraindications.contraindication_code)) > 0)
    result = db.execute(stmt).all()
    return [dict(zip(["client_id", "name", "contraindications_count"], row)) for row in result]

def clients_count_by_loyalty(db: Session):
    stmt = select(
        Clients.loyalty_card_category.label('category'),
        func.count().label('amount')
    ).group_by(Clients.loyalty_card_category)
    result = db.execute(stmt).all()
    return [dict(zip(["category", "amount"], row)) for row in result]

def doctors_revenue_ranking(db: Session):
    rank_stmt = func.rank().over(order_by=func.sum(Payments.sum).desc())
    stmt = select(
        Doctors.id.label('doctor_id'),
        Doctors.name,
        func.sum(Payments.sum).label('total_revenue'),
        rank_stmt.label('rank')
    ).join(VisitsHistory, Doctors.id == VisitsHistory.doctor_id)
    stmt = stmt.join(Payments, and_(Payments.client_id == VisitsHistory.client_id, Payments.procedure_id == VisitsHistory.procedure_id))
    stmt = stmt.group_by(Doctors.id, Doctors.name).order_by(func.sum(Payments.sum).desc())
    result = db.execute(stmt).all()
    return [dict(zip(["doctor_id", "name", "total_revenue", "rank"], row)) for row in result]

def clients_age_group_distribution(db: Session):
    age = func.strftime('%Y','now').cast(Integer) - func.strftime('%Y', Clients.date_of_birth).cast(Integer)
    stmt = select(
        case(
            (age < 18, 'До 18'),
            (age.between(18,35), '18–35'),
            (age.between(36,60), '36–60'),
            else_='60+'
        ).label('age_group'),
        func.count().label('clients_count')
    ).group_by('age_group').order_by(func.count().desc())
    result = db.execute(stmt).all()
    return [dict(zip(["age_group", "clients_count"], row)) for row in result]

def avg_rush_markup(db: Session):
    stmt = select(func.avg(Analysis.price_rush - Analysis.price).label('avg_rush_markup')).where(Analysis.price_rush.isnot(None))
    result = db.execute(stmt).scalar()
    return {"avg_rush_markup": result}

def monthly_revenue_trend(db: Session):
    stmt = select(
        func.strftime('%Y-%m', Payments.date_of_payment).label('month'),
        func.sum(Payments.sum).label('monthly_revenue')
    ).group_by('month').order_by('month')
    result = db.execute(stmt).all()
    return [dict(zip(["month", "monthly_revenue"], row)) for row in result]

def most_requested_procedures(db: Session):
    stmt = select(
        Procedures.name.label('procedure_name'),
        func.count(VisitsHistory.procedure_id).label('visits_count')
    ).join(VisitsHistory).group_by(Procedures.id).order_by(func.count().desc())
    result = db.execute(stmt).all()
    return [dict(zip(["procedure_name", "visits_count"], row)) for row in result]

def loyalty_null_clients_message(db: Session):
    stmt = select(
        Clients.name,
        Clients.phone_number,
        Clients.email,
        func.json_object(
            'message',
            func.concat(
                'Здравствуйте, ', Clients.name,
                '! Мы заметили, что у вас еще нет карты лояльности. Получите карту и получите скидку на следующие процедуры!'
            )
        ).label('message')
    ).where(Clients.loyalty_card_category.is_(None)).order_by(Clients.name)
    result = db.execute(stmt).all()
    return [dict(zip(["name", "phone_number", "email", "message"], row)) for row in result]

def monthly_doctor_revenue(db: Session):
    stmt = select(
        Doctors.id.label('doctor_id'),
        Doctors.name,
        func.strftime('%Y-%m', Payments.date_of_payment).label('month'),
        func.sum(Payments.sum).label('revenue')
    ).join(VisitsHistory, Doctors.id == VisitsHistory.doctor_id)
    stmt = stmt.join(Payments, and_(Payments.client_id == VisitsHistory.client_id, Payments.procedure_id == VisitsHistory.procedure_id))
    stmt = stmt.group_by(Doctors.id, 'month').order_by(Doctors.id, 'month')
    result = db.execute(stmt).all()
    return [dict(zip(["doctor_id", "name", "month", "revenue"], row)) for row in result]

def unique_procedures_per_client(db: Session):
    stmt = select(
        VisitsHistory.client_id,
        Clients.name,
        func.count(distinct(VisitsHistory.procedure_id)).label('unique_procedures')
    ).join(Clients, VisitsHistory.client_id == Clients.id)
    stmt = stmt.group_by(VisitsHistory.client_id, Clients.name).order_by(func.count(distinct(VisitsHistory.procedure_id)).desc())
    result = db.execute(stmt).all()
    return [dict(zip(["client_id", "name", "unique_procedures"], row)) for row in result]

def distinct_doctors_per_client(db: Session):
    stmt = select(
        VisitsHistory.client_id,
        Clients.name,
        func.count(distinct(VisitsHistory.doctor_id)).label('distinct_doctors')
    ).join(Clients, VisitsHistory.client_id == Clients.id)
    stmt = stmt.group_by(VisitsHistory.client_id, Clients.name).order_by(func.count(distinct(VisitsHistory.doctor_id)).desc())
    result = db.execute(stmt).all()
    return [dict(zip(["client_id", "name", "distinct_doctors"], row)) for row in result]

def visit_counts_per_client(db: Session):
    stmt = select(
        Clients.id,
        Clients.name,
        func.count(VisitsHistory.client_id).label('visit_count')
    ).outerjoin(VisitsHistory, Clients.id == VisitsHistory.client_id)
    stmt = stmt.group_by(Clients.id).order_by(func.count().desc())
    result = db.execute(stmt).all()
    return [dict(zip(["client_id", "name", "visit_count"], row)) for row in result]

def clients_for_specific_analysis(db: Session):
    stmt = select(
        Clients.id,
        Clients.name
    ).distinct().join(PrescribedAnalysis, Clients.id == PrescribedAnalysis.client_id)
    stmt = stmt.join(Analysis, PrescribedAnalysis.analysis_id == Analysis.id)
    stmt = stmt.where(Analysis.name == 'Общий анализ крови')
    result = db.execute(stmt).all()
    return [dict(zip(["client_id", "name"], row)) for row in result]

def repeat_visit_messages(db: Session):
    stmt = select(
        Clients.name.label('client_name'),
        Procedures.name.label('procedure_name'),
        Doctors.name.label('doctor_name'),
        func.concat(
            'Здравствуйте, ', Clients.name,
            '! Вам назначен повторный прием у врача по имени ', Doctors.name, '.'
        ).label('message')
    )
    stmt = stmt.select_from(VisitsHistory)
    stmt = stmt.join(Clients, VisitsHistory.client_id == Clients.id)
    stmt = stmt.join(Procedures, VisitsHistory.procedure_id == Procedures.id)
    stmt = stmt.join(Doctors, VisitsHistory.doctor_id == Doctors.id)
    stmt = stmt.where(VisitsHistory.doctors_report.like('%Необходима повторна%'))
    stmt = stmt.order_by(Clients.name)
    result = db.execute(stmt).all()
    return [dict(zip(["client_name", "procedure_name", "doctor_name", "message"], row)) for row in result]
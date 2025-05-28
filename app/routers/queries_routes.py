import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.encoders import jsonable_encoder
from app.database import SessionLocal
from app.models import Clients
from app.crud.queries import *

router = APIRouter(prefix="/api")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.get("/top_5_doctors_revenue", tags=["Doctors", "Financial"])
# def route_top_5_doctors_revenue(db: Session = Depends(get_db)):
#     return log_and_respond(top_5_doctors_revenue, db)

@router.get("/top_5_doctors_revenue", tags=["Doctors"])
def get_top_5_doctors_revenue(db: Session = Depends(get_db)):
    data = top_5_doctors_revenue(db)
    print("DEBUG:", data) 
    return data

@router.get("/avg_stay_by_ward", tags=["Operations"])
def route_avg_stay_by_ward(db: Session = Depends(get_db)):
    return log_and_respond(avg_stay_by_ward, db)

@router.get("/clients_with_procedure_and_contra", tags=["Clients", "Procedures"])
def route_clients_with_procedure_and_contra(db: Session = Depends(get_db)):
    return log_and_respond(clients_with_procedure_and_contra, db)

@router.get("/supplies_count_by_procedure", tags=["Procedures", "Operations"])
def route_supplies_count_by_procedure(db: Session = Depends(get_db)):
    return log_and_respond(supplies_count_by_procedure, db)

@router.get("/cumulative_revenue", tags=["Financial"])
def route_cumulative_revenue(db: Session = Depends(get_db)):
    return log_and_respond(cumulative_revenue, db)

@router.get("/clients_with_analysis_no_payment", tags=["Clients", "Financial"])
def route_clients_with_analysis_no_payment(db: Session = Depends(get_db)):
    return log_and_respond(clients_with_analysis_no_payment, db)

@router.get("/staff_salary_categorized", tags=["Operations"])
def route_staff_salary_categorized(db: Session = Depends(get_db)):
    return log_and_respond(staff_salary_categorized, db)

@router.get("/clients_glucose_level", tags=["Clients"])
def route_clients_glucose_level(db: Session = Depends(get_db)):
    return log_and_respond(clients_glucose_level, db)

@router.get("/top_10_procedures_by_visits", tags=["Procedures"])
def route_top_10_procedures_by_visits(db: Session = Depends(get_db)):
    return log_and_respond(top_10_procedures_by_visits, db)

@router.get("/top_doctors_by_analysis", tags=["Doctors"])
def route_top_doctors_by_analysis(db: Session = Depends(get_db)):
    return log_and_respond(top_doctors_by_analysis, db)

@router.get("/frequent_clients_last_3_months", tags=["Clients"])
def route_frequent_clients_last_3_months(db: Session = Depends(get_db)):
    return log_and_respond(frequent_clients_last_3_months, db)

@router.get("/appointments_per_doctor", tags=["Doctors"])
def route_appointments_per_doctor(db: Session = Depends(get_db)):
    return log_and_respond(appointments_per_doctor, db)

@router.get("/procedures_with_contra_clients", tags=["Procedures"])
def route_procedures_with_contra_clients(db: Session = Depends(get_db)):
    return log_and_respond(procedures_with_contra_clients, db)

@router.get("/top_3_procedures_by_avg_payment", tags=["Procedures", "Financial"])
def route_top_3_procedures_by_avg_payment(db: Session = Depends(get_db)):
    return log_and_respond(top_3_procedures_by_avg_payment, db)

@router.get("/repeat_procedure_clients", tags=["Clients", "Procedures"])
def route_repeat_procedure_clients(db: Session = Depends(get_db)):
    return log_and_respond(repeat_procedure_clients, db)

@router.get("/contraindications_stats", tags=["Operations"])
def route_contraindications_stats(db: Session = Depends(get_db)):
    return log_and_respond(contraindications_stats, db)

@router.get("/doctors_unique_clients", tags=["Doctors"])
def route_doctors_unique_clients(db: Session = Depends(get_db)):
    return log_and_respond(doctors_unique_clients, db)

@router.get("/inactive_clients_2_months", tags=["Clients"])
def route_inactive_clients_2_months(db: Session = Depends(get_db)):
    return log_and_respond(inactive_clients_2_months, db)

@router.get("/paid_unpaid_procedures_count", tags=["Procedures", "Financial"])
def route_paid_unpaid_procedures_count(db: Session = Depends(get_db)):
    return log_and_respond(paid_unpaid_procedures_count, db)

@router.get("/avg_procedure_cost_per_doctor", tags=["Doctors", "Financial"])
def route_avg_procedure_cost_per_doctor(db: Session = Depends(get_db)):
    return log_and_respond(avg_procedure_cost_per_doctor, db)

@router.get("/one_visit_clients", tags=["Clients"])
def route_one_visit_clients(db: Session = Depends(get_db)):
    return log_and_respond(one_visit_clients, db)

@router.get("/monthly_new_clients_growth", tags=["Clients"])
def route_monthly_new_clients_growth(db: Session = Depends(get_db)):
    return log_and_respond(monthly_new_clients_growth, db)

@router.get("/avg_payment_by_weekday", tags=["Financial"])
def route_avg_payment_by_weekday(db: Session = Depends(get_db)):
    return log_and_respond(avg_payment_by_weekday, db)

@router.get("/busiest_hours", tags=["Operations"])
def route_busiest_hours(db: Session = Depends(get_db)):
    return log_and_respond(busiest_hours, db)

@router.get("/payment_method_distribution", tags=["Financial"])
def route_payment_method_distribution(db: Session = Depends(get_db)):
    return log_and_respond(payment_method_distribution, db)

@router.get("/high_avg_paying_clients", tags=["Clients", "Financial"])
def route_high_avg_paying_clients(db: Session = Depends(get_db)):
    return log_and_respond(high_avg_paying_clients, db)

@router.get("/doctors_salary_calculation", tags=["Doctors", "Financial"])
def route_doctors_salary_calculation(db: Session = Depends(get_db)):
    return log_and_respond(doctors_salary_calculation, db)

@router.get("/top_3_most_profitable_procedures", tags=["Procedures", "Financial"])
def route_top_3_most_profitable_procedures(db: Session = Depends(get_db)):
    return log_and_respond(top_3_most_profitable_procedures, db)

@router.get("/top_5_procedures_assigned", tags=["Procedures"])
def route_top_5_procedures_assigned(db: Session = Depends(get_db)):
    return log_and_respond(top_5_procedures_assigned, db)

@router.get("/avg_days_between_visits", tags=["Clients"])
def route_avg_days_between_visits(db: Session = Depends(get_db)):
    return log_and_respond(avg_days_between_visits, db)

@router.get("/top_10_peak_days", tags=["Operations"])
def route_top_10_peak_days(db: Session = Depends(get_db)):
    return log_and_respond(top_10_peak_days, db)

@router.get("/clients_with_contra_count", tags=["Clients"])
def route_clients_with_contra_count(db: Session = Depends(get_db)):
    return log_and_respond(clients_with_contra_count, db)

@router.get("/clients_count_by_loyalty", tags=["Clients"])
def route_clients_count_by_loyalty(db: Session = Depends(get_db)):
    return log_and_respond(clients_count_by_loyalty, db)

@router.get("/doctors_revenue_ranking", tags=["Doctors", "Financial"])
def route_doctors_revenue_ranking(db: Session = Depends(get_db)):
    return log_and_respond(doctors_revenue_ranking, db)

@router.get("/clients_age_group_distribution", tags=["Clients"])
def route_clients_age_group_distribution(db: Session = Depends(get_db)):
    return log_and_respond(clients_age_group_distribution, db)

@router.get("/avg_rush_markup", tags=["Financial"])
def route_avg_rush_markup(db: Session = Depends(get_db)):
    return log_and_respond(avg_rush_markup, db)

@router.get("/monthly_revenue_trend", tags=["Financial"])
def route_monthly_revenue_trend(db: Session = Depends(get_db)):
    return log_and_respond(monthly_revenue_trend, db)

@router.get("/most_requested_procedures", tags=["Procedures"])
def route_most_requested_procedures(db: Session = Depends(get_db)):
    return log_and_respond(most_requested_procedures, db)

@router.get("/loyalty_null_clients_message", tags=["Clients"])
def route_loyalty_null_clients_message(db: Session = Depends(get_db)):
    return log_and_respond(loyalty_null_clients_message, db)

@router.get("/monthly_doctor_revenue", tags=["Doctors", "Financial"])
def route_monthly_doctor_revenue(db: Session = Depends(get_db)):
    return log_and_respond(monthly_doctor_revenue, db)

@router.get("/unique_procedures_per_client", tags=["Clients", "Procedures"])
def route_unique_procedures_per_client(db: Session = Depends(get_db)):
    return log_and_respond(unique_procedures_per_client, db)

@router.get("/distinct_doctors_per_client", tags=["Clients", "Doctors"])
def route_distinct_doctors_per_client(db: Session = Depends(get_db)):
    return log_and_respond(distinct_doctors_per_client, db)

@router.get("/visit_counts_per_client", tags=["Clients"])
def route_visit_counts_per_client(db: Session = Depends(get_db)):
    return log_and_respond(visit_counts_per_client, db)

@router.get("/clients_for_specific_analysis", tags=["Clients"])
def route_clients_for_specific_analysis(db: Session = Depends(get_db)):
    return log_and_respond(clients_for_specific_analysis, db)

@router.get("/repeat_visit_messages", tags=["Clients", "Operations"])
def route_repeat_visit_messages(db: Session = Depends(get_db)):
    return log_and_respond(repeat_visit_messages, db)

@router.get("/test")
def test(db: Session = Depends(get_db)):
    try:
        logger.info("Running test query for Clients")
        result = db.execute(select(Clients)).scalars().all()
        logger.info(f"Test query returned {len(result)} records")
        return jsonable_encoder(result)
    except Exception as e:
        logger.error(f"Test query failed: {e}", exc_info=True)
        return {"error": str(e)}

@router.get("/ping_db")
def ping_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        logger.info("Database ping successful")
        return {"status": "ok", "message": "Database connection successful"}
    except Exception as e:
        logger.error(f"Database ping failed: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}

@router.get("/current_db")
def current_db(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("PRAGMA database_list")).fetchall()
        logger.info(f"PRAGMA database_list result: {result}")
        main_db = next((row[2] for row in result if row[1] == 'main'), None)
        return {"current_database_file": main_db}
    except Exception as e:
        logger.error(f"Error executing PRAGMA database_list query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
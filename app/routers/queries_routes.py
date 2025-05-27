from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud.queries import (
    top_5_doctors_revenue,
    avg_stay_by_ward,
    clients_with_procedure_and_contra,
    supplies_count_by_procedure,
    cumulative_revenue,
    clients_with_analysis_no_payment,
    staff_salary_categorized,
    clients_glucose_level,
    top_10_procedures_by_visits,
    top_doctors_by_analysis,
    frequent_clients_last_3_months,
    appointments_per_doctor,
    procedures_with_contra_clients,
    top_3_procedures_by_avg_payment,
    repeat_procedure_clients,
    contraindications_stats,
    doctors_unique_clients,
    inactive_clients_2_months,
    paid_unpaid_procedures_count,
    avg_procedure_cost_per_doctor,
    one_visit_clients,
    monthly_new_clients_growth,
    avg_payment_by_weekday,
    busiest_hours,
    payment_method_distribution,
    high_avg_paying_clients,
    doctors_salary_calculation,
    top_3_most_profitable_procedures,
    top_5_procedures_assigned,
    avg_days_between_visits,
    top_10_peak_days,
    clients_with_contra_count,
    clients_count_by_loyalty,
    doctors_revenue_ranking,
    clients_age_group_distribution,
    avg_rush_markup,
    monthly_revenue_trend,
    most_requested_procedures,
    loyalty_null_clients_message,
    monthly_doctor_revenue,
    unique_procedures_per_client,
    distinct_doctors_per_client,
    visits_count_per_doctor,
    visit_counts_per_client,
    clients_for_specific_analysis,
    repeat_visit_messages
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/top5_doctors")
def read_top5_doctors(db: Session = Depends(get_db)):
    return top_5_doctors_revenue(db)

@router.get("/avg_stay_ward")
def read_avg_stay_ward(db: Session = Depends(get_db)):
    return avg_stay_by_ward(db)

@router.get("/clients_contra")
def read_clients_contra(db: Session = Depends(get_db)):
    return clients_with_procedure_and_contra(db)

@router.get("/supplies_count")
def read_supplies_count(db: Session = Depends(get_db)):
    return supplies_count_by_procedure(db)

@router.get("/cumulative_revenue")
def read_cumulative_revenue(db: Session = Depends(get_db)):
    return cumulative_revenue(db)

@router.get("/clients_no_payment")
def read_clients_no_payment(db: Session = Depends(get_db)):
    return clients_with_analysis_no_payment(db)

@router.get("/staff_salary")
def read_staff_salary(db: Session = Depends(get_db)):
    return staff_salary_categorized(db)

@router.get("/glucose_level")
def read_glucose_level(db: Session = Depends(get_db)):
    return clients_glucose_level(db)

@router.get("/top10_procedures")
def read_top10_procedures(db: Session = Depends(get_db)):
    return top_10_procedures_by_visits(db)

@router.get("/top_doctors_analysis")
def read_top_doctors_analysis(db: Session = Depends(get_db)):
    return top_doctors_by_analysis(db)

@router.get("/frequent_clients")
def read_frequent_clients(db: Session = Depends(get_db)):
    return frequent_clients_last_3_months(db)

@router.get("/appointments_per_doctor")
def read_appointments_per_doctor(db: Session = Depends(get_db)):
    return appointments_per_doctor(db)

@router.get("/procedures_with_contra")
def read_procedures_with_contra(db: Session = Depends(get_db)):
    return procedures_with_contra_clients(db)

@router.get("/top3_avg_payment")
def read_top3_avg_payment(db: Session = Depends(get_db)):
    return top_3_procedures_by_avg_payment(db)

@router.get("/repeat_clients")
def read_repeat_clients(db: Session = Depends(get_db)):
    return repeat_procedure_clients(db)

@router.get("/contra_stats")
def read_contra_stats(db: Session = Depends(get_db)):
    return contraindications_stats(db)

@router.get("/unique_clients")
def read_unique_clients(db: Session = Depends(get_db)):
    return doctors_unique_clients(db)

@router.get("/inactive_clients")
def read_inactive_clients(db: Session = Depends(get_db)):
    return inactive_clients_2_months(db)

@router.get("/paid_unpaid_count")
def read_paid_unpaid_count(db: Session = Depends(get_db)):
    return paid_unpaid_procedures_count(db)

@router.get("/avg_cost_doctor")
def read_avg_cost_doctor(db: Session = Depends(get_db)):
    return avg_procedure_cost_per_doctor(db)

@router.get("/one_visit_clients")
def read_one_visit_clients(db: Session = Depends(get_db)):
    return one_visit_clients(db)

@router.get("/new_clients_growth")
def read_new_clients_growth(db: Session = Depends(get_db)):
    return monthly_new_clients_growth(db)

@router.get("/avg_payment_weekday")
def read_avg_payment_weekday(db: Session = Depends(get_db)):
    return avg_payment_by_weekday(db)

@router.get("/busiest_hours")
def read_busiest_hours(db: Session = Depends(get_db)):
    return busiest_hours(db)

@router.get("/payment_distribution")
def read_payment_distribution(db: Session = Depends(get_db)):
    return payment_method_distribution(db)

@router.get("/high_avg_clients")
def read_high_avg_clients(db: Session = Depends(get_db)):
    return high_avg_paying_clients(db)

@router.get("/doctor_salary_calc")
def read_doctor_salary_calc(db: Session = Depends(get_db)):
    return doctors_salary_calculation(db)

@router.get("/top3_profit_procedures")
def read_top3_profit_procedures(db: Session = Depends(get_db)):
    return top_3_most_profitable_procedures(db)

@router.get("/top5_assigned")
def read_top5_assigned(db: Session = Depends(get_db)):
    return top_5_procedures_assigned(db)

@router.get("/avg_days_between_visits")
def read_avg_days_between_visits(db: Session = Depends(get_db)):
    return avg_days_between_visits(db)

@router.get("/top10_peak_days")
def read_top10_peak_days(db: Session = Depends(get_db)):
    return top_10_peak_days(db)

@router.get("/contra_count_clients")
def read_contra_count_clients(db: Session = Depends(get_db)):
    return clients_with_contra_count(db)

@router.get("/clients_by_loyalty")
def read_clients_by_loyalty(db: Session = Depends(get_db)):
    return clients_count_by_loyalty(db)

@router.get("/revenue_ranking")
def read_revenue_ranking(db: Session = Depends(get_db)):
    return doctors_revenue_ranking(db)

@router.get("/age_group_distribution")
def read_age_group_distribution(db: Session = Depends(get_db)):
    return clients_age_group_distribution(db)

@router.get("/avg_rush_markup")
def read_avg_rush_markup(db: Session = Depends(get_db)):
    return avg_rush_markup(db)

@router.get("/monthly_trend")
def read_monthly_trend(db: Session = Depends(get_db)):
    return monthly_revenue_trend(db)

@router.get("/most_requested")
def read_most_requested(db: Session = Depends(get_db)):
    return most_requested_procedures(db)

@router.get("/notify_loyalty")
def read_notify_loyalty(db: Session = Depends(get_db)):
    return loyalty_null_clients_message(db)

@router.get("/monthly_doctor_revenue")
def read_monthly_doctor_revenue(db: Session = Depends(get_db)):
    return monthly_doctor_revenue(db)

@router.get("/unique_procedures_client")
def read_unique_procedures_client(db: Session = Depends(get_db)):
    return unique_procedures_per_client(db)

@router.get("/distinct_doctors_client")
def read_distinct_doctors_client(db: Session = Depends(get_db)):
    return distinct_doctors_per_client(db)

@router.get("/visits_per_doctor")
def read_visits_per_doctor(db: Session = Depends(get_db)):
    return visits_count_per_doctor(db)

@router.get("/visits_per_client")
def read_visits_per_client(db: Session = Depends(get_db)):
    return visit_counts_per_client(db)

@router.get("/specific_analysis_clients")
def read_specific_analysis_clients(db: Session = Depends(get_db)):
    return clients_for_specific_analysis(db)

@router.get("/repeat_visit_messages")
def read_repeat_visit_messages(db: Session = Depends(get_db)):
    return repeat_visit_messages(db)
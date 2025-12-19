from data.process_raw_data import process_data


def generate_analysis() -> dict:
    """Generate the analysis for the equipment failures."""
    equipment_failures = process_data()

    # Question 1: How many equipment failures happened?
    print("Answering question 1...")
    q1_resultv1 = equipment_failures \
        .shape[0]

    q1_resultv2 = equipment_failures \
        .drop_duplicates(subset=["equipment_id", "timestamp"]) \
        .shape[0]
    
    q1_result = {
        "v1": q1_resultv1,
        "v2": q1_resultv2
    }

    # Question 2: Which piece of equipment had most failures?
    print("Answering question 2...")
    q2_result = equipment_failures \
        .drop_duplicates(subset=["equipment_id", "timestamp"]) \
        .groupby(["equipment_id", "equipment_name"]).size().rename("failures") \
        .sort_values(ascending=False) \
        .reset_index()

    q2_result["percentage"] = round(q2_result["failures"] / q2_result["failures"].sum() * 100, 2)
    q2_result["percentage"] = q2_result["percentage"].astype(str) + "%"

    # Question 3: Average failures per asset across equipment groups
    print("Answering question 3...")
    q3_result = equipment_failures \
        .groupby(["equipment_group", "equipment_id"])["timestamp"].nunique().rename("failures") \
        .reset_index()

    q3_result = q3_result \
        .groupby("equipment_group").agg(
            equipment_list=("equipment_id", lambda x: sorted(list(x))),
            avg_failures=("failures", "mean"),
            total_failures=("failures", "sum")
        ).sort_values(by="total_failures", ascending=True) \
        .reset_index()

    q3_result["percentage"] = round(q3_result["total_failures"] / q3_result["total_failures"].sum() * 100, 2)
    q3_result["percentage"] = q3_result["percentage"].astype(str) + "%"

    # Question 4: Rank sensors by failures per asset
    print("Answering question 4...")
    q4_result = equipment_failures \
        .groupby(["equipment_id", "equipment_name", "equipment_group", "sensor_id"]).size().rename("failures") \
        .reset_index() \
        .sort_values(by=["equipment_id", "failures"], ascending=[True, False]) \
        .groupby("equipment_id").head(3)

    return {
        "q1_result": q1_result,
        "q2_result": q2_result,
        "q3_result": q3_result,
        "q4_result": q4_result
    }

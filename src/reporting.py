def build_summary(df):
    if df.empty:
        return {"total": 0, "pending": 0, "high": 0, "resolved": 0}
    return {
        "total": int(len(df)),
        "pending": int((df["status"] == "Pending").sum()),
        "high": int((df["priority"] == "High").sum()),
        "resolved": int((df["status"] == "Resolved").sum())
    }

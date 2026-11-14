"""Fixed per-vital checklist questions. An LLM may rephrase these; it may not add or drop any."""

CHECKLISTS: dict[str, list[str]] = {
    "pulse": [
        "Any fever, chills, sore throat, cough or congestion in the last 48 hours?",
        "Any change in caffeine, hydration, sleep or medication since yesterday?",
        "Was the reading taken at rest, at the usual time?",
    ],
    "temp_c": [
        "Any chills, sweats, aches or sore throat in the last 48 hours?",
        "Was the reading taken at the usual time, before exercise and meals?",
        "Has the cabin or room felt warmer than usual?",
    ],
    "resp_rate": [
        "Any cough, shortness of breath or chest discomfort?",
        "Any nasal congestion or sore throat in the last 48 hours?",
        "Was the reading taken at rest?",
    ],
    "sbp": [
        "Any headache, dizziness or visual change today?",
        "Any change in salt intake, fluids or medication since yesterday?",
        "Was the reading taken at rest, with the usual cuff and position?",
    ],
    "dbp": [
        "Any headache, dizziness or visual change today?",
        "Any change in salt intake, fluids or medication since yesterday?",
        "Was the reading taken at rest, with the usual cuff and position?",
    ],
}

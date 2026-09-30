"""History model helper and re-exports."""
from app.models.recommendation import Plan

# Plan model serves both the recommendation representation and history logs.
# We expose Plan as HistoryEntry for semantic clarity where needed.
HistoryEntry = Plan

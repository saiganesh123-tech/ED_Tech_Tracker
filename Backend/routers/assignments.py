from fastapi import APIRouter, HTTPException

router = APIRouter()

# Mock database for assignments
assignments = []

@router.get("/assignments", tags=["Assignments"])
async def get_assignments():
    """
    Retrieve all assignments.
    """
    return {"assignments": assignments}

@router.post("/assignments", tags=["Assignments"])
async def create_assignment(assignment: dict):
    """
    Create a new assignment.
    """
    if not assignment.get("title") or not assignment.get("description"):
        raise HTTPException(status_code=400, detail="Title and description are required.")
    assignments.append(assignment)
    return {"message": "Assignment created successfully", "assignment": assignment}

@router.delete("/assignments/{assignment_id}", tags=["Assignments"])
async def delete_assignment(assignment_id: int):
    """
    Delete an assignment by ID.
    """
    if assignment_id < 0 or assignment_id >= len(assignments):
        raise HTTPException(status_code=404, detail="Assignment not found.")
    deleted_assignment = assignments.pop(assignment_id)
    return {"message": "Assignment deleted successfully", "assignment": deleted_assignment}
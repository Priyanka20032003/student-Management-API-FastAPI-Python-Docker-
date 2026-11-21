from fastapi import FastAPI,HTTPException, status
from pydantic import BaseModel, EmailStr,Field
from typing import Optional


app = FastAPI(
    title="student management api",
    description="student details"
)

class studentCreate(BaseModel):
    name:str=Field(min_length=2,max_length=50)
    age:int
    email:EmailStr
    dept:str
    fees:float

class student(studentCreate):
    id:int
    
students=[]
next_id=1

@app.get("/")
def Home():
    return {
        "message":"Student details"
    }
     
#create a student

@app.post(
    "/students",
    response_model=student,
    status_code=status.HTTP_201_CREATED
    )
def create_student(studentData:studentCreate):
    global next_id
    
    new_student=student(
        id=next_id,
        name=studentData.name,
        age=studentData.age,
        email=studentData.email,
        dept=studentData.dept,
        fees=studentData.fees
    )
    
    students.append(new_student)
    next_id +=1
    
    return new_student
    
    
@app.get(
    "/students",
    response_model=list[student],
    status_code=status.HTTP_200_OK
)
def get_students(
    dept:Optional[str]=None
):
    
    if dept:
        return [
            student
            for student in students
            if student.dept.lower()==dept.lower()
        ]
    return students


@app.get(
    "/students/{student_id}",
    response_model=student,
    status_code=status.HTTP_200_OK
)
def get_student_by_id(student_id:int):
    
    for student in students:
        if student.id==student_id:
            return student
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )


@app.put(
    "/students/{student_id}",
    response_model=student,
    status_code=status.HTTP_200_OK
)
def update_student(
    student_id:int,
    student_data:studentCreate
):
    
    for index,existing_student in enumerate(students):
        if existing_student.id==student_id:
            updated_studentData = student(
                id=student_id,
                name=student_data.name,
                age=student_data.age,
                email=student_data.email,
                dept=student_data.dept,
                fees=student_data.fees
            )
            
            students[index] = updated_studentData
            return updated_studentData
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Student not found"
    )
        
@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(student_id:int):
    
    for index,existing_student in enumerate(students):
        if existing_student.id==student_id:
            students.pop(index)
            
            return
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="student not found"
    )
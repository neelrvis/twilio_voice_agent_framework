from pydantic import BaseModel


class OpenDentalBookAppointmentRequest(BaseModel): 
    PatNum: int

class OpenDentalBookAppointmentResponse(BaseModel):
    

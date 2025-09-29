from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime, timezone
from configs.enums import ReportType

class Report(BaseModel):
    report_id : ObjectId
    report_type : ReportType
    report_title : str
    report_content : dict
    report_created_at : datetime = Field( default= datetime.now(timezone.utc) )

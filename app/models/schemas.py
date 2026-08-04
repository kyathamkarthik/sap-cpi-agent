from pydantic import BaseModel, Field

# What we receive from the SAP BTP logs
class FailedLogRequest(BaseModel):
    log_id: str = Field(..., description="Unique identifier for the failed SAP message log")
    integration_flow_name: str = Field(..., description="Name of the SAP iFlow that failed")
    error_message: str = Field(..., description="The raw error message from SAP CPI")
    raw_payload: str = Field(..., description="The broken XML or JSON payload")

# What we send back to the dashboard/SAP
class DiagnosticsResponse(BaseModel):
    log_id: str
    root_cause_explanation: str = Field(..., description="AI's explanation of the failure")
    corrected_payload: str = Field(..., description="The fixed XML/JSON ready for reprocessing")
    confidence_score: float = Field(..., description="AI's confidence in the fix (0.0 to 1.0)")
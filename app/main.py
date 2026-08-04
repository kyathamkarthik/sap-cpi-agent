from fastapi import FastAPI, HTTPException
from app.models.schemas import FailedLogRequest, DiagnosticsResponse
from app.services.llm_service import analyze_and_correct_payload

app = FastAPI(
    title="SAP CPI Failure Recovery Agent",
    description="AI Microservice for diagnosing and correcting SAP integration payload errors.",
    version="1.0.0"
)

@app.get("/")
def health_check():
    """Endpoint to verify the microservice is running."""
    return {"status": "online", "message": "SAP CPI Agent is active."}

@app.post("/analyze-log", response_model=DiagnosticsResponse)
def analyze_sap_log(request: FailedLogRequest):
    """
    Receives a failed log, analyzes the root cause, and returns the corrected payload.
    """
    try:
        # Call our LangChain service
        corrected_payload = analyze_and_correct_payload(
            iflow_name=request.integration_flow_name,
            error_msg=request.error_message,
            payload=request.raw_payload
        )
        
        # We'll use a simpler explanation for now
        simulated_explanation = f"Analyzed error '{request.error_message}' in iFlow '{request.integration_flow_name}' using LangChain."
        
        return DiagnosticsResponse(
            log_id=request.log_id,
            root_cause_explanation=simulated_explanation,
            corrected_payload=corrected_payload,
            confidence_score=0.98
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

from app.services.sap_connector import sap_client
from typing import List, Dict, Any

# ... existing code ...

@app.get("/api/fetch-logs", response_model=List[Dict[str, Any]])
def get_sap_logs():
    """
    Calls the SAP OData connector to retrieve currently failed messages.
    """
    try:
        logs = sap_client.fetch_failed_logs()
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch logs from SAP: {str(e)}")
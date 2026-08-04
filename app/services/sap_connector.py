import time
from datetime import datetime, timedelta

class SAPCPIMockConnector:
    """
    Simulates the SAP BTP Integration Suite OData API.
    Endpoint Simulated: /api/v1/MessageProcessingLogs
    """
    def __init__(self, tenant_url: str = "https://mock-tenant.cpi.ondemand.com"):
        self.tenant_url = tenant_url

    def fetch_failed_logs(self):
        """
        Simulates a GET request to SAP CPI with filter: $filter=Status eq 'FAILED'
        """
        # Simulating network latency
        time.sleep(0.5)
        
        # Dynamic timestamps for realism
        now = datetime.now()
        
        # This matches the exact nested JSON structure SAP's OData API returns
        mock_odata_response = {
            "d": {
                "results": [
                    {
                        "MessageGuid": "LOG_99812",
                        "IntegrationFlowName": "Inbound_Order_Processing",
                        "Status": "FAILED",
                        "LogStart": (now - timedelta(minutes=45)).isoformat(),
                        "ErrorMessage": "XML Parsing Error: Missing required closing tag </Quantity> and invalid date format in OrderDate field.",
                        "Payload": "<Order><Header><OrderID>100234</OrderID><OrderDate>31/12/2026</OrderDate></Header><Item><MaterialID>MAT-901</MaterialID><Quantity>500</Item></Order>"
                    },
                    {
                        "MessageGuid": "LOG_99813",
                        "IntegrationFlowName": "Employee_Master_Sync",
                        "Status": "FAILED",
                        "LogStart": (now - timedelta(minutes=12)).isoformat(),
                        "ErrorMessage": "JSON Schema Validation Failed: 'department' field is required but missing.",
                        "Payload": '{\n  "employeeId": "EMP-4592",\n  "firstName": "John",\n  "lastName": "Doe",\n  "status": "ACTIVE"\n}'
                    }
                ]
            }
        }
        
        # Map the heavy OData structure to our clean Pydantic schema
        formatted_logs = []
        for item in mock_odata_response["d"]["results"]:
            formatted_logs.append({
                "log_id": item["MessageGuid"],
                "integration_flow_name": item["IntegrationFlowName"],
                "error_message": item["ErrorMessage"],
                "raw_payload": item["Payload"]
            })
            
        return formatted_logs

    def retrigger_message(self, log_id: str, corrected_payload: str):
        """
        Simulates a POST request to re-inject the corrected payload back into the iFlow HTTP endpoint.
        """
        # In production, this uses the `requests` library to POST the fixed payload
        time.sleep(1) # Simulate network call
        
        return {
            "status": "success",
            "message": f"Payload for {log_id} successfully re-triggered in SAP CPI.",
            "http_code": 202
        }

# Instantiate a global connector for the app to use
sap_client = SAPCPIMockConnector()
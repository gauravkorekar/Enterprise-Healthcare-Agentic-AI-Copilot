from mcp.server.fastmcp import FastMCP #FastMCP is a framework that helps create MCP servers.

from Backend.MCP.tools import (
    Search_patients,
    Get_patient_history,
    Get_lab_results,
    Get_payment_summary
)

mcp = FastMCP("MediAssist MCP Server") #Creates an MCP server object.

#@mcp.tool() tells MCP: Register this function as a Tool so it can be available to AI agents
@mcp.tool()
def search_patients(patient_name: str):
    """Search patient by name or patient code."""
    return Search_patients(patient_name)


@mcp.tool()
def get_patient_history(patient_id: int):
    """Get admission and prescription history for a patient."""
    return Get_patient_history(patient_id)


@mcp.tool()
def get_lab_results(patient_id: int):
    """Get lab results for a patient."""
    return Get_lab_results(patient_id)


@mcp.tool()
def get_payment_summary(patient_id: int):
    """Get billing and payment summary for a patient."""
    return Get_payment_summary(patient_id)


if __name__ == "__main__":
    print("MCP Server Started...")
    print("Waiting for client requests...")
    mcp.run()
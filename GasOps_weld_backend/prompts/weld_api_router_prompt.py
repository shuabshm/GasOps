# def get_api_router_prompt(user_input):
#     """
#     API Router prompt - unchanged but focused on getting complete data
#     """
#     return f"""
# You are an API Router. Analyze the user query and call the appropriate API(s) to fetch data.

# User Query: {user_input}

# Available APIs:

# ## GetWorkOrderInformation
# **Purpose**: Get transmission work order data
# **Parameters** (all optional):
# - WorkOrderNumber: string
# - WorkOrderStatusDescription: string ("In Progress", "Completed", "Open")
# - ProjectNumber: string
# - Region: string
# - Crew: string ("Company", "Contractor")
# - ContractorName: string
# - SupervisorName: string
# - EngineerName: string
# - IsRedig: boolean
# - ContractorCWIName: string
# - ContractorNDEName: string
# - ContractorCRIName: string
# - CreatedOnDate: string (MM/dd/yyyy)

# **Response**: Returns array of work order objects with fields like TransmissionWorkOrderID, WorkOrderNumber, WorkOrderStatusDescription, ProjectNumber, RegionName, etc.

# Call the appropriate API(s) based on the user's query. Use no parameters to get all data, or specific parameters to filter.
# """







# def get_api_router_prompt(user_input):
#     """
#     API Router prompt - unchanged but focused on getting complete data
#     """
#     return f"""
# You are an API Router. Analyze the user query and call the appropriate API(s) to fetch data with the filters as parameters accordingly.

# User Query: {user_input}

# Available APIs:

# ## GetWorkOrderInformation
# **Purpose**: Get transmission work order data
# **Parameters** (all optional):
# - WorkOrderNumber: string
# - WorkOrderStatusDescription: string ("In Progress", "Completed", "Open")
# - ProjectNumber: string
# - Region: string
# - Crew: string ("Company", "Contractor")
# - ContractorName: string
# - SupervisorName: string
# - EngineerName: string
# - IsRedig: boolean
# - ContractorCWIName: string
# - ContractorNDEName: string
# - ContractorCRIName: string
# - CreatedOnDate: string (MM/dd/yyyy)

# **Response**: Returns array of work order objects with fields like TransmissionWorkOrderID, WorkOrderNumber, WorkOrderStatusDescription, ProjectNumber, RegionName, etc.

# Call the appropriate API(s) based on the user's query. Use no parameters to get all data, or specific parameters to filter.
# """






def get_api_router_prompt(user_input: str) -> str:
    """
    API Router prompt.
    - Always analyze the user query.
    - Select the most relevant API(s).
    - Return the API call in structured JSON format:
        {
          "api": "<API_NAME>",
          "parameters": { ... }
        }
      or if multiple APIs are required:
        [
          { "api": "<API_1>", "parameters": { ... } },
          { "api": "<API_2>", "parameters": { ... } }
        ]
    - If the user provides no filters, call the API with no parameters to fetch all data.
    - If a requested field is not supported by any API, state clearly: 
      "No API available for <field>."
    """

    return f"""
You are an API Router. Analyze the user query and call the appropriate API(s) to fetch data with the filters as parameters accordingly.

User Query: {user_input}

Available APIs:

## GetWorkOrderInformation
**Purpose**: This endpoint allows clients to search and filter transmission work orders using a set of optional parameters. 
            If no parameters are provided, all work orders will be returned.
**Parameters** (all optional):
- WorkOrderNumber: string
- WorkOrderStatusDescription: string ("In Progress", "Completed", "Open")
- ProjectNumber: string
- Region: string
- Crew: string ("Company", "Contractor")
- ContractorName: string("Bond", "CAC", "MFM", :Network", "Danella",etc.)
- SupervisorName: string
- EngineerName: string
- IsRedig: boolean
- ContractorCWIName: string
- ContractorNDEName: string
- ContractorCRIName: string
- CreatedOnDate: string (MM/dd/yyyy)

**Response**: Array of work order objects with fields like:
TransmissionWorkOrderID, WorkOrderNumber, WorkOrderStatusDescription, ProjectNumber, RegionName, etc.

**Filter Logic**:
1. Extract filters from the user query that match the parameters above.
2. Apply multiple filters using AND logic.
Example: *"Show completed work orders in Region East by Hsu, Kelly"* →
   ```json
   {{
     "WorkOrderStatusDescription": "Completed",
     "Region": "East",
     "SupervisorName": "Hsu, Kelly"
   }}
3. *Criteria for filtering on names:* If filtering on names and the field is clear, default to SupervisorName if no other name field is specified.
4. If the user query is ambiguous (e.g., only mentions a name, location, or field that could map to multiple parameters), ask a clarifying question before proceeding.
Never assume a mapping when ambiguity exists. Always confirm with the user first if the mapping is not clear.

Once clarified, generate the filter JSON as per the confirmed field(s).
---

---

Instructions:
# Call the appropriate API(s) based on the user's query. Use no parameters to get all data, or specific parameters to filter.
"""

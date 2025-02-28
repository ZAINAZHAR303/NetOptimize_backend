from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Google API Key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Missing Google API Key. Set the GOOGLE_API_KEY environment variable.")

# Initialize ChatGoogleGenerativeAI model
chat_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY
)

# Define request body models
class PolicyAnalysisRequest(BaseModel):
    country: str
    policy_text: str

class NetworkDesignRequest(BaseModel):
    region: str
    terrain_data: str
    existing_infrastructure: list[str]
    budget: int

class ResourceOptimizationRequest(BaseModel):
    region: str
    existing_assets: list[str]
    user_demand: str
    budget: int

# Route for Policy & Regulation Analysis
from fastapi import HTTPException
import logging

logging.basicConfig(level=logging.DEBUG)  # Enable debug logging

@app.post("/analyze_policy/")
async def analyze_policy(request: PolicyAnalysisRequest):
    try:
        # Include system instructions in the prompt
        prompt = f"""
        You are an AI expert in telecom policies. Provide a concise summary, risk assessment, and recommendations in JSON format.
        Summarize the following telecom policy in {request.country}. Identify compliance risks and provide actionable recommendations: {request.policy_text}
        """
        
        # Only use HumanMessage
        response = chat_model([
            HumanMessage(content=prompt)
        ])
        
        return response.content
    except Exception as e:
        logging.error(f"Error in analyze_policy: {e}", exc_info=True)  # Log the full exception
        raise HTTPException(status_code=500, detail=str(e))
    
# Route for Network Design Optimization
@app.post("/optimize_network/")
async def optimize_network(request: NetworkDesignRequest):
    # Include system instructions in the prompt
    prompt = f"""
    You are an AI specializing in network optimization. Provide a structured network plan, cost estimate, and coverage percentage in JSON format.
    Optimize network design for {request.region} with terrain: {request.terrain_data}. Infrastructure: {request.existing_infrastructure}. Budget: ${request.budget}.
    """
    
    # Only use HumanMessage
    response = chat_model([
        HumanMessage(content=prompt)
    ])
    
    return response.content

@app.post("/resource_allocation/")
async def resource_allocation(request: ResourceOptimizationRequest):
    # Include system instructions in the prompt
    prompt = f"""
    You are an AI expert in telecom resource management. Provide underutilized assets, suggested allocation, and cost savings in JSON format.
    Optimize resource allocation in {request.region}. Existing assets: {request.existing_assets}. User demand: {request.user_demand}. Budget: ${request.budget}.
    """
    
    # Only use HumanMessage
    response = chat_model([
        HumanMessage(content=prompt)
    ])
    
    return response.content

# Root Endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to NetOptimize AI Backend!"}

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from .logic import intake, decision_engine, guardrails, builder, gate
from .logic.utils import write_json
from . import llm

app = FastAPI(title='DevX Gateway MCP', version='0.1.0')

class DiscoverReq(BaseModel):
    workspaceRoot: str
    globs: Optional[List[str]] = None
class AnalyzeReq(BaseModel):
    oasPath: str
    useAI: bool = True
    model: Optional[str] = None
class DecideReq(BaseModel):
    traits: Dict[str, Any]
    useAI: bool = True
    model: Optional[str] = None
class ControlsReq(BaseModel):
    traits: Dict[str, Any]
    useAI: bool = True
    model: Optional[str] = None
class BundleReq(BaseModel):
    oasPath: str
    decision: Dict[str, Any]
    plan: Dict[str, Any]
    outDir: str = '.out'
class GateReq(BaseModel):
    plan: Dict[str, Any]
    appliedControls: List[str]
class AssistantReq(BaseModel):
    oasPath: str
    outDir: str = '.out'
    useAI: bool = True
    model: Optional[str] = None

@app.post('/tools/discover_oas')
def discover_oas(req: DiscoverReq):
    return intake.discover_oas(req.workspaceRoot, req.globs)

@app.post('/tools/analyze_oas')
def analyze_oas(req: AnalyzeReq):
    spec=intake.load_oas(req.oasPath)
    traits=intake.extract_traits(spec)
    if req.useAI: traits=llm.merge_llm_traits(spec, traits, model=req.model)
    return traits

@app.post('/tools/decide_gateway')
def decide_gateway(req: DecideReq):
    return decision_engine.decide(req.traits, model=req.model if req.useAI else None)

@app.post('/tools/synthesize_guardrails')
def synthesize_guardrails(req: ControlsReq):
    return guardrails.plan_from_traits(req.traits, use_llm=req.useAI, model=req.model)

@app.post('/tools/generate_bundle')
def generate_bundle(req: BundleReq):
    spec=intake.load_oas(req.oasPath)
    return builder.generate_bundle(spec, req.plan, req.outDir, req.decision)

@app.post('/tools/opa_gate')
def opa_gate(req: GateReq):
    return gate.evaluate(req.plan, req.appliedControls)

@app.post('/tools/run_gateway_assistant')
def run_gateway_assistant(req: AssistantReq):
    spec=intake.load_oas(req.oasPath)
    traits=intake.extract_traits(spec)
    if req.useAI: traits=llm.merge_llm_traits(spec, traits, model=req.model)
    decision=decision_engine.decide(traits, model=req.model if req.useAI else None)
    plan=guardrails.plan_from_traits(traits, use_llm=req.useAI, model=req.model)
    result=builder.generate_bundle(spec, plan, req.outDir, decision)
    gate_result=gate.evaluate(plan, result.get('applied_controls', []))
    summary={'decision':decision,'plan':plan,'gate':gate_result,'artifacts':result.get('artifacts',[])}
    write_json(summary, f"{req.outDir}/summary.json")
    return summary

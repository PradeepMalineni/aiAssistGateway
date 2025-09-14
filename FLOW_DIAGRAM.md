# DevX Gateway Assistant - Complete Flow Diagram

## 🔄 **Main Enterprise Flow**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   DEVELOPER     │───▶│   DEVX AGENT    │───▶│   ORCHESTRA     │
│   (VS Code)     │    │   (Enterprise)  │    │   AUTOMATION    │
│                 │    │                 │    │   SERVICE       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   prompt.md     │    │   index.csv     │
                       │   (Intent Map)  │    │   (Registry)    │
                       └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │  workflow.json  │───▶│   MCP SERVER    │
                       │  (Instructions) │    │   (Tools)       │
                       └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   .out/         │
                                               │   (Artifacts)   │
                                               └─────────────────┘
```

## 📋 **Detailed 6-Step Workflow**

### **Step 1: Discover OpenAPI**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Search    │───▶│   Find      │───▶│  OpenAPI    │
│   Workspace │    │   OAS Files │    │  Found      │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ▼
                   ┌─────────────┐
                   │ STEP1.      │
                   │ firstMatch  │
                   └─────────────┘
```

### **Step 2: Analyze OAS**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Load      │───▶│   Extract   │───▶│   Traits    │
│   OpenAPI   │    │   Traits    │    │   Analysis  │
└─────────────┘    └─────────────┘    └─────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Check for  │    │   AI/LLM    │    │  Public/    │
│ gateway.hints│    │ Analysis   │    │ Internal,   │
│    .yaml    │    │            │    │ PII/PCI     │
└─────────────┘    └─────────────┘    └─────────────┘
```

### **Step 3: Validate Hints**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Check if  │───▶│   Merge     │───▶│   Re-run    │
│ hints exist │    │ with OAS    │    │ Analysis    │
└─────────────┘    └─────────────┘    └─────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Enhanced   │    │  Complete   │    │ STEP3.json  │
│  Context    │    │  Traits     │    │ (Final)     │
└─────────────┘    └─────────────┘    └─────────────┘
```

### **Step 4: Decide Gateway**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   AI        │───▶│   Gateway   │───▶│   User      │
│ Decision    │    │ Selection   │    │ Approval    │
└─────────────┘    └─────────────┘    └─────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Apigee vs   │    │ Decision    │    │ "Proceed?   │
│ DataPower   │    │ Logic       │    │ (yes/no)"   │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                           ▼
                   ┌─────────────┐
                   │ STEP4.json  │
                   └─────────────┘
```

### **Step 5: Synthesize Guardrails**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Security  │───▶│   Control   │───▶│   Policy    │
│   Analysis  │    │   Planning  │    │   Catalog   │
└─────────────┘    └─────────────┘    └─────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ mtls,       │    │ Required    │    │ STEP5.json  │
│ spike-arrest│    │ Controls    │    │ (Plan)      │
│ oauth, etc. │    │ List        │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
```

### **Step 6: Generate & Validate**
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Generate  │───▶│   Apply     │───▶│   Validate  │
│   Bundle    │    │   Policies  │    │   Controls  │
└─────────────┘    └─────────────┘    └─────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Proxy       │    │ Security    │    │ OPA Gate    │
│ Templates   │    │ Controls    │    │ Check       │
└─────────────┘    └─────────────┘    └─────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Deployment  │    │ Applied     │    │ PASS/FAIL   │
│ Artifacts   │    │ Controls    │    │ Decision    │
└─────────────┘    └─────────────┘    └─────────────┘
        │                   │                   │
        ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   .out/     │    │ STEP6.json  │    │ Final       │
│ (Artifacts) │    │ (Results)   │    │ Summary     │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 🛠️ **MCP Tools Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                MCP SERVER (Port 8765)                   │
├─────────────────────────────────────────────────────────┤
│  /.well-known/mcp.json  (Auto-discovery manifest)      │
├─────────────────────────────────────────────────────────┤
│  /tools/                                               │
│  ├── discover_oas     (Find OpenAPI files)             │
│  ├── analyze_oas      (Extract traits + AI analysis)   │
│  ├── decide_gateway   (Apigee vs DataPower selection)  │
│  ├── synthesize_guardrails (Security control planning) │
│  ├── generate_bundle  (Create proxy artifacts)         │
│  ├── opa_gate         (Policy validation)              │
│  └── run_gateway_assistant (End-to-end workflow)       │
└─────────────────────────────────────────────────────────┘
```

## 🔄 **Alternative Flows**

### **Direct MCP Usage**
```
Developer → IDE MCP Extension → Direct Tool Calls → Results
```

### **One-Shot Workflow**
```
Developer → run_gateway_assistant → Complete Flow → .out/ Artifacts
```

### **Enterprise Integration**
```
DevX Agent → Orchestra Service → MCP Server → Gateway Tools → Artifacts
```

## 📊 **Data Flow Summary**

1. **Input**: Developer query in IDE
2. **Routing**: DevX Agent maps query to workflow
3. **Execution**: 6-step workflow using MCP tools
4. **Processing**: AI-powered analysis and decision making
5. **Generation**: Proxy bundles with security controls
6. **Validation**: Policy compliance checking
7. **Output**: Deployable artifacts in `.out/` directory

## 🎯 **Key Integration Points**

- **Enterprise DevX Agent**: Routes queries via prompt.md
- **Orchestra Service**: Executes workflows via index.csv
- **MCP Server**: Provides gateway-specific tools
- **AI/LLM**: Powers analysis and decision making
- **Policy Engine**: Ensures compliance and security

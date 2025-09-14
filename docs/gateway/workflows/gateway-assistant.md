# Gateway Assistant Workflow

## Overview
The Gateway Assistant automates API gateway selection and proxy generation with security guardrails.

## Workflow Steps

### 1. Discover OpenAPI
- Automatically finds OpenAPI specification files
- Supports `.yaml`, `.yml`, and `.json` formats

### 2. Analyze API Traits
- Extracts security requirements (PII/PCI, public/internal)
- Identifies rate limiting needs
- Determines compliance requirements

### 3. Gateway Selection
- **Apigee**: For cloud-native, scalable APIs
- **DataPower**: For enterprise-grade security and compliance

### 4. Security Guardrails
- Automatically applies appropriate security controls
- Configures authentication and authorization
- Sets up rate limiting and monitoring

### 5. Proxy Generation
- Creates deployable proxy bundles
- Generates configuration files
- Includes security policies and templates

### 6. Validation
- Validates security controls against requirements
- Ensures compliance with enterprise policies
- Provides deployment-ready artifacts

## Usage
Ask the Gateway Assistant: "Decide the right API gateway for my service" and follow the guided workflow.

## Output
Generated artifacts are placed in the `.out/` directory with complete deployment configuration.

# Implementation Plan

Convert the consolidated research agent notebook design into a series of implementation tasks that build incrementally on the existing codebase and notebooks. Each task focuses on creating, modifying, or testing specific code components while maintaining educational clarity and test alignment.

## Task List

- [x] 1. Environment Bootstrap and Configuration

  - Create robust environment setup using environs package for early API key loading
  - Configure rich traceback and loguru logging for educational clarity
  - Implement path discovery system to locate src/research_agent_framework
  - Add comprehensive error handling with educational fallbacks
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [ ] 2. Framework Component Demonstrations
- [ ] 2.1 Pydantic Model Showcase (Pydantic v2 ONLY)
  - Demonstrate Scope, ResearchTask, EvalResult, SerpResult with validation examples using Pydantic v2
  - Show nested model construction (Location, Address, Coordinates, Rating, PriceLevel)
  - Use assertpy for clear validation assertions and educational feedback
  - Include TypeAdapter examples for Pydantic v2 compatibility
  - Reference existing research_agent_framework models as primary preference
  - _Requirements: 2.1, 2.2, 2.3_

- [ ] 2.2 LLM Client Integration
  - Demonstrate MockLLM first for deterministic educational examples
  - Show OpenAI and Anthropic client configuration with environment variables
  - Include error handling for missing API keys with educational messages
  - _Requirements: 2.5_

- [ ] 2.3 Search Adapter System with Full Pydantic v2 Decomposition
  - Use existing research_agent_framework adapters as primary preference: MockSearchAdapter, SerpAPISearchAdapter, TavilySearchAdapter
  - Create comprehensive Pydantic v2 models for each request/reply decomposed to built-in types only
  - Include enums, constants, and nested models until all leaf nodes contain only built-in types
  - Show from_raw construction patterns and raw data preservation
  - Include empty-limit behavior and error handling examples
  - Reference existing notebooks for usage patterns
  - _Requirements: 2.4_

- [ ] 3. Jinja Template System Implementation
- [ ] 3.1 Template Conversion and Organization
  - Convert existing prompts from src/deep_research_from_scratch/prompts.py to Jinja templates
  - Create template directory structure under src/research_agent_framework/prompts/templates/
  - Implement StrictUndefined configuration to catch missing variables
  - _Requirements: 3.1, 3.2_

- [ ] 3.2 Template Renderer with Educational Examples
  - Create render_template function with comprehensive error handling
  - Demonstrate template rendering with context examples
  - Show both successful rendering and error cases for education
  - Include examples using clarify_with_user_instructions.j2 and research_agent_prompt.j2
  - _Requirements: 3.3, 3.4, 3.5_

- [ ] 4. Complete Workflow Implementation
- [ ] 4.1 State Management and Graph Construction
  - Use existing deep_research_from_scratch models as primary preference: AgentState and AgentInputState
  - Create StateGraph following the exact pattern from 5_full_agent.ipynb
  - Add proper node connections: START → clarify_with_user → write_research_brief → supervisor_subgraph → final_report_generation → END
  - Reference existing notebooks for state management patterns
  - _Requirements: 4.1, 4.2_

- [ ] 4.2 Clarify with User Implementation
  - Implement clarify_with_user node using existing clarify_with_user_instructions prompt
  - Add human interaction loop for clarification questions ONLY as needed (not always)
  - Include JSON response parsing and validation
  - _Requirements: 4.1, 4.3_

- [ ] 4.3 Research Brief Generation with Evaluation Cell
  - Implement write_research_brief node using transform_messages_into_research_topic_prompt
  - Add evaluation cell immediately after brief generation using BRIEF_CRITERIA_PROMPT and BRIEF_HALLUCINATION_PROMPT
  - Include educational examples showing how to validate AI-generated briefs
  - Demonstrate quality gate implementation before proceeding to expensive multi-agent research
  - _Requirements: 4.2, 10.1_

- [ ] 4.4 Supervisor Subgraph Implementation with Research Quality Evaluation
  - Implement supervisor_agent using lead_researcher_prompt
  - Add multi-agent coordination with ConductResearch and ResearchComplete tools
  - Add evaluation cell after individual agent research to assess quality and completeness before compression
  - Support scaling to ~100 x 2 sub-agents (expert + local-expert pairs)
  - Include research compression using compress_research_system_prompt
  - Demonstrate "fail fast" principle by catching quality issues early
  - _Requirements: 4.3, 4.4, 10.2, 10.4_

- [ ] 4.5 Final Report Generation with Final Evaluation Cell
  - Implement final_report_generation using final_report_generation_prompt
  - Add comprehensive report synthesis from research findings
  - Add evaluation cell after report generation to assess comprehensiveness and citation quality
  - Include proper citation formatting and source management
  - Demonstrate complete quality control workflow from brief to final report
  - _Requirements: 4.5, 10.4_

- [ ] 5. MCP Integration Implementation
- [ ] 5.1 MCP Client Configuration
  - Implement MCP client setup based on 3_research_agent_mcp.ipynb
  - Configure filesystem MCP server for local document access
  - Add lazy initialization pattern for LangGraph Platform compatibility
  - _Requirements: 5.1, 5.2_

- [ ] 5.2 MCP Tool Integration
  - Implement async tool execution for MCP filesystem operations
  - Add file operations: read_file, list_directory, search_files
  - Include proper error handling and fallback to in-process agents
  - _Requirements: 5.3, 5.4_

- [ ] 5.3 Report Saving with MCP
  - Implement final report saving using MCP filesystem tools
  - Add proper file naming and organization
  - Include error handling for file operations
  - _Requirements: 4.5_

- [ ] 6. Evaluation System Integration with Strategic Cell Placement
- [ ] 6.1 Three Strategic Evaluation Cells Throughout Workflow
  - **Evaluation Cell 1**: After research brief generation (Task 4.3) using BRIEF_CRITERIA_PROMPT and BRIEF_HALLUCINATION_PROMPT
  - **Evaluation Cell 2**: After individual agent research (Task 4.4) to assess research quality before compression
  - **Evaluation Cell 3**: After final report generation (Task 4.5) to evaluate comprehensiveness and citations
  - Demonstrate "fail fast" quality control methodology
  - Show educational examples of AI content validation
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 7. Educational Content and Documentation
- [ ] 7.1 Comprehensive Markdown Explanations
  - Add detailed markdown cells before all code sections
  - Include explanations of concepts, workflow steps, and design decisions
  - Add links to relevant documentation and resources
  - Include diagrams and visual aids where helpful
  - _Requirements: 6.1, 6.2_

- [ ] 7.2 Code Comments and Documentation
  - Add detailed code comments describing all code blocks
  - Include docstrings for functions and classes
  - Explain complex logic and design patterns
  - Add references to corresponding test cases
  - _Requirements: 6.3_

- [ ] 8. Test Alignment and Validation
- [ ] 8.1 Test Suite Synchronization and Functional Alignment
  - Ensure notebook examples match existing pytest test cases exactly
  - Add new tests for consolidated functionality that remain functionally in-sync with notebook
  - Create bidirectional validation: notebook changes must update tests, test changes must update notebook
  - Include Hypothesis property-based testing examples
  - Validate all examples against test expectations continuously
  - _Requirements: 7.1, 7.2_

- [ ] 8.2 Property-Based Testing Demonstrations
  - Show Hypothesis examples for key invariants
  - Demonstrate MockLLM deterministic behavior testing
  - Include adapter testing with from_raw patterns
  - Add model validation testing examples
  - _Requirements: 7.3, 7.4, 7.5_

- [ ] 9. Error Handling and Fallbacks
- [ ] 9.1 Graceful Degradation Implementation
  - Add comprehensive error handling for missing dependencies
  - Implement fallbacks for MCP unavailability
  - Include educational error messages prioritizing learning over production concerns
  - Add safe defaults for missing environment variables
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [ ] 9.2 Async Operation Safety
  - Implement notebook-friendly async execution patterns
  - Add nest_asyncio compatibility for Jupyter environments
  - Include proper error handling for async operations
  - _Requirements: 9.5_

- [ ] 10. Educational Clarity and Understanding Features
- [ ] 10.1 Understandability Over Production-Ready
  - Prioritize clear, educational code over production optimizations
  - Add comprehensive explanations for complex operations
  - Include step-by-step breakdowns of multi-agent coordination
  - Focus on learning outcomes rather than performance metrics
  - _Requirements: 9.4, 10.5_

- [ ] 10.2 Rich Output Formatting for Education
  - Implement clear, educational rich formatting without overwhelming output
  - Add progress indicators that explain what's happening at each step
  - Include structured output that teaches research methodology
  - _Requirements: 10.5_

- [ ] 11. Integration Testing and Validation
- [ ] 11.1 End-to-End Workflow Testing
  - Test complete workflow from human input to final report
  - Validate MCP integration with filesystem operations
  - Include error recovery and fallback testing
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 11.2 Educational Effectiveness Validation
  - Verify incremental learning progression
  - Test component demonstrations for clarity
  - Validate alignment with existing test suite
  - Ensure comprehensive coverage of framework features
  - _Requirements: 6.4, 6.5_

## Implementation Notes

- **Notebook Name**: research_workflow.ipynb (consolidated research agent workflow)
- **Pydantic Version**: Use Pydantic v2 ONLY - no v1 compatibility
- **Framework Preference**: Use existing research_agent_framework capabilities as primary preference unless concerns identified
- **Package Consistency**: Use packages as used in existing notebooks (5_full_agent.ipynb, 3_research_agent_mcp.ipynb) vs introducing new packages
- **Reference Patterns**: Reference existing notebooks for usage patterns and implementation guidance
- **Evaluation Strategy**: Three strategic evaluation cells placed at key quality gates throughout workflow
- **Incremental Development**: Each task builds on previous tasks and can be tested independently
- **Educational Focus**: All implementations prioritize learning and understanding over production optimization
- **Test Alignment**: Every feature must align with existing pytest/hypothesis test cases
- **Error Handling**: Comprehensive error handling with educational messages throughout
- **MCP Integration**: Proper async handling and fallback mechanisms for MCP operations

## Success Criteria

- **Functionality**: All features from the 5 original notebooks work correctly
- **Education**: Clear progression from basic concepts to advanced multi-agent coordination
- **Testing**: All examples align with and extend the existing test suite
- **Reliability**: Robust error handling and graceful degradation in all scenarios
- **Performance**: Efficient handling of concurrent operations and resource management

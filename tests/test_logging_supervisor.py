import logging
import io
from deep_research_from_scratch.multi_agent_supervisor import LoggingSupervisor, LoggingAgentTask
from research_agent_framework.config import get_logger
from rich.markdown import Markdown

def test_logging_supervisor_and_agents_logs_messages(monkeypatch):
    # Capture logs in a StringIO buffer
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    logger = get_logger(backend="std")
    logger.addHandler(handler)
    logger.level = "INFO"

    # Create logging agent tasks with injected logger
    agent_tasks = [
        LoggingAgentTask(agent_id="A1", description="Find top-rated coffee shops in SF.", logger=logger),
        LoggingAgentTask(agent_id="A2", description="Check which shops are open now.", logger=logger),
        LoggingAgentTask(agent_id="A3", description="Filter for no cover charge in SOMA.", logger=logger)
    ]
    supervisor = LoggingSupervisor(logger=logger)
    results = supervisor.coordinate(agent_tasks)

    # Remove handler and get log output
    logger.removeHandler(handler)
    log_output = log_stream.getvalue()

    # Assert log output contains expected messages
    assert "Supervisor: Starting coordination" in log_output
    for task in agent_tasks:
        assert f"Agent {task.agent_id} starting: {task.description}" in log_output
        assert f"Agent {task.agent_id} finished: Completed: {task.description}" in log_output
        assert f"Supervisor: Agent {task.agent_id} outcome: Completed: {task.description}" in log_output
    assert "Supervisor: Coordination complete" in log_output

    # Optionally, print results for manual inspection
    for result in results:
        print(Markdown(f"**Agent {result.agent_id} outcome:**\n\n{result.outcome}"))

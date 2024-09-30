from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
from anthropic import Anthropic
import logging 

# Uncomment the following line to use an example of a custom tool
# from pilot.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool
anthropic = Anthropic()

def anth_llm(**kwargs):
    return anthropic.completions.create(
        model="claude-3-sonnet-20240229",
        max_tokens_to_sample=1000,
        **kwargs
    )
@CrewBase
class PilotCrew():
	"""Pilot crew"""
	code_llm=LLM(model="ollama/codellama", base_url="http://localhost:11434",timeout=3600.0)
	logging.info(f"LLM initialization with model :{code_llm}, base url:{code_llm.base_url}")

	chat_llm = LLM(model="ollama/mistral",base_url="http://localhost:11434",timeout=3600.0)
	logging.info(f"LLM initialization with model :{chat_llm}, base url:{chat_llm.base_url}")

	@agent
	def software_developer(self)-> Agent:
		return Agent(config= self.agents_config['software_developer'],
			   llm='claude-2',
			   allow_delegation=False,
			   verbose=True
			)

	@task
	def development_task(self)-> Task:
		return Task(
			config=self.tasks_config['development_task'],
			output_file='test2.py'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Pilot crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
from crewai import Agent, Crew, Process, Task,LLM
from crewai.project import CrewBase, agent, crew, task
import logging 

# Uncomment the following line to use an example of a custom tool
# from pilot.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class PilotCrew():
	"""Pilot crew"""
	code_llm=LLM(model="ollama/codellama", base_url="http://localhost:11434",timeout=3600.0)
	logging.info(f"LLM initialization with model :{code_llm}, base url:{code_llm.base_url}")

	chat_llm = LLM(model="ollama/mistral",base_url="http://localhost:11434",timeout=3600.0)
	logging.info(f"LLM initialization with model :{chat_llm}, base url:{chat_llm.base_url}")

	@agent
	def researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			llm=self.chat_llm,
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			llm=self.chat_llm,
			verbose=True
		)

	@agent
	def principal_software_developer(self)-> Agent:
		return Agent(config= self.agents_config['principal_software_developer'],
			   llm=self.code_llm,
			   verbose=True
			)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='report.md'
		)

	@task
	def development_task(self)-> Task:
		return Task(
			config=self.tasks_config['development_task'],
			output_file='test.py'
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
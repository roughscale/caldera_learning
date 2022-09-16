import random
import logging
from app.objects.secondclass.c_fact import Fact
from app.utility.base_service import BaseService
from app.plugin.learning.objects.CybORG import CybORG
from app.plugin.learning.objects.CybORG.CybORG.Agents import RedMeanderAgent

class LogicalPlanner:

    def __init__(self, operation, planning_svc, stopping_conditions=()):
        self.operation = operation
        self.planning_svc = planning_svc
        self.knowledge_svc = BaseService.get_service('knowledge_svc')
        self.stopping_conditions = stopping_conditions
        self.stopping_condition_met = False
        self.log = logging.getLogger('random_planner')
        self.env = None
        self.env_agent = None # learning agent in the environment
        #self.learning_agent = None
        self.learning_params = None
        self._initialise_learning_agent()

    def _initialise_learning_agent():
        #self.env = CybORG.CybORG(env="caldera",agent=self.learning_agent)
        self.env = CybORG.CybORG(env="caldera") # this uses the Caldera EnvironmentController
        #
        # hard code the Agent and Action and Observation objects
        self.env_agent = RedAgent()
        
        # need to import/generate the Action Ability m
        #self.learning_agent = TabularQLearningAgent(
        #  self.env, verbose=args.quite, **vars(args)
        #)
        #self.learning_params = {
        #  "epsilon" = 0.5
        #}
        # implement the caldera interface within the network object to begin with
        #c2 = CalderaInterface(self.operation, self.planning_svc)
        # add the caldera interfaces to the emulated network object
        # the interface needs to implement a number of methods
        #self.env.network.caldera_interface(self.operation, self.planning_svc)
 
    async def execute(self):
        #
        steps = 0
        episode_return = 0
        done = False
        env_step_limit_reached = False 
        # no learning at the moment
        #epsilon = self.learning_params["epsilon"]

        s = self.env.reset()

        while not done and not env_step_limit_reached:
            action = self.env.get_action(s)
            next_s, r, done, env_step_limit_reached, _ = env.step(agent=env_agent.agent_name, 
                 action=action) # the Caldera EnvironmentController performs the action
            s = next_s
            episode_return += r
            steps += 1

        #return episode_return, steps, env.goal_reached()
        # once done or env_step_limit_reached, terminate operation


        # the following needs to go into the Caldera Controller class
        #  ability = { "name": "NMAP scan" }
        #  # this gets the untrimmed actions
        #  Need to distinguish between CybORG agent (env_agent) and Caldera agent (c2_agent)
        #  raw_action = await self._get_links(agent=c2_agent, ability=ability)
        #  # now need to add the relevant facts to the link
        #  raw_action.facts=[Fact(trait='target.ip',value='192.168.121.8',score=1)]
        #  # and use planning_svc.add_test_variants to populate the commands vars
        #  # and generate link id
        #  actions = await self.planning_svc.add_test_variants([raw_action], c2_agent, facts=raw_action.facts,
        #    operation=self.operation, trim_unset_variables=True, trim_missing_requirements=True)
        #  action = actions[0]
        #else:
        #  agent = self.operation.agents[random.randrange(0,len(self.operation.agents))]
        #  possible_agent_links = await self._get_links(agent=c2_agent)
        #  action = possible_agent_links[random.randrange(0,len(possible_agent_links))]

        #if action:
        #  next_link=[]

        #  next_link.append(await self.operation.apply(action))
          
        #  await self.operation.wait_for_links_completion(next_link)

        # query knowledge service for facts
        self.log.debug("Knowledge Service: {0}".format(dir(self.knowledge_svc)))
        # criteria=None will return all facts
        self.log.debug("Knowledge Service facts: {0}".format(await self.knowledge_svc.get_facts(criteria=None)))
        for fact in await self.knowledge_svc.get_facts(criteria=None):
          self.log.debug("fact trait {0}".format(fact.trait))
          self.log.debug("fact value {0}".format(fact.value))
          self.log.debug("fact collected_by {0}".format(fact.collected_by))
          self.log.debug("fact relationships {0}".format(fact.relationships))
          self.log.debug("fact origin_type {0}".format(fact.origin_type))
          self.log.debug("fact source {0}".format(fact.source))

        return

    async def _get_links(self, agent=None, ability=None, trim=False):
        links = []
        abilities = await self.planning_svc.get_service('data_svc').locate('abilities')
 
        links=await self.planning_svc.generate_and_trim_links(agent, self.operation, abilities, trim=trim)

        # filter links to match the provided ability attributes 
        if ability:
          for link in links:
            if link.ability.name == ability['name']:
              return link
          return None
        return links

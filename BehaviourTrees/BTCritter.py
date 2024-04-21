import asyncio
import random
import py_trees
import py_trees as pt
from py_trees import common
import Goals_BT
import Sensors
import time


class BN_DoNothing(pt.behaviour.Behaviour):
    '''
    Description: Behaviour that makes the agent do nothing
    '''
    def __init__(self, aagent):
        '''
        init method for BN_DoNothing
        '''
        #Set the goal to None
        self.my_goal = None
        #Print a message to the terminal
        print("Initializing BN_DoNothing")
        #Call the parent constructor
        super(BN_DoNothing, self).__init__("BN_DoNothing")
        #get the agent
        self.my_agent = aagent

    def initialise(self):
        '''
        initialise method for BN_DoNothing, creates a task to make the agent do nothing
        '''
        self.my_goal = asyncio.create_task(Goals_BT.DoNothing(self.my_agent).run())

    def update(self):
        '''
        update method for BN_DoNothing:
        checks if the goal is done, if it is, checks if the goal was successful or not
        '''
        #Check if the goal is not done
        if not self.my_goal.done():
            #Return running
            return pt.common.Status.RUNNING
        #If the goal is done
        else:
            #Check if the goal was successful
            if self.my_goal.result():
                print("BN_DoNothing completed with SUCCESS")
                #Return success
                return pt.common.Status.SUCCESS
            #If the goal was not successful
            else:
                print("BN_DoNothing completed with FAILURE")
                #Return failure
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        '''
        terminate method for BN_DoNothing by cancelling the goal
        '''
        #we have to stop the associated task
        self.my_goal.cancel()



class BN_ForwardRandom(pt.behaviour.Behaviour):
    '''
    Description: Behaviour that moves the agent forward for a random distance
    '''
    def __init__(self, aagent):
        '''
        init method for BN_ForwardRandom
        '''
        #Set the goal to None
        self.my_goal = None
        #Print a message to the terminal
        print("Initializing BN_ForwardRandom")
        #Call the parent constructor
        super(BN_ForwardRandom, self).__init__("BN_ForwardRandom")
        #log the message
        self.logger.debug("Initializing BN_ForwardRandom")
        #Get the agent
        self.my_agent = aagent
        

    def initialise(self):
        '''
        initialise method for BN_ForwardRandom, creates a task to move the agent forward
        '''
        #Print a message to the terminal
        self.logger.debug("Create Goals_BT.ForwardDist task")
        #Create a task to move the agent forward for 1 to 5 units of distance
        self.my_goal = asyncio.create_task(Goals_BT.ForwardDist(self.my_agent, -1, 1, 5).run())

    def update(self):
        '''
        update method for BN_ForwardRandom: 
        checks if the goal is done, if it is, checks if the goal was successful or not  
        '''
        #Check if the goal is not done
        if not self.my_goal.done():
            #Return running
            return pt.common.Status.RUNNING
        #If the goal is done
        else:
            #Check if the goal was successful
            if self.my_goal.result():
                self.logger.debug("BN_ForwardRandom completed with SUCCESS")
                print("BN_ForwardRandom completed with SUCCESS")
                #Return success
                return pt.common.Status.SUCCESS
            #If the goal was not successful
            else:
                self.logger.debug("BN_ForwardRandom completed with FAILURE")
                print("BN_ForwardRandom completed with FAILURE")
                #Return failure
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        '''
        terminate method for BN_ForwardRandom by cancelling the goal
        '''
        # we have to stop the associated task
        self.logger.debug("Terminate BN_ForwardRandom")
        self.my_goal.cancel()



class BN_TurnRandom(pt.behaviour.Behaviour):
    '''
    Description: Behaviour that turns the agent for a random angle
    '''
    def __init__(self, aagent):
        '''
        init method for BN_TurnRandom
        '''
        #Set the goal to None
        self.my_goal = None
        #Print a message to the terminal
        print("Initializing BN_TurnRandom")
        #Call the parent constructor
        super(BN_TurnRandom, self).__init__("BN_TurnRandom")
        #get the agent
        self.my_agent = aagent

    def initialise(self):
        '''
        initialise method for BN_TurnRandom, creates a task to turn the agent
        '''
        self.my_goal = asyncio.create_task(Goals_BT.Turn(self.my_agent).run())

    def update(self):
        '''
        update method for BN_TurnRandom: 
        checks if the goal is done, if it is, checks if the goal was successful or not
        '''
        #Check if the goal is not done
        if not self.my_goal.done():
            #Return running
            return pt.common.Status.RUNNING
        #If the goal is done
        else:
            #If the goal was successful
            if self.my_goal.result():
                print("BN_Turn completed with SUCCESS")
                #Return success
                return pt.common.Status.SUCCESS
            #If the goal was not successful
            else:
                print("BN_Turn completed with FAILURE")
                #Return failure
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        '''
        terminate method for BN_TurnRandom by cancelling the goal
        '''
        # we have to stop the associated task
        self.logger.debug("Terminate BN_TurnRandom")
        self.my_goal.cancel()



class BN_DetectFlower(pt.behaviour.Behaviour):
    '''
    Description: Behaviour that detects a flower in the environment
                 using the raycast sensor of the critter
    '''
    def __init__(self, aagent):
        '''
        init method for BN_DetectFlower
        '''
        #Set the goal to None
        self.my_goal = None
        #Print a message to the terminal
        print("Initializing BN_DetectFlower")
        #Call the parent constructor
        super(BN_DetectFlower, self).__init__("BN_DetectFlower")
        #get the agent
        self.my_agent = aagent

    def initialise(self):
        '''
        initialise method for BN_DetectFlower, does nothing, pass
        '''
        pass

    def update(self):
        '''
        update method for BN_DetectFlower:
        checks if the raycast sensor detects a flower in the environment or not 
        '''
        #Get the object information from the raycast sensor
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        #Iterate through the object information
        for index, value in enumerate(sensor_obj_info):
            #If there is a hit with an object
            if value:  
                #If the object it hits is a flower
                if value["tag"] == "Flower": 
                    # a flower is detected, print a message to the terminal
                    print("BN_DetectFlower completed with SUCCESS")
                    #Return success
                    return pt.common.Status.SUCCESS
        #If no flower is detected, print a message to the terminal
        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        '''
        terminate method for BN_DetectFlower, does nothing, pass
        '''
        pass
    
    

class BN_EatFlower(pt.behaviour.Behaviour):
    '''
    Description: Behaviour that makes the agent eat a flower in the environment 
                 basically it stops the agent for 5 seconds next to the flower
                 to simulate the eating process
    '''
    def __init__(self, aagent):
        '''
        init method for BN_EatFlower
        '''
        #Set the goal to None
        self.my_goal = None
        #Print a message to the terminal
        print("Initializing BN_EatFlower")
        #Call the parent constructor
        super(BN_EatFlower, self).__init__("BN_EatFlower")
        #get the agent
        self.my_agent = aagent

    def initialise(self):
        '''
        initialise method for BN_EatFlower, creates a task to eat the flower
        '''
        self.my_goal = asyncio.create_task(Goals_BT.EatFlower(self.my_agent).run())

    def update(self):
        '''
        update method for BN_EatFlower: 
        checks if the goal is done, if it is, checks if the goal was successful or not
        '''
        #Print a message to the terminal
        print("inside BN_EatFlower")
        #Check if the goal is not done
        if not self.my_goal.done():
            print("running BN_EatFlower")
            #Return running
            return pt.common.Status.RUNNING
        #If the goal is done
        else:
            #Check if the goal was successful
            if  self.my_goal.result():
                print("BN_EatFlower completed with SUCCESS")
                #Return success
                return pt.common.Status.SUCCESS
            #If the goal was not successful
            else:
                print("BN_EatFlower completed with FAILURE")
                #Return failure
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        '''
        terminate method for BN_EatFlower by cancelling the goal
        '''
        #we have to stop the associated task
        self.logger.debug("Terminate BN_EatFlower")
        self.my_goal.cancel()



class BN_DetectObstacle(pt.behaviour.Behaviour):
    '''
    Description: Behaviour that detects an obstacle in the environment
                 using the raycast sensor of the critter
    '''
    def __init__(self, aagent):
        '''
        init method for BN_DetectObstacle
        '''
        #Set the goal to None
        self.my_goal = None
        #Print a message to the terminal
        print("Initializing BN_DetectObstacle")
        #Call the parent constructor
        super(BN_DetectObstacle, self).__init__("BN_DetectObstacle")
        #get the agent
        self.my_agent = aagent

    def initialise(self):
        '''
        initialise method for BN_DetectObstacle, does nothing, pass
        '''
        pass

    def update(self):
        '''
        update method for BN_DetectObstacle:
        checks if the raycast sensor detects an obstacle in the environment or not
        '''
        #Get the object information from the raycast sensor
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        #Iterate through the object information
        for index, value in enumerate(sensor_obj_info):
            #If there is a hit with an object
            if value: 
                #If the object it hits is not an astronaut
                if value["tag"] != "Astronaut":
                    # an obstacle is detected, print a message to the terminal
                    print("BN_DetectObstacle completed with SUCCESS")
                    #Return success
                    return pt.common.Status.SUCCESS
        #Return failure if no obstacle is detected
        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        '''
        terminate method for BN_DetectObstacle, does nothing, pass
        '''
        pass

class BN_Avoid(pt.behaviour.Behaviour):
    '''
    Description: Behaviour that makes the agent avoid an obstacle in the environment
                 using the raycast sensor of the critter
    '''
    def __init__(self, aagent):
        '''
        init method for BN_Avoid
        '''
        #Set the goal to None
        self.my_goal = None
        #Print a message to the terminal
        print("Initializing BN_Avoid")
        #Call the parent constructor
        super(BN_Avoid, self).__init__("BN_Avoid")
        #get the agent
        self.my_agent = aagent

    def initialise(self):
        '''
        initialise method for BN_Avoid, creates a task to avoid the obstacle
        '''
        self.my_goal = asyncio.create_task(Goals_BT.Avoid(self.my_agent).run())

    def update(self):
        '''
        update method for BN_Avoid:
        checks if the goal is done, if it is, checks if the goal was successful or not
        '''
        #Check if the goal is not done
        if not self.my_goal.done():
            #Return running
            return pt.common.Status.RUNNING
        #If the goal is done
        else:
            #Check if the goal was successful
            if self.my_goal.result():
                print("BN_Avoid completed with SUCCESS")
                #Return success
                return pt.common.Status.SUCCESS
            #If the goal was not successful
            else:
                print("BN_Avoid completed with FAILURE")
                #Return failure
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        '''
        terminate method for BN_Avoid by cancelling the goal
        '''
        # we have to stop the associated task
        self.logger.debug("Terminate BN_Avoid")
        self.my_goal.cancel()


class HungryTimer(pt.behaviour.Behaviour):
    '''
    Description: Behaviour to know when the critter is hungry, 
                 it has a timer of 15 seconds of not hungry, then it gets hungry
    '''
    def __init__(self, agent , current_time, name="HungryTimer"):
        '''
        init method for HungryTimer 
        '''
        #Call the parent constructor
        super(HungryTimer, self).__init__(name)
        #Set the agent
        self.agent = agent
        #Set the start time
        self.agent.hungry = True
        #Set the start time
        self.start_time = current_time

    def initialise(self):
        '''
        initialise method for HungryTimer, does nothing, pass
        '''
        pass

    def update(self):
        '''
        update method for HungryTimer:
        checks if the critter is hungry or not
        '''
        #Get the current time
        current_time = time.time()
        #If the critter is hungry
        if self.agent.hungry:
            print("Hungry completed with SUCCESS")
            #Return success
            return pt.common.Status.SUCCESS
        
        #If the critter is not hungry and the timer is greater than 15 seconds
        if not self.agent.hungry and current_time - self.start_time > 15:
            #Set the hungry flag to True
            self.agent.hungry = True  
            #Set the start time to the current time, resetting the timer
            self.start_time = current_time
            print("Hungry completed with SUCCESS")
            #Return success
            return pt.common.Status.SUCCESS
        #If the critter is not hungry and the timer is less than 15 seconds
        else:
            print("Hungry completed with FAILURE")
            #Return failure
            return pt.common.Status.FAILURE

    def terminate(self, new_status):
        '''
        terminate method for HungryTimer, checks the new status,
        if it is invalid, the timer is stopped'''
        #If the new status is invalid
        if new_status == pt.common.Status.INVALID:
            #Stop the timer
            self.timer_started = False



class BN_DetectAstro(pt.behaviour.Behaviour):
    '''
    Description: Behaviour that detects an astronaut in the environment
                 using the raycast sensor of the critter
    '''    
    def __init__(self, aagent):
        '''
        init method for BN_DetectAstro
        '''
        #Set the goal to None
        self.my_goal = None
        #Print a message to the terminal
        print("Initializing BN_DetectAstro")
        #Call the parent constructor
        super(BN_DetectAstro, self).__init__("BN_DetectAstro")
        #get the agent
        self.my_agent = aagent
        #Create a variable to store the sensor index, initialized to None
        self.my_agent.det_sensor = None

    def initialise(self):
        '''
        initialise method for BN_DetectAstro, does nothing, pass
        '''
        pass

    def update(self):
        '''
        update method for BN_DetectAstro:
        checks if the raycast sensor detects an astronaut in the environment or not
        '''
        #Get the object information from the raycast sensor
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        #Iterate through the object information
        for index, value in enumerate(sensor_obj_info):
            #If there is a hit with an object
            if value:  
                #If the object it hits is an astronaut
                if value["tag"] == "Astronaut": 
                    # an astronaut is detected, print a message to the terminal
                    print("BN_DetectAstro completed with SUCCESS")
                    #Set the sensor index to the index of the astronaut
                    self.my_agent.det_sensor = index
                    #Return success
                    return pt.common.Status.SUCCESS
        #Return failure if no astronaut is detected
        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        '''
        terminate method for BN_DetectAstro, does nothing, pass
        '''
        pass

class BN_FollowAstro(pt.behaviour.Behaviour):
    '''
    Description: Behaviour that makes the agent follow an astronaut in the environment
    '''
    def __init__(self, aagent):
        '''
        init method for BN_FollowAstro
        '''
        #Set the goal to None
        self.my_goal = None
        #Print a message to the terminal
        print("Initializing BN_FollowAstro")
        #Call the parent constructor
        super(BN_FollowAstro, self).__init__("BN_FollowAstro")
        #get the agent
        self.my_agent = aagent

    def initialise(self):
        '''
        initialise method for BN_FollowAstro, creates a task to follow the astronaut
        '''
        self.my_goal = asyncio.create_task(Goals_BT.FollowAstronaut(self.my_agent).run())

    def update(self):
        '''
        update method for BN_FollowAstro:
        checks if the goal is done, if it is, checks if the goal was successful or not
        '''
        #Check if the goal is not done
        if not self.my_goal.done():
            #Return running
            return pt.common.Status.RUNNING
        #If the goal is done
        else:
            #Check if the goal was successful
            if self.my_goal.result():
                print("BN_FollowAstro completed with SUCCESS")
                #Return success
                return pt.common.Status.SUCCESS
            #If the goal was not successful
            else:
                print("BN_FollowAstro completed with FAILURE")
                #Return failure
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        '''
        terminate method for BN_FollowAstro by cancelling the goal
        '''
        # we have to stop the associated task
        self.logger.debug("Terminate BN_FollowAstro")
        self.my_goal.cancel()



class BTCritter:
    '''
    Description: Class that contains the behaviour tree for the critter, this is the main class
                 which will be called from the UI to run the behaviour tree
    Summary of the strategy and structure of the behaviour tree:
        - The critter will start by detecting a flower in the environment
        - If a flower is detected, the critter will eat the flower
        - If no flower is detected, the critter will detect an astronaut in the environment
        - If an astronaut is detected, the critter will follow the astronaut
        - If no astronaut is detected, the critter will detect an obstacle in the environment
        - If an obstacle is detected, the critter will avoid the obstacle
        - If no obstacle is detected, the critter will roam around randomly
        
        Drawing of the behaviour tree:
        selector:  [Selector]
            sequence:  [Sequence]
                detect flower:  [BN_DetectFlower]
                sequence:  [Sequence]
                    hungry timer:  [HungryTimer]
                    eat flower:  [BN_EatFlower]
            sequence:  [Sequence]
                detect astronaut:  [BN_DetectAstro]
                follow astronaut:  [BN_FollowAstro]
            sequence:  [Sequence]
                detect avoid:  [BN_DetectObstacle]
                avoid:  [BN_Avoid]
            parallel:  [Parallel]
                forward random:  [BN_ForwardRandom]
                turn random:  [BN_TurnRandom]      
    '''
    def __init__(self, aagent):
        '''
        init method for BTCritter
        '''
        #Set the agent
        self.aagent = aagent  
        #Get the current time
        current_time = time.time()
        #Create a HungryTimer object to check if the critter is hungry
        hungry_timer = HungryTimer(self.aagent, current_time)

        #Create the eat flower sequence with the hungry timer and the eat flower behaviour
        eat_flower = pt.composites.Sequence(name="EatFlower", memory=True)
        #Add the hungry timer and the eat flower behaviour to the sequence as children
        eat_flower.add_children([hungry_timer, BN_EatFlower(aagent)])
        
        #Create the detect flower sequence with the detect flower behaviour and the eat flower sequence
        det_flower = pt.composites.Sequence(name="DetectFlower", memory=True)
        #Add the detect flower behaviour and the eat flower sequence to the sequence as children
        det_flower.add_children([BN_DetectFlower(aagent), eat_flower])
        
        #Create the roaming parallel with the forward random and turn random behaviours
        roaming = pt.composites.Parallel("Parallel", policy=py_trees.common.ParallelPolicy.SuccessOnAll())
        #Add the forward random and turn random behaviours to the parallel as children
        roaming.add_children([BN_ForwardRandom(aagent), BN_TurnRandom(aagent)])

        #Create the detect avoid sequence with the detect obstacle and avoid behaviours
        det_avoid = pt.composites.Sequence(name="Detect_Avoid", memory=True)
        #Add the detect obstacle and avoid behaviours to the sequence as children
        det_avoid.add_children([BN_DetectObstacle(aagent), BN_Avoid(aagent)])
        
        #Create the detect follow sequence with the detect astronaut and follow astronaut behaviours
        det_astro = pt.composites.Sequence(name="Detect_Follow", memory=True)
        #Add the detect astronaut and follow astronaut behaviours to the sequence as children
        det_astro.add_children([BN_DetectAstro(aagent), BN_FollowAstro(aagent)])
        
        #Create the root selector with the detect flower, detect astronaut, detect avoid, and roaming behaviours
        self.root = pt.composites.Selector(name="Selector", memory=False)
        #Add the detect flower, detect astronaut, detect avoid, and roaming behaviours to the selector as children
        self.root.add_children([det_flower, det_astro, det_avoid, roaming])

        #set the behaviour tree with the root
        self.behaviour_tree = pt.trees.BehaviourTree(self.root)



    def set_invalid_state(self, node):
        '''
        set_invalid_state method for BTCritter, sets the status of the node to invalid in a recursive way'''
        #Set the status of the node to invalid
        node.status = pt.common.Status.INVALID
        #Iterate through the children of the node
        for child in node.children:
            #Call the set_invalid_state method for the children
            self.set_invalid_state(child)

    def stop_behaviour_tree(self):
        '''
        stop_behaviour_tree method for BTCritter, sets the status of all the nodes to invalid
        '''
        # Setting all the nodes to invalid, we force the associated asyncio tasks to be cancelled
        self.set_invalid_state(self.root)

    async def tick(self):
        '''
        tick method for BTCritter, runs the behaviour tree
        '''
        #Run the behaviour tree
        self.behaviour_tree.tick()
        #Wait for 0 seconds to allow other tasks to run
        await asyncio.sleep(0)

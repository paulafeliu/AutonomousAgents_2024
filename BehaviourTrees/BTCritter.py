import asyncio
import random
import py_trees
import py_trees as pt
from py_trees import common
import Goals_BT
import Sensors
import time


class BN_DoNothing(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_agent = aagent
        self.my_goal = None
        print("Initializing BN_DoNothing")
        super(BN_DoNothing, self).__init__("BN_DoNothing")

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.DoNothing(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            if self.my_goal.result():
                print("BN_DoNothing completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("BN_DoNothing completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.my_goal.cancel()


class BN_ForwardRandom(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_ForwardRandom")
        super(BN_ForwardRandom, self).__init__("BN_ForwardRandom")
        self.logger.debug("Initializing BN_ForwardRandom")
        self.my_agent = aagent

    def initialise(self):
        self.logger.debug("Create Goals_BT.ForwardDist task")
        self.my_goal = asyncio.create_task(Goals_BT.ForwardDist(self.my_agent, -1, 1, 5).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            if self.my_goal.result():
                self.logger.debug("BN_ForwardRandom completed with SUCCESS")
                print("BN_ForwardRandom completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                self.logger.debug("BN_ForwardRandom completed with FAILURE")
                print("BN_ForwardRandom completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_ForwardRandom")
        self.my_goal.cancel()


class BN_TurnRandom(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_TurnRandom")
        super(BN_TurnRandom, self).__init__("BN_TurnRandom")
        self.my_agent = aagent

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.Turn(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("BN_Turn completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("BN_Turn completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_TurnRandom")
        self.my_goal.cancel()


class BN_DetectFlower(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_DetectFlower")
        super(BN_DetectFlower, self).__init__("BN_DetectFlower")
        self.my_agent = aagent

    def initialise(self):
        pass

    def update(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        for index, value in enumerate(sensor_obj_info):
            if value:  # there is a hit with an object
                if value["tag"] == "Flower":  # If it is a flower
                    # print("Flower detected!")
                    print("BN_DetectFlower completed with SUCCESS")
                    return pt.common.Status.SUCCESS
        # print("No flower...")
        # print("BN_DetectFlower completed with FAILURE")
        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass

class BN_EatFlower(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_EatFlower")
        super(BN_EatFlower, self).__init__("BN_EatFlower")
        self.my_agent = aagent

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.EatFlower(self.my_agent).run())

    def update(self):
        print("inside BN_EatFlower")
        if not self.my_goal.done():
            print("running BN_EatFlower")
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("BN_EatFlower completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("BN_EatFlower completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_EatFlower")
        self.my_goal.cancel()



class BN_DetectObstacle(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_DetectObstacle")
        super(BN_DetectObstacle, self).__init__("BN_DetectObstacle")
        self.my_agent = aagent

    def initialise(self):
        pass

    def update(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        for index, value in enumerate(sensor_obj_info):
            if value:  # there is a hit with an object
                if value["tag"] != "Astronaut":
                    print("BN_DetectObstacle completed with SUCCESS")
                    return pt.common.Status.SUCCESS
        # print("No obstacle...")
        # print("BN_DetectObstacle completed with FAILURE")
        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass

class BN_Avoid(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_Avoid")
        super(BN_Avoid, self).__init__("BN_Avoid")
        self.my_agent = aagent

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.Avoid(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("BN_Avoid completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("BN_Avoid completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_Avoid")
        self.my_goal.cancel()


class HungryTimer(pt.behaviour.Behaviour):
    def __init__(self, agent , current_time, name="HungryTimer"):
        super(HungryTimer, self).__init__(name)
        self.agent = agent
        self.agent.hungry = True
        self.start_time = current_time

    def initialise(self):
        pass

    def update(self):
        current_time = time.time()  # Get the current time
        if self.agent.hungry:
            print("Hungry completed with SUCCESS")
            return pt.common.Status.SUCCESS

        if not self.agent.hungry and current_time - self.start_time > 15:
            self.agent.hungry = True  # Set the hungry flag to True
            self.start_time = current_time  # Reset the timer
            print("Hungry completed with SUCCESS")
            return pt.common.Status.SUCCESS
        
        else:
            print("Hungry completed with FAILURE")
            return pt.common.Status.FAILURE

    def terminate(self, new_status):
        if new_status == pt.common.Status.INVALID:
            self.timer_started = False

class BN_DetectAstro(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_DetectAstro")
        super(BN_DetectAstro, self).__init__("BN_DetectAstro")
        self.my_agent = aagent
        self.my_agent.det_sensor = None

    def initialise(self):
        pass

    def update(self):
        sensor_obj_info = self.my_agent.rc_sensor.sensor_rays[Sensors.RayCastSensor.OBJECT_INFO]
        for index, value in enumerate(sensor_obj_info):
            if value:  # there is a hit with an object
                if value["tag"] == "Astronaut":  # If it is the astronaut
                    # print("Flower detected!")
                    self.my_agent.det_sensor = index
                    print("BN_DetectAstro completed with SUCCESS")
                    return pt.common.Status.SUCCESS
        # print("No flower...")
        #print("BN_Detect astronaut completed with FAILURE")
        return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        pass

class BN_FollowAstro(pt.behaviour.Behaviour):
    def __init__(self, aagent):
        self.my_goal = None
        print("Initializing BN_FollowAstro")
        super(BN_FollowAstro, self).__init__("BN_FollowAstro")
        self.my_agent = aagent

    def initialise(self):
        self.my_goal = asyncio.create_task(Goals_BT.FollowAstronaut(self.my_agent).run())

    def update(self):
        if not self.my_goal.done():
            return pt.common.Status.RUNNING
        else:
            res = self.my_goal.result()
            if res:
                print("BN_FollowAstro completed with SUCCESS")
                return pt.common.Status.SUCCESS
            else:
                print("BN_FollowAstro completed with FAILURE")
                return pt.common.Status.FAILURE

    def terminate(self, new_status: common.Status):
        # Finishing the behaviour, therefore we have to stop the associated task
        self.logger.debug("Terminate BN_FollowAstro")
        self.my_goal.cancel()



class BTCritter:
    def __init__(self, aagent):
        # py_trees.logging.level = py_trees.logging.Level.DEBUG

        self.aagent = aagent
        #self.hungry = True

        # VERSION 1
        # self.root = pt.composites.Sequence(name="Sequence", memory=True)
        # self.root.add_children([BN_TurnRandom(aagent),
        #                         BN_ForwardRandom(aagent),
        #                         BN_DoNothing(aagent)])

        # VERSION 2
        # self.root = pt.composites.Parallel("Parallel", policy=py_trees.common.ParallelPolicy.SuccessOnAll())
        # self.root.add_children([BN_ForwardRandom(aagent), BN_TurnRandom(aagent)])

        # VERSION 3 (with DetectFlower)
        current_time = time.time()
        hungry_timer = HungryTimer(self.aagent, current_time)

        eat_flower = pt.composites.Sequence(name="EatFlower", memory=True)
        eat_flower.add_children([hungry_timer, BN_EatFlower(aagent)])

        det_flower = pt.composites.Sequence(name="DetectFlower", memory=True)
        det_flower.add_children([BN_DetectFlower(aagent), eat_flower])
        
        roaming = pt.composites.Parallel("Parallel", policy=py_trees.common.ParallelPolicy.SuccessOnAll())
        roaming.add_children([BN_ForwardRandom(aagent), BN_TurnRandom(aagent)])

        det_avoid = pt.composites.Sequence(name="Detect_Avoid", memory=True)
        det_avoid.add_children([BN_DetectObstacle(aagent), BN_Avoid(aagent)])
        
        det_astro = pt.composites.Sequence(name="Detect_Follow", memory=True)
        det_astro.add_children([BN_DetectAstro(aagent), BN_FollowAstro(aagent)])
        
        self.root = pt.composites.Selector(name="Selector", memory=False)
        self.root.add_children([det_flower, det_astro, det_avoid, roaming])

        self.behaviour_tree = pt.trees.BehaviourTree(self.root)

    # Function to set invalid state for a node and its children recursively
    def set_invalid_state(self, node):
        node.status = pt.common.Status.INVALID
        for child in node.children:
            self.set_invalid_state(child)

    def stop_behaviour_tree(self):
        # Setting all the nodes to invalid, we force the associated asyncio tasks to be cancelled
        self.set_invalid_state(self.root)

    async def tick(self):
        self.behaviour_tree.tick()
        await asyncio.sleep(0)

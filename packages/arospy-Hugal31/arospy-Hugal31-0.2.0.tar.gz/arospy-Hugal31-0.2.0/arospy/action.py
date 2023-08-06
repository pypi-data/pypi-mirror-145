import actionlib
import asyncio
import logging
import rospy


_logger = logging.getLogger("arospy.action")


class SimpleActionClient:
    def __init__(self, ns, action_spec, event_loop=None):
        self.event_loop = event_loop if event_loop is not None else asyncio.get_running_loop()
        self.impl = actionlib.SimpleActionClient(ns, action_spec)
        self._done_cb = self._feedback_cb = self._active_cb = None

    async def wait_for_server(self, timeout=rospy.Duration()):
        return await self.event_loop.run_in_executor(None, self.impl.wait_for_server, timeout)

    def send_goal(self, goal, done_cb=None, active_cb=None, feedback_cb=None):
        self._done_cb = done_cb
        self._active_cb = active_cb
        self._feedback_cb = feedback_cb
        self.impl.send_goal(goal,
                            done_cb=self._inner_done_callback if done_cb is not None else None,
                            active_cb=self._inner_active_cb if active_cb is not None else None,
                            feedback_cb=self._inner_feedback_cb if feedback_cb is not None else None)

    async def send_goal_and_wait(self, goal, execute_timeout=rospy.Duration(), preempt_timeout=rospy.Duration()):
        self.send_goal(goal)
        if not await self.wait_for_result(execute_timeout):
            # preempt action
            _logger.debug("Canceling goal")
            self.cancel_goal()
            if await self.wait_for_result(preempt_timeout):
                _logger.debug("Preempt finished within specified preempt_timeout [%.2f]", preempt_timeout.to_sec())
            else:
                _logger.debug("Preempt didn't finish specified preempt_timeout [%.2f]", preempt_timeout.to_sec())
        return self.get_state()

    async def wait_for_result(self, timeout: rospy.Duration):
        return await self.event_loop.run_in_executor(None, self.impl.wait_for_result, timeout)

    @property
    def gh(self):
        return self.impl.gh

    @property
    def simple_state(self) -> actionlib.SimpleGoalState:
        return self.impl.simple_state

    def get_result(self):
        return self.impl.get_result()

    def get_state(self) -> actionlib.GoalStatus:
        return self.impl.get_state()

    def get_goal_status_text(self):
        return self.impl.get_goal_status_text()

    def cancel_goal(self):
        self.impl.cancel_goal()

    def cancel_all_goals(self):
        self.impl.cancel_all_goals()

    def cancel_goals_at_and_before_time(self, time):
        self.impl.cancel_goals_at_and_before_time(time)

    def stop_tracking_goal(self):
        self.impl.stop_tracking_goal()

    def _inner_active_cb(self):
        future = asyncio.run_coroutine_threadsafe(self._active_cb(), loop=self.event_loop)
        future.result()

    def _inner_feedback_cb(self, feedback):
        future = asyncio.run_coroutine_threadsafe(self._feedback_cb(feedback), loop=self.event_loop)
        future.result()

    def _inner_done_callback(self, status: actionlib.GoalStatus, result):
        future = asyncio.run_coroutine_threadsafe(self._done_cb(status, result), loop=self.event_loop)
        future.result()

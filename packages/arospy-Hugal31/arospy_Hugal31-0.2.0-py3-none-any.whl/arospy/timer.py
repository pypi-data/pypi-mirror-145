import asyncio
import genpy
from typing import Optional, Union
import rospy


class Rate(rospy.Rate):
    async def sleep(self):
        """
        :note Copy-pasted from rospy.timer
        """
        curr_time = rospy.rostime.get_rostime()
        try:
            await sleep(self._remaining(curr_time))
        except rospy.exceptions.ROSTimeMovedBackwardsException:
            if not self._reset:
                raise
            self.last_time = rospy.rostime.get_rostime()
            return
        self.last_time = self.last_time + self.sleep_dur

        # detect time jumping forwards, as well as loops that are
        # inherently too slow
        if curr_time - self.last_time > self.sleep_dur * 2:
            self.last_time = curr_time


async def sleep(duration: Union[float, genpy.Duration], loop: Optional[asyncio.AbstractEventLoop] = None):
    """
    Sleep for a given duration, using the ROS clock if needed (i.e. if /use_sim_time == True).
    :param duration: The duration to sleep for.
    :param loop: An event loop
    """
    if rospy.rostime.is_wallclock():
        if isinstance(duration, genpy.Duration):
            duration = duration.to_sec()

        await asyncio.sleep(duration, loop=loop)

    else:
        if loop is None:
            loop = asyncio.get_running_loop()

        await loop.run_in_executor(None, rospy.timer.sleep, duration)

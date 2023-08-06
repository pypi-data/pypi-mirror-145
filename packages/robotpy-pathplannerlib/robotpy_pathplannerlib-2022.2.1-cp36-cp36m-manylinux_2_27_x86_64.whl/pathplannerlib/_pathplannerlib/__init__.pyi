import pathplannerlib._pathplannerlib
import typing
import wpimath._controls._controls.trajectory
import wpimath.geometry._geometry

__all__ = [
    "GeometryUtil",
    "PathPlanner",
    "PathPlannerTrajectory"
]


class GeometryUtil():
    def __init__(self) -> None: ...
    @staticmethod
    def cubicLerp(a: wpimath.geometry._geometry.Translation2d, b: wpimath.geometry._geometry.Translation2d, c: wpimath.geometry._geometry.Translation2d, d: wpimath.geometry._geometry.Translation2d, t: float) -> wpimath.geometry._geometry.Translation2d: ...
    @staticmethod
    def isFinite(u: meters) -> bool: ...
    @staticmethod
    def isNaN(u: meters) -> bool: ...
    @staticmethod
    def modulo(a: degrees, b: degrees) -> degrees: ...
    @staticmethod
    def quadraticLerp(a: wpimath.geometry._geometry.Translation2d, b: wpimath.geometry._geometry.Translation2d, c: wpimath.geometry._geometry.Translation2d, t: float) -> wpimath.geometry._geometry.Translation2d: ...
    @staticmethod
    def rotationLerp(startVal: wpimath.geometry._geometry.Rotation2d, endVal: wpimath.geometry._geometry.Rotation2d, t: float) -> wpimath.geometry._geometry.Rotation2d: ...
    @staticmethod
    def translationLerp(startVal: wpimath.geometry._geometry.Translation2d, endVal: wpimath.geometry._geometry.Translation2d, t: float) -> wpimath.geometry._geometry.Translation2d: ...
    @staticmethod
    @typing.overload
    def unitLerp(startVal: meters, endVal: meters, t: float) -> meters: ...
    @staticmethod
    @typing.overload
    def unitLerp(startVal: meters_per_second, endVal: meters_per_second, t: float) -> meters_per_second: ...
    @staticmethod
    @typing.overload
    def unitLerp(startVal: meters_per_second_squared, endVal: meters_per_second_squared, t: float) -> meters_per_second_squared: ...
    @staticmethod
    @typing.overload
    def unitLerp(startVal: radians_per_meter, endVal: radians_per_meter, t: float) -> radians_per_meter: ...
    @staticmethod
    @typing.overload
    def unitLerp(startVal: radians_per_second, endVal: radians_per_second, t: float) -> radians_per_second: ...
    @staticmethod
    @typing.overload
    def unitLerp(startVal: radians_per_second_squared, endVal: radians_per_second_squared, t: float) -> radians_per_second_squared: ...
    @staticmethod
    @typing.overload
    def unitLerp(startVal: seconds, endVal: seconds, t: float) -> seconds: ...
    pass
class PathPlanner():
    def __init__(self) -> None: ...
    @staticmethod
    @typing.overload
    def loadPath(name: str, maxVel: meters_per_second, maxAccel: meters_per_second_squared) -> PathPlannerTrajectory: ...
    @staticmethod
    @typing.overload
    def loadPath(name: str, maxVel: meters_per_second, maxAccel: meters_per_second_squared, reversed: bool) -> PathPlannerTrajectory: ...
    resolution = 0.004
    pass
class PathPlannerTrajectory():
    class PathPlannerState():
        def __init__(self) -> None: ...
        def interpolate(self, endVal: PathPlannerTrajectory.PathPlannerState, t: float) -> PathPlannerTrajectory.PathPlannerState: ...
        @property
        def acceleration(self) -> meters_per_second_squared:
            """
            :type: meters_per_second_squared
            """
        @property
        def angularAccel(self) -> radians_per_second_squared:
            """
            :type: radians_per_second_squared
            """
        @property
        def angularVel(self) -> radians_per_second:
            """
            :type: radians_per_second
            """
        @property
        def curveRadius(self) -> meters:
            """
            :type: meters
            """
        @property
        def deltaPos(self) -> meters:
            """
            :type: meters
            """
        @property
        def holonomicRotation(self) -> wpimath.geometry._geometry.Rotation2d:
            """
            :type: wpimath.geometry._geometry.Rotation2d
            """
        @property
        def pose(self) -> wpimath.geometry._geometry.Pose2d:
            """
            :type: wpimath.geometry._geometry.Pose2d
            """
        @property
        def position(self) -> meters:
            """
            :type: meters
            """
        @property
        def time(self) -> seconds:
            """
            :type: seconds
            """
        @property
        def velocity(self) -> meters_per_second:
            """
            :type: meters_per_second
            """
        pass
    class Waypoint():
        def __init__(self, anchorPoint: wpimath.geometry._geometry.Translation2d, prevControl: wpimath.geometry._geometry.Translation2d, nextControl: wpimath.geometry._geometry.Translation2d, velocityOverride: meters_per_second, holonomicRotation: wpimath.geometry._geometry.Rotation2d, isReversal: bool) -> None: ...
        @property
        def anchorPoint(self) -> wpimath.geometry._geometry.Translation2d:
            """
            :type: wpimath.geometry._geometry.Translation2d
            """
        @property
        def holonomicRotation(self) -> wpimath.geometry._geometry.Rotation2d:
            """
            :type: wpimath.geometry._geometry.Rotation2d
            """
        @property
        def isReversal(self) -> bool:
            """
            :type: bool
            """
        @isReversal.setter
        def isReversal(self, arg0: bool) -> None:
            pass
        @property
        def nextControl(self) -> wpimath.geometry._geometry.Translation2d:
            """
            :type: wpimath.geometry._geometry.Translation2d
            """
        @property
        def prevControl(self) -> wpimath.geometry._geometry.Translation2d:
            """
            :type: wpimath.geometry._geometry.Translation2d
            """
        @property
        def velocityOverride(self) -> meters_per_second:
            """
            :type: meters_per_second
            """
        pass
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, states: typing.List[PathPlannerTrajectory.PathPlannerState]) -> None: ...
    @typing.overload
    def __init__(self, waypoints: typing.List[PathPlannerTrajectory.Waypoint], maxVelocity: meters_per_second, maxAcceleration: meters_per_second_squared, reversed: bool) -> None: ...
    def asWPILibTrajectory(self) -> wpimath._controls._controls.trajectory.Trajectory: ...
    def getEndState(self) -> PathPlannerTrajectory.PathPlannerState: ...
    def getInitialState(self) -> PathPlannerTrajectory.PathPlannerState: ...
    def getState(self, i: int) -> PathPlannerTrajectory.PathPlannerState: ...
    def getStates(self) -> typing.List[PathPlannerTrajectory.PathPlannerState]: ...
    def getTotalTime(self) -> seconds: ...
    def numStates(self) -> int: ...
    def sample(self, time: seconds) -> PathPlannerTrajectory.PathPlannerState: ...
    pass

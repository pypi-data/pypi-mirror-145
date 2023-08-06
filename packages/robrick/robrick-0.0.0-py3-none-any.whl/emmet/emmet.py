import hub  # noqa: E402
import time


def time_function(f, *args, **kwargs):
    """
    Decorator to time a function.
    """
    start = time.ticks_ms()
    result = f(*args, **kwargs)
    diff = time.ticks_diff(start, time.ticks_ms())
    print(f"{f.__name__} took {diff:.2f} ms")

    return result


class RemoteControl:
    pass


class Device:
    def __init__(self, port):
        self._port = getattr(hub, port)

    def is_connected(self):
        return self._port.device is not None

    def is_motor(self):
        return self._port.motor is not None

    @property
    def data(self):
        return self._port.device.get()

    @property
    def info(self):
        return self._port.info()


class ColorLightMatrix(Device):
    id = "color_light_matrix"


class ColorSensor(Device):
    id = "color_sensor"


class DistanceSensor(Device):
    id = "distance_sensor"


class ForceSensor(Device):
    id = "force_sensor"


class Motor(Device):
    pass


class MotorS(Motor):
    id = "motor_s"


class MotorM(Motor):
    id = "motor_m"


class MotorL(Motor):
    id = "motor_l"


def get_device_class(type_id):
    try:
        return {
            48: MotorM,
            49: MotorL,
            61: ColorSensor,
            62: DistanceSensor,
            63: ForceSensor,
            64: ColorLightMatrix,
            65: MotorS,
        }[type_id]
    except KeyError:
        return Device


class Robot:
    _devices = {}
    hub_front_side = hub.FRONT
    hub_top_side = hub.TOP

    def __init__(self):
        hub.motion.align_to_model(top=self.hub_top_side, front=self.hub_front_side, nsamples=1000)

        # check connected devices
        for port in ["A", "B", "C", "D", "E", "F"]:
            device = Device(port)

            if device.is_connected():
                self._devices[port] = get_device_class(device.info["type"])(port)
                print(port, self._devices[port].id)  # TODO: remove this

    def off(self):
        hub.power_off(fast=True, restart=False)

    def on(self):
        """
        Start listening to external inputs (devices) data and react accordingly.
        Include here the basic Robot logic.
        """
        raise NotImplementedError


class MotorizedRobot(Robot):
    driving_motor_port = None

    def __init__(self):
        super().__init__()

        if not self.driving_motor_port or not isinstance(self._devices[self.driving_motor_port], Motor):
            raise AttributeError("Make sure that `driving_motor_port` is a valid port with a motor attached.")

    @property
    def driving_motor(self):
        return self._devices[self.driving_motor_port]

    def brake(self):
        self.driving_motor.brake()

    def run(self):
        self.driving_motor.run_for_time(10)

    def stop(self):
        raise NotImplementedError


class SteeredRobot(MotorizedRobot):
    steering_motor_port = None

    def __init__(self):
        super().__init__()

        if not self.steering_motor_port or not isinstance(self._devices[self.steering_motor_port], Motor):
            raise AttributeError("Make sure that `steering_motor_port` is a valid port with a motor attached.")

        self.steering_motor.preset()

    @property
    def steering_motor(self):
        return self._devices[self.steering_motor_port]

    def turn_left(self, degrees):
        self.steering_motor.run_to_position(degrees)

    def turn_right(self, degrees):
        self.steering_motor.run_to_position(-degrees)


class BikeRobot(SteeredRobot):
    wheel_base = 100  # currently not used
    wheel_radius = 100  # currently not used

    def on(self):
        """
        BikeRobot moves forwars and it self balances at the same time.
        It can turn also, but it needs to build some speed not to fall.
        An optional leg can help it stand when it stops.
        """
        pass


class CarRobot(SteeredRobot):
    """
    https://antonsmindstorms.com/2021/06/19/how-to-remote-control-lego-spike-prime-and-robot-inventor-with-python/
    """

    def on(self):
        """
        CarRobot moves forward and can be steered.
        """
        while True:
            self.driving_motor.run()
            self.steering_motor.turn_left(10)
            time.sleep(2)
            self.steering_motor.turn_right(10)
            print("driving:", self.driving_motor.data)
            print("steering:", self.steering_motor.data)


class SelfBalancingRobot(Robot):
    pass


class WalkingRobot(Robot):
    pass


# how to use

class Buggy(CarRobot):
    driving_motor_port = "A"
    steering_motor_port = "B"


buggy = Buggy()
buggy.on()
time.sleep(10)
buggy.off()

raise SystemExit

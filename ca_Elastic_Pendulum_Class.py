import numpy as np
import math
import scipy.constants as const


class ElasticPendulum:
    # In this class I'll define an elastic pendulum in 2D in polar coordinates, i.e., self.position[0] is the radius and self.position[1] is the azimuth
    # therefore, self.velocity[1] is the angular speed
        # The pole is at the point of suspension; the polar axis is vertically bellow the pole, where anti-clockwise movement is positive.
    def __init__(
            self,
            name='Elastic Pendulum',
            mass=2, # mass of the mass attached to the spring
            k=20, # spring constant
            length=10, # length of the spring at rest
            position=np.array([0, 0], dtype=float),
            velocity=np.array([0, 0], dtype=float),
            acceleration=np.array([0, 0], dtype=float)
                ):
        self.name = name
        self.mass = mass
        self.k = k
        self.length = length
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.acceleration = np.array(acceleration, dtype=float)
        self.rest_position = length+mass*const.g/k # r when mass is at rest, i.e., weight = spring force


    def __str__(self): # this would be to give the information of the point mass, but i won't be using it
        return "Particle: {0}, Mass: {1:.3e}, Position: {2}, Velocity: {3}, Acceleration: {4}".format(
            self.name, self.mass, self.position, self.velocity, self.acceleration
            )
    

    def update_acceleration(self): # using F=ma, Hooke's law and W=mg
        self.acceleration[0] = (self.position[0] * self.velocity[1]**2) - (self.k * (self.position[0] - self.length) / self.mass) + (const.g * math.cos(self.position[1]))
        self.acceleration[1] = - (const.g * math.sin(self.position[1]) / self.position[0]) - (2 * self.velocity[0] * self.velocity[1] / self.position[0])


    def forward_euler(self, dt): # calculating velocity and position using the forward-euler method
        self.position += self.velocity * dt
        self.velocity += self.acceleration * dt


    def euler_cromer(self, dt): # calculating velocity and position using the forward-euler-cromer method
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt


    def midpoint(self, dt): # i ended up not using this since midpoint_3rd_attempt was givving better values after being tested with energy conservation
        initial_acceceleration = self.acceleration
        initial_velocity = self.velocity
        initial_position = self.position

        acceleration_at_midpoint = initial_acceceleration + 0.5 * initial_acceceleration * dt
        velocity_at_midpoint = initial_velocity + 0.5 * initial_velocity * dt

        self.velocity = initial_velocity + acceleration_at_midpoint * dt
        self.position = initial_position + velocity_at_midpoint * dt


    def midpoint_2nd_attempt(self, dt): # i ended up not using this since midpoint_3rd_attempt was givving better values after being tested with energy conservation
        initial_position = self.position
        initial_velocity = self.velocity
        initial_acceleration = self.acceleration
        final_velocity = initial_acceleration * dt # this is just an approximation of the final velocity to get the value of the midpoint of acceleration


        acceleration_at_midpoint = ( final_velocity - initial_velocity ) / dt
        velocity_at_midpoint = initial_velocity + 0.5 * initial_acceleration * dt

        self.velocity = initial_velocity + acceleration_at_midpoint * dt
        self.position = initial_position + velocity_at_midpoint * dt


    def midpoint_3rd_attempt(self, dt): # calculating velocity and position using the midpoint method
        initial_velocity = self.velocity
        initial_acceleration = self.acceleration

        velocity_at_midpoint = initial_velocity + 0.5 * initial_acceleration * dt

        self.velocity += self.acceleration * dt
        self.position += velocity_at_midpoint * dt


    def midpoint_4th_attempt(self, dt): # i ended up not using this since midpoint_3rd_attempt was givving better values after being tested with energy conservation
        initial_position = self.position
        initial_velocity = self.velocity
        initial_acceleration = self.acceleration

        velocity_at_midpoint = initial_velocity + 0.5 * initial_acceleration * dt

        self.position += velocity_at_midpoint * dt
        self.velocity = ( 2 * ( self.position - initial_position ) / dt ) - initial_velocity


    def E_k(self):
        # Calculating the pendulum's kinetic energy using the formula:
        # E = 0.5 * m * v ^2, where v = angular speed * radius
        return 0.5 * self.mass * ( ( self.velocity[1] * self.position[0] )**2 + self.velocity[0]**2 )
    

    def E_gp(self):
        # Calculating the pendulum's gravitational potential energy using the formula:
        # E = m * g * h, where h = radius * cos( azimuth )
        return self.mass * const.g * (self.rest_position - self.position[0] * math.cos(self.position[1]))
    

    def E_ep(self):
        # Calculating the pendulum's elastic potential energy using the formula:
        # E = 0.5 * k * change in position, where change in position = radius - length (sine is only moving in 1D)
        return 0.5 * self.k * ( self.position[0] - self.length )**2
    

    def E_T(self):
        # Calculating total energy
        return 0.5 * self.mass * ( ( self.velocity[1] * self.position[0] )**2 + self.velocity[0]**2 )   +   self.mass * const.g * (self.rest_position - self.position[0] * math.cos(self.position[1]))   +   0.5 * self.k * ( self.position[0] - self.length )**2


    def momentum_1(self):
        # calculating momentum using (x,y) coordinates, i.e., momentum = m * v
        x_velocity = self.velocity[0] * math.sin(self.position[1]) + self.position[0] * math.cos(self.position[1])
        y_velocity = self.velocity[0] * math.cos(self.position[1]) - self.position[0] * math.sin(self.position[1])
        return self.mass * math.sqrt( x_velocity**2 + y_velocity**2 )
    

    def momentum_2(self):
        # calculating the momentum of the point mass attached to the elastic pendulum
        # however, since the momentum of the spring isn't being considered, we can't use the momentum to test the coding, since the momentum of just the point mass itself isn't conserved
        return self.mass * math.sqrt( ( self.velocity[1] * self.position[0] )**2 + self.velocity[0]**2 )


######################################################################################################################################################################################################################################



"""
Copyright 2023 Ethan Christensen

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import math
import random
from typing import List
from bruhcolor import bruhcolored as bc
from .base_effect import BaseEffect
from ..bruhutil.bruhffer import Buffer
from ..bruhutil.bruhtypes import (
    FireworkType,
    valid_firework_types,
    FireworkColorType,
    valid_firework_color_types,
    two_tone_colors,
)


class Particle:
    def __init__(self, x, y, dx, dy, width, height, symbol="*", life: int = None):
        self.x = x
        self.y = y
        self.previous_x = x
        self.previous_y = y
        self.dx = dx
        self.dy = dy
        self.width = width
        self.height = height
        self.life = life if life else random.randint(8, 15)  # Random lifespan for particle
        self.symbol = symbol

    def update(self):
        # Update position
        self.previous_x = self.x
        self.previous_y = self.y
        self.x += self.dx
        self.y += self.dy
        # Apply gravity to simulate a slight downward motion
        self.dy += 0.05
        # Decrease life
        self.life -= 1
        # Flicker effect
        if random.random() > 0.5:
            self.symbol = "*" if self.symbol == "." else "."

    def is_alive(self):
        # Particle is alive if it has life left and is within bounds
        return (
            self.life > 0
            and 0 <= int(self.x) < self.width
            and 0 <= int(self.y) < self.height
        )


class Firework:
    def __init__(self, firework_type: FireworkType, height, width, firework_color_type: str = None, color_enabled: bool = False, allowed_firework_types: List[str] = None):
        self.width = width
        self.height = height
        self.x = random.randint(0, self.width - 1)
        self.y = height - 1
        self.previous_x = self.x
        self.previous_y = self.y
        self.peak = random.randint(5, self.height // 2)
        self.exploded = False
        self.particles = []
        self.allowed_fire_work_types = allowed_firework_types or valid_firework_types
        self.explosion_type = (
            firework_type
            if (firework_type != "random" and firework_type in valid_firework_types)
            else random.choice(self.allowed_fire_work_types)
        )
        self.clear_particles = []
        self.caught_last_trail = False
        self.speed = 3
        self.firework_color_type = firework_color_type
        self.colors = self.get_colors()
        self.color_enabled = color_enabled

        self.trajectory_type = random.choice(['straight', 'arc', 'zigzag'])
        self.angle = random.uniform(-0.5, 0.5)  # Angle for non-straight trajectories
        self.arc_direction = random.choice([-1, 1])  # Direction of arc curve
        self.zigzag_phase = 0  # For zigzag pattern
        self.zigzag_amplitude = random.uniform(0.2, 0.5)  # Width of zigzag

    def update(self):
        if not self.exploded:
            # Store previous position
            self.previous_x = self.x
            self.previous_y = self.y
            
            # Update position based on trajectory type
            if self.trajectory_type == 'straight':
                self.move_straight()
            elif self.trajectory_type == 'arc':
                self.move_arc()
            else:  # zigzag
                self.move_zigzag()
            
            # Check if reached peak
            if self.y <= self.peak:
                self.exploded = True
                self.create_particles()
        else:
            # Update particles
            for particle in self.particles:
                particle.update()
            # Remove dead particles
            for p in self.particles:
                if not p.is_alive():
                    self.clear_particles.append(p)

            self.particles = [p for p in self.particles if p.is_alive()]

    def move_straight(self):
        # Move upward with slight angle
        self.y -= self.speed
        self.x += math.sin(self.angle) * self.speed * 0.5

    def move_arc(self):
        # Create arcing trajectory
        progress = (self.height - self.y) / (self.height - self.peak)
        arc_offset = math.sin(progress * math.pi) * 2.0
        self.y -= self.speed
        self.x += self.arc_direction * arc_offset * 0.2

    def move_zigzag(self):
        # Create zigzag pattern
        self.zigzag_phase += 0.2
        self.y -= self.speed
        self.x += math.sin(self.zigzag_phase) * self.zigzag_amplitude

    def create_particles(self):
        if self.explosion_type == 'circular':
            self.circular_explosion()
        elif self.explosion_type == 'ring':
            self.ring_explosion()
        elif self.explosion_type == 'starburst':
            self.starburst_explosion()
        elif self.explosion_type == 'cone':
            self.cone_explosion()
        elif self.explosion_type == 'spiral':
            self.spiral_explosion()
        elif self.explosion_type == 'wave':
            self.wave_explosion()
        elif self.explosion_type == 'burst':
            self.burst_explosion()
        elif self.explosion_type == 'cross':
            self.cross_explosion()
        elif self.explosion_type == "flower":
            self.flower_explosion()
        elif self.explosion_type == "doublering":
            self.double_ring_explosion()
        elif self.explosion_type == "heart":
            self.heart_explosion()
        elif self.explosion_type == "star":
            self.star_explosion()
        elif self.explosion_type == "fireball":
            self.fireball_explosion()
        elif self.explosion_type == "diamond":
            self.diamond_explosion()
        elif self.explosion_type == "shockwave":
            self.burst_with_shockwave_explosion()
        elif self.explosion_type == "snowflake":
            self.snowflake_explosion()
        elif self.explosion_type == "cluster":
            self.cluster_explosion()
        elif self.explosion_type == "comet":
            self.comet_tail_explosion()
        elif self.explosion_type == "willow":
            self.willow_explosion()
        elif self.explosion_type == "dna":
            self.dna_explosion()
        elif self.explosion_type == "infinity":
            self.infinity_explosion()
        elif self.explosion_type == "galaxy":
            self.galaxy_explosion()
        elif self.explosion_type == "phoenix":
            self.phoenix_explosion()
        elif self.explosion_type == "fountain":
            self.fountain_explosion()
        elif self.explosion_type == "butterfly":
            self.butterfly_explosion()
        elif self.explosion_type == "dragon":
            self.dragon_explosion()
        elif self.explosion_type == "tornado":
            self.tornado_explosion()
        elif self.explosion_type == "matrix":
            self.matrix_explosion()
        elif self.explosion_type == "portal":
            self.portal_explosion()
        
    def circular_explosion(self):
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 1.5)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))

    def ring_explosion(self):
        for angle in range(0, 360, 12):  # Ring pattern with evenly spaced particles
            rad = math.radians(angle)
            dx = math.cos(rad)
            dy = math.sin(rad)
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))

    def starburst_explosion(self):
        for angle in range(
            0, 360, 45
        ):  # Starburst with particles in specific directions
            rad = math.radians(angle)
            speed = random.uniform(1, 1.5)
            dx = math.cos(rad) * speed
            dy = math.sin(rad) * speed
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))

    def cone_explosion(self):
        for _ in range(20):
            angle = random.uniform(
                -math.pi / 6, math.pi / 6
            )  # Narrow range for cone shape
            speed = random.uniform(0.5, 1.5)
            dx = math.cos(angle) * speed
            dy = -abs(math.sin(angle) * speed)  # Force particles upward
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))

    def spiral_explosion(self):
        for i in range(20):
            angle = i * 0.3  # Gradually increasing angle for spiral effect
            speed = 0.1 * i  # Particles spread out as the spiral grows
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))

    def wave_explosion(self):
        for i in range(30):
            angle = i * 0.2  # Slightly increase angle for wave effect
            speed = random.uniform(0.5, 1.0)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed * 0.5  # Particles move slower upward
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))

    def burst_explosion(self):
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)  # Random angles for burst
            speed = random.uniform(0.5, 1.5)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))
        # Particles gradually fall downward after a burst
        for particle in self.particles:
            particle.dy += 0.5  # Increase downward velocity

    def cross_explosion(self):
        for angle in [0, 90, 180, 270]:  # Particles in cross directions
            rad = math.radians(angle)
            speed = random.uniform(0.5, 1.5)
            dx = math.cos(rad) * speed
            dy = math.sin(rad) * speed
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))

    def flower_explosion(self):
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            speed = random.uniform(0.5, 1.0)
            dx = math.cos(rad) * speed
            dy = math.sin(rad) * speed
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))
            # Add smaller "petal" particles around each main particle
            for petal_angle in [-0.1, 0.1]:
                dx_petal = math.cos(rad + petal_angle) * (speed * 0.7)
                dy_petal = math.sin(rad + petal_angle) * (speed * 0.7)
                self.particles.append(Particle(self.x, self.y, dx_petal, dy_petal, self.width, self.height))
    
    def double_ring_explosion(self):
        for radius_multiplier in [0.8, 1.2]:  # Two rings at slightly different radii
            for angle in range(0, 360, 15):
                rad = math.radians(angle)
                speed = 1.0 * radius_multiplier
                dx = math.cos(rad) * speed
                dy = math.sin(rad) * speed
                self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))

    def heart_explosion(self):
        for t in range(0, 360, 10):  # Parametric heart shape
            rad = math.radians(t)
            dx = 16 * math.sin(rad) ** 3 * 0.1
            dy = -(13 * math.cos(rad) - 5 * math.cos(2 * rad) - 2 * math.cos(3 * rad) - math.cos(4 * rad)) * 0.05
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))
    
    def star_explosion(self):
        for i in range(5):  # 5-point star
            angle = i * 2 * math.pi / 5
            dx = math.cos(angle) * 1.5
            dy = math.sin(angle) * 1.5
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))
            # Add particles in opposite direction for a sharper effect
            self.particles.append(Particle(self.x, self.y, -dx, -dy, self.width, self.height))
    
    def fireball_explosion(self):
        for _ in range(50):  # Dense number of particles
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.2, 1.5)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))
    
    def diamond_explosion(self):
        for angle in [45, 135, 225, 315]:  # Four main directions for diamond points
            rad = math.radians(angle)
            dx = math.cos(rad) * 1.5
            dy = math.sin(rad) * 1.5
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))
            # Add smaller particles near each main point for a thicker diamond shape
            for offset in [-0.1, 0.1]:
                dx_offset = math.cos(rad + offset) * 1.2
                dy_offset = math.sin(rad + offset) * 1.2
                self.particles.append(Particle(self.x, self.y, dx_offset, dy_offset, self.width, self.height))

    def burst_with_shockwave_explosion(self):
        # Main burst particles
        for angle in range(0, 360, 20):
            rad = math.radians(angle)
            speed = random.uniform(0.8, 1.2)
            dx = math.cos(rad) * speed
            dy = math.sin(rad) * speed
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))
        
        # Shockwave particles in a ring around the burst
        for angle in range(0, 360, 5):
            rad = math.radians(angle)
            dx = math.cos(rad) * 1.5
            dy = math.sin(rad) * 1.5
            self.particles.append(Particle(self.x, self.y, dx * 0.5, dy * 0.5, self.width, self.height, life=5))  # Short lifespan for shockwave

    def snowflake_explosion(self):
        for angle in range(0, 360, 60):  # Six main directions
            rad = math.radians(angle)
            speed = random.uniform(0.8, 1.0)
            dx = math.cos(rad) * speed
            dy = math.sin(rad) * speed
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))
            
            # Small branches off each main point for the snowflake effect
            for branch_angle in [-15, 15]:  # Offset angles for branches
                rad_branch = rad + math.radians(branch_angle)
                dx_branch = math.cos(rad_branch) * (speed * 0.6)
                dy_branch = math.sin(rad_branch) * (speed * 0.6)
                self.particles.append(Particle(self.x, self.y, dx_branch, dy_branch, self.width, self.height))
    
    def cluster_explosion(self):
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            speed = 1.2
            dx = math.cos(rad) * speed
            dy = math.sin(rad) * speed
            main_particle = Particle(self.x, self.y, dx, dy, self.width, self.height)
            self.particles.append(main_particle)
            
            # Surround each main particle with smaller "cluster" particles
            for _ in range(6):
                offset_dx = dx + random.uniform(-0.2, 0.2)
                offset_dy = dy + random.uniform(-0.2, 0.2)
                self.particles.append(Particle(self.x + offset_dx, self.y + offset_dy, offset_dx * 0.5, offset_dy * 0.5, self.width, self.height))
    
    def comet_tail_explosion(self):
        # Main comet direction
        comet_angle = random.choice([45, 135, 225, 315])  # Random diagonal angle for comet
        rad = math.radians(comet_angle)
        speed = 1.5
        main_dx = math.cos(rad) * speed
        main_dy = math.sin(rad) * speed
        
        for i in range(8):  # Comet particles along the main direction
            trail_dx = main_dx * (1 - i * 0.1)
            trail_dy = main_dy * (1 - i * 0.1)
            self.particles.append(Particle(self.x, self.y, trail_dx, trail_dy, self.width, self.height))
        
        # Small trailing particles
        for i in range(1, 5):  
            trail_dx = main_dx * 0.3
            trail_dy = main_dy * 0.3
            self.particles.append(Particle(self.x - trail_dx * i, self.y - trail_dy * i, trail_dx * 0.5, trail_dy * 0.5, self.width, self.height))

    def willow_explosion(self):
        num_arms = 10  # Number of branches in the willow effect
        angle_offset = 70  # Constrain angle range to mostly horizontal

        for i in range(num_arms):
            # Each arm has an angle mostly to the sides (slightly up or down)
            angle = random.uniform(-angle_offset, angle_offset) if i < num_arms / 2 else random.uniform(180 - angle_offset, 180 + angle_offset)
            rad = math.radians(angle)
            initial_speed = random.uniform(0.5, 1.0)
            
            # Calculate initial movement in a mostly horizontal direction
            dx = math.cos(rad) * initial_speed
            dy = math.sin(rad) * initial_speed * 0.3  # Smaller upward component for the drooping effect
            
            # Main particle at the start of each "arm"
            main_particle = Particle(self.x, self.y, dx, dy, self.width, self.height, life=25)
            self.particles.append(main_particle)
            
            # Trailing particles along each arm, curving downwards like branches
            for j in range(1, 6):
                # Reduce horizontal speed gradually, add downward pull for the arc
                arc_dx = dx * (1 - j * 0.1)  # Slightly reduce horizontal speed over time
                arc_dy = dy + j * 0.1        # Increase downward speed to mimic gravity
                trail_particle = Particle(self.x, self.y, arc_dx, arc_dy, self.width, self.height, life=25 - j * 8)
                self.particles.append(trail_particle)

    def dna_explosion(self):
        """Creates a double helix pattern resembling DNA structure"""
        num_points = 30
        radius = 1.0
        vertical_stretch = 0.5
        
        for i in range(num_points):
            t = (i / num_points) * 4 * math.pi  # Two complete rotations
            
            # First strand
            dx1 = math.cos(t) * radius
            dy1 = -vertical_stretch * t  # Negative for upward movement
            self.particles.append(Particle(self.x, self.y, dx1, dy1, self.width, self.height))
            
            # Second strand (offset by pi)
            dx2 = math.cos(t + math.pi) * radius
            dy2 = -vertical_stretch * t
            self.particles.append(Particle(self.x, self.y, dx2, dy2, self.width, self.height))
            
            # "Bridges" between strands (occasional connectors)
            if i % 4 == 0:
                dx_bridge = (dx1 + dx2) / 2
                dy_bridge = dy1
                self.particles.append(Particle(self.x, self.y, dx_bridge, dy_bridge, self.width, self.height, symbol="-"))

    def infinity_explosion(self):
        """Creates an infinity symbol (∞) pattern"""
        num_points = 40
        size = 1.2
        
        for i in range(num_points):
            t = (i / num_points) * 2 * math.pi
            
            # Parametric equations for infinity symbol
            dx = size * math.cos(t) / (1 + math.sin(t)**2)
            dy = size * math.sin(t) * math.cos(t) / (1 + math.sin(t)**2)
            
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))

    def galaxy_explosion(self):
        """Creates a spiral galaxy pattern with arms and central bulge"""
        # Central bulge
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.2, 0.5)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height, symbol="·"))
        
        # Spiral arms
        arms = 2
        for arm in range(arms):
            start_angle = (2 * math.pi * arm) / arms
            for i in range(30):
                radius = 0.1 + (i * 0.05)
                angle = start_angle + (i * 0.3)
                dx = math.cos(angle) * radius
                dy = math.sin(angle) * radius
                self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))

    def phoenix_explosion(self):
        """Creates a rising phoenix pattern with wings and tail"""
        # Central rising column
        for i in range(10):
            dy = -1.0 - (i * 0.1)  # Upward movement
            dx = random.uniform(-0.2, 0.2)
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height))
        
        # Wings
        wing_span = 15
        for i in range(wing_span):
            # Left wing
            angle_left = math.radians(150 - (i * 4))  # Sweep from 150° to 90°
            dx_left = math.cos(angle_left) * (i * 0.1)
            dy_left = math.sin(angle_left) * (i * 0.1)
            self.particles.append(Particle(self.x, self.y, dx_left, dy_left, self.width, self.height))
            
            # Right wing
            angle_right = math.radians(30 + (i * 4))  # Sweep from 30° to 90°
            dx_right = math.cos(angle_right) * (i * 0.1)
            dy_right = math.sin(angle_right) * (i * 0.1)
            self.particles.append(Particle(self.x, self.y, dx_right, dy_right, self.width, self.height))
        
        # Tail feathers
        for i in range(5):
            angle = math.radians(270 + random.uniform(-30, 30))
            speed = 0.5 + (i * 0.1)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height, symbol="~"))

    def fountain_explosion(self):
        """Creates an upward-shooting fountain pattern with cascading particles"""
        num_streams = 5
        particles_per_stream = 8
        
        for stream in range(num_streams):
            base_angle = -90 + random.uniform(-15, 15)  # Mostly upward
            base_speed = random.uniform(1.0, 1.5)
            
            for i in range(particles_per_stream):
                angle = math.radians(base_angle)
                speed = base_speed - (i * 0.1)  # Particles get slower toward end of stream
                
                dx = math.cos(angle) * speed
                dy = math.sin(angle) * speed
                
                # Add some slight random variation to each particle
                dx += random.uniform(-0.1, 0.1)
                dy += random.uniform(-0.1, 0.1)
                
                particle = Particle(
                    self.x, self.y, dx, dy, self.width, self.height,
                    symbol=":" if i < particles_per_stream // 2 else ".",
                    life=20 - i  # Particles at end of stream die sooner
                )
                self.particles.append(particle)

    def butterfly_explosion(self):
        """Creates a butterfly pattern with wings that flutter"""
        # Wing shape parameters
        wing_points = 20
        flutter_speed = 0.2
        
        for i in range(wing_points):
            t = (i / wing_points) * 2 * math.pi
            
            # Parametric equations for wing shape (modified heart curve)
            base_dx = math.sin(t) * (math.exp(math.cos(t)) - 2*math.cos(4*t))
            base_dy = math.cos(t) * (math.exp(math.cos(t)) - 2*math.cos(4*t))
            
            # Create left and right wings with flutter effect
            for side in [-1, 1]:  # Left and right wings
                dx = base_dx * side * 0.3
                dy = base_dy * 0.3
                
                # Add flutter movement
                dx += math.sin(t * flutter_speed) * 0.1
                
                particle = Particle(self.x, self.y, dx, dy, self.width, self.height, 
                                symbol="·" if i % 2 == 0 else "*",
                                life=random.randint(15, 25))
                self.particles.append(particle)
            
            # Add body particles
            if i < 5:
                self.particles.append(Particle(self.x, self.y, 0, i*0.1, 
                                            self.width, self.height, symbol="█"))

    def dragon_explosion(self):
        """Creates a dragon shape with body, wings, and fire breath"""
        # Body
        body_length = 15
        for i in range(body_length):
            angle = math.radians(random.uniform(-10, 10))  # Slight wiggle
            dx = math.cos(angle) * 0.3
            dy = -0.5 + (i * 0.05)  # Curves upward
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height, 
                                        symbol="▲", life=20))
        
        # Wings
        wing_span = 12
        for i in range(wing_span):
            # Left and right wings
            for side in [-1, 1]:
                angle = math.radians(45 * side)
                dx = math.cos(angle) * (i * 0.15) * side
                dy = math.sin(angle) * (i * 0.1) - 0.5
                self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height,
                                            symbol="*", life=15))
        
        # Fire breath
        breath_particles = 20
        for i in range(breath_particles):
            angle = math.radians(random.uniform(-30, 30))
            speed = random.uniform(1.0, 2.0)
            dx = math.cos(angle) * speed
            dy = -math.sin(angle) * speed  # Upward fire breath
            symbol = random.choice(["^", "*", "●"])
            self.particles.append(Particle(self.x, self.y, dx, dy, self.width, self.height,
                                        symbol=symbol, life=10))

    def tornado_explosion(self):
        """Creates a spinning tornado effect that grows wider at the top"""
        height_layers = 15
        base_radius = 0.2
        
        for layer in range(height_layers):
            radius = base_radius + (layer * 0.1)  # Gets wider as it goes up
            particles_in_layer = int(6 + layer * 1.5)  # More particles in higher layers
            
            for p in range(particles_in_layer):
                angle = (p / particles_in_layer) * 2 * math.pi
                # Add spin effect
                angle += layer * 0.5
                
                dx = math.cos(angle) * radius
                dy = -1 + (layer * 0.1)  # Upward movement, slowing at top
                
                # Vary the symbols based on position
                symbol = "●" if layer < 3 else ("*" if layer < 10 else "·")
                
                particle = Particle(self.x, self.y, dx, dy, self.width, self.height,
                                symbol=symbol, life=20-layer)
                self.particles.append(particle)

    def matrix_explosion(self):
        """Creates a Matrix-style digital rain effect"""
        num_streams = 15
        chars_per_stream = 8
        
        for stream in range(num_streams):
            # Calculate stream position
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0.5, 2.0)
            base_dx = math.cos(angle) * distance
            base_dy = math.sin(angle) * distance
            
            for i in range(chars_per_stream):
                # Delay each character in stream
                dx = base_dx
                dy = base_dy + (i * 0.15)
                
                # Use Matrix-like symbols
                symbol = random.choice(['0', '1', '█', '▀', '▄', '■', '░', '▒', '▓'])
                
                # Particles later in stream die sooner
                life = 20 - i
                
                self.particles.append(Particle(self.x, self.y, dx, dy, 
                                            self.width, self.height,
                                            symbol=symbol, life=life))

    def portal_explosion(self):
        """Creates two connected portals with particles flowing between them"""
        # Portal parameters
        portal_radius = 1.2
        num_particles = 50
        
        # Create two portal rings
        for portal in range(2):
            angle_offset = math.pi * portal  # Second portal on opposite side
            distance = 2.0  # Distance between portals
            
            # Portal position
            portal_x = math.cos(angle_offset) * distance
            portal_y = math.sin(angle_offset) * distance
            
            # Create portal ring
            for i in range(12):
                angle = (i / 12) * 2 * math.pi
                dx = portal_x + math.cos(angle) * portal_radius
                dy = portal_y + math.sin(angle) * portal_radius
                
                self.particles.append(Particle(self.x, self.y, dx*0.2, dy*0.2,
                                            self.width, self.height,
                                            symbol="O", life=25))
        
        # Particles flowing between portals
        for _ in range(num_particles):
            t = random.uniform(0, 1)  # Position along path
            
            # Curved path between portals
            dx = math.cos(t * math.pi * 2) * portal_radius
            dy = math.sin(t * math.pi * 2) * portal_radius
            
            # Add some randomness to path
            dx += random.uniform(-0.2, 0.2)
            dy += random.uniform(-0.2, 0.2)
            
            symbol = random.choice(["*", "·", "•", "+"])
            self.particles.append(Particle(self.x, self.y, dx*0.3, dy*0.3,
                                        self.width, self.height,
                                        symbol=symbol, life=10))

    def is_active(self):
        # Firework is active if it has not exploded or if particles are still alive
        return not self.exploded or len(self.particles) > 0

    def get_colors(self):
        if self.firework_color_type == "solid":
            return [random.randint(0, 255)]
        elif self.firework_color_type == "twotone":
            return random.choice(two_tone_colors)
        elif self.firework_color_type == "random":
            return [
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            ]
        elif self.firework_color_type == "rainbow":
            return [
                196, 208, 190, 46, 27, 92
            ]

    def render(self, buffer: Buffer):
        # Draw firework trail or particles in the buffer
        if not self.exploded:
            if 0 <= self.x < self.width and 0 <= self.y < self.height:
                buffer.put_char(int(self.x), int(self.y), val="|")
                buffer.put_char(int(self.previous_x), int(self.previous_y), val=" ")
            else:
                buffer.put_char(int(self.previous_x), int(self.previous_y), val=" ")
        else:
            if not self.caught_last_trail:
                self.caught_last_trail = True
                buffer.put_char(int(self.previous_x), int(self.previous_y), val=" ")

            for particle in self.particles:
                px, py = int(particle.x), int(particle.y)
                if 0 <= px < self.width and 0 <= py < self.height:
                    if self.color_enabled:
                        color = random.choice(self.colors)
                        buffer.put_char(px, py, val=bc(particle.symbol, color=color).colored)
                    else:
                        buffer.put_char(px, py, val=particle.symbol)
                    buffer.put_char(int(particle.previous_x), int(particle.previous_y), val=" ")
            for particle in self.clear_particles:
                buffer.put_char(int(particle.previous_x), int(particle.previous_y), val=" ")


class FireworkEffect(BaseEffect):
    """
    Class for generating fireworks
    """

    def __init__(self, buffer: Buffer, background: str):
        super(FireworkEffect, self).__init__(buffer, background)
        self.firework_type: FireworkType = "circular"
        self.firework_color_type: FireworkColorType = "solid"
        self.color_enabled: bool = False
        self.fireworks: list[Firework] = []
        self.firework_rate: float = 0.05
        self.allowed_firework_types = valid_firework_types

    def set_firework_type(self, firework_type: FireworkType):
        """
        Function to set the firework type of the effect
        """
        if firework_type in valid_firework_types or firework_type == "random":
            self.firework_type = firework_type

    def set_firework_color_enabled(self, color_enabled: bool):
        """
        Function to set whether or not fireworks should have color
        """
        self.color_enabled = color_enabled

    def set_firework_color_type(self, firework_color_type: FireworkColorType):
        """
        Function to set the firework color type of the effect
        """
        if firework_color_type in valid_firework_color_types:
            self.firework_color_type = firework_color_type

    def set_firework_rate(self, firework_rate: float):
        """
        Function to set the rate at which fireworks should be launched
        """
        if firework_rate > 0.0 and firework_rate <= 1.0:
            self.firework_rate = firework_rate

    def set_allowed_firework_types(self, allowed_firework_types):
        """
        Function to set the chosen firework types of the effect
        """
        allowed_firework_types = [ft for ft in allowed_firework_types if ft in valid_firework_types]
        if len(allowed_firework_types) > 0:
            self.allowed_firework_types = allowed_firework_types

    def render_frame(self, frame_number):
        """
        Renders the background to the screen
        """

        if random.random() < self.firework_rate:
            self.fireworks.append(
                Firework(
                    firework_type=self.firework_type,
                    height=self.buffer.height(),
                    width=self.buffer.width(),
                    firework_color_type=self.firework_color_type,
                    color_enabled=self.color_enabled,
                    allowed_firework_types=self.allowed_firework_types
                )
            )

        for firework in self.fireworks:
            firework.update()
            firework.render(self.buffer)
            
        self.fireworks = [
            firework for firework in self.fireworks if firework.is_active()
        ]

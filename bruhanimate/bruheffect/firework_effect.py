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
    def __init__(self, firework_type: FireworkType, height, width, firework_color_type: str = None, color_enabled: bool = False):
        self.width = width
        self.height = height
        self.x = random.randint(0, self.width - 1)
        self.y = height - 1
        self.previous_x = self.x
        self.previous_y = self.y
        self.peak = random.randint(5, self.height // 2)
        self.exploded = False
        self.particles = []
        self.explosion_type = (
            firework_type
            if (firework_type != "random" and firework_type in valid_firework_types)
            else random.choice(valid_firework_types)
        )
        self.clear_particles = []
        self.caught_last_trail = False
        self.speed = random.randint(1, 3)
        self.firework_color_type = firework_color_type
        self.colors = self.get_colors()
        self.color_enabled = color_enabled

    def update(self):
        if not self.exploded:
            # Move firework up
            self.previous_y = self.y
            self.y -= self.speed
            if self.y <= self.peak:
                # Explode when it reaches the peak
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
                    color_enabled=self.color_enabled
                )
            )

        for firework in self.fireworks:
            firework.update()
            firework.render(self.buffer)
            
        self.fireworks = [
            firework for firework in self.fireworks if firework.is_active()
        ]

import pygame
import random
import math

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
NIGHT_COLOR = (0, 0, 30)
DAY_COLOR = (135, 206, 250)

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crop Plantation Simulation")

# Define time and environmental variables
time_of_day = 0.0
day_length = 500
temperature = 25.0

# Simple crop class
class Crop:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.growth_rate = 0.0001
        self.scale = 1.0
        self.matured = False

    def grow(self):
        self.scale += self.growth_rate
        if self.scale >= 2.0:
            self.matured = True

# Simple weed class
class Weed(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super(Weed, self).__init__(*groups)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLACK, (10, 10), 10)  # Weed shape
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.growth_rate = 0.0002
        self.scale = 1.0

    def grow(self):
        self.scale += self.growth_rate
        if self.scale >= 1.5:  # Define the threshold for weed removal
            self.remove()

# Simple drone class
class Drone(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super(Drone, self).__init__(*groups)
        self.image = pygame.Surface((40, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, RED, (0, 0, 40, 20))  # Car body
        pygame.draw.circle(self.image, BLACK, (10, 18), 6)  # Left wheel
        pygame.draw.circle(self.image, BLACK, (30, 18), 6)  # Right wheel
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.task = None  # Initialize with no task
        self.target_index = 0  # Index for the current target in drone_targets

    # Update method in the Drone class
    def update(self):
        # Perform assigned task
        if self.task == "water":
            self.water_crops()
        elif self.task == "monitor":
            self.monitor_crops()

        # Move the drone along a predefined path
        self.move_along_path()

    def move_along_path(self):
        # List of waypoints for the drone to follow
        x_values = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        y_values = [0, 100, 200, 300, 400, 500, 600, 700]
        waypoints = []  # Add more waypoints as needed

        for i in x_values:
            for j in y_values:
                waypoints.append((i, j))

        # Move towards the current waypoint
        if self.target_index < len(waypoints):
            target_x, target_y = waypoints[self.target_index]
            dx = target_x - self.rect.x
            dy = target_y - self.rect.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            # Normalize the direction vector
            if distance > 0:
                dx /= distance
                dy /= distance

            # Move the drone towards the current waypoint
            self.rect.x += int(dx * 5)
            self.rect.y += int(dy * 5)

            # Check if the drone has reached the current waypoint
            if distance < 10:
                # Drone has reached the current waypoint, move to the next waypoint
                self.target_index += 1
        else:
            # Reset the target index to start over the path
            self.target_index = 0

    def water_crops(self):
        # Implement logic for watering crops
        # For simplicity, increase the growth rate of nearby crops
        for crop in crops:
            if (
                abs(self.rect.x - crop.x) < 30
                and abs(self.rect.y - crop.y) < 30
            ):
                crop.growth_rate += 0.000010

    def monitor_crops(self):
        # Implement logic for monitoring crops
        # For simplicity, print a message indicating monitoring
        print("Drone is monitoring crops.")

# Simple tractor class
class Tractor(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Tractor, self).__init__(*groups)
        self.image = pygame.Surface((40, 20), pygame.SRCALPHA)
        pygame.draw.rect(self.image, ORANGE, (0, 0, 40, 20))  # Tractor body
        pygame.draw.circle(self.image, BLACK, (10, 18), 6)  # Left wheel
        pygame.draw.circle(self.image, BLACK, (30, 18), 6)  # Right wheel
        self.rect = self.image.get_rect()
        self.task = None  # Initialize with no task
        self.target_crops = []

    def update(self):
        # Simulate tractor movement
        if self.target_crops:
            self.move_towards_targets()
        else:
            self.rect.x += random.randint(-5, 5)
            self.rect.y += random.randint(-5, 5)

        # Perform assigned task
        if self.task == "harvest":
            self.harvest_crops()

    def move_towards_targets(self):
        # Move the tractor towards the target crops
        target = self.target_crops[0]  # Consider the first target
        dx = target.x - self.rect.x
        dy = target.y - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)

        # Normalize the direction vector
        if distance > 0:
            dx /= distance
            dy /= distance

        # Move the tractor towards the target crop
        self.rect.x += int(dx * 5)
        self.rect.y += int(dy * 5)

        # Check if the tractor has reached the target crop
        if distance < 10:
            # Harvest the crop and remove it from the target list
            crops.remove(target)
            self.target_crops.pop(0)

    def harvest_crops(self):
        # Implement logic for harvesting mature crops
        # For simplicity, remove mature crops from the list
        global crops
        matured_crops = [crop for crop in crops if crop.matured]
        self.target_crops = matured_crops
        self.task = "harvest"

# Function to create a grid of crop positions in the field with equal spacing, removing alternate rows and columns
def generate_crops(spacing):
    crops = []
    for x in range(0, WIDTH, 2 * spacing):
        for y in range(0, HEIGHT, 2 * spacing):
            crops.append(Crop(x, y))
    return crops

# Function to create weeds in the field
def generate_weeds(num_weeds):
    weeds = pygame.sprite.Group()
    for _ in range(num_weeds):
        x, y = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        weeds.add(Weed(x, y))
    return weeds

# List to store crops
crops = generate_crops(50)  # Adjust the spacing as needed

# List to store weeds
weeds = generate_weeds(5)  # Adjust the number of weeds as needed

# Create sprite groups
all_sprites = pygame.sprite.Group()
drones = pygame.sprite.Group()
tractors = pygame.sprite.Group()
weeds_group = pygame.sprite.Group(weeds)  # Sprite group for weeds

# Create drone instances
drone1 = Drone(WIDTH // 2, HEIGHT // 2, all_sprites, drones)
all_sprites.add(drone1)

# Create tractor instances
tractor1 = Tractor(all_sprites, tractors)
all_sprites.add(tractor1)

# Font for UI text
font = pygame.font.Font(None, 36)

# List to store drone movement targets
drone_targets = [(100, 100), (200, 200), (300, 300)]  # Add more targets as needed

# Function to reset drone task and targets
def reset_drone():
    drone1.task = None
    drone1.target_index = 0

# Main game loop
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle user input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                time_of_day -= 10  # Adjust the time of day by subtracting 10
            elif event.key == pygame.K_DOWN:
                time_of_day += 10  # Adjust the time of day by adding 10
            elif event.key == pygame.K_w:
                # Assign watering task to the drone
                reset_drone()  # Reset the drone task and targets
                drone1.task = "water"
            elif event.key == pygame.K_m:
                # Assign monitoring task to the drone
                reset_drone()  # Reset the drone task and targets
                drone1.task = "monitor"
            elif event.key == pygame.K_h:
                # Assign harvesting task to the tractor
                tractor1.task = "harvest"
                # Find the nearest matured crops and set them as the targets for the tractor
                tractor1.target_crops = [crop for crop in crops if crop.matured]

    # Update time of day
    time_of_day = (time_of_day + 1) % day_length

    # Adjust background color based on time of day
    if time_of_day < day_length / 2:
        screen.fill(DAY_COLOR)
    else:
        screen.fill(NIGHT_COLOR)

    # Adjust temperature based on time of day
    temperature = 30.0 if time_of_day < day_length / 2 else 15.0

    # Update crop growth based on temperature
    for crop in crops:
        crop.grow()

    # Update weed growth
    weeds_group.update()

    # Check if weeds have grown more than required and send a tractor to remove them
    for weed in weeds_group:
        weed.grow()
        if weed.scale >= 1.5:  # Define the threshold for weed removal
            weeds_group.remove(weed)
            tractor1.task = "remove_weeds"
            tractor1.target_weeds = [weed]

    # Update drones, tractors, and weeds
    all_sprites.update()

    # Draw crops with custom tree shape
    for crop in crops:
        # Define custom tree shape points
        custom_tree_shape = [(0, 0), (10, 0), (5, -20), (0, 0), (-5, -20), (-10, 0), (0, 0)]

        # Scale and translate the custom tree shape based on crop attributes
        scaled_tree_shape = [(p[0] * crop.scale + crop.x, p[1] * crop.scale + crop.y) for p in custom_tree_shape]

        # Draw the custom tree shape
        pygame.draw.polygon(screen, GREEN, scaled_tree_shape)

    # Draw weeds with a simple circle
    weeds_group.draw(screen)

    # Draw drones with custom car shape
    for drone in drones:
        # Define custom car shape points
        custom_car_shape = [(-15, -10), (15, -10), (15, 10), (-15, 10)]

        # Scale and translate the custom car shape based on drone attributes
        scaled_car_shape = [(p[0] + drone.rect.x, p[1] + drone.rect.y) for p in custom_car_shape]

        # Draw the custom car shape
        pygame.draw.polygon(screen, RED, scaled_car_shape)

    # Draw tractors with custom tractor shape
    for tractor in tractors:
        # Define custom tractor shape points
        custom_tractor_shape = [(-15, -10), (15, -10), (20, 0), (15, 10), (-15, 10)]

        # Scale and translate the custom tractor shape based on tractor attributes
        scaled_tractor_shape = [(p[0] + tractor.rect.x, p[1] + tractor.rect.y) for p in custom_tractor_shape]

        # Draw the custom tractor shape
        pygame.draw.polygon(screen, ORANGE, scaled_tractor_shape)

    # Draw UI text
    text = font.render(f"Time of Day: {int(time_of_day)} Temperature: {int(temperature)}", True, WHITE)
    screen.blit(text, (10, 10))

    # Refresh the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()


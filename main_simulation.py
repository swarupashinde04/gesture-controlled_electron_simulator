import cv2
import mediapipe as mp
import pygame
import random
import math

# -------------------- PYGAME SETUP --------------------
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Controlled Electric Field")
clock = pygame.time.Clock()

# -------------------- CAMERA SETUP --------------------
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7,
                      min_tracking_confidence=0.7)

# -------------------- ELECTRIC FIELD SETTINGS --------------------
field_x = WIDTH // 2
field_y = HEIGHT // 2

# -------------------- CREATE ELECTRONS --------------------
electrons = []
num_electrons = 15

for i in range(num_electrons):
    electrons.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "vx": 0,
        "vy": 0
    })

running = True

while running:

    # -------- CAMERA FRAME --------
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)  # mirror camera
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # Index finger tip = landmark 8
            cx = int(handLms.landmark[8].x * WIDTH)
            cy = int(handLms.landmark[8].y * HEIGHT)

            field_x = cx
            field_y = cy

    # -------- PYGAME DRAW --------
    screen.fill((0, 0, 0))

    # Draw positive charge (pink)
    pygame.draw.circle(screen, (255, 0, 255), (field_x, field_y), 12)

    for electron in electrons:

        dx = field_x - electron["x"]
        dy = field_y - electron["y"]

        distance = math.sqrt(dx*dx + dy*dy)

    if distance > 10:

    # Much stronger visible force
      force = 3000 / (distance * distance)

    ax = force * dx / distance
    ay = force * dy / distance

    electron["vx"] += ax
    electron["vy"] += ay


        # Damping (energy loss)
    electron["vx"] *= 0.95
    electron["vy"] *= 0.95

        # Limit maximum speed
    max_speed = 6
    electron["vx"] = max(-max_speed, min(max_speed, electron["vx"]))
    electron["vy"] = max(-max_speed, min(max_speed, electron["vy"]))

    electron["x"] += electron["vx"]
    electron["y"] += electron["vy"]

        # Bounce from walls
    if electron["x"] <= 0 or electron["x"] >= WIDTH:
            electron["vx"] *= -1
    if electron["y"] <= 0 or electron["y"] >= HEIGHT:
            electron["vy"] *= -1

    pygame.draw.circle(screen, (0, 255, 255),
                           (int(electron["x"]), int(electron["y"])), 5)

    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

cap.release()
pygame.quit()

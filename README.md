# Neon Asteroids 🚀

A retro 2D space shooter built in Python using the standard `turtle` graphics module. Instead of standard rigid movements, this game implements smooth drift physics, particle effects, and a persistent scoring system. 

Built as a university computer science project to demonstrate clean object-oriented programming (OOP) and state management in Python.

---

## ✨ Features

* **Smooth Space Physics:** Features real momentum and drift. When you thrust, the ship accelerates based on its angle; let go, and space friction slowly brings you to a coasting stop.
* **Exhaust Particle Trails:** Stepping on the gas spawns a stream of glowing fuel particles that fade from yellow to red as they disappear.
* **Smart Screen Wrapping:** Objects that drift off any edge of the screen seamlessly loop back around from the opposite side.
* **High Score Memory:** Tracks both your current run and your all-time best score. The high score stays saved even when you restart the match.
* **Instant Restart:** No need to relaunch the script when you crash. Just tap the **R** key on the game over screen to instantly wipe the board and start fresh.

---

## 🎮 How to Play

* **Up Arrow** – Fire Thrusters (Accelerate)
* **Left / Right Arrows** – Rotate Ship
* **Spacebar** – Shoot Lasers (Max 4 projectiles on screen at once)
* **R Key** – Restart Game (Only works after you crash!)

 Per kill gives a flat **10 points**.

---


## Screeshots
<img width="799" height="592" alt="Screenshot 2026-05-26 194629" src="https://github.com/user-attachments/assets/5954eb6a-5ee4-44c3-a688-e40563e6b045" />

---

<img width="796" height="597" alt="Screenshot 2026-05-26 195029" src="https://github.com/user-attachments/assets/3bcd243d-b2d0-4121-a9bf-987a71e5fe14" />

---
## 🚀 Running the Game

No extra libraries or installations required. Just make sure you have Python 3 installed, clone the repo, and run the file:

```bash
git clone [https://github.com/YOUR_USERNAME/neon-asteroids.git](https://github.com/YOUR_USERNAME/neon-asteroids.git)
cd neon-asteroids
python vibrant_asteroids.py

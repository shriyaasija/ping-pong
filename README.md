# Ping Pong Game - Software Engineering Lab 4

A fully functional real-time ping pong game built with Python and Pygame, featuring robust collision detection, match-based gameplay, sound effects, and an interactive menu system.

**Developer:** Shriya Asija (PES1UG23CS568)  
**Course:** Software Engineering - Lab 4 (Vibe Coding)

---

## Project Overview

This project demonstrates iterative software development using AI-assisted "vibe coding" with ChatGPT. Starting from a basic framework, the game was enhanced with four critical features through an iterative development process involving code generation, testing, debugging, and refinement.

### Key Features Implemented

✅ **Enhanced Collision Detection** - Swept collision technique prevents fast-moving ball from passing through paddles  
✅ **Match System** - Best of 3/5/7 games with round-based scoring (each game to 5 points)  
✅ **Game Over & Replay** - Complete menu system with match winner display and replay options  
✅ **Sound Feedback** - Immersive audio for paddle hits, wall bounces, and scoring events  
✅ **Main Menu** - Clean state-driven interface for game configuration

---

## Development Process

This project was completed using an AI-assisted workflow:
- **AI Assistant:** ChatGPT for initial code generation and feature suggestions
- **Human Oversight:** Critical code review, debugging, and architectural refinement
- **Iteration:** Multiple rounds of testing and improvement for each feature

### Links
- **GitHub Repository:** [github.com/shriyaasija/ping-pong](https://github.com/shriyaasija/ping-pong)
- **ChatGPT Conversation:** [View full development chat](https://chatgpt.com/share/68ef145c-8628-8004-90d3-565adba59af1)

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- Pygame library

### Installation

1. Clone the repository:
```bash
git clone https://github.com/shriyaasija/ping-pong.git
cd ping-pong
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

---

## How to Play

### Controls
- **W** - Move player paddle up
- **S** - Move player paddle down
- **3/5/7** - Select match type (Best of 3/5/7 games)
- **ESC** - Exit game

### Gameplay
- First player to win the majority of games wins the match
- Each game is played to 5 points
- AI opponent automatically tracks and responds to ball movement
- Score display shows: `Current Points (Games Won)`

---

## Technical Implementation

### Task 1: Refined Ball Collision Logic
**Problem:** Fast-moving ball could pass through paddles without registering hits

**Solution:** Implemented swept collision detection using a "travel rectangle" that covers the ball's entire movement path per frame, ensuring no collision is missed regardless of speed.

**File Modified:** `game/ball.py`

### Task 2 & 3: Game Over System and Match Structure
**Problem:** Needed complete round-based match system with replay functionality

**Solution:** Developed through iterative refinement:
1. Added basic game-over state detection
2. Introduced replay menu with match type selection
3. Redesigned logic to support best-of-N match system with individual game tracking
4. Added score variables to track both current points and games won

**File Modified:** `game/game_engine.py`

### Task 4: Sound Feedback
**Problem:** Initial implementation caused TypeError crashes due to missing sound object parameters

**Solution:** Integrated pygame.mixer with proper sound object passing between GameEngine and Ball class. Added audio triggers for:
- Paddle hits
- Wall bounces
- Scoring events

**Files Modified:** `game/game_engine.py`, `game/ball.py`

---

## Project Structure

```
ping-pong/
├── main.py                 # Entry point and game loop
├── requirements.txt        # Python dependencies
├── game/
│   ├── game_engine.py     # Core game logic and state management
│   ├── paddle.py          # Player and AI paddle classes
│   └── ball.py            # Ball physics and collision detection
├── wall_bounce.wav        # Sound effects
├── paddle_hit.wav
├── score.wav
└── README.md
```

---

## Key Learnings

This lab demonstrated the practical application of AI-assisted development while highlighting the critical role of human oversight in software engineering:

- **Iterative Development:** Features evolved through multiple refinement cycles
- **AI as a Tool:** ChatGPT accelerated initial implementation but required careful review
- **Debugging Skills:** Human intervention was essential for fixing edge cases and integration issues
- **Architectural Design:** Strategic decisions about game state management required human judgment

---

## Submission Checklist

- ✅ All 4 tasks completed
- ✅ Game behaves as expected with no crashes
- ✅ Final score and winner display works correctly
- ✅ Code reviewed and refined post-AI generation
- ✅ Dependencies listed in `requirements.txt`
- ✅ Clean, modular, and understandable codebase
- ✅ Complete ChatGPT conversation history included

---

## License

This project was developed as part of the Software Engineering course curriculum at PES University.

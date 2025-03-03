# Garden Simulator 🌱

Garden Simulator is a command-line gardening simulation game where you can grow plants, manage your soil, and deal with random events such as droughts, storms, or even zombies! The goal is to keep your plants healthy and maximize your harvest.

## Features

- 🌿 **Grow Plants**: Add vegetables, fruits, and flowers to your garden.
- 💧 **Resource Management**: Water, fertilize, and maintain your plants to keep them healthy.
- 🌞 **Dynamic Conditions**: Light, season, and soil type affect plant growth.
- ☔️ **Random Events**: Face droughts, storms, diseases, and even zombies!
- 🎰 **Casino**: Use your harvest to play the slot machine and win money or loose it...
- 💾 **Save and Load**: Save your progress and continue later.

## Installation

### Prerequisites

- **Python 3.x**: Make sure Python is installed on your machine.
- **Colorama**: The project uses the `colorama` library for console colors.

### Installation Steps

Clone this repository to your machine:

```bash
git clone https://github.com/Spiexo/GardenSimulator.git
cd GardenSimulator
```

Install dependencies:

```bash
pip install colorama
```

Run the game:

```bash
python main.py
```

## How to Play

- **Choose your soil**: At the beginning, select a soil type (rich, sandy, clay) that will affect plant growth.
- **Add plants**: Select plants to add to your garden (tomatoes, carrots, lettuce, etc.).
- **Take care of your plants**:
  - Water them to maintain moisture levels.
  - Fertilize them to increase nutrients.
  - Maintain them to improve their health.
- **Advance to the next day**: Each day, plants grow and produce crops.
- **Sell or use your harvest**: Sell vegetables, fruits, and flowers to earn money, and use your money in the casino.
- **Face events**: Random events such as droughts, storms, or zombies can occur. Be ready to react!

## Project Structure

```
garden-simulator/
│
├── main.py            # Game entry point
├── game.py            # Main game logic
├── garden.py          # Garden management
├── plants.py          # Plant class
├── inventory.py       # Inventory management
├── enums.py           # Enumerations (soil types, species, etc.)
├── casino.py          # Casino logic
├── README.md          # Project documentation
└── data.json          # Save file (automatically created)
```

## Available Commands

1. **Water a plant**: Give water to a plant.
2. **Fertilize a plant**: Add nutrients to a plant.
3. **Maintain a plant**: Improve a plant's health.
4. **Add a plant**: Add a new plant to your garden.
5. **Remove a plant**: Remove a plant from your garden.
6. **Skip to the next day**: Advance time and update plant status.
7. **Save the game**: Save your progress.
8. **Load a save**: Load your previous progress.
9. **View inventory**: Check your harvest and money.
10. **Sell produce**: Sell vegetables, fruits, or flowers.
11. **Use produce**: Use your money in the casino.
12. **Visit the casino**: Play the slot machine to win money or loose it...
13. **View rules**: Check the game rules.
14. **Quit the game**: Exit the game.

## Example Gameplay

```bash
🌞 Day 1 - Light Level: 65% - Season: Spring - Soil Type: Rich Soil

🌱 Tomato - Health: 100%, Water: 50.00%, Maturity: 0%, Soil Nutrients: 50%
 Tomato, which is a fruit, needs Water: 60%, Light: 70%. Its growth speed is 5%.

What would you like to do?
1.  Water a plant
2.  Fertilize a plant
3.  Maintain a plant
4.  Add a plant
5.  Remove a plant
6.  Skip to the next day
7.  Save the game
8.  Load a save
9.  View inventory
10. Sell produce
11. Use produce
12. Visit the Casino
13. Rules
14. Quit The Game

➡️  Your choice: 1
```

## Author

Spiexo - [Your GitHub](https://github.com/Spiexo)

Enjoy the game and have fun growing your virtual garden! 🌻



# User manual

## 🚀 Solving a Sudoku puzzle

### Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/apiramaruchunarajah/sudoku_solver.git
   cd sudoku_solver
   ```

2. Solve a Sudoku puzzle:

   ```bash
   python3 main.py path_to_puzzle
   ```

---
## 🧪 Testing Guide
### Hard coded examples
We provide here a list of parameters that can be used to test our API.

1. `playerName`, `friendName`:
    - **"Jules"**
    - **"Marc"**

2. `gameName`:
    - **"Mario"** 
    - **"Minecraft"** 
    - **"CoD"**

3. `achievementName`:
    - for "Mario":
        - **"finishGameMa"**
        - **"firstJump"**

    - for "Minecraft":
        - **"finishGameMi"**
        - **"firstBlock"**

    - for "CoD":
        - **"finishGameC"**
        - **"firstKill"**

Jules and Marc are friends. Jules plays Mario and CoD, and Marc plays Mario and Minecraft.   

### Test Examples

1. **List all players**:
   - Request URL: `http://localhost:8080/players`
   - Method: `GET`
   - Expected Response:
        ```json
        {
        "username" : ["Jules", "Marc"]
        }
        ```

2. **List the games played by Jules**:
   - Request URL: `http://localhost:8080/players/Jules/games/`
   - Method: `GET`
   - Expected Response:
        ```json
        {
            "games": ["CoD", "Mario"]
        }
        ```

3. **List all the achievements of the game Mario**:
   - Request URL: `http://localhost:8080/games/Mario/achievements/`
   - Method: `GET`
   - Expected Response:
        ```json
        {
            "name": [
                "finishGameMa",
                "firstJump"
            ]
        }
        ```

4. **Retrieve the details of the achievement "firstJump" of Mario**:
   - Request URL: `http://localhost:8080/games/Mario/achievements/firstJump/`
   - Method: `GET`
   - Expected Response:
        ```json
        {
            "name": "firstJump",
            "hidden": false,
            "successRate": 0.9,
            "description": "Awarded after the first jump"
        }
        ```

5. **Retrieve the status of the achievement "firstJump" of Mario for Jules**:
   - Request URL: `http://localhost:8080/players/Jules/games/Mario/achievements/firstJump/`
   - Method: `GET`
   - Expected Response:
        ```json
        {
            "progress": 100,
            "unlockedDate": "10/03/2024"
        }
        ```

5. **Retrieve a comparision, for Mario and between Jules and Marc who are friends, of the status of their achievements**:
   - Request URL: `http://localhost:8080/games/Mario/players/Jules/compare/Marc/`
   - Method: `GET`
   - Expected Response:
        ```json
        {
            "firstJump": {
                "Jules": {
                    "progress": 100,
                    "unlockedDate": "10/03/2024"
                },
                "Marc": {
                    "progress": 100,
                    "unlockedDate": "04/06/2024"
                }
            },
            "finishGameMa": {
                "Jules": {
                    "progress": 100,
                    "unlockedDate": "28/03/2024"
                },
                "Marc": {
                    "progress": 70,
                    "unlockedDate": "null"
                }
            }
        }
        ```


---

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const scoreText = document.getElementById("score");
const highScoreText = document.getElementById("highScore");
const restartButton = document.getElementById("restartButton");


const gridSize = 20;

const tileCount = canvas.width / gridSize;


let snake;
let food;

let direction;

let nextDirection;

let score = 0;

let highScore = localStorage.getItem("snakeHighScore") || 0;

let gameSpeed = 100;

let gameOver = false;

let gameLoop;


highScoreText.textContent = highScore;


// Start game
function startGame() {

    snake = [
        {
            x: 15,
            y: 15
        }
    ];


    food = createFood();


    direction = {
        x: 0,
        y: 0
    };


    nextDirection = {
        x: 0,
        y: 0
    };


    score = 0;

    gameSpeed = 100;

    gameOver = false;


    scoreText.textContent = score;


    clearInterval(gameLoop);

    gameLoop = setInterval(updateGame, gameSpeed);

    drawGame();
}


// Create random food
function createFood() {

    let newFood;


    do {

        newFood = {
            x: Math.floor(Math.random() * tileCount),
            y: Math.floor(Math.random() * tileCount)
        };

    } while (
        snake.some(
            segment =>
                segment.x === newFood.x &&
                segment.y === newFood.y
        )
    );


    return newFood;
}


// Draw everything
function drawGame() {

    // Background
    ctx.fillStyle = "grey";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    // Food
    ctx.fillStyle = "lightblue";

    ctx.beginPath();

    ctx.arc(
        food.x * gridSize + gridSize / 2,
        food.y * gridSize + gridSize / 2,
        gridSize / 2 - 2,
        0,
        Math.PI * 2
    );

    ctx.fill();


    // Snake
    ctx.fillStyle = "lightpink";


    snake.forEach(segment => {

        ctx.fillRect(
            segment.x * gridSize,
            segment.y * gridSize,
            gridSize - 2,
            gridSize - 2
        );

    });
}


// Update game
function updateGame() {

    if (gameOver) {
        return;
    }


    direction = nextDirection;


    // If the player hasn't started moving
    if (direction.x === 0 && direction.y === 0) {

        drawGame();

        return;
    }


    const head = {
        x: snake[0].x + direction.x,
        y: snake[0].y + direction.y
    };


    // Check border collision
    if (
        head.x < 0 ||
        head.x >= tileCount ||
        head.y < 0 ||
        head.y >= tileCount
    ) {

        endGame();

        return;
    }


    // Check body collision
    for (let i = 0; i < snake.length; i++) {

        if (
            head.x === snake[i].x &&
            head.y === snake[i].y
        ) {

            endGame();

            return;
        }
    }


    snake.unshift(head);


    // Check food collision
    if (
        head.x === food.x &&
        head.y === food.y
    ) {

        score += 10;


        if (score > highScore) {

            highScore = score;

            localStorage.setItem(
                "snakeHighScore",
                highScore
            );

        }


        scoreText.textContent = score;

        highScoreText.textContent = highScore;


        food = createFood();


        // Increase speed
        if (gameSpeed > 40) {

            gameSpeed -= 1;

            clearInterval(gameLoop);

            gameLoop = setInterval(
                updateGame,
                gameSpeed
            );

        }

    } else {

        // Remove tail
        snake.pop();

    }


    drawGame();
}


// Game over
function endGame() {

    gameOver = true;

    clearInterval(gameLoop);


    ctx.fillStyle = "rgba(0, 0, 0, 0.6)";

    ctx.fillRect(
        0,
        0,
        canvas.width,
        canvas.height
    );


    ctx.fillStyle = "white";

    ctx.font = "40px Arial";

    ctx.textAlign = "center";

    ctx.fillText(
        "GAME OVER",
        canvas.width / 2,
        canvas.height / 2 - 20
    );


    ctx.font = "20px Arial";

    ctx.fillText(
        "Press Restart to play again",
        canvas.width / 2,
        canvas.height / 2 + 30
    );
}


// Keyboard controls
document.addEventListener("keydown", function(event) {

    if (event.key === "ArrowUp") {

        if (direction.y !== 1) {

            nextDirection = {
                x: 0,
                y: -1
            };

        }

        event.preventDefault();
    }


    if (event.key === "ArrowDown") {

        if (direction.y !== -1) {

            nextDirection = {
                x: 0,
                y: 1
            };

        }

        event.preventDefault();
    }


    if (event.key === "ArrowLeft") {

        if (direction.x !== 1) {

            nextDirection = {
                x: -1,
                y: 0
            };

        }

        event.preventDefault();
    }


    if (event.key === "ArrowRight") {

        if (direction.x !== -1) {

            nextDirection = {
                x: 1,
                y: 0
            };

        }

        event.preventDefault();
    }

});


// Restart button
restartButton.addEventListener(
    "click",
    startGame
);


// Start the game
startGame();
import pygame
import random
import math

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = 255

moves = [[1, 0], [-1, 0], [0, -1], [0, 1]]


class Direction():
    up = 0
    down = 1
    left = 2
    right = 3


class Node:
    def __init__(self, pos, came_from, steps, score):
        self.pos = pos
        self.came_from = came_from
        self.steps = steps
        self.score = score


class Game:
    def __init__(self, a, s):
        self.panic = False
        self.show_path = s
        self.speed = a
        self.speeds = [20, 40, 100, math.inf]

        self.w = 30  # In tiles
        self.h = 30  # ^

        self.sqsize = round(600 / self.w)

        self.window = pygame.display.set_mode((self.w * self.sqsize, self.h * self.sqsize))

        self.reset()

    # Snake changes to red if no path found
    def snake_color(self):

        if self.panic:
            return red

        return green

    def reset(self):
        self.snake = [[self.h / 2, self.w / 2],
                      [self.h / 2, self.w / 2 - 1],
                      [self.h / 2, self.w / 2 - 2]]  # Points are [y, x]

        self.direction = Direction.right
        self.score = 0
        self.apple = None
        self.new_apple()

    def game_step(self, action, path):
        # Take input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "WIN_QUIT"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.speed += 1
                    # print("Speed set to " + str(self.speeds[self.speed % len(self.speeds)] / self.speeds[0]) + "x")

                if event.key == pygame.K_p:
                    if self.show_path:
                        self.show_path = False

                    else:
                        self.show_path = True

        # Move snake
        self.move(action)

        # Check if ded
        if self.collision(self.snake[0]):
            pygame.quit()
            return "ded"

        # Check if apple is eaten, if not then delete tail
        if self.snake[0] == self.apple:
            self.score += 1
            self.new_apple()

        else:
            self.snake.pop()

        # Redraw window
        self.render(path)

        if self.panic:
            pygame.time.Clock().tick(self.speeds[0])

        else:
            pygame.time.Clock().tick(self.speeds[self.speed % len(self.speeds)])

    def render(self, path):
        self.window.fill(black)

        # Draw path
        if self.show_path:
            for i in range(len(path)):
                # Color goes from White --> Pink gradient as path gets closer to apple

                pygame.draw.circle(self.window, (purple, round(i * (purple / len(path))), purple),
                                   (path[i][1] * self.sqsize + self.sqsize / 2,
                                    path[i][0] * self.sqsize + self.sqsize / 2),
                                   self.sqsize / 2.5)

                if i != len(path) - 1:
                    dir = [path[i][0] - path[i + 1][0], path[i][1] - path[i + 1][1]]

                    pygame.draw.rect(self.window, (purple, round(i * (purple / len(path))), purple),
                                     pygame.Rect(
                                         path[i][1] * self.sqsize + self.sqsize * 0.1 - dir[1] * (self.sqsize / 2),
                                         path[i][0] * self.sqsize + self.sqsize * 0.1 - dir[0] * (self.sqsize / 2),
                                         self.sqsize * (-abs(dir[0] * 0.2) + 1),
                                         self.sqsize * (-abs(dir[1] * 0.2) + 1)))

            if path:
                dir = [path[len(path) - 1][0] - self.snake[0][0], path[len(path) - 1][1] - self.snake[0][1]]

                pygame.draw.rect(self.window, (purple, round(i * (purple / len(path))), purple),
                                 pygame.Rect(
                                     path[len(path) - 1][1] * self.sqsize + self.sqsize * 0.1 - dir[1] * (
                                             self.sqsize / 2),
                                     path[len(path) - 1][0] * self.sqsize + self.sqsize * 0.1 - dir[0] * (
                                             self.sqsize / 2),
                                     self.sqsize * (-abs(dir[0] * 0.2) + 1), self.sqsize * (-abs(dir[1] * 0.2) + 1)))

        # Draw snake
        for i in range(len(self.snake)):
            pygame.draw.circle(self.window, self.snake_color(),
                               (self.snake[i][1] * self.sqsize + self.sqsize / 2,
                                self.snake[i][0] * self.sqsize + self.sqsize / 2),
                               self.sqsize / 2.5)

            if i != len(self.snake) - 1:
                dir = [self.snake[i][0] - self.snake[i + 1][0], self.snake[i][1] - self.snake[i + 1][1]]

                pygame.draw.rect(self.window, self.snake_color(),
                                 pygame.Rect(
                                     self.snake[i][1] * self.sqsize + self.sqsize * 0.1 - dir[1] * (
                                             self.sqsize / 2),
                                     self.snake[i][0] * self.sqsize + self.sqsize * 0.1 - dir[0] * (
                                             self.sqsize / 2),
                                     self.sqsize * (-abs(dir[0] * 0.2) + 1), self.sqsize * (-abs(dir[1] * 0.2) + 1)))

        # Draw apple
        pygame.draw.circle(self.window, red,
                           (self.apple[1] * self.sqsize + self.sqsize / 2,
                            self.apple[0] * self.sqsize + self.sqsize / 2),
                           self.sqsize / 2)

        pygame.display.update()

    def new_apple(self):
        self.apple = [random.randint(0, self.h - 1), random.randint(0, self.w - 1)]

        # Check if new apple is in snake
        if self.apple in self.snake:
            self.new_apple()

    def collision(self, point):
        # If snake hits the wall
        if point[0] >= self.h or point[0] < 0 or point[1] >= self.w or point[1] < 0:
            return True

        # If snake hits itself
        if point in self.snake[1:]:
            return True

        # If no collision
        return False

    def move(self, action):
        # [1, 0, 0, 0] -> up
        # [0, 1, 0, 0] -> down
        # [0, 0, 1, 0] -> left
        # [0, 0, 0, 1] -> right

        if action[0] == 1:
            self.direction = Direction.up
            self.snake.insert(0, [self.snake[0][0] - 1, self.snake[0][1]])

        elif action[1] == 1:
            self.direction = Direction.down
            self.snake.insert(0, [self.snake[0][0] + 1, self.snake[0][1]])

        elif action[2] == 1:
            self.direction = Direction.left
            self.snake.insert(0, [self.snake[0][0], self.snake[0][1] - 1])

        else:  # [0, 0, 0, 1]
            self.direction = Direction.right
            self.snake.insert(0, [self.snake[0][0], self.snake[0][1] + 1])

    def pathfind(self, board):
        # Non-explored nodes
        open_list = [Node(self.snake[0], self.snake[0], 0, 0)]  # Current pos, prev pos, move number, score

        # Already explored nodes
        closed_list = []

        # Loop expansion
        while True:
            # Finding next node to explore
            best_score = math.inf
            for i in range(len(open_list)):
                if open_list[i].score < best_score:
                    best_score = open_list[i].score
                    best_i = i

            # Check if no open nodes
            if len(open_list) == 0:
                return []

            # Select new node
            current_node = open_list[best_i]
            open_list.pop(best_i)
            closed_list.append(current_node)

            # Check if path was found
            if current_node.pos == self.apple:
                path = [[int(self.apple[0]), int(self.apple[1])]]
                while True:
                    for i in range(len(closed_list)):
                        if closed_list[i].pos == current_node.came_from:
                            if closed_list[i].pos != self.snake[0]:
                                path.append([int(current_node.came_from[0]), int(current_node.came_from[1])])
                                current_node = closed_list[i]

                            else:
                                return path

            # Evaluate new nodes
            for move in moves:

                child_node = [current_node.pos[0] + move[0], current_node.pos[1] + move[1]]

                # If in bounds
                if 0 <= child_node[0] < self.h and 0 <= child_node[1] < self.w:

                    # If not in wall or start node
                    if board[int(child_node[0])][int(child_node[1])] == 0 or board[int(child_node[0])][
                        int(child_node[1])] == 4:
                        # Get distance to end node
                        y = abs(child_node[0] - self.apple[0])
                        x = abs(child_node[1] - self.apple[1])

                        h = abs(x + y)

                        # Get final score based on game score

                        f = h + current_node.steps

                        open_list.append(Node(child_node, current_node.pos, current_node.steps + 1, f))
                        board[int(child_node[0])][int(child_node[1])] = 5

    def arrayize(self):
        arr = []
        for i in range(self.h):
            arr.append([])
            for j in range(self.w):
                arr[i].append(0)

        for snek in self.snake:
            arr[int(snek[0])][int(snek[1])] = 1

        return arr


def main():
    best_score = 0
    game = Game(0, True)

    while True:
        dest = [0, 0, 0, 1]  # Failsafe

        path = game.pathfind(game.arrayize())

        # Survive if no path
        if path == []:
            game.panic = True
            for move in moves:
                if not game.collision([int(game.snake[0][0] + move[0]), int(game.snake[0][1] + move[1])]):
                    dest = [game.snake[0][0] + move[0], game.snake[0][1] + move[1]]

        else:
            game.panic = False
            dest = path.pop()

        action = [int(game.snake[0][0] - dest[0]), int(dest[1] - game.snake[0][1])]

        if action == moves[0]:
            dir = [1, 0, 0, 0]

        if action == moves[1]:
            dir = [0, 1, 0, 0]

        if action == moves[2]:
            dir = [0, 0, 1, 0]

        if action == moves[3]:
            dir = [0, 0, 0, 1]

        e = game.game_step(dir, path)

        if e == "WIN_QUIT":
            return

        elif e != None:
            if game.score > best_score:
                best_score = game.score
            print("Score:", game.score, "Best:", best_score)

            game = Game(game.speed, game.show_path)


if __name__ == "__main__":
    main()

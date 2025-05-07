import random
import copy
import pygame
import time

POPULATION_SIZE = 500
MUTATION_RATE = 0.1
MAX_GENERATIONS = 1000

def fitness(candidate):
    size = len(candidate)
    score = 0
    block_rows = block_cols = int(size ** 0.5)
    if size == 6:
        block_rows, block_cols = 2, 3

    for i in range(size):
        score += len(set(candidate[i]))
        col = [candidate[j][i] for j in range(size)]
        score += len(set(col))

    for box_row in range(0, size, block_rows):
        for box_col in range(0, size, block_cols):
            box = []
            for i in range(block_rows):
                for j in range(block_cols):
                    box.append(candidate[box_row + i][box_col + j])
            score += len(set(box))

    return score

def is_valid_candidate(candidate):
    for row in candidate:
        if 0 in row:
            return False
    return True

def fill_missing_cells(puzzle):
    size = len(puzzle)
    candidate = copy.deepcopy(puzzle)
    for i in range(size):
        used = set(candidate[i])
        missing = [x for x in range(1, size + 1) if x not in used]
        random.shuffle(missing)
        for j in range(size):
            if candidate[i][j] == 0:
                if not missing:
                    return fill_missing_cells(puzzle)
                candidate[i][j] = missing.pop()
    return candidate

def mutate(candidate, puzzle):
    size = len(candidate)
    row = random.randint(0, size - 1)
    indices = [i for i in range(size) if puzzle[row][i] == 0]
    if len(indices) >= 2:
        i1, i2 = random.sample(indices, 2)
        candidate[row][i1], candidate[row][i2] = candidate[row][i2], candidate[row][i1]

def crossover(parent1, parent2, puzzle):
    size = len(parent1)
    point = random.randint(1, size - 1)
    child1 = [row[:] for row in parent1[:point]] + [row[:] for row in parent2[point:]]
    child2 = [row[:] for row in parent2[:point]] + [row[:] for row in parent1[point:]]
    return child1, child2

def draw_board(screen, board, size, generation, fitness_score):
    screen.fill((255, 255, 255))
    tile_size = 540 // size
    font = pygame.font.SysFont("lato", 28)
    for i in range(size):
        for j in range(size):
            pygame.draw.rect(screen, (0, 0, 0), (j * tile_size, i * tile_size, tile_size, tile_size), 1)
            value = board[i][j]
            if value != 0:
                text = font.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=(j * tile_size + tile_size // 2, i * tile_size + tile_size // 2))
                screen.blit(text, text_rect)

    font = pygame.font.SysFont("Bahnschrift", 24)
    screen.blit(font.render(f"Gen: {generation}", True, (0, 0, 255)), (10, 545))
    screen.blit(font.render(f"Fitness: {fitness_score}", True, (0, 128, 0)), (400, 545))
    pygame.display.flip()

def solve_with_genetic(puzzle, screen=None, delay=100):
    size = len(puzzle)
    max_fitness = size * 3 * size
    population = [fill_missing_cells(puzzle) for _ in range(POPULATION_SIZE)]

    for generation in range(MAX_GENERATIONS):
        population.sort(key=lambda x: -fitness(x))
        best = population[0]
        best_score = fitness(best)

        if screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            draw_board(screen, best, size, generation, best_score)
            pygame.time.delay(delay)

        if best_score >= max_fitness and is_valid_candidate(best):
            return best

        next_generation = population[:50]
        while len(next_generation) < POPULATION_SIZE:
            parent1, parent2 = random.sample(population[:100], 2)
            child1, child2 = crossover(parent1, parent2, puzzle)
            if random.random() < MUTATION_RATE:
                mutate(child1, puzzle)
            if random.random() < MUTATION_RATE:
                mutate(child2, puzzle)
            next_generation += [child1, child2]
        population = next_generation

    return population[0]
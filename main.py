import apps.MicroCraft.worldgen
import math
import random

displayWidth = math.ceil(width/32)
displayHeight = math.ceil(height/32)

chunkHeight = 96
chunkWidth = displayWidth

TEXTURENAME = 'default'

# import texture definition
exec('from apps.MicroCraft.textures.'+TEXTURENAME+'.blocks import blocks')

def calc_points(x0, y0, x1, y1):
    points=[]
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return points

def perlin_noise(x, seed):
    n = x + seed * 57
    n = (n << 13) ^ n
    return (1.0 - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0)

def drawBlock(blockIndex, x, y):
    if type(blocks[blockIndex]) is int:
        display.fill_rect(x, y, 32, 32, blocks[blockIndex])
    elif type(blocks[blockIndex]) is str:
        display.png(blocks[blockIndex], x, y)

def render(blocksArray):
    for x, column in enumerate(blocksArray):
        gc.collect()
        for y, block in enumerate(column):
            drawBlock(block, x*32, y*32)

def generate_chunk(lastHeight, seed=random.randint(0, 1000)):
    chunk = []
    chunk_height = int(perlin_noise(round(seed*5/13), seed) * 4 + round(chunkHeight-(chunkHeight/4)))
    height_variation = chunk_height
    slopePoints = calc_points(0, lastHeight, chunkWidth // 2, chunk_height)
    for x in range(chunkWidth):
        column = []
        height_variation = slopePoints[x]
        for y in range(chunkHeight):
            if y < chunkHeight-height_variation:
                column.append(0)
            elif y == chunkHeight-height_variation:
                column.append(2)
            elif y < chunkHeight-height_variation + 3:
                column.append(1)
            else:
                column.append(3)
        chunk.append(column)
    return chunk

def get_buffer(chunk, y):
    buffer = []
    for column in chunk:
        buffercolumn = []
        for block in range(y, y+displayHeight):
            buffercolumn.append(column[block])
        buffer.append(buffercolumn)
    return buffer
import random
import logging
import pyglet

from .astar import AStar

WORLD_SIZE = 98

ROOM_MAX_SIZE = 16
ROOM_MIN_SIZE = 8
ROOM_MAX_ATTEMPTS = 30

TILE_SIZE = 64
TILE_FLOOR = 10
TILE_WALL = 50

TEXTURE_FLOOR = pyglet.resource.texture('rock_floor.png')
TEXTURE_WALL = pyglet.resource.texture('wall.gif')


class Room:
    x = None
    y = None
    width = None
    height = None


class World:

    _astar = None
    _rooms = []
    _tiles = []
    _sprites = []
    _batch = None
    _spawn_x = None
    _spawn_y = None

    def get_tiles(self):
        return self._tiles

    def get_spawn_x(self):
        return self._spawn_x

    def get_spawn_y(self):
        return self._spawn_y

    def _reset(self):
        self._astar = None
        self._rooms = []
        self._tiles = []
        self._sprites = []
        self._batch = pyglet.graphics.Batch()
        self._spawn_x = None
        self._spawn_y = None

    def generate(self):
        logging.debug('Generating world')
        self._reset()
        # initialize the 2d array according to the world size
        for y in range(0, WORLD_SIZE):
            self._tiles.append([0] * WORLD_SIZE)

        self._create_rooms()
        self._create_tunnels()
        self._create_sprites()

    def _create_rooms(self):
        no_of_rooms = WORLD_SIZE / 4.5
        logging.debug('Creating {0} rooms'.format(no_of_rooms))
        for i in range(0, int(no_of_rooms)):
            logging.debug('Room #{0}'.format(i))
            attempt = 0  # current attempt
            room = Room()
            while attempt < ROOM_MAX_ATTEMPTS:
                logging.debug('Attempt #{0}'.format(attempt))
                # give some initial random values to the room
                room.x = random.randrange(2, WORLD_SIZE)
                room.y = random.randrange(2, WORLD_SIZE)
                room.width = random.randrange(ROOM_MIN_SIZE, ROOM_MAX_SIZE)
                room.height = random.randrange(ROOM_MIN_SIZE, ROOM_MAX_SIZE)

                # adjust room height if needed
                while room.height < room.width / 2.5 or room.height > room.width * 1.5:
                    logging.debug('Adjusting room size')
                    room.height = random.randrange(room.width, ROOM_MAX_SIZE)

                # out of bounds, try again
                if room.x + room.width >= WORLD_SIZE - 2 or room.y + room.height >= WORLD_SIZE - 2:
                    attempt += 1
                    continue

                # determine if this room intersects with any other room
                intersects = False
                for j in range(0, len(self._rooms)):
                    if self._rooms_intersect(room, self._rooms[j]):
                        intersects = True
                        break

                # found an intersection, try again
                if intersects:
                    attempt += 1
                    continue

                # add room data to our 2d tile array
                logging.debug('Adding room data to world')
                y = room.y
                while y <= room.y + room.height:
                    x = room.x
                    while x <= room.x + room.width:
                        if x == room.x or x == room.x + room.width or y == room.y or y == room.y + room.height:
                            self._tiles[y][x] = TILE_WALL
                        else:
                            self._tiles[y][x] = TILE_FLOOR
                        x += 1
                    y += 1

                self._rooms.append(room)
                # set the players spawn to the first room generated
                if not self._spawn_x and not self._spawn_y:
                    self._spawn_x = int((room.x * TILE_SIZE) + ((room.width / 2) * TILE_SIZE))
                    self._spawn_y = int((room.y * TILE_SIZE) + ((room.height / 2) * TILE_SIZE))
                break

    def _create_tunnels(self):
        logging.debug('Creating tunnels')
        for room in self._rooms:
            target_room = None

            # get a random target
            while not target_room:
                target_room = self._rooms[random.randrange(0, len(self._rooms))]
                if room == target_room:  # same as current room
                    target_room = None
                    continue

            # calculate the center of the rooms
            start_x = int(room.x + (room.width / 2))
            start_y = int(room.y + (room.height / 2))
            end_x = int(target_room.x + (target_room.width / 2))
            end_y = int(target_room.y + (target_room.height / 2))
            logging.debug('Tunneling from {0},{1} to {2},{3}'.format(start_x, start_y, end_x, end_y))

            self._astar = AStar(self._tiles, WORLD_SIZE)
            path = self.find_path(start_x, start_y, end_x, end_y)
            # add the tunnel to the 2d tile array
            for pos in path:
                self._tiles[pos[0]][pos[1]] = 10

            logging.debug('Adding walls to tunnels')
            # add walls around the tunnel
            for pos in path:
                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        ty = pos[0] + y
                        tx = pos[1] + x
                        if self._tiles[ty][tx] == 0:
                            self._tiles[ty][tx] = TILE_WALL

    def _create_sprites(self):
        logging.debug('Creating sprites')
        for y in range(0, WORLD_SIZE):
            for x in range(0, WORLD_SIZE):
                tile = self._tiles[y][x]
                if tile == 0:
                    continue
                self._sprites.append(
                    pyglet.sprite.Sprite(
                        x=x * TILE_SIZE,
                        y=y * TILE_SIZE,
                        img=self._get_tile_texture(tile),
                        batch=self._batch
                    )
                )

    def _get_tile_texture(self, tile):
        if tile == TILE_FLOOR:
            return TEXTURE_FLOOR
        if tile == TILE_WALL:
            return TEXTURE_WALL

    def _rooms_intersect(self, a, b):
        return (
            a.x < (b.x + b.width) + 2 and
            a.x + a.width > b.x - 2 and
            a.y < (b.y + b.height) + 2 and
            a.y + a.height > b.y - 2
        )

    def find_path(self, sx, sy, ex, ey):
        return self._astar.find_path(sx, sy, ex, ey)

    def on_draw(self):
        self._batch.draw()

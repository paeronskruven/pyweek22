import random
import logging
import pyglet

from .astar import AStar

WORLD_SIZE = 98

ROOM_MAX_SIZE = 16
ROOM_MIN_SIZE = 8
ROOM_MAX_ATTEMPTS = 30

TILE_SIZE = 8


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
    _batch = pyglet.graphics.Batch()

    # todo: remove, tmp
    _floor = pyglet.image.SolidColorImagePattern(color=(60, 60, 60, 255)).create_image(TILE_SIZE, TILE_SIZE)
    _wall = pyglet.image.SolidColorImagePattern(color=(120, 120, 120, 255)).create_image(TILE_SIZE, TILE_SIZE)

    def __init__(self):
        pass

    def generate(self):
        logging.debug('Generating world')
        # initialize the 2d array according to the world size
        for y in range(0, WORLD_SIZE):
            self._tiles.append([0] * WORLD_SIZE)

        self._create_rooms()
        self._astar = AStar(self._tiles)

        self._create_tunnels()
        self._create_sprites()

    def _create_rooms(self):
        no_of_rooms = 20  # todo: calculate this with some algorithm
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
                            self._tiles[x][y] = 50
                        else:
                            self._tiles[x][y] = 10
                        x += 1
                    y += 1

                self._rooms.append(room)
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

            path = self.find_path(start_x, start_y, end_x, end_y)
            for pos in path:
                self._tiles[pos[0]][pos[1]] = 10

    def _create_sprites(self):
        logging.debug('Creating sprites')
        # todo: rework this to support multiple tile types
        for y in range(0, WORLD_SIZE):
            for x in range(0, WORLD_SIZE):
                if self._tiles[y][x] == 50:
                    self._sprites.append(
                        pyglet.sprite.Sprite(
                            x=x * TILE_SIZE,
                            y=y * TILE_SIZE,
                            img=self._wall,
                            batch=self._batch
                        )
                    )
                if self._tiles[y][x] == 10:
                    self._sprites.append(
                        pyglet.sprite.Sprite(
                            x=x * TILE_SIZE,
                            y=y * TILE_SIZE,
                            img=self._floor,
                            batch=self._batch
                        )
                    )

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

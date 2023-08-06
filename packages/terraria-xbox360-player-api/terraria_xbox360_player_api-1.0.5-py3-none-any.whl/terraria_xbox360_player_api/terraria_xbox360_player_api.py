from terraria_apis_objects import Color, Item, Buff, SpawnPoint
from datetime import timedelta
import bitarray as Bitarray
import binary_rw


class TerrariaXbox360Player:
	def __init__(self, path: str = None, version: int = None):
		if path is not None:
			self.read_from_file(path, version)

	@staticmethod
	def read_version_from_file(path: str) -> int:
		with binary_rw.BinaryReader(path) as file:
			return file.read_uint16()

	def reset(self):
		self.version = 21
		self.control_number = 0
		self.player_id = 0
		self.name = ""
		self.difficulty = 0
		self.hair_type = 0
		self.hair_dye = 0
		self.male = False
		self.life = 20
		self.max_life = 20
		self.mana = 20
		self.max_mana = 20
		self.angler_quests_finished = 0
		self.pet = -1

		self.hair_color = Color(0, 0, 0)
		self.skin_color = Color(0, 0, 0)
		self.eye_color = Color(0, 0, 0)
		self.shirt_color = Color(0, 0, 0)
		self.under_shirt_color = Color(0, 0, 0)
		self.pants_color = Color(0, 0, 0)
		self.shoe_color = Color(0, 0, 0)

		self.armor_and_accessories = []
		self.vanity_armor_and_accessories = []
		self.dyes = []
		self.inventory = []
		self.coins = []
		self.ammo = []
		self.piggy_bank = []
		self.safe = []
		self.buffs = []
		self.spawn_points = []
		self.quick_shortcuts = [-1, -1, -1, -1]

		self.is_accessories_hidden = Bitarray.bitarray()
		self.items_found = Bitarray.bitarray()
		self.recipes_found = Bitarray.bitarray()
		self.recipes_new = Bitarray.bitarray()
		self.crafting_stations_found = Bitarray.bitarray()

	def read_from_file(self, path: str, version: int = None) -> None:
		with binary_rw.BinaryReader(path) as file:
			def read_color() -> Color:
				return Color(file.read_byte(), file.read_byte(), file.read_byte())

			def read_item(disable_stack=False, disable_prefix=False) -> Item:  # normal read item
				id = file.read_int16()
				stack = 1
				prefix = 0
				if id != 0:
					if not disable_stack:
						stack = file.read_int16()
					if not disable_prefix:
						prefix = file.read_byte()
				return Item(id, stack, prefix)

			def read_bitarray(size_byte: int = -1) -> Bitarray.bitarray:
				if size_byte < 0:
					size_byte = file.read_uint16()
				bitarray = Bitarray.bitarray()
				for _ in range(0, size_byte):
					byte = file.read_byte()
					for x in range(7, -1, -1):
						bitarray.append(byte >> x & 1)
				return bitarray

			def read_container() -> list:
				def read_item2():
					stack = file.read_int16()
					id = file.read_int16()
					prefix = file.read_byte()
					return Item(id, stack, prefix)

				is_item = []
				for x in range(0, file.read_byte()):
					is_item.append(file.read_byte())

				container = []
				for x1 in is_item:
					row = []
					for x2 in range(0, 8):
						if x1 >> x2 & 1:
							row.append(read_item2())
						else:
							row.append(Item(0, 0, 0))
					container.append(row)
				return container

			self.reset()

			self.version = file.read_int16()
			self.control_number = file.read_uint32()
			self.name = file.read_string()
			self.difficulty = file.read_byte()
			self.hair_type = file.read_byte()
			self.hair_dye = file.read_byte()
			file.read_byte()
			self.male = file.read_bool()
			self.life = file.read_int16()
			self.max_life = file.read_int16()
			self.mana = file.read_int16()
			self.max_mana = file.read_int16()

			self.hair_color = read_color()
			self.skin_color = read_color()
			self.eye_color = read_color()
			self.shirt_color = read_color()
			self.under_shirt_color = read_color()
			self.pants_color = read_color()
			self.shoe_color = read_color()

			for _ in range(0, 8):  # read armor and accessories
				self.armor_and_accessories.append(read_item(disable_stack=True))

			for _ in range(0, 8):  # read vanity armor and accessories
				self.vanity_armor_and_accessories.append(read_item(disable_stack=True))

			file.read_byte()

			for _ in range(0, 8):  # read dyes
				self.dyes.append(read_item(disable_stack=True, disable_prefix=True))

			for _ in range(0, 4):  # read items in main inventory
				rows = []
				for _ in range(0, 10):
					rows.append(read_item())
				self.inventory.append(rows)

			for _ in range(0, 4):  # read items in coin slots
				self.coins.append(read_item())

			for _ in range(0, 4):  # read items in ammo slots
				self.ammo.append(read_item())

			self.piggy_bank = read_container()

			self.safe = read_container()

			for x in range(0, file.read_byte()):  # read buffs
				self.buffs.append(Buff(file.read_byte(), timedelta(microseconds=int(file.read_uint32()*16666.66))))

			self.pet = file.read_sbyte()

			self.quick_shortcuts[0] = file.read_sbyte()
			self.quick_shortcuts[2] = file.read_sbyte()
			self.quick_shortcuts[3] = file.read_sbyte()
			self.quick_shortcuts[1] = file.read_sbyte()

			self.items_found = read_bitarray()

			recipes_amount = file.read_uint16()

			self.recipes_found = read_bitarray(recipes_amount)

			self.recipes_new = read_bitarray(recipes_amount)

			self.crafting_stations_found = read_bitarray()

			for _ in range(0, 200):  # read spawn points
				x = file.read_int16()
				if x == -1:
					break
				else:
					self.spawn_points.append(
						SpawnPoint(x, file.read_int16(), file.read_int32(), file.read_string()))

			self.player_id = file.read_int32()
			self.angler_quests_finished = file.read_uint32()

			self.is_accessories_hidden = read_bitarray(1)
			for _ in range(0, 3):  # read which accessories are hidden
				self.is_accessories_hidden.pop(5)

	def write_to_file(self, path: str, version: int) -> None:
		with binary_rw.BinaryWriter(path) as file:
			def write_color(color: Color) -> None:
				if not isinstance(color, Color):
					raise TypeError("color must be an Color")
				file.write_byte(color.red)
				file.write_byte(color.green)
				file.write_byte(color.blue)

			def write_item(item: Item, disable_stack=False, disable_prefix=False) -> None:
				if not isinstance(item, Item):
					raise TypeError("item must be an Item")
				file.write_int16(item.id)
				if item.id != 0:
					if not disable_stack:
						file.write_int16(item.stack)
					if not disable_prefix:
						file.write_byte(item.prefix)

			def try_read_index(array, index, default):
				try:
					return array[index]
				except IndexError:
					return default

			def write_bitarray(bitarray: Bitarray.bitarray, size_byte: int, disable_writing_size=False) -> None:
				if not isinstance(bitarray, Bitarray.bitarray):
					raise TypeError("bitarray must be an bitarray")
				if not isinstance(size_byte, int):
					raise TypeError("size_byte must be an int")
				if not disable_writing_size:
					file.write_uint16(size_byte)
				for x1 in range(0, size_byte):
					byte = 0
					for x2 in range(0, 8):
						byte += 2 ** x2 * try_read_index(bitarray, x1 * 8 - x2 + 7, 0)
					file.write_byte(byte)

			def write_container(container: list) -> None:
				def write_item2(item: Item) -> None:
					if not isinstance(item, Item):
						raise TypeError("item must be an Item")
					file.write_int16(item.stack)
					file.write_int16(item.id)
					file.write_byte(item.prefix)

				file.write_byte(5)
				if not isinstance(container, list):
					raise TypeError("container must be a list")
				pos1 = file.file.tell()
				is_item = []
				for _ in range(0, 5):
					file.write_byte(0)

				for x1 in range(0, 5):
					if not isinstance(try_read_index(container, x1, []), list):
						raise TypeError("Elements of container must be a list")
					byte = 0
					for x2 in range(0, 8):
						if isinstance(try_read_index(try_read_index(container, x1, []), x2, None), Item):
							if container[x1][x2].id != 0:
								write_item2(container[x1][x2])
								byte += 2 ** x2
					is_item.append(byte)

				pos2 = file.file.tell()
				file.file.seek(pos1)
				for x in is_item:
					file.write_byte(x)
				file.file.seek(pos2)

			file.write_int16(self.version)
			file.write_uint32(self.control_number)
			file.write_string(self.name)
			file.write_byte(self.difficulty)
			file.write_byte(self.hair_type)
			file.write_byte(self.hair_dye)
			file.write_byte(0)
			file.write_bool(self.male)
			file.write_int16(self.life)
			file.write_int16(self.max_life)
			file.write_int16(self.mana)
			file.write_int16(self.max_mana)

			write_color(self.hair_color)
			write_color(self.skin_color)
			write_color(self.eye_color)
			write_color(self.shirt_color)
			write_color(self.under_shirt_color)
			write_color(self.pants_color)
			write_color(self.shoe_color)

			if not isinstance(self.armor_and_accessories, list):  # write armor and accessories
				raise TypeError("armor_and_accessories must be an list")
			for x in range(0, 8):
				write_item(try_read_index(self.armor_and_accessories, x, Item()), disable_stack=True)

			if not isinstance(self.vanity_armor_and_accessories, list):  # write vanity armor and accessories
				raise TypeError("vanity_armor_and_accessories must be an list")
			for x in range(0, 8):
				write_item(try_read_index(self.vanity_armor_and_accessories, x, Item()), disable_stack=True)

			file.write_byte(8)
			if not isinstance(self.dyes, list):  # write dyes
				raise TypeError("dyes must be an list")
			for x in range(0, 8):
				write_item(try_read_index(self.dyes, x, Item()), disable_stack=True, disable_prefix=True)

			if not isinstance(self.inventory, list):  # write items in main inventory
				raise TypeError("inventory must be an list")
			for x1 in range(0, 4):
				for x2 in range(0, 10):
					if not isinstance(try_read_index(self.inventory, x1, []), list):
						raise TypeError("Elements of inventory must be a list")
					write_item(try_read_index(try_read_index(self.inventory, x1, []), x2, Item()))

			if not isinstance(self.coins, list):  # write items in coin slots
				raise TypeError("coins must be an list")
			for x in range(0, 4):
				write_item(try_read_index(self.coins, x, Item()))

			if not isinstance(self.ammo, list):  # write items in ammo slots
				raise TypeError("ammo must be an list")
			for x in range(0, 4):
				write_item(try_read_index(self.ammo, x, Item()))

			if not isinstance(self.piggy_bank, list):  # write items in piggy bank
				raise TypeError("piggy_bank must be an list")
			write_container(self.piggy_bank)

			if not isinstance(self.safe, list):  # write items in safe
				raise TypeError("safe must be an list")
			write_container(self.safe)

			if not isinstance(self.buffs, list):  # write buffs
				raise TypeError("buffs must be an list")
			file.write_byte(len(self.buffs))
			for x in range(0, len(self.buffs)):
				if isinstance(self.buffs[x], Buff):
					file.write_byte(self.buffs[x].id)
					if self.buffs[x].time.total_seconds() > 71582788.26666:
						raise ValueError("time in Buff may not be above 828.12:06:28.266666")
					if self.buffs[x].time.total_seconds() < 0:
						raise ValueError("time in Buff may not be below 0.00:00:00.000000")
					file.write_int32(int(self.buffs[x].time.total_seconds()*60))
					file.write_uint32(int(self.buffs[x].time.total_seconds()*60))
				else:
					raise TypeError("Elements of buffs must be a Buff")

			file.write_sbyte(self.pet)

			if not isinstance(self.quick_shortcuts, list):  # write quick shortcuts
				raise TypeError("quick_shortcuts must be an list")
			file.write_sbyte(try_read_index(self.quick_shortcuts, 0, -1))
			file.write_sbyte(try_read_index(self.quick_shortcuts, 2, -1))
			file.write_sbyte(try_read_index(self.quick_shortcuts, 3, -1))
			file.write_sbyte(try_read_index(self.quick_shortcuts, 1, -1))

			if not isinstance(self.items_found, Bitarray.bitarray):  # write found items
				raise TypeError("items_found must be an bitarray")
			write_bitarray(self.items_found, 445)

			if not isinstance(self.recipes_found, Bitarray.bitarray):  # write found recipes
				raise TypeError("recipes_found must be an bitarray")
			write_bitarray(self.recipes_found, 185)

			if not isinstance(self.recipes_new, Bitarray.bitarray):  # write new recipes
				raise TypeError("recipes_new must be an bitarray")
			write_bitarray(self.recipes_new, 185, disable_writing_size=True)

			if not isinstance(self.crafting_stations_found, Bitarray.bitarray):  # write found crafting stations
				raise TypeError("crafting_stations_found must be an bitarray")
			write_bitarray(self.crafting_stations_found, 43)

			if not isinstance(self.spawn_points, list):  # write spawn points
				raise TypeError("spawn_points must be an list")
			for x in range(0, min(200, len(self.spawn_points))):
				if not isinstance(self.spawn_points[x], SpawnPoint):
					raise TypeError("Elements of spawn_points must be a SpawnPoint")
				file.write_int16(self.spawn_points[x].x)
				file.write_int16(self.spawn_points[x].y)
				file.write_int32(self.spawn_points[x].world_id)
				file.write_string(self.spawn_points[x].world_name)
			file.write_int16(-1)

			file.write_int32(self.player_id)
			file.write_uint32(self.angler_quests_finished)

			if not isinstance(self.is_accessories_hidden, Bitarray.bitarray):  # write which accessories are hidden
				raise TypeError("is_accessories_hidden must be an bitarray")
			write_bitarray(self.is_accessories_hidden, 1, disable_writing_size=True)

	MAX_SUPPORTED_VERSION = 21
	MIN_SUPPORTED_VERSION = 21

	version = 21
	control_number = 0
	player_id = 0
	name = ""
	difficulty = 0  # 0 - softcore, 1 - mediumcore, 2 - hardcore
	hair_type = 0
	hair_dye = 0
	male = False
	life = 20
	max_life = 20
	mana = 20
	max_mana = 20
	angler_quests_finished = 0
	pet = -1

	hair_color = Color(0, 0, 0)
	skin_color = Color(0, 0, 0)
	eye_color = Color(0, 0, 0)
	shirt_color = Color(0, 0, 0)
	under_shirt_color = Color(0, 0, 0)
	pants_color = Color(0, 0, 0)
	shoe_color = Color(0, 0, 0)

	armor_and_accessories = []
	vanity_armor_and_accessories = []
	dyes = []
	inventory = []
	coins = []
	ammo = []
	piggy_bank = []
	safe = []
	buffs = []
	spawn_points = []
	quick_shortcuts = [-1, -1, -1, -1]

	is_accessories_hidden = Bitarray.bitarray()
	items_found = Bitarray.bitarray()
	recipes_found = Bitarray.bitarray()
	recipes_new = Bitarray.bitarray()
	crafting_stations_found = Bitarray.bitarray()

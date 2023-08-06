from terraria_apis_objects import Color, Item, Buff, SpawnPoint
from binary_rw import BinaryReader, BinaryWriter
import terraria_pc_apis_ids
import bitarray as Bitarray
from Crypto.Cipher import AES
from tempfile import gettempdir
from time import time_ns
from os import remove
from datetime import datetime, timedelta


class InventoryItem(Item):
	is_favorite = False

	def __init__(self, id: int = 0, stack: int = 0, prefix: int = 0, is_favorite: bool = False):
		self.is_favorite = is_favorite
		super().__init__(id, stack, prefix)


class TerrariaPCPlayer:
	def __init__(self, path: str = None, version: int = None):
		if path is not None:
			self.read_from_file(path, version)

	class BinaryReaderDecrypt(BinaryReader):
		def __init__(self, path: str, key: bytes, block_size: int = 2048):
			file_path = f"{gettempdir()}/binary_rw_decrypted_{time_ns()}.tmp"
			decrypt_aes = AES.new(key, AES.MODE_CBC, key)
			with open(path, "rb") as file_in, open(file_path, "wb") as file_out:  # decrypt file
				while True:
					data = file_in.read(block_size)
					if not data:
						break
					file_out.write(decrypt_aes.decrypt(data))

			super().__init__(file_path)

		def __exit__(self, exc_type, exc_value, tb):
			super().__exit__(exc_type, exc_value, tb)

			remove(self.file.name)

	class BinaryWriterEncrypt(BinaryWriter):
		def __init__(self, path: str, key: bytes, block_size: int = 2048):
			self.path = path
			self.key = key
			self.block_size = block_size
			self.file_path = f"{gettempdir()}/binary_rw_unencrypted_{time_ns()}.tmp"
			super().__init__(self.file_path)

		def __exit__(self, exc_type, exc_value, tb):
			super().__exit__(exc_type, exc_value, tb)
			encrypt_aes = AES.new(self.key, AES.MODE_CBC, self.key)
			with open(self.file_path, "rb") as file_in, open(self.path, "wb") as file_out:
				while True:
					data = file_in.read(self.block_size)
					if len(data) % 16 != 0:
						ending_bytes = 16 - (len(data) % 16)
						data += bytes([ending_bytes] * ending_bytes)
						file_out.write(encrypt_aes.encrypt(data))
						break
					file_out.write(encrypt_aes.encrypt(data))

			remove(self.file.name)

	@staticmethod
	def read_version_from_file(path: str) -> int:
		with TerrariaPCPlayer.BinaryReaderDecrypt(path, bytes.fromhex("6800330079005F006700550079005A00")) as file:
			return file.read_int32()

	def reset(self):
		self.version = 244
		self.is_favorite = False
		self.name = ""
		self.difficulty = 0
		self.playtime = timedelta()
		self.hair = 0
		self.hair_dye = 0
		self.is_accessories_hidden = Bitarray.bitarray()
		self.is_pet_hidden = False
		self.is_light_pet_hidden = False
		self.is_male = False
		self.style = 0
		self.life = 100
		self.max_life = 100
		self.mana = 20
		self.max_mana = 20
		self.has_demon_heart_accessory_slot = False
		self.is_biome_torches_unlocked = False
		self.is_using_biome_torches = False
		self.has_downed_DD2_event = False
		self.tax_money = 0
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
		self.misc_equips = []
		self.misc_dyes = []
		self.piggy_bank = []
		self.safe = []
		self.defenders_forge = []
		self.void_vault = []
		self.is_void_vault_enabled = False
		self.buffs = []
		self.spawn_points = []
		self.is_hotbar_locked = False
		self.is_time_info_hidden = False
		self.is_weather_info_hidden = False
		self.is_fishing_power_info_hidden = False
		self.is_position_info_hidden = False
		self.is_depth_info_hidden = False
		self.is_creature_count_info_hidden = False
		self.is_kill_count_info_hidden = False
		self.is_moon_phase_info_hidden = False
		self.is_movement_speed_info_hidden = False
		self.is_treasure_finder_info_hidden = False
		self.is_rare_creatures_finder_info_hidden = False
		self.is_damage_per_second_info_hidden = False
		self.angler_quests_finished = 0
		self.quick_shortcuts = [-1, -1, -1, -1]
		self.is_ruler_enabled = False
		self.is_mechanical_ruler_enabled = False
		self.is_auto_placement_actuators_enabled = False
		self.is_auto_paint_enabled = False
		self.red_wires_visibility = 0
		self.blue_wires_visibility = 0
		self.green_wires_visibility = 0
		self.yellow_wires_visibility = 0
		self.is_showing_showing_wires_and_actuators_forced = False
		self.actuators_visibility = 0
		self.is_tile_replacement_enabled = True
		self.is_biome_torches_enabled = False
		self.bartender_quest_log = 0
		self.is_dead = False
		self.time_to_respawn = timedelta()
		self.last_time_player_was_saved = datetime(1, 1, 1)
		self.golfer_score_accumulated = 0
		self.item_research = {}
		self.temporary_mouse_item = Item()
		self.temporary_research_item = Item()
		self.temporary_guide_item = Item()
		self.temporary_goblin_item = Item()
		self.is_godmode_enabled = False
		self.is_far_placement_enabled = True
		self.spawn_rate = 0.5

	def read_from_file(self, path: str, version: int = None) -> None:
		with TerrariaPCPlayer.BinaryReaderDecrypt(path, bytes.fromhex("6800330079005F006700550079005A00")) as file:
			self.version = file.read_int32()
			if version is None:
				version = self.version
			if not isinstance(version, int):
				raise TypeError("version must be int")

			def read_color() -> Color:
				return Color(file.read_byte(), file.read_byte(), file.read_byte())

			def read_item(disable_stack: bool = False, disable_prefix: bool = False) -> Item:  # normal read item
				if version < 38:
					return read_item_legacy(disable_stack, disable_prefix)
				id = file.read_int32()
				stack = 1
				prefix = 0
				if -48 <= id <= -1:
					to_new_id = (3521, 3520, 3519, 3518, 3517, 3516, 3515, 3514, 3513, 3512, 3511, 3510, 3509, 3508,
								 3507, 3506, 3505, 3504, 3764, 3765, 3766, 3767, 3768, 3769, 3503, 3502, 3501, 3500,
								 3499, 3498, 3497, 3496, 3495, 3494, 3493, 3492, 3491, 3490, 3489, 3488, 3487, 3486,
								 3485, 3484, 3483, 3482, 3481, 3480)
					id = to_new_id[-id - 1]
				elif id < -48:
					id = 0

				if not disable_stack:
					stack = file.read_int32()

				if not disable_prefix:
					prefix = file.read_byte()

				return Item(id, stack, prefix)

			def read_item_legacy(disable_stack: bool = False, disable_prefix: bool = False) -> Item:
				name = file.read_string()
				stack = 1
				prefix = 0
				if not disable_stack:
					stack = file.read_int32()
				if (not disable_prefix) and version >= 36:
					prefix = file.read_byte()

				if version <= 4:
					if name == "Cobalt Helmet":
						name = "Jungle Hat"
					elif name == "Cobalt Breastplate":
						name = "Jungle Shirt"
					elif name == "Cobalt Greaves":
						name = "Jungle Pants"
				if version <= 13 and name == "Jungle Rose":
					name = "Jungle Spores"
				if version <= 20:
					if name == "Gills potion":
						name = "Gills Potion"
					elif name == "Thorn Chakrum":
						name = "Thorn Chakram"
					elif name == "Ball 'O Hurt":
						name = "Ball O' Hurt"
				if version <= 41 and name == "Iron Chain":
					name = "Chain"
				if version <= 44 and name == "Orb of Light":
					name = "Shadow Orb"
				if version <= 46:
					if name == "Black Dye":
						name = "Black Thread"
					elif name == "Green Dye":
						name = "Green Thread"

				return Item(terraria_pc_apis_ids.item_name_to_id(name)[0], stack, prefix)

			def read_bitarray(size: int = -1) -> Bitarray.bitarray:
				if not isinstance(size, int):
					raise TypeError("size must be an int")

				if size < 0:
					size = file.read_uint16()
				bitarray = Bitarray.bitarray()
				for _ in range(0, size):
					byte = file.read_byte()
					for x in range(0, 8):
						bitarray.append(byte >> x & 1)
				return bitarray

			def read_container(size_x: int = 10, size_y: int = 4):
				if not isinstance(size_x, int):
					raise TypeError("size_x must be an int")
				if not isinstance(size_y, int):
					raise TypeError("size_y must be an int")

				container = []
				for _ in range(0, size_y):
					row = []
					for _ in range(0, size_x):
						row.append(read_item())
					container.append(row)
				return container

			if version >= 135:
				file.read_int64()
				file.read_int32()
				self.is_favorite = bool(file.read_uint64() & 1)

			self.name = file.read_string()

			if version >= 10:
				if version >= 17:
					self.difficulty = file.read_byte()
				else:
					self.difficulty = file.read_bool() * 2

			if version >= 138:
				self.playtime = timedelta(microseconds=int(file.read_int64() / 10))

			self.hair = file.read_int32()

			if version >= 82:
				self.hair_dye = file.read_byte()

			if version >= 83:
				if version >= 124:
					self.is_accessories_hidden += read_bitarray(2)
					for _ in range(0, 6):
						self.is_accessories_hidden.pop(10)

				else:
					self.is_accessories_hidden = read_bitarray(1)

			if version >= 119:
				byte = file.read_byte()
				self.is_pet_hidden = bool(byte & 1)
				self.is_light_pet_hidden = bool(byte >> 1 & 1)

			if version <= 17:
				self.is_male = not (self.hair == 5 or self.hair == 6 or self.hair == 9 or self.hair == 11)
				self.style = 0
			elif version < 107:
				self.is_male = file.read_bool()
				self.style = 0
			else:
				byte = file.read_byte()
				if byte <= 7:
					self.style = byte % 4
					self.is_male = byte < 4
				else:
					self.style = int(byte / 2)
					self.is_male = not (byte & 1)

			if version < 161 and self.style == 3 and (not self.is_male):
				self.style = 4

			self.life = file.read_int32()
			self.max_life = file.read_int32()
			self.mana = file.read_int32()
			self.max_mana = file.read_int32()

			if version >= 125:
				self.has_demon_heart_accessory_slot = file.read_bool()

			if version >= 229:
				self.is_biome_torches_unlocked = file.read_bool()
				self.is_using_biome_torches = file.read_bool()

			if version >= 182:
				self.has_downed_DD2_event = file.read_bool()

			if version >= 128:
				self.tax_money = file.read_int32()

			self.hair_color = read_color()
			self.skin_color = read_color()
			self.eye_color = read_color()
			self.shirt_color = read_color()
			self.under_shirt_color = read_color()
			self.pants_color = read_color()
			self.shoe_color = read_color()

			amount = 10
			if version < 124:
				amount = 8

			for _ in range(0, amount):
				self.armor_and_accessories.append(read_item(disable_stack=True))

			amount = 10
			if version < 81:
				amount = 3
			elif version < 124:
				amount = 8

			if version >= 6:
				for _ in range(0, amount):
					self.vanity_armor_and_accessories.append(read_item(disable_stack=True))

			if version >= 47:
				for _ in range(0, amount):
					self.dyes.append(read_item(disable_stack=True))

			amount = 4
			if version >= 58:
				amount = 5

			for _ in range(0, amount):
				row = []
				for _ in range(0, 10):
					item = read_item()
					if version >= 114:
						item = InventoryItem(item.id, item.stack, item.prefix, file.read_bool())
					row.append(item)
				self.inventory.append(row)

			for _ in range(0, 4):
				item = read_item()
				if version >= 114:
					item = InventoryItem(item.id, item.stack, item.prefix, file.read_bool())
				self.coins.append(item)

			if version >= 15:
				for _ in range(0, 4):
					item = read_item()
					if version >= 114:
						item = InventoryItem(item.id, item.stack, item.prefix, file.read_bool())
					self.ammo.append(item)

			if version >= 117:
				if version < 136:
					self.misc_equips.append(Item())
					self.misc_dyes.append(Item())
				for _ in range(version < 136, 5):
					self.misc_equips.append(read_item(disable_stack=True))
					self.misc_dyes.append(read_item(disable_stack=True))

			amount = 10
			if version < 58:
				amount = 5

			self.piggy_bank = read_container(amount)

			if version >= 20:
				self.safe = read_container(amount)

			if version >= 182:
				self.defenders_forge = read_container()

			if version >= 198:
				self.void_vault = read_container()

			if version >= 199:
				self.is_void_vault_enabled = file.read_bool()

			if version >= 11:
				amount = 22
				if version < 74:
					amount = 10

				for _ in range(0, amount):
					buff_id = file.read_int32()
					buff_time = file.read_int32()
					if buff_id != 0:
						self.buffs.append(Buff(buff_id, timedelta(microseconds=int(buff_time * 16666.66))))

			for _ in range(0, 200):
				x = file.read_int32()
				if x == -1:
					break
				self.spawn_points.append(SpawnPoint(x, file.read_int32(), file.read_int32(), file.read_string()))

			if version >= 16:
				self.is_hotbar_locked = file.read_bool()

			if version >= 115:
				self.is_time_info_hidden = file.read_bool()
				self.is_weather_info_hidden = file.read_bool()
				self.is_fishing_power_info_hidden = file.read_bool()
				self.is_position_info_hidden = file.read_bool()
				self.is_depth_info_hidden = file.read_bool()
				self.is_creature_count_info_hidden = file.read_bool()
				self.is_kill_count_info_hidden = file.read_bool()
				self.is_moon_phase_info_hidden = file.read_bool()
				file.read_bool()
				self.is_movement_speed_info_hidden = file.read_bool()
				self.is_treasure_finder_info_hidden = file.read_bool()
				self.is_rare_creatures_finder_info_hidden = file.read_bool()
				self.is_damage_per_second_info_hidden = file.read_bool()

			if version >= 115:
				self.angler_quests_finished = file.read_int32()

			if version >= 164:
				for x in range(0, 4):
					self.quick_shortcuts[x] = file.read_int32()

			if version >= 164:
				self.is_ruler_enabled = not file.read_int32()
				self.is_mechanical_ruler_enabled = not file.read_int32()
				self.is_auto_placement_actuators_enabled = not file.read_int32()
				self.is_auto_paint_enabled = not file.read_int32()
				self.red_wires_visibility = file.read_int32()
				self.blue_wires_visibility = file.read_int32()
				self.green_wires_visibility = file.read_int32()
				self.yellow_wires_visibility = file.read_int32()

			if version >= 167:
				self.is_showing_showing_wires_and_actuators_forced = not file.read_int32()
				self.actuators_visibility = file.read_int32()

			if version >= 197:
				self.is_tile_replacement_enabled = not file.read_int32()

			if version >= 230:
				self.is_biome_torches_enabled = not file.read_int32()

			if version >= 181:
				self.bartender_quest_log = file.read_int32()

			if version >= 200:
				self.is_dead = file.read_bool()
				if self.is_dead:
					self.time_to_respawn = timedelta(microseconds=int(file.read_int32() * 16666.66))

			if version >= 202:
				self.last_time_player_was_saved += timedelta(microseconds=int((file.read_uint64() & 4611686018427387903) / 10))

			if version >= 206:
				self.golfer_score_accumulated = file.read_int32()

			if version >= 218:
				for _ in range(0, file.read_int32()):
					key = file.read_string()
					self.item_research[terraria_pc_apis_ids.item_game_name_to_id(key)[0]] = file.read_int32()

			if version >= 214:
				byte = file.read_byte()
				if byte & 1:
					self.temporary_mouse_item = read_item()
				if byte >> 1 & 1:
					self.temporary_research_item = read_item()
				if byte >> 2 & 1:
					self.temporary_guide_item = read_item()
				if byte >> 3 & 1:
					self.temporary_goblin_item = read_item()

			if version >= 220:
				while file.read_bool():
					key = file.read_int16()
					if key == 5:
						self.is_godmode_enabled = file.read_bool()
					elif key == 11:
						self.is_far_placement_enabled = file.read_bool()
					elif key == 14:
						self.spawn_rate = file.read_single()

	def write_to_file(self, path: str, version: int = None) -> None:
		if version is None:
			version = self.version
		if not isinstance(version, int):
			raise TypeError("version must be int")

		with TerrariaPCPlayer.BinaryWriterEncrypt(path, bytes.fromhex("6800330079005F006700550079005A00")) as file:
			def write_color(color: Color) -> None:
				if not isinstance(color, Color):
					raise TypeError("color must be an Color")
				file.write_byte(color.red)
				file.write_byte(color.green)
				file.write_byte(color.blue)

			def write_item(item: Item, disable_stack: bool = False, disable_prefix: bool = False) -> None:
				if not isinstance(item, Item):
					raise TypeError("item must be an Item")
				if item.id == 0:
					item.prefix = 0
					item.stack = 0
				if version < 38:
					write_item_legacy(item, disable_stack, disable_prefix)
					return
				if version < 146:
					to_old_id = {3521: -1, 3520: -2, 3519: -3, 3518: -4, 3517: -5, 3516: -6, 3515: -7, 3514: -8,
								 3513: -9, 3512: -10, 3511: -11, 3510: -12, 3509: -13, 3508: -14, 3507: -15, 3506: -16,
								 3505: -17, 3504: -18, 3764: -19, 3765: -20, 3766: -21, 3767: -22, 3768: -23, 3769: -24,
								 3503: -25, 3502: -26, 3501: -27, 3500: -28, 3499: -29, 3498: -30, 3497: -31, 3496: -32,
								 3495: -33, 3494: -34, 3493: -35, 3492: -36, 3491: -37, 3490: -38, 3489: -39, 3488: -40,
								 3487: -41, 3486: -42, 3485: -43, 3484: -44, 3483: -45, 3482: -46, 3481: -47, 3480: -48}
					item.id = to_old_id.get(item.id, item.id)
				file.write_int32(item.id)
				if not disable_stack:
					file.write_int32(item.stack)
				if not disable_prefix:
					file.write_byte(item.prefix)

			def write_item_legacy(item: Item, disable_stack: bool = False, disable_prefix: bool = False) -> None:
				if not isinstance(item, Item):
					raise TypeError("item must be an Item")
				if 1 <= item.id <= 603 or item.id in (3521, 3520, 3519, 3518, 3517, 3516, 3515, 3514, 3513, 3512, 3511,
													  3510, 3509, 3508, 3507, 3506, 3505, 3504, 3764, 3765, 3766, 3767,
													  3768, 3769, 3503, 3502, 3501, 3500, 3499, 3498, 3497, 3496, 3495,
													  3494, 3493, 3492, 3491, 3490, 3489, 3488, 3487, 3486, 3485, 3484,
													  3483, 3482, 3481, 3480):
					name = terraria_pc_apis_ids.item_id_to_name(item.id)
					if version <= 4:
						if name == "Jungle Hat":
							name = "Cobalt Helmet"
						elif name == "Jungle Shirt":
							name = "Cobalt Breastplate"
						elif name == "Jungle Pants":
							name = "Cobalt Greaves"
					if version <= 13 and name == "Jungle Spores":
						name = "Jungle Rose"
					if version <= 20:
						if name == "Gills Potion":
							name = "Gills potion"
						elif name == "Thorn Chakram":
							name = "Thorn Chakrum"
						elif name == "Ball O' Hurt":
							name = "Ball 'O Hurt"
					if version <= 41 and name == "Chain":
						name = "Iron Chain"
					if version <= 44 and name == "Shadow Orb":
						name = "Orb of Light"
					if version <= 46:
						if name == "Black Thread":
							name = "Black Dye"
						elif name == "Green Thread":
							name = "Green Dye"
				else:
					name = ""
				file.write_string(name)
				if name == "None" or name == "":
					item.stack = 0
					item.prefix = 0
				if not disable_stack:
					file.write_int32(item.stack)
				if (not disable_prefix) and version >= 36:
					file.write_byte(item.prefix)

			def try_read_index(array, index, default):
				try:
					return array[index]
				except IndexError:
					return default

			def write_bitarray(bitarray: Bitarray.bitarray, size: int, disable_writing_size: bool = False) -> None:
				if not isinstance(bitarray, Bitarray.bitarray):
					raise TypeError("bitarray must be an bitarray")
				if not isinstance(size, int):
					raise TypeError("size_byte must be an int")
				if not disable_writing_size:
					file.write_uint16(size)
				for x1 in range(0, size):
					byte = 0
					for x2 in range(0, 8):
						byte += 2 ** x2 * try_read_index(bitarray, x1 * 8 + x2, 0)
					file.write_byte(byte)

			def write_container(container: list = None, size_x: int = 10, size_y: int = 4):
				if container is None:
					container = []
				if not isinstance(container, list):
					raise TypeError("container must be an list")
				if not isinstance(size_x, int):
					raise TypeError("size_x must be an int")
				if not isinstance(size_y, int):
					raise TypeError("size_y must be an int")

				for x1 in range(0, size_y):
					if not isinstance(try_read_index(container, x1, []), list):
						raise TypeError("Elements of container must be a list")
					for x2 in range(0, size_x):
						write_item(try_read_index(try_read_index(container, x1, []), x2, Item()))

			file.write_int32(version)

			if version >= 135:
				file.write_int64(244154697780061554)
				file.write_int32(0)
				file.write_int64(int(self.is_favorite))

			file.write_string(self.name)

			if version >= 10:
				if version >= 17:
					file.write_byte(self.difficulty)
				else:
					file.write_bool(int(self.difficulty / 2))

			if version >= 138:
				if not isinstance(self.playtime, timedelta):
					raise TypeError("playtime must be an timedelta")
				if self.playtime.total_seconds() > 922337203685.4774169921875:
					raise ValueError("playtime may not be above 10675199.2:48:05.477478")
				if self.playtime.total_seconds() < -922337203685.4776611328125:
					raise ValueError("playtime may not be above -10675200,21:11:54.522278")
				file.write_int64(int(self.playtime.total_seconds() * 10000000))

			file.write_int32(self.hair)

			if version >= 82:
				file.write_byte(self.hair_dye)

			if version >= 83:
				if version >= 124:
					write_bitarray(self.is_accessories_hidden, 2, True)
				else:
					write_bitarray(self.is_accessories_hidden, 1, True)

			if version >= 119:
				if self.is_pet_hidden != 0 and self.is_pet_hidden != 1:
					raise ValueError(f"is_pet_hidden must be true or false")
				if self.is_light_pet_hidden != 0 and self.is_light_pet_hidden != 1:
					raise ValueError(f"is_light_pet_hidden must be true or false")
				byte = self.is_pet_hidden
				byte += self.is_light_pet_hidden << 1
				file.write_byte(byte)

			if version > 17:
				if self.is_male != 0 and self.is_male != 1:
					raise ValueError(f"is_male must be true or false")
				if version < 107:
					file.write_bool(self.is_male)
				else:
					if not isinstance(self.style, int):
						raise TypeError("style must be an int")
					style = self.style
					if version < 161 and style == 4 and (not self.is_male):
						style = 3
					if 0 > style:
						file.write_byte((not self.is_male) * 4)
					elif style < 4:
						file.write_byte((not self.is_male) * 4 + style)
					else:
						file.write_byte(style * 2 + (not self.is_male))

			file.write_int32(self.life)
			file.write_int32(self.max_life)
			file.write_int32(self.mana)
			file.write_int32(self.max_mana)

			if version >= 125:
				file.write_bool(self.has_demon_heart_accessory_slot)

			if version >= 229:
				file.write_bool(self.is_biome_torches_unlocked)
				file.write_bool(self.is_using_biome_torches)

			if version >= 182:
				file.write_bool(self.has_downed_DD2_event)

			if version >= 128:
				file.write_int32(self.tax_money)

			write_color(self.hair_color)
			write_color(self.skin_color)
			write_color(self.eye_color)
			write_color(self.shirt_color)
			write_color(self.under_shirt_color)
			write_color(self.pants_color)
			write_color(self.shoe_color)

			amount = 10
			if version < 124:
				amount = 8

			if not isinstance(self.armor_and_accessories, list):
				raise TypeError("armor_and_accessories must be an list")
			for x in range(0, amount):
				write_item(try_read_index(self.armor_and_accessories, x, Item()), disable_stack=True)

			amount = 10
			if version < 81:
				amount = 3
			elif version < 124:
				amount = 8

			if version >= 6:
				if not isinstance(self.vanity_armor_and_accessories, list):
					raise TypeError("vanity_armor_and_accessories must be an list")
				for x in range(0, amount):
					write_item(try_read_index(self.vanity_armor_and_accessories, x, Item()), disable_stack=True)

			if version >= 47:
				if not isinstance(self.dyes, list):
					raise TypeError("dyes must be an list")
				for x in range(0, amount):
					write_item(try_read_index(self.dyes, x, Item()), disable_stack=True)

			amount = 4
			if version >= 58:
				amount = 5

			if not isinstance(self.inventory, list):
				raise TypeError("inventory must be an list")
			for x1 in range(0, amount):
				if not isinstance(try_read_index(self.inventory, x1, []), list):
					raise TypeError("Elements of inventory must be a list")
				for x2 in range(0, 10):
					item = try_read_index(try_read_index(self.inventory, x1, []), x2, InventoryItem())
					write_item(item)
					if version >= 114:
						try:
							file.write_bool(item.is_favorite)
						except AttributeError:
							file.write_bool(False)

			if not isinstance(self.coins, list):
				raise TypeError("coins must be an list")
			for x in range(0, 4):
				item = try_read_index(self.coins, x, InventoryItem())
				write_item(item)
				if version >= 114:
					try:
						file.write_bool(item.is_favorite)
					except AttributeError:
						file.write_bool(False)

			if version >= 15:
				if not isinstance(self.ammo, list):
					raise TypeError("ammo must be an list")
				for x in range(0, 4):
					item = try_read_index(self.ammo, x, InventoryItem())
					write_item(item)
					if version >= 114:
						try:
							file.write_bool(item.is_favorite)
						except AttributeError:
							file.write_bool(False)

			if version >= 117:
				if not isinstance(self.misc_equips, list):
					raise TypeError("misc_equips must be an list")
				if not isinstance(self.misc_dyes, list):
					raise TypeError("misc_dyes must be an list")
				for x in range(version < 136, 5):
					write_item(try_read_index(self.misc_equips, x, Item()), disable_stack=True)
					write_item(try_read_index(self.misc_dyes, x, Item()), disable_stack=True)

			amount = 10
			if version < 58:
				amount = 5

			write_container(self.piggy_bank, amount)
			if version >= 20:
				write_container(self.safe, amount)

			if version >= 182:
				write_container(self.defenders_forge)

			if version >= 198:
				write_container(self.void_vault)

			if version >= 199:
				file.write_bool(self.is_void_vault_enabled)

			if version >= 11:
				amount = 22
				if version < 74:
					amount = 10

				if not isinstance(self.buffs, list):
					raise TypeError("buffs must be an list")
				for x in range(0, amount):
					buff = try_read_index(self.buffs, x, Buff())
					if not isinstance(buff, Buff):
						raise TypeError("Elements of buffs must be a Buff")
					file.write_int32(buff.id)
					if not isinstance(buff.time, timedelta):
						raise TypeError("time in Buff must be timedelta")
					if self.playtime.total_seconds() > 35791394.116667:
						raise ValueError("time in Buff may not be above 414.06:03:14.116667")
					if self.playtime.total_seconds() < -35791394.149999:
						raise ValueError("time in Buff may not be below -415.17:56:45.850001")
					file.write_int32(int(buff.time.total_seconds() * 60))

			if not isinstance(self.spawn_points, list):
				raise TypeError("spawn_points must be an list")
			for x in range(0, min(len(self.spawn_points), 200)):
				if not isinstance(self.spawn_points[x], SpawnPoint):
					raise TypeError("Elements of spawn_points must be a SpawnPoint")
				file.write_int32(self.spawn_points[x].x)
				file.write_int32(self.spawn_points[x].y)
				file.write_int32(self.spawn_points[x].world_id)
				file.write_string(self.spawn_points[x].world_name)
			file.write_int32(-1)

			if version >= 16:
				file.write_bool(self.is_hotbar_locked)

			if version >= 115:
				file.write_bool(self.is_time_info_hidden)
				file.write_bool(self.is_weather_info_hidden)
				file.write_bool(self.is_fishing_power_info_hidden)
				file.write_bool(self.is_position_info_hidden)
				file.write_bool(self.is_depth_info_hidden)
				file.write_bool(self.is_creature_count_info_hidden)
				file.write_bool(self.is_kill_count_info_hidden)
				file.write_bool(self.is_moon_phase_info_hidden)
				file.write_bool(False)
				file.write_bool(self.is_movement_speed_info_hidden)
				file.write_bool(self.is_treasure_finder_info_hidden)
				file.write_bool(self.is_rare_creatures_finder_info_hidden)
				file.write_bool(self.is_damage_per_second_info_hidden)

			if version >= 115:
				file.write_int32(self.angler_quests_finished)

			if version >= 164:
				if not isinstance(self.quick_shortcuts, list):
					raise TypeError("quick_shortcuts must be an list")
				for x in range(0, 4):
					file.write_int32(try_read_index(self.quick_shortcuts, x, -1))

			if version >= 164:
				file.write_int32(not self.is_ruler_enabled)
				file.write_int32(not self.is_mechanical_ruler_enabled)
				file.write_int32(not self.is_auto_placement_actuators_enabled)
				file.write_int32(not self.is_auto_paint_enabled)
				file.write_int32(self.red_wires_visibility)
				file.write_int32(self.blue_wires_visibility)
				file.write_int32(self.green_wires_visibility)
				file.write_int32(self.yellow_wires_visibility)

			if version >= 167:
				file.write_int32(not self.is_showing_showing_wires_and_actuators_forced)
				file.write_int32(self.actuators_visibility)

			if version >= 197:
				file.write_int32(not self.is_tile_replacement_enabled)

			if version >= 230:
				file.write_int32(not self.is_biome_torches_enabled)

			if version >= 181:
				file.write_int32(self.bartender_quest_log)

			if version >= 200:
				file.write_bool(self.is_dead)
				if self.is_dead:
					if not isinstance(self.time_to_respawn, timedelta):
						raise TypeError("time_to_respawn must be timedelta")
					if self.playtime.total_seconds() > 35791394.116667:
						raise ValueError("time_to_respawn may not be above 414.06:03:14.116667")
					if self.playtime.total_seconds() < -35791394.149999:
						raise ValueError("time_to_respawn not be below -415.17:56:45.850001")
					file.write_int32(int(self.time_to_respawn.total_seconds() * 60))

			if version >= 202:
				if not isinstance(self.last_time_player_was_saved, datetime):
					raise TypeError("last_time_player_was_saved must be an datetime")
				file.write_uint64(int((self.last_time_player_was_saved - datetime(1, 1, 1)).total_seconds() * 10000000))

			if version >= 206:
				file.write_int32(self.golfer_score_accumulated)

			if version >= 218:
				file.write_int32(len(self.item_research))
				for key, value in self.item_research.items():
					file.write_string(terraria_pc_apis_ids.item_id_to_game_name(key))
					file.write_int32(value)

			if version >= 214:
				if not isinstance(self.temporary_mouse_item, Item):
					raise TypeError("temporary_mouse_item must be an Item")
				if not isinstance(self.temporary_research_item, Item):
					raise TypeError("temporary_research_item must be an Item")
				if not isinstance(self.temporary_guide_item, Item):
					raise TypeError("temporary_guide_item must be an Item")
				if not isinstance(self.temporary_goblin_item, Item):
					raise TypeError("temporary_goblin_item must be an Item")

				file.write_byte(bool(self.temporary_mouse_item.id) + (bool(self.temporary_research_item.id) << 1) +
								(bool(self.temporary_guide_item.id) << 2) + (bool(self.temporary_goblin_item.id) << 3))

				if self.temporary_mouse_item.id != 0:
					write_item(self.temporary_mouse_item)

				if self.temporary_research_item.id != 0:
					write_item(self.temporary_research_item)

				if self.temporary_guide_item.id != 0:
					write_item(self.temporary_guide_item)

				if self.temporary_goblin_item.id != 0:
					write_item(self.temporary_goblin_item)

			if version >= 220:
				file.write_bool(True)
				file.write_int16(5)
				file.write_bool(self.is_godmode_enabled)

				file.write_bool(True)
				file.write_int16(11)
				file.write_bool(self.is_far_placement_enabled)

				file.write_bool(True)
				file.write_int16(14)
				file.write_single(self.spawn_rate)

				file.write_bool(False)

	MAX_SUPPORTED_VERSION = 244
	MIN_SUPPORTED_VERSION = 0

	version = 244
	is_favorite = False
	name = ""
	difficulty = 0
	playtime = timedelta()
	hair = 0
	hair_dye = 0
	is_accessories_hidden = Bitarray.bitarray()
	is_pet_hidden = False
	is_light_pet_hidden = False
	is_male = False
	style = 0
	life = 100
	max_life = 100
	mana = 20
	max_mana = 20
	has_demon_heart_accessory_slot = False
	is_biome_torches_unlocked = False
	is_using_biome_torches = False
	has_downed_DD2_event = False
	tax_money = 0
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
	misc_equips = []
	misc_dyes = []
	piggy_bank = []
	safe = []
	defenders_forge = []
	void_vault = []
	is_void_vault_enabled = False
	buffs = []
	spawn_points = []
	is_hotbar_locked = False
	is_time_info_hidden = False
	is_weather_info_hidden = False
	is_fishing_power_info_hidden = False
	is_position_info_hidden = False
	is_depth_info_hidden = False
	is_creature_count_info_hidden = False
	is_kill_count_info_hidden = False
	is_moon_phase_info_hidden = False
	is_movement_speed_info_hidden = False
	is_treasure_finder_info_hidden = False
	is_rare_creatures_finder_info_hidden = False
	is_damage_per_second_info_hidden = False
	angler_quests_finished = 0
	quick_shortcuts = [-1, -1, -1, -1]
	is_ruler_enabled = False
	is_mechanical_ruler_enabled = False
	is_auto_placement_actuators_enabled = False
	is_auto_paint_enabled = False
	red_wires_visibility = 0
	blue_wires_visibility = 0
	green_wires_visibility = 0
	yellow_wires_visibility = 0
	is_showing_showing_wires_and_actuators_forced = False
	actuators_visibility = 0
	is_tile_replacement_enabled = False
	is_biome_torches_enabled = False
	bartender_quest_log = 0
	is_dead = False
	time_to_respawn = timedelta()
	last_time_player_was_saved = datetime(1, 1, 1)
	golfer_score_accumulated = 0
	item_research = {}  # key is item id, value is how many items are given to research
	temporary_mouse_item = Item()
	temporary_research_item = Item()
	temporary_guide_item = Item()
	temporary_goblin_item = Item()
	is_godmode_enabled = False
	is_far_placement_enabled = True
	spawn_rate = 0.5

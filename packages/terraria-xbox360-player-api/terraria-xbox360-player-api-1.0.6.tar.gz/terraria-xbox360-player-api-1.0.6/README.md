# terraria xbox360 player API

API for reading and modifying xbox 360 terraria player files.

## Examples

Change player max life to 300
```python
>>> import terraria_xbox360_player_api
>>> player = terraria_xbox360_player_api.TerrariaXbox360Player("PLAYER1.PLR")
>>> player.max_life = 300
>>> player.write_to_file("PLAYER1.PLR")
```

Set 999 dirt items to first inventory slot
```python
>>> import terraria_xbox360_player_api
>>> player = terraria_xbox360_player_api.TerrariaXbox360Player("PLAYER1.PLR")
>>> player.inventory[0][0] = terraria_xbox360_player_api.Item(2, 999, 0)
>>> player.write_to_file("PLAYER1.PLR")
```

Read player name
```python
>>> import terraria_xbox360_player_api
>>> terraria_xbox360_player_api.TerrariaXbox360Player("PLAYER1.PLR").name
'test_plr'
```

## Dependencies

* [bitarray](https://github.com/ilanschnell/bitarray)
* [binary-rw](https://gitlab.com/fkwilczek/binary-rw)
* [terraria-apis-objects](https://gitlab.com/fkwilczek/terraria-apis-objects)

## Installation
```
pip install terraria-xbox360-player-api
```

## License

[GPL v3](LICENSE) © Filip K.

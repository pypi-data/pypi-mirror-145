# Pydisco

Simplified and powerful bots are here.

[Discord Server](https://discord.gg/5zR7dTcPhv)

### What is done

- Basic HTTP and WebSocket client
- Caching
- `Channel` implementation (needs to be rewritten)
- `Emoji` implementation
- `Guild` implementation
- `Intents` implementation
- `Role` implementation
- `User` implementation
- Tests for mostly implemented classes

### What needs to be done

- Continue implementing unimplemented things in already implemented classes
- Implement slash commands, messages, messages components
- Voice implementation
- Update all current implementation to latest Discord's API
- Implement stages
- Audit/Application implementation (? - do we really need this?)
- Implement all events
- Check if everything works good and fast :)

### Installation
In order to use PyDisco, you need Python >=3.8. To install package, use pip:
```bash
# Unix
python -m pip install pydiscoo

# Windows
pip install pydiscoo
```

### Examples

```python
from pydisco import Client

client = Client('your-token-here')


# You can specify gateway version (by default 9) and intents (by default all available).

@client.on('ready')
async def on_ready():
    print('Client is ready!')


client.run()
```

(you can find more [here](https://github.com/Pelfox/pydisco/tree/main/examples))

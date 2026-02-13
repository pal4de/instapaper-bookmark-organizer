# Instapaper Bookmark Organizer

A CLI tool to efficiently organize Instapaper unread bookmarks. With domain-based rule learning, it automatically sorts bookmarks into appropriate folders.

## Features

- 🔐 **Secure Authentication**: One-time xAuth authentication, tokens stored securely thereafter
- 🤖 **Auto-sorting**: Automatically move bookmarks to folders based on domain rules
- 📚 **Rule Learning**: Automatically remembers manually sorted domains
- ⌨️ **Simple UI**: Quick keyboard-only operation

## Installation

### Requirements

- Python 3.7+
- Instapaper account
- Instapaper API keys (Consumer Key/Secret)

### Install uv

First, install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or using Homebrew:

```bash
brew install uv
```

### Install Dependencies

```bash
uv sync
```

## Setup

### 1. Get Instapaper API Keys

1. Visit [Instapaper API](https://www.instapaper.com/api)
2. Obtain Consumer Key and Consumer Secret

### 2. Set Environment Variables

**Required (always):**
```bash
export INSTAPAPER_CONSUMER_KEY="your_consumer_key"
export INSTAPAPER_CONSUMER_SECRET="your_consumer_secret"
```

**First run only:**
```bash
export INSTAPAPER_USERNAME="your_email@example.com"
export INSTAPAPER_PASSWORD="your_password"
```

> 💡 After the first run, authentication tokens are saved to `~/.config/instapaper-cli/credentials.json`, so username and password are no longer needed.

### 3. Create Folders in Instapaper

Before using the tool, create folders for organization on the Instapaper website or app.

## Usage

### Basic Usage

```bash
uv run python main.py
```

Or as an installed script:

```bash
uv run instapaper-organize
```

### Operations

When you launch the tool, unread bookmarks are displayed one at a time:

```
Folders (1..9):
  1: Tech (id=123456)
  2: News (id=234567)
  3: Blog (id=345678)

Controls: [1-9]=move  [a]=auto(move by rule)  [s]=save rule for domain  [n]=skip  [q]=quit

[12345] Example Article Title
  example.com
  suggestion: Tech
>
```

#### Commands

| Key | Action |
|------|------|
| `1-9` | Move to corresponding folder |
| `a` | Auto-move based on rules (if rule exists) |
| `s` | Save folder rule for current domain |
| `n` | Skip (next bookmark) |
| `q` | Quit |

### How Rules Work

- **Auto-learning**: When you move to a folder with number keys (1-9), the domain is automatically remembered
- **Explicit saving**: Use `s` key to save specific domain-folder combinations
- **Subdomain support**: Rules like `.example.com` can match all subdomains
- **Rule storage**: `~/.config/instapaper-cli/rules.json`

## File Structure

```
~/.config/instapaper-cli/
├── credentials.json  # Authentication tokens (permission: 600)
└── rules.json        # Domain sorting rules
```

## Troubleshooting

### Authentication Errors

- Verify Consumer Key/Secret are correct
- For first run, ensure `INSTAPAPER_USERNAME` and `INSTAPAPER_PASSWORD` are set
- Try deleting `~/.config/instapaper-cli/credentials.json` and re-authenticating

### No Folders Displayed

- Create at least one folder on the Instapaper website or app

### API Rate Limiting

- The tool has built-in auto-retry with exponential backoff
- If errors persist, wait a while before retrying

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing

Pull requests and issue reports are welcome!

## API Documentation

- [Instapaper API Documentation](https://www.instapaper.com/api)

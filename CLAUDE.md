# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a macOS development environment setup repository using Homebrew Bundle. It contains a Brewfile that defines:
- Homebrew taps (third-party repositories)
- Command-line tools and libraries via `brew` formulas
- GUI applications via `cask` installations
- VS Code extensions via `vscode` entries

## Common Commands

### Basic Operations
```sh
# Install all packages and applications
brew bundle

# Check what would be installed/removed
brew bundle check --verbose

# Install new packages after updating Brewfile
brew bundle install

# Install without upgrading existing packages
HOMEBREW_BUNDLE_NO_UPGRADE=1 brew bundle
```

### Package Management
```sh
# Add a new formula to Brewfile and install
brew bundle add <formula>

# Add a new cask to Brewfile and install
brew bundle add --cask <cask>

# Add a VS Code extension to Brewfile and install
brew bundle add --vscode <extension>

# Remove package from Brewfile and uninstall
brew bundle remove <formula>
```

### Maintenance and Updates
```sh
# Update the Brewfile with currently installed packages
brew bundle dump --force

# Remove packages not listed in Brewfile
brew bundle cleanup --force

# See what would change without making changes
brew bundle install --dry-run
```

### Environment Management
```sh
# Run commands with Brewfile environment
brew bundle exec <command>

# Export environment variables from Brewfile
brew bundle env

# Use a specific Brewfile
brew bundle --file=Brewfile.work
```

## Architecture

### File Structure
- `Brewfile` - Main configuration file defining all packages and applications
- `Brewfile.lock.json` - Lock file tracking exact versions and commit hashes of taps
- `README.md` - Basic usage instructions

### Package Categories in Brewfile
- **Taps**: Third-party Homebrew repositories (lines 1-10)
- **Formulas**: Command-line tools and libraries (lines 11-113) 
- **Casks**: GUI applications (lines 114-164)
- **VS Code Extensions**: Development environment extensions (lines 165-197)

### Development Environment Included
- Languages: Node.js, Python (3.9, 3.10, 3.11, 3.12), Go, Rust, Ruby, PHP
- Version managers: nvm, pyenv, rbenv, tfenv
- Development tools: Docker, Git, GitHub CLI, various databases
- Text editors: VS Code, Cursor
- Communication: Discord, Slack alternatives (Ferdium)

## Maintenance Notes

- The lock file (`Brewfile.lock.json`) ensures reproducible installations across machines
- Services with `restart_service: :changed` (privoxy, tor) will auto-restart when updated
- Custom taps include specialized tools like QMK for keyboard firmware and ChatGPT desktop app

## Environment Configuration

### Environment Variables
Important variables for customizing brew bundle behavior:
- `HOMEBREW_BUNDLE_NO_UPGRADE=1` - Skip upgrading existing packages during install
- `HOMEBREW_BUNDLE_BREW_SKIP="package1 package2"` - Skip specific formulas
- `HOMEBREW_BUNDLE_CASK_SKIP="app1 app2"` - Skip specific casks
- `HOMEBREW_BUNDLE_FILE` - Set custom Brewfile location (default: ./Brewfile)

### Multiple Environment Support
For different development scenarios:
```sh
# Development environment
brew bundle --file=Brewfile.dev

# Minimal environment for CI/containers
brew bundle --file=Brewfile.minimal

# Work-specific tools
brew bundle --file=Brewfile.work
```

## Troubleshooting

### Common Issues and Solutions
- **Lock file conflicts**: Remove `Brewfile.lock.json` and run `brew bundle` again
- **Service startup failures**: Check status with `brew services list`
- **Package conflicts**: Use `brew bundle check` to verify state before changes
- **Permission issues**: Ensure Homebrew directories have correct ownership

### Verification Commands
```sh
# Check if system matches Brewfile exactly
brew bundle check

# Preview changes without applying
brew bundle install --dry-run

# List services and their status
brew services list
```

## Making Changes

### Best Practices
1. **Before making changes**: Run `brew bundle check` to verify current state
2. **Adding packages**: Use `brew bundle add <package>` for automatic Brewfile updates
3. **Removing packages**: Use `brew bundle remove <package>` to clean up both Brewfile and system
4. **Testing changes**: Use `--dry-run` flag to preview effects
5. **Environment management**: Consider using environment variables for different scenarios

### Workflow
1. Add new entries using `brew bundle add` commands when possible
2. Run `brew bundle check --verbose` to see what will change
3. Apply changes with `brew bundle install`
4. Update lock file with `brew bundle dump --force` if adding many packages manually
5. Clean up unused packages with `brew bundle cleanup --force`
# Brewfile

A declarative configuration for macOS development environment using Homebrew Bundle.

## Requirements

* [Homebrew](https://brew.sh) (Bundle is now included in core Homebrew)

## Quick Start

### Install all packages and applications
```sh
brew bundle
```

### Check what would be installed
```sh
brew bundle check --verbose
```

## Package Management

### Adding packages
```sh
# Add a formula
brew bundle add <formula>

# Add a cask
brew bundle add --cask <cask>

# Add a VS Code extension  
brew bundle add --vscode <extension>
```

### Removing packages
```sh
# Remove from Brewfile and uninstall
brew bundle remove <formula>
```

### Update and maintenance
```sh
# Update Brewfile with currently installed packages
brew bundle dump --force

# Remove packages not listed in Brewfile
brew bundle cleanup --force

# Install new packages after updating Brewfile
brew bundle install

# Install without upgrading existing packages
HOMEBREW_BUNDLE_NO_UPGRADE=1 brew bundle
```

## Advanced Usage

### Environment Management
```sh
# Run commands with Brewfile environment
brew bundle exec <command>

# Export environment variables from Brewfile
brew bundle env
```

### Multiple Environments
You can create environment-specific Brewfiles:
```sh
# Use a specific Brewfile
brew bundle --file=Brewfile.work

# Set default Brewfile location
export HOMEBREW_BUNDLE_FILE=~/dotfiles/Brewfile
```

### Environment Variables
- `HOMEBREW_BUNDLE_NO_UPGRADE=1` - Skip upgrading existing packages
- `HOMEBREW_BUNDLE_BREW_SKIP="package1 package2"` - Skip specific formulas
- `HOMEBREW_BUNDLE_CASK_SKIP="app1 app2"` - Skip specific casks
- `HOMEBREW_BUNDLE_FILE` - Set custom Brewfile location

## Troubleshooting

### Common Issues
- **Lock conflicts**: Remove `Brewfile.lock.json` and run `brew bundle` again
- **Service startup failures**: Check with `brew services list`
- **Permission issues**: Ensure Homebrew directories have correct permissions

### Verification
```sh
# Check if environment matches Brewfile
brew bundle check

# See what would change
brew bundle install --dry-run
```

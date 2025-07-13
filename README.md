# Brewfile

![Brewfile CI](https://github.com/yshrkume/Brewfile/workflows/Brewfile%20CI/badge.svg)

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

## Continuous Integration

This repository includes optimized GitHub Actions CI that validates:
- **Package availability**: Tests all brew formulas and casks exist in repositories
- **CI environment compatibility**: Automatically skips Mac App Store apps (unsupported in CI)
- **Real installation testing**: Installs critical packages to verify functionality
- **Weekly maintenance**: Scheduled runs detect deprecated packages early

**CI Features:**
- Runs on push/PR to `main` + weekly on Sundays
- Environment-aware (skips MAS apps in CI with `$CI` variable)
- Tests actual package installation for critical tools
- Performance optimized with `HOMEBREW_NO_AUTO_UPDATE`

## Troubleshooting

### Common Issues
- **Lock conflicts**: Remove `Brewfile.lock.json` and run `brew bundle` again
- **Service startup failures**: Check with `brew services list`
- **Permission issues**: Ensure Homebrew directories have correct permissions
- **CI failures**: Check the Actions tab for detailed error logs

### Verification
```sh
# Check if environment matches Brewfile
brew bundle check

# See what would change
brew bundle install --dry-run

# Run similar checks as CI locally
brew bundle check --verbose
brew info git jq gh  # Test critical packages
brew info --cask visual-studio-code  # Test cask availability
```

## Continuous Integration

This repository includes automated validation:

- **Syntax validation**: Checks Brewfile for errors and duplicates
- **Security check**: Warns about insecure HTTP taps  
- **Monthly updates**: Automated check for package updates

The workflow runs on pushes to main and can be triggered manually via GitHub Actions.

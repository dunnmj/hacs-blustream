# Blustream ACM-210 Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Home Assistant custom integration for the Blustream ACM-210 AVoIP module. This branch is specifically designed for ACM-210 devices (not matrixes) and has been tested on an ACM-210.

**Note:** Camera entity support requires both AVoIP equipment and an ACM device. If you do not have AVoIP endpoints, the camera platform will not function.

## Supported Devices

- Tested on: **Blustream ACM-210**
- Camera support: Requires AVoIP endpoints and an ACM device

This branch is not intended for matrix switchers. Use the original [designer-living/hacs-blustream](https://github.com/designer-living/hacs-blustream) for matrix support.

## Features

- **Media Player entities** - Control each ACM-210 output zone as a media player
- **Camera entities** - (Requires AVoIP) View source inputs as camera entities
- **Local Push** - Real-time updates from the ACM-210
- **Config Flow** - Easy setup through the Home Assistant UI

## Installation

### HACS (Recommended)

1. Make sure [HACS](https://hacs.xyz/) is installed in your Home Assistant instance
2. Add this repository as a custom repository in HACS:
   - Click on HACS in the sidebar
   - Click on "Integrations"
   - Click the three dots in the top right corner
   - Select "Custom repositories"
   - Add the repository URL: `https://github.com/designer-living/hacs-blustream`
   - Select category: "Integration"
   - Click "Add"
3. Click "Install" on the Blustream integration
4. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/blustream` folder from this repository
2. Copy the entire `blustream` folder to your Home Assistant's `custom_components` directory
   - If the `custom_components` directory doesn't exist, create it in your Home Assistant configuration directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **Blustream**
4. Enter the following information:
   - **Name**: A friendly name for your ACM-210 (e.g., "ACM-210")
   - **Host**: IP address of your ACM-210
   - **Port**: TCP port (default: 23)
5. Click **Submit**

## Usage

### Media Players

Each output zone on your ACM-210 will appear as a media player entity. You can:

- Turn zones on/off
- Select source inputs
- View current source selection
- Control through the Home Assistant UI, automations, or scripts

### Cameras

If you have AVoIP endpoints and an ACM device, source inputs will appear as camera entities, allowing you to:

- Preview sources in the Home Assistant UI
- Use in picture cards
- Reference in automations

## Troubleshooting

### Connection Issues

- Verify the ACM-210 IP address is correct and reachable from your Home Assistant instance
- Check that port 23 (or your configured port) is not blocked by a firewall
- Ensure the ACM-210 is powered on and connected to your network

### Entities Not Appearing

- Check the Home Assistant logs for error messages
- Try restarting Home Assistant
- Verify your ACM-210 is compatible

### Debug Logging

To enable debug logging, add this to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.blustream: debug
    pyblustream: debug
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This integration is released under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## Credits

- Original integration by [designer-living](https://github.com/designer-living) and [@foxy82](https://github.com/foxy82)
- Maintained fork by [@dunnmj](https://github.com/dunnmj)
- Uses the [pyblustream](https://pypi.org/project/pyblustream/) library

## Support

If you encounter any issues, please [open an issue](https://github.com/dunnmj/hacs-blustream/issues) on GitHub.

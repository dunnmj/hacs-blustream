
# Blustream ACM-210 Integration

Control your Blustream ACM-210 audio control module directly from Home Assistant.

**This branch is specifically for ACM-210 devices (not matrixes) and has been tested on an ACM-210.**

## What This Integration Provides

- **Media Player Entities** - Each ACM-210 output zone becomes a controllable media player
- **Camera Entities** - (Requires AVoIP endpoints and an ACM device) Source inputs appear as camera entities for previewing
- **Real-time Updates** - Local push integration provides instant status updates
- **Easy Setup** - Simple configuration flow through the UI

## Quick Start

1. Install this integration through HACS
2. Restart Home Assistant
3. Go to Settings → Devices & Services → Add Integration
4. Search for "Blustream" and follow the setup wizard
5. Enter your ACM-210's IP address and port (default: 23)

## Requirements

- A Blustream ACM-210 connected to your network
- (Optional) AVoIP endpoints for camera support
- The ACM-210 must be accessible from your Home Assistant instance
- TCP port 23 (or configured port) must be accessible

## Need Help?

Visit the [GitHub repository](https://github.com/dunnmj/hacs-blustream) for detailed documentation and support.

---
**This is a maintained fork by [@dunnmj](https://github.com/dunnmj) of the original [designer-living/hacs-blustream](https://github.com/designer-living/hacs-blustream) integration.**

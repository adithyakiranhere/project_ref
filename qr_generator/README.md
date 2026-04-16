# 🎨 QR Art Generator

Generate **beautiful, styled QR codes** for URLs, Wi-Fi networks, and contact cards — with custom colors, rounded modules, gradients, and embedded logos. Because the default black-and-white QR codes are boring.

## What you can make

| URL QR with logo | Wi-Fi QR with gradient | vCard contact QR |
|:---:|:---:|:---:|
| ![](docs/url.png) | ![](docs/wifi.png) | ![](docs/card.png) |

## Features

- 🎨 **Three styles**: rounded, circle, or classic square modules
- 🌈 **Custom colors** with hex codes, plus optional radial gradient
- 🖼️ **Embed a logo** right in the center (with automatic safe background)
- 📡 **Wi-Fi QR codes** — guests scan with their camera and auto-connect, no typing passwords
- 👤 **vCard QR codes** — scan to save your name, phone, and email as a contact
- 🛡️ High error correction keeps codes scannable even with logos and styling
- 💻 Simple CLI — three subcommands, shared styling options

## Install

```bash
git clone https://github.com/YOUR_USERNAME/qr-art-generator.git
cd qr-art-generator
pip install -r requirements.txt
```

## Usage

### URL QR

```bash
python qr_art.py url "https://github.com/YOUR_USERNAME" -o mylink.png
```

### Styled URL QR with a logo and gradient

```bash
python qr_art.py url "https://github.com/YOUR_USERNAME" \
  --style rounded \
  --fg "#6B46C1" --bg "#FFFFFF" \
  --gradient \
  --logo logo.png \
  -o fancy.png
```

### Wi-Fi QR — the killer feature

Put this on your fridge. Guests scan it. Their phone auto-connects. No more reading a 16-character password aloud.

```bash
python qr_art.py wifi \
  --ssid "MyHomeWiFi" \
  --password "SuperSecret123" \
  --style circle \
  --fg "#1E40AF" \
  -o wifi.png
```

### Contact card QR

```bash
python qr_art.py card \
  --name "Jane Doe" \
  --phone "+91 98765 43210" \
  --email "jane@example.com" \
  --org "Acme Corp" \
  --style rounded \
  --fg "#DC2626" \
  -o card.png
```

## Options

| Flag | Description | Default |
|---|---|---|
| `-o, --output` | Output file path | `qr.png` |
| `--style` | `square`, `rounded`, or `circle` | `rounded` |
| `--fg` | Foreground hex color | `#000000` |
| `--bg` | Background hex color | `#FFFFFF` |
| `--gradient` | Apply radial gradient fill | off |
| `--logo` | Path to center logo image | none |

## Tips for best scannability

- Keep **high contrast** between foreground and background
- Don't make the logo too big (the script caps it at 25% of QR width)
- Stick to rounded or square styles for printed codes — circle style is trendier but slightly harder for older scanners
- Test on a real phone before printing — always

## Ideas for contributions

- SVG output for infinite scaling
- Batch mode — generate QR codes from a CSV of URLs
- Animated GIF QR codes (yes, this is a thing)
- A simple web UI with Flask or Streamlit

## License

MIT

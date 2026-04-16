import argparse
import sys
from pathlib import Path

import qrcode
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask, SolidFillColorMask
from qrcode.image.styles.moduledrawers.pil import (
    CircleModuleDrawer,
    RoundedModuleDrawer,
    SquareModuleDrawer,
)

STYLES = {
    "square": SquareModuleDrawer(),
    "rounded": RoundedModuleDrawer(),
    "circle": CircleModuleDrawer(),
}


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert a #RRGGBB string to (r, g, b)."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color}")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def build_wifi_payload(ssid: str, password: str, security: str = "WPA") -> str:
    """Build the Wi-Fi QR payload format that phone cameras understand."""
    return f"WIFI:T:{security};S:{ssid};P:{password};;"


def build_vcard_payload(name: str, phone: str, email: str, org: str = "") -> str:
    """Build a minimal vCard 3.0 payload that saves as a contact on scan."""
    return (
        "BEGIN:VCARD\n"
        "VERSION:3.0\n"
        f"FN:{name}\n"
        f"TEL:{phone}\n"
        f"EMAIL:{email}\n"
        f"ORG:{org}\n"
        "END:VCARD"
    )


def generate_qr(
    data: str,
    output: Path,
    style: str,
    fg_color: str,
    bg_color: str,
    gradient: bool,
    logo_path: Path | None,
) -> None:
    """Generate a styled QR code and save it to disk."""
    # High error correction so the logo doesn't break the code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)

    drawer = STYLES.get(style, RoundedModuleDrawer())
    fg = hex_to_rgb(fg_color)
    bg = hex_to_rgb(bg_color)

    if gradient:
        color_mask = RadialGradiantColorMask(
            back_color=bg,
            center_color=fg,
            edge_color=(fg[0] // 2, fg[1] // 2, fg[2] // 2),
        )
    else:
        color_mask = SolidFillColorMask(back_color=bg, front_color=fg)

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=drawer,
        color_mask=color_mask,
    ).convert("RGBA")

    # Embed a centered logo if provided
    if logo_path:
        if not logo_path.exists():
            print(f"⚠️  Logo not found: {logo_path} — skipping.")
        else:
            logo = Image.open(logo_path).convert("RGBA")
            qr_w, qr_h = img.size
            logo_size = qr_w // 4  # Logo takes ~25% of the QR width
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

            # White rounded background behind the logo for scannability
            pad = logo_size // 10
            bg_box = Image.new("RGBA", (logo_size + pad * 2, logo_size + pad * 2), bg + (255,))
            bg_pos = ((qr_w - bg_box.width) // 2, (qr_h - bg_box.height) // 2)
            img.paste(bg_box, bg_pos, bg_box)

            logo_pos = ((qr_w - logo_size) // 2, (qr_h - logo_size) // 2)
            img.paste(logo, logo_pos, logo)

    img.save(output)
    print(f"✅ Saved: {output}")
    print(f"   📐 Size: {img.size[0]}×{img.size[1]}px")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate beautiful, styled QR codes for URLs, Wi-Fi, and contacts.",
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # URL / text mode
    url_p = subparsers.add_parser("url", help="QR code for a URL or any text")
    url_p.add_argument("data", help="URL or text to encode")

    # Wi-Fi mode
    wifi_p = subparsers.add_parser("wifi", help="QR code for Wi-Fi credentials")
    wifi_p.add_argument("--ssid", required=True, help="Wi-Fi network name")
    wifi_p.add_argument("--password", required=True, help="Wi-Fi password")
    wifi_p.add_argument("--security", default="WPA", choices=["WPA", "WEP", "nopass"])

    # vCard mode
    card_p = subparsers.add_parser("card", help="QR code for contact info (vCard)")
    card_p.add_argument("--name", required=True)
    card_p.add_argument("--phone", required=True)
    card_p.add_argument("--email", required=True)
    card_p.add_argument("--org", default="")

    # Shared styling options for every subcommand
    for sub in (url_p, wifi_p, card_p):
        sub.add_argument("-o", "--output", type=Path, default=Path("qr.png"))
        sub.add_argument("--style", choices=list(STYLES), default="rounded")
        sub.add_argument("--fg", default="#000000", help="Foreground color hex")
        sub.add_argument("--bg", default="#FFFFFF", help="Background color hex")
        sub.add_argument("--gradient", action="store_true", help="Radial gradient fill")
        sub.add_argument("--logo", type=Path, help="Path to a logo image to embed")

    args = parser.parse_args()

    if args.mode == "url":
        payload = args.data
    elif args.mode == "wifi":
        payload = build_wifi_payload(args.ssid, args.password, args.security)
    else:  # card
        payload = build_vcard_payload(args.name, args.phone, args.email, args.org)

    try:
        generate_qr(
            data=payload,
            output=args.output,
            style=args.style,
            fg_color=args.fg,
            bg_color=args.bg,
            gradient=args.gradient,
            logo_path=args.logo,
        )
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

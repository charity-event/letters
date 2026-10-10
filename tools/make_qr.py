#!/usr/bin/env python3
"""生成指向落地页的二维码（纠错等级 H，适合放进公众号推送）。

用法:
    python3 tools/make_qr.py https://你的项目.edgeone.app -o output/qr.png
"""
import argparse
import sys
from pathlib import Path

try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H
except ImportError:
    sys.exit("缺少依赖，请先执行: pip install 'qrcode[pil]'")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("url", help="落地页完整地址，必须以 https:// 开头")
    parser.add_argument("-o", "--output", default="output/qr.png", help="输出 PNG 路径（默认 output/qr.png）")
    parser.add_argument("--box", type=int, default=24, help="每个格子的像素数，越大图越清晰（默认 24）")
    parser.add_argument("--border", type=int, default=4, help="四周留白格数，微信识别建议不小于 4（默认 4）")
    args = parser.parse_args()

    if not args.url.startswith("https://"):
        sys.exit("地址必须以 https:// 开头，否则微信内打开会被拦截或提示不安全")

    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=args.box, border=args.border)
    qr.add_data(args.url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)

    side = (qr.modules_count + 2 * args.border) * args.box
    print(f"已生成 {out}  尺寸 {side}x{side} px  版本 {qr.version}  纠错 H")
    print("发到公众号时图片宽度建议不小于 600 px，不要再二次压缩或加滤镜。")


if __name__ == "__main__":
    main()

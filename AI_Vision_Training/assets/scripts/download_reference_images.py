#!/usr/bin/env python3
"""Download licensed reference images once; reuse local files for offline lessons.
Usage: python download_reference_images.py --course-root PATH_TO_AI_Vision_Training
Requires Pillow, already present in the course base environment. Does not generate images.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import time
from urllib.request import Request, urlopen
from xml.etree import ElementTree
from PIL import Image

ASSETS = [
  {
    "name": "brick.png",
    "url": "https://gitlab.com/scikit-image/data/-/raw/5c090b56df3988d988ff97928e2ef2d2cbe38e1b/brick.png",
    "bytes": 106634,
    "sha256": "7966caf324f6ba843118d98f7a07746d22f6a343430add0233eca5f6eaaa8fcf",
    "author": "CC0Textures; processed by scikit-image",
    "license": "CC0 1.0",
    "source": "https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.brick",
    "license_url": "https://creativecommons.org/publicdomain/zero/1.0/"
  },
  {
    "name": "camera.png",
    "url": "https://gitlab.com/scikit-image/data/-/raw/5c090b56df3988d988ff97928e2ef2d2cbe38e1b/camera.png",
    "bytes": 139512,
    "sha256": "b0793d2adda0fa6ae899c03989482bff9a42d3d5690fc7e3648f2795d730c23a",
    "author": "Lav Varshney",
    "license": "CC0 1.0",
    "source": "https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.camera",
    "license_url": "https://creativecommons.org/publicdomain/zero/1.0/"
  },
  {
    "name": "chelsea.png",
    "url": "https://gitlab.com/scikit-image/data/-/raw/5c090b56df3988d988ff97928e2ef2d2cbe38e1b/chelsea.png",
    "bytes": 240512,
    "sha256": "596aa1e7cb875eb79f437e310381d26b338a81c2da23439704a73c4651e8c4bb",
    "author": "Stefan van der Walt",
    "license": "CC0 1.0",
    "source": "https://scikit-image.org/docs/stable/api/skimage.data.html#skimage.data.chelsea",
    "license_url": "https://creativecommons.org/publicdomain/zero/1.0/"
  },
  {
    "name": "VisA_samples.png",
    "url": "https://raw.githubusercontent.com/amazon-science/spot-diff/2a692ab575001cbde74d402d897a7286086c6199/figures/VisA_samples.png",
    "bytes": 2390610,
    "sha256": "d707e2e95d3b98336c99e2b8aa6049f65f1f7044542f2839a63df74b9ba3a629",
    "author": "Yang Zou, Jongheon Jeong, Latha Pemula, Dongqing Zhang, Onkar Dabeer / Amazon Science",
    "license": "CC BY 4.0 (VisA dataset)",
    "source": "https://github.com/amazon-science/spot-diff/tree/2a692ab575001cbde74d402d897a7286086c6199",
    "license_url": "https://creativecommons.org/licenses/by/4.0/"
  }
]
MAX_BYTES = 8 * 1024 * 1024


def check_bytes(data, item):
    if len(data) > MAX_BYTES:
        raise ValueError('download exceeds size limit')
    if hashlib.sha256(data).hexdigest() != item['sha256']:
        raise ValueError('SHA-256 does not match the reviewed file')
    if item['name'].endswith('.svg'):
        root = ElementTree.fromstring(data)
        if root.tag.rsplit('}', 1)[-1] != 'svg':
            raise ValueError('not an SVG document')
    else:
        with Image.open(io.BytesIO(data)) as image:
            image.verify()


def write_atomic(path, data):
    fd, temp_name = tempfile.mkstemp(prefix=path.name + '.', suffix='.part', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
        os.replace(temp_name, path)
    finally:
        Path(temp_name).unlink(missing_ok=True)


def download(item, directory, offline):
    path = directory / item['name']
    if path.is_file():
        try:
            check_bytes(path.read_bytes(), item)
            print('確認済み / cached:', item['name'])
            return
        except (OSError, ValueError, ElementTree.ParseError):
            if offline:
                raise ValueError('cached file is invalid: ' + item['name'])
    if offline:
        raise FileNotFoundError('offline file missing: ' + item['name'])
    last_error = None
    for attempt in range(3):
        try:
            request = Request(item['url'], method='GET', headers={
                'User-Agent': 'Kaseihin-Training-Reference-Downloader/1.0',
                'Accept': 'image/*,application/octet-stream;q=0.9',
            })
            with urlopen(request, timeout=20) as response:
                if response.status != 200:
                    raise ValueError('HTTP status ' + str(response.status))
                data = response.read(MAX_BYTES + 1)
            check_bytes(data, item)
            write_atomic(path, data)
            print('保存 / downloaded:', item['name'])
            return
        except Exception as error:
            last_error = error
            if attempt < 2:
                time.sleep(attempt + 1)
    raise RuntimeError(item['name'] + ': ' + str(last_error))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--course-root', type=Path, required=True)
    parser.add_argument('--offline', action='store_true', help='verify cache without any network request')
    args = parser.parse_args()
    root = args.course_root.expanduser().resolve()
    if not root.is_dir() or not (root / 'assets').is_dir():
        parser.error('--course-root must be an existing course folder containing assets/')
    target = root / 'assets' / 'external_samples' / 'open_reference'
    target.mkdir(parents=True, exist_ok=True)
    failures = []
    for item in ASSETS:
        try:
            download(item, target, args.offline)
        except Exception as error:
            failures.append(str(error))
            print('取得失敗 / failed:', error, file=sys.stderr)
    if failures:
        print('必要な画像がそろっていません。接続を確認して再実行してください。\n'
              'Reference images are incomplete. Check connectivity and rerun; valid cached files are retained.',
              file=sys.stderr)
        return 1
    manifest = {'schema_version': 1, 'reviewed_on': '2026-11-13',
                'purpose': 'teaching reference only; not training or test data', 'assets': ASSETS}
    write_atomic(target / 'manifest.json', (json.dumps(manifest, indent=2, ensure_ascii=False) + '\n').encode('utf-8'))
    lines = ['# 外部参考画像 / External reference images', '',
             'Downloaded originals, unchanged. These are teaching references, not factory PVC photographs or model outputs.', '',
             '| File | Creator/source | Licence | Source page | Download | SHA-256 |',
             '|---|---|---|---|---|---|']
    for item in ASSETS:
        lines.append('| {name} | {author} | [{license}]({license_url}) | [source]({source}) | [GET]({url}) | {sha256} |'.format(**item))
    lines += ['', 'VisA credit: Zou et al., SPot-the-Difference Self-Supervised Pre-training for Anomaly Detection and Segmentation (2022).',
              'VisA overview is reproduced unchanged; the source dataset is CC BY 4.0. No training dataset is downloaded.',
              'If an image is later cropped or annotated, retain the original and mark the derivative as modified.', '']
    write_atomic(target / 'ATTRIBUTION.md', '\n'.join(lines).encode('utf-8'))
    print('完了 / complete:', target)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

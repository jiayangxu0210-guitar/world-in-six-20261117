// Entry point for the make.fun news-image-20261117 entry.
//
// The image is drawn ahead of time by draw.py and shipped in this
// repository as entry.png. This program only places that file where the
// grader expects it. It uses the standard library only, reads nothing
// from the network, and writes the same bytes on every run.
//
// Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const IMAGE_FILE = 'entry.png';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const source = resolve(dirname(fileURLToPath(import.meta.url)), IMAGE_FILE);

if (!existsSync(source)) {
  throw new Error(`Missing ${IMAGE_FILE} next to main.ts`);
}

if (!existsSync(OUTPUT_DIR)) {
  mkdirSync(OUTPUT_DIR, { recursive: true });
}

copyFileSync(source, join(OUTPUT_DIR, IMAGE_FILE));

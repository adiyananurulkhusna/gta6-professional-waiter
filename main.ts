// Entry program for the gta6-meme-x-01 bounty, Node 22, standard library only.
//
// What this entry is: the X post itself is the meme. This program does the
// one job the bounty harness asks of it — it hands POST.json (the post's
// address, filled in after the meme is posted on X) from the repository root
// to the output directory, so the gate can read it and fetch the post.
//
// POST.json starts as a placeholder; the real post address replaces it before
// submitting. Nothing about the post is judged from what this program writes.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });

const source = join(botDir, "POST.json");
const target = join(outDir, "POST.json");

let contents: string;
try {
  contents = readFileSync(source, "utf8");
} catch (err) {
  console.error(`could not read ${source}: ${(err as Error).message}`);
  process.exit(1);
}

// Validate before handing the file to the gate: a placeholder or malformed
// POST.json would otherwise be copied silently and only fail later, when the
// gate tries to fetch the post. Fail fast here with a clear message instead.
let postUrl: unknown;
try {
  postUrl = (JSON.parse(contents) as { url?: unknown }).url;
} catch (err) {
  console.error(`POST.json in ${source} is not valid JSON: ${(err as Error).message}`);
  process.exit(1);
}
if (typeof postUrl !== "string" || !/^https:\/\/(x\.com|twitter\.com)\/\w+\/status\/\d+/.test(postUrl)) {
  console.error(
    `POST.json in ${source} has no usable post URL (expected https://x.com/<handle>/status/<id>); ` +
    `replace the placeholder with the real posted address before submitting.`
  );
  process.exit(1);
}
console.log(`handing off post: ${postUrl}`);

try {
  writeFileSync(target, contents);
} catch (err) {
  console.error(`could not write ${target}: ${(err as Error).message}`);
  process.exit(1);
}

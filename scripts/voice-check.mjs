// Runs the vendored voice/style linter across all docs content.
// Fails (exit 1) if any .md/.mdx page under content/ has a lint ERROR.
// See scripts/voice-lint.py for the rules (vendored from the humanizer skill).

import { readdirSync } from 'node:fs'
import { join } from 'node:path'
import { execFileSync } from 'node:child_process'

const CONTENT_DIR = 'content'
const LINTER = join('scripts', 'voice-lint.py')

const python = process.env.PYTHON ?? 'python3'

function collectDocs(dir) {
  const out = []
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = join(dir, entry.name)
    if (entry.isDirectory()) out.push(...collectDocs(full))
    else if (/\.mdx?$/.test(entry.name)) out.push(full)
  }
  return out
}

const files = collectDocs(CONTENT_DIR).sort()
let failed = 0

for (const file of files) {
  try {
    execFileSync(python, [LINTER, file, '--voice', 'product'], { stdio: 'pipe' })
  } catch (err) {
    failed++
    process.stdout.write(`\n${file}\n`)
    process.stdout.write((err.stdout?.toString() ?? '') + (err.stderr?.toString() ?? ''))
  }
}

if (failed > 0) {
  console.error(`\nVoice lint failed: ${failed} of ${files.length} file(s) have issues.`)
  process.exit(1)
}

console.log(`Voice lint clean: ${files.length} file(s) checked.`)

#!/usr/bin/env node

import { spawn } from "node:child_process";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const serverPath = path.join(__dirname, "server.js");
const child = spawn(process.execPath, [serverPath], {
  cwd: path.resolve(__dirname, "../.."),
  stdio: ["pipe", "pipe", "inherit"]
});

const rl = readline.createInterface({ input: child.stdout, crlfDelay: Infinity });
const pending = new Map();
let nextId = 1;

rl.on("line", (line) => {
  const message = JSON.parse(line);
  if (message.id && pending.has(message.id)) {
    pending.get(message.id)(message);
    pending.delete(message.id);
  }
});

function request(method, params = {}) {
  const id = nextId++;
  const payload = { jsonrpc: "2.0", id, method, params };
  child.stdin.write(`${JSON.stringify(payload)}\n`);
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      pending.delete(id);
      reject(new Error(`Timed out waiting for ${method}`));
    }, 2000);

    pending.set(id, (message) => {
      clearTimeout(timer);
      if (message.error) {
        reject(new Error(message.error.message));
      } else {
        resolve(message.result);
      }
    });
  });
}

function notify(method, params = {}) {
  child.stdin.write(`${JSON.stringify({ jsonrpc: "2.0", method, params })}\n`);
}

try {
  const initialized = await request("initialize", {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: {
      name: "ads-analyst-mock-mcp-smoke-test",
      version: "0.1.0"
    }
  });

  notify("notifications/initialized");

  const listed = await request("tools/list");
  const google = await request("tools/call", {
    name: "get_google_ads_campaign_performance",
    arguments: {
      start_date: "2026-05-01",
      end_date: "2026-05-28"
    }
  });

  const parsed = JSON.parse(google.content[0].text);
  const output = {
    server: initialized.serverInfo,
    tool_count: listed.tools.length,
    tool_names: listed.tools.map((tool) => tool.name),
    google_ads_row_count: parsed.row_count,
    google_ads_source_type: parsed.source.source_type
  };

  console.log(JSON.stringify(output, null, 2));
  child.kill();
} catch (error) {
  child.kill();
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
}

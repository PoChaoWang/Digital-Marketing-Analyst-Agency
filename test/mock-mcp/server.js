#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const fixturesDir = path.join(__dirname, "fixtures");

const PROTOCOL_VERSION = "2024-11-05";

function readFixture(name) {
  const fixturePath = path.join(fixturesDir, name);
  return JSON.parse(fs.readFileSync(fixturePath, "utf8"));
}

function filterRowsByDate(payload, args = {}) {
  const startDate = args.start_date || payload.date_range?.start_date;
  const endDate = args.end_date || payload.date_range?.end_date;
  const rows = (payload.rows || []).filter((row) => {
    if (!row.date) return true;
    return row.date >= startDate && row.date <= endDate;
  });

  return {
    ...payload,
    date_range: {
      start_date: startDate,
      end_date: endDate
    },
    row_count: rows.length,
    source: {
      name: "mock_mcp_development",
      source_type: "mock_mcp",
      environment: "development",
      production_allowed: false,
      fixture_path: path.relative(process.cwd(), fixturesDir)
    },
    rows
  };
}

const tools = [
  {
    name: "get_environment_info",
    description: "Return mock MCP environment metadata, fixture version, date range, timezone, currency, and limitations.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {}
    }
  },
  {
    name: "get_google_ads_campaign_performance",
    description: "Return fake Google Ads campaign performance rows for development testing.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        start_date: { type: "string", description: "Inclusive start date in YYYY-MM-DD format." },
        end_date: { type: "string", description: "Inclusive end date in YYYY-MM-DD format." }
      }
    }
  },
  {
    name: "get_meta_ads_campaign_performance",
    description: "Return fake Meta Ads campaign performance rows for development testing.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        start_date: { type: "string", description: "Inclusive start date in YYYY-MM-DD format." },
        end_date: { type: "string", description: "Inclusive end date in YYYY-MM-DD format." }
      }
    }
  },
  {
    name: "get_ga4_landing_page_performance",
    description: "Return fake GA4 landing page performance rows for development testing.",
    inputSchema: {
      type: "object",
      additionalProperties: false,
      properties: {
        start_date: { type: "string", description: "Inclusive start date in YYYY-MM-DD format." },
        end_date: { type: "string", description: "Inclusive end date in YYYY-MM-DD format." }
      }
    }
  }
];

function toolResult(payload) {
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify(payload, null, 2)
      }
    ]
  };
}

function callTool(name, args) {
  if (name === "get_environment_info") {
    return toolResult(readFixture("environment.json"));
  }

  if (name === "get_google_ads_campaign_performance") {
    return toolResult(filterRowsByDate(readFixture("google_ads_campaign_performance.json"), args));
  }

  if (name === "get_meta_ads_campaign_performance") {
    return toolResult(filterRowsByDate(readFixture("meta_ads_campaign_performance.json"), args));
  }

  if (name === "get_ga4_landing_page_performance") {
    return toolResult(filterRowsByDate(readFixture("ga4_landing_page_performance.json"), args));
  }

  throw new Error(`Unknown tool: ${name}`);
}

function send(message) {
  process.stdout.write(`${JSON.stringify(message)}\n`);
}

function sendResult(id, result) {
  send({ jsonrpc: "2.0", id, result });
}

function sendError(id, code, message) {
  send({ jsonrpc: "2.0", id, error: { code, message } });
}

async function handleRequest(request) {
  if (!request || request.jsonrpc !== "2.0") return;

  const { id, method, params } = request;

  if (method?.startsWith("notifications/")) {
    return;
  }

  try {
    if (method === "initialize") {
      sendResult(id, {
        protocolVersion: params?.protocolVersion || PROTOCOL_VERSION,
        capabilities: {
          tools: {}
        },
        serverInfo: {
          name: "ads-analyst-mock-mcp",
          version: "0.1.0"
        }
      });
      return;
    }

    if (method === "ping") {
      sendResult(id, {});
      return;
    }

    if (method === "tools/list") {
      sendResult(id, { tools });
      return;
    }

    if (method === "tools/call") {
      sendResult(id, callTool(params?.name, params?.arguments || {}));
      return;
    }

    sendError(id, -32601, `Method not found: ${method}`);
  } catch (error) {
    sendError(id, -32000, error instanceof Error ? error.message : String(error));
  }
}

const rl = readline.createInterface({
  input: process.stdin,
  crlfDelay: Infinity
});

rl.on("line", (line) => {
  const trimmed = line.trim();
  if (!trimmed) return;

  try {
    handleRequest(JSON.parse(trimmed));
  } catch (error) {
    sendError(null, -32700, error instanceof Error ? error.message : String(error));
  }
});


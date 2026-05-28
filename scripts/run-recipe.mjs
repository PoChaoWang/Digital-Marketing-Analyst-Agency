#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";
import { spawn } from "node:child_process";

const REPO_ROOT = process.cwd();

const RECIPES = {
  "platform-campaign-performance": {
    file: "recipes/platform-campaign-performance.yml",
    platforms: ["google_ads", "meta_ads"]
  },
  "ga4-landing-page-quality": {
    file: "recipes/ga4-landing-page-quality.yml",
    platforms: ["ga4"]
  },
  "cross-channel-period-compare": {
    file: "recipes/cross-channel-period-compare.yml",
    platforms: ["google_ads", "meta_ads", "ga4"]
  }
};

const MOCK_TOOLS = {
  google_ads: "get_google_ads_campaign_performance",
  meta_ads: "get_meta_ads_campaign_performance",
  ga4: "get_ga4_landing_page_performance"
};

function parseArgs(argv) {
  const args = {
    recipeId: argv[2],
    platform: null,
    startDate: null,
    endDate: null,
    previousStartDate: null,
    previousEndDate: null,
    out: null,
    pretty: true
  };

  for (let index = 3; index < argv.length; index += 1) {
    const arg = argv[index];
    const next = argv[index + 1];
    if (arg === "--platform") {
      args.platform = next;
      index += 1;
    } else if (arg === "--start" || arg === "--start-date") {
      args.startDate = next;
      index += 1;
    } else if (arg === "--end" || arg === "--end-date") {
      args.endDate = next;
      index += 1;
    } else if (arg === "--previous-start") {
      args.previousStartDate = next;
      index += 1;
    } else if (arg === "--previous-end") {
      args.previousEndDate = next;
      index += 1;
    } else if (arg === "--out") {
      args.out = next;
      index += 1;
    } else if (arg === "--compact") {
      args.pretty = false;
    } else if (arg === "--help" || arg === "-h") {
      printHelp();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  return args;
}

function printHelp() {
  console.log(`Usage:
  node scripts/run-recipe.mjs platform-campaign-performance --platform meta_ads [--start YYYY-MM-DD --end YYYY-MM-DD]
  node scripts/run-recipe.mjs ga4-landing-page-quality [--start YYYY-MM-DD --end YYYY-MM-DD]
  node scripts/run-recipe.mjs cross-channel-period-compare --start YYYY-MM-DD --end YYYY-MM-DD --previous-start YYYY-MM-DD --previous-end YYYY-MM-DD

Options:
  --platform           google_ads, meta_ads, or ga4 depending on recipe
  --start             inclusive start date
  --end               inclusive end date
  --previous-start    comparison start date for period compare
  --previous-end      comparison end date for period compare
  --out               write JSON result to file
  --compact           print compact JSON
`);
}

function readText(relativePath) {
  return fs.readFileSync(path.join(REPO_ROOT, relativePath), "utf8");
}

function assertFile(relativePath) {
  const absolutePath = path.join(REPO_ROOT, relativePath);
  if (!fs.existsSync(absolutePath)) {
    throw new Error(`Required file not found: ${relativePath}`);
  }
  return absolutePath;
}

function getConfigSourceBlock(configText, sourceName) {
  const start = configText.indexOf(`  ${sourceName}:`);
  if (start === -1) return "";
  const rest = configText.slice(start);
  const next = rest.slice(1).search(/\n  [a-zA-Z0-9_-]+:\n/);
  return next === -1 ? rest : rest.slice(0, next + 1);
}

function readScalar(block, key) {
  const match = block.match(new RegExp(`\\n\\s+${key}:\\s*(.+)`));
  if (!match) return null;
  return match[1].trim().replace(/^["']|["']$/g, "");
}

function readEnvironment(configText) {
  const match = configText.match(/^environment:\s*(.+)$/m);
  return match ? match[1].trim() : "development";
}

function checkMockMcpAllowed() {
  const configPath = process.env.DATA_SOURCE_CONFIG || "config/data-sources.yml";
  const configText = readText(configPath);
  const environment = process.env.APP_ENV || readEnvironment(configText) || "development";
  const block = getConfigSourceBlock(configText, "mock_mcp_development");
  const enabled = readScalar(block, "enabled") === "true";
  const sourceEnvironment = readScalar(block, "environment");
  const sourceType = readScalar(block, "source_type");
  const productionAllowed = readScalar(block, "production_allowed") === "true";
  const sourcePath = readScalar(block, "path");

  const allowed =
    enabled &&
    sourceType === "mock_mcp" &&
    sourceEnvironment === environment &&
    environment !== "production" &&
    sourcePath === "test/mock-mcp/";

  return {
    allowed,
    config_path: configPath,
    app_env: environment,
    source: {
      name: "mock_mcp_development",
      enabled,
      environment: sourceEnvironment,
      source_type: sourceType,
      production_allowed: productionAllowed,
      path: sourcePath
    },
    rejected_reason: allowed
      ? null
      : "mock_mcp_development is not enabled for the current non-production environment"
  };
}

function metricRatio(numerator, denominator) {
  return denominator ? numerator / denominator : null;
}

function round(value, digits = 6) {
  if (value === null || value === undefined || Number.isNaN(value)) return null;
  const factor = 10 ** digits;
  return Math.round(value * factor) / factor;
}

function addTotals(total, row) {
  total.impressions += Number(row.impressions || 0);
  total.clicks += Number(row.clicks || 0);
  total.spend += Number(row.spend || 0);
  total.conversions += Number(row.conversions || 0);
  total.revenue += Number(row.conversion_value ?? row.revenue ?? 0);
  return total;
}

function addGa4Totals(total, row) {
  total.sessions += Number(row.sessions || 0);
  total.users += Number(row.users || 0);
  total.engaged_sessions += Number(row.engaged_sessions || 0);
  total.events += Number(row.events || 0);
  total.key_events += Number(row.key_events || 0);
  total.conversions += Number(row.conversions || 0);
  total.revenue += Number(row.revenue || 0);
  return total;
}

function emptyAdTotals() {
  return {
    impressions: 0,
    clicks: 0,
    spend: 0,
    conversions: 0,
    revenue: 0
  };
}

function emptyGa4Totals() {
  return {
    sessions: 0,
    users: 0,
    engaged_sessions: 0,
    events: 0,
    key_events: 0,
    conversions: 0,
    revenue: 0
  };
}

function adMetrics(totals) {
  return {
    ctr: round(metricRatio(totals.clicks, totals.impressions)),
    cpc: round(metricRatio(totals.spend, totals.clicks), 2),
    cpm: round(metricRatio(totals.spend * 1000, totals.impressions), 2),
    cvr: round(metricRatio(totals.conversions, totals.clicks)),
    cpa: round(metricRatio(totals.spend, totals.conversions), 2),
    roas: round(metricRatio(totals.revenue, totals.spend), 4)
  };
}

function ga4Metrics(totals) {
  return {
    engagement_rate: round(metricRatio(totals.engaged_sessions, totals.sessions)),
    session_cvr: round(metricRatio(totals.conversions, totals.sessions)),
    key_event_rate: round(metricRatio(totals.key_events, totals.sessions)),
    revenue_per_session: round(metricRatio(totals.revenue, totals.sessions), 2)
  };
}

function percentChange(current, previous) {
  if (previous === null || previous === undefined || previous === 0) return null;
  return round((current - previous) / previous);
}

function compareObjects(current, previous) {
  const result = {};
  for (const key of Object.keys(current)) {
    if (typeof current[key] === "number" && typeof previous[key] === "number") {
      result[key] = percentChange(current[key], previous[key]);
    }
  }
  return result;
}

function groupByCampaign(rows) {
  const grouped = new Map();
  for (const row of rows) {
    const key = row.campaign_name || row.campaign || "unknown";
    if (!grouped.has(key)) {
      grouped.set(key, emptyAdTotals());
    }
    addTotals(grouped.get(key), row);
  }
  return [...grouped.entries()]
    .map(([campaign_name, totals]) => ({
      campaign_name,
      totals,
      metrics: adMetrics(totals)
    }))
    .sort((a, b) => b.totals.spend - a.totals.spend);
}

function groupByLandingPage(rows) {
  const grouped = new Map();
  for (const row of rows) {
    const key = row.landing_page || "unknown";
    if (!grouped.has(key)) {
      grouped.set(key, emptyGa4Totals());
    }
    addGa4Totals(grouped.get(key), row);
  }
  return [...grouped.entries()]
    .map(([landing_page, totals]) => ({
      landing_page,
      totals,
      metrics: ga4Metrics(totals)
    }))
    .sort((a, b) => b.totals.revenue - a.totals.revenue);
}

class MockMcpClient {
  constructor() {
    this.child = null;
    this.rl = null;
    this.nextId = 1;
    this.pending = new Map();
  }

  async start() {
    this.child = spawn(process.execPath, ["test/mock-mcp/server.js"], {
      cwd: REPO_ROOT,
      stdio: ["pipe", "pipe", "inherit"]
    });
    this.rl = readline.createInterface({ input: this.child.stdout, crlfDelay: Infinity });
    this.rl.on("line", (line) => {
      const message = JSON.parse(line);
      if (message.id && this.pending.has(message.id)) {
        this.pending.get(message.id)(message);
        this.pending.delete(message.id);
      }
    });
    await this.request("initialize", {
      protocolVersion: "2024-11-05",
      capabilities: {},
      clientInfo: {
        name: "ads-analyst-recipe-runner",
        version: "0.1.0"
      }
    });
    this.notify("notifications/initialized");
  }

  request(method, params = {}) {
    const id = this.nextId++;
    this.child.stdin.write(`${JSON.stringify({ jsonrpc: "2.0", id, method, params })}\n`);
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`Timed out waiting for ${method}`));
      }, 5000);
      this.pending.set(id, (message) => {
        clearTimeout(timer);
        if (message.error) {
          reject(new Error(message.error.message));
        } else {
          resolve(message.result);
        }
      });
    });
  }

  notify(method, params = {}) {
    this.child.stdin.write(`${JSON.stringify({ jsonrpc: "2.0", method, params })}\n`);
  }

  async callTool(name, args = {}) {
    const result = await this.request("tools/call", { name, arguments: args });
    return JSON.parse(result.content[0].text);
  }

  stop() {
    this.child?.kill();
  }
}

function buildArgs(args) {
  const toolArgs = {};
  if (args.startDate) toolArgs.start_date = args.startDate;
  if (args.endDate) toolArgs.end_date = args.endDate;
  return toolArgs;
}

function sourceTrace(payload) {
  return {
    name: payload.source?.name || "mock_mcp_development",
    source_type: payload.source?.source_type || "mock_mcp",
    environment: payload.source?.environment || "development",
    production_allowed: Boolean(payload.source?.production_allowed),
    fixture_path: payload.source?.fixture_path
  };
}

async function runPlatformCampaignPerformance(client, args, gate) {
  if (!args.platform || !["google_ads", "meta_ads"].includes(args.platform)) {
    throw new Error("platform-campaign-performance requires --platform google_ads or --platform meta_ads");
  }
  const payload = await client.callTool(MOCK_TOOLS[args.platform], buildArgs(args));
  const totals = payload.rows.reduce(addTotals, emptyAdTotals());
  return {
    recipe_id: "platform-campaign-performance",
    recipe_file: RECIPES["platform-campaign-performance"].file,
    connector_adapter: "connectors/mock-mcp.adapter.yml",
    platform: args.platform,
    source: sourceTrace(payload),
    environment_gate: gate,
    date_range: payload.date_range,
    timezone: payload.timezone,
    currency: payload.currency,
    row_count: payload.row_count,
    totals,
    metrics: adMetrics(totals),
    top_campaigns_by_spend: groupByCampaign(payload.rows).slice(0, 10),
    data_gaps: [
      "Mock MCP data only; not production account data.",
      "Attribution window and conversion definition are not provided by mock fixture."
    ]
  };
}

async function runGa4LandingPageQuality(client, args, gate) {
  const payload = await client.callTool(MOCK_TOOLS.ga4, buildArgs(args));
  const rows = payload.rows.filter((row) => {
    if (args.platform === "google_ads") return row.source === "google" && row.medium === "cpc";
    if (args.platform === "meta_ads") return row.source === "meta" && row.medium === "paid_social";
    return true;
  });
  const totals = rows.reduce(addGa4Totals, emptyGa4Totals());
  return {
    recipe_id: "ga4-landing-page-quality",
    recipe_file: RECIPES["ga4-landing-page-quality"].file,
    connector_adapter: "connectors/mock-mcp.adapter.yml",
    platform: "ga4",
    filter_platform: args.platform,
    source: sourceTrace(payload),
    environment_gate: gate,
    date_range: payload.date_range,
    timezone: payload.timezone,
    currency: payload.currency,
    row_count: rows.length,
    totals,
    metrics: ga4Metrics(totals),
    top_landing_pages_by_revenue: groupByLandingPage(rows).slice(0, 10),
    data_gaps: [
      "Mock MCP data only; not production GA4 data.",
      "Device, geo, funnel, path, consent mode, and event definitions are not provided by mock fixture."
    ]
  };
}

async function runCrossChannelPeriodCompare(client, args, gate) {
  if (!args.startDate || !args.endDate || !args.previousStartDate || !args.previousEndDate) {
    throw new Error("cross-channel-period-compare requires --start, --end, --previous-start, and --previous-end");
  }

  async function period(startDate, endDate) {
    const periodArgs = { ...args, startDate, endDate };
    const google = await runPlatformCampaignPerformance(client, { ...periodArgs, platform: "google_ads" }, gate);
    const meta = await runPlatformCampaignPerformance(client, { ...periodArgs, platform: "meta_ads" }, gate);
    const ga4 = await runGa4LandingPageQuality(client, periodArgs, gate);
    const adTotals = [google.totals, meta.totals].reduce(
      (acc, item) => {
        for (const key of Object.keys(acc)) acc[key] += item[key] || 0;
        return acc;
      },
      emptyAdTotals()
    );
    return {
      date_range: { start_date: startDate, end_date: endDate },
      google_ads: google,
      meta_ads: meta,
      ga4,
      paid_media_totals: adTotals,
      paid_media_metrics: adMetrics(adTotals)
    };
  }

  const current = await period(args.startDate, args.endDate);
  const previous = await period(args.previousStartDate, args.previousEndDate);

  return {
    recipe_id: "cross-channel-period-compare",
    recipe_file: RECIPES["cross-channel-period-compare"].file,
    connector_adapter: "connectors/mock-mcp.adapter.yml",
    source: {
      name: "mock_mcp_development",
      source_type: "mock_mcp",
      environment: "development",
      production_allowed: false
    },
    environment_gate: gate,
    current_period: current,
    previous_period: previous,
    comparison: {
      paid_media_totals_change: compareObjects(current.paid_media_totals, previous.paid_media_totals),
      paid_media_metrics_change: compareObjects(current.paid_media_metrics, previous.paid_media_metrics),
      ga4_totals_change: compareObjects(current.ga4.totals, previous.ga4.totals),
      ga4_metrics_change: compareObjects(current.ga4.metrics, previous.ga4.metrics)
    },
    data_gaps: [
      "Mock MCP data only; not production account data.",
      "Platform and GA4 conversions are not assumed equivalent.",
      "Attribution window, conversion definition, timezone alignment, and deduplication logic are not provided by mock fixture."
    ]
  };
}

async function main() {
  const args = parseArgs(process.argv);
  if (!args.recipeId || !RECIPES[args.recipeId]) {
    printHelp();
    throw new Error(`Unknown or missing recipe id: ${args.recipeId || "(missing)"}`);
  }

  assertFile(RECIPES[args.recipeId].file);
  assertFile("connectors/mock-mcp.adapter.yml");
  assertFile("test/mock-mcp/server.js");

  const gate = checkMockMcpAllowed();
  if (!gate.allowed) {
    throw new Error(`Environment Gate failed: ${gate.rejected_reason}`);
  }

  const client = new MockMcpClient();
  await client.start();
  try {
    let result;
    if (args.recipeId === "platform-campaign-performance") {
      result = await runPlatformCampaignPerformance(client, args, gate);
    } else if (args.recipeId === "ga4-landing-page-quality") {
      result = await runGa4LandingPageQuality(client, args, gate);
    } else if (args.recipeId === "cross-channel-period-compare") {
      result = await runCrossChannelPeriodCompare(client, args, gate);
    }

    result.generated_at = new Date().toISOString();
    const output = JSON.stringify(result, null, args.pretty ? 2 : 0);
    if (args.out) {
      const outputPath = path.resolve(REPO_ROOT, args.out);
      fs.mkdirSync(path.dirname(outputPath), { recursive: true });
      fs.writeFileSync(outputPath, `${output}\n`);
    }
    console.log(output);
  } finally {
    client.stop();
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});


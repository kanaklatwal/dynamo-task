There is an access log at /app/access.log. Analyze the traffic and summarize what you
find — how many requests there were, the clients involved, and which pages were
popular.

Save your findings as JSON to /app/report.json with exactly these keys:

- "total_requests": total number of log lines/requests (integer)
- "unique_ips": number of distinct client IPs (integer)
- "top_path": the single most-requested path (string)
# Proxy Pattern

## What problem does it solve?

Sometimes you need to control access to an object — delay its creation, check permissions, or throttle calls — without the caller knowing. The proxy sits in front of the real object and intercepts calls.

## What it does

A proxy implements the same interface as the real object and holds a reference to it. The caller talks to the proxy as if it were the real thing. The proxy decides whether and how to forward the call.

```
Caller → Proxy → Real Object
          ↑
    intercept here:
    lazy init / auth / rate limit
```

## Three proxy types

### 1. Virtual Proxy — lazy initialization
Delays creating an expensive object until it's actually needed.

```python
proxy = LazyLLMProxy()       # no client created yet
proxy.chat(...)              # client created here, on first use
proxy.chat(...)              # reuses existing client
```

Useful when initialization is slow (loading SDK, validating API key) and the object may never be used.

### 2. Protection Proxy — access control
Checks permissions before forwarding the call.

```python
protected.chat(..., role="admin")   # allowed → forwarded
protected.chat(..., role="guest")   # blocked → PermissionError
```

Useful for multi-tenant systems where different users have different LLM access levels.

### 3. Rate Limiting Proxy — throttling
Tracks call frequency and blocks calls that exceed a threshold.

```python
# max 3 calls per 5 seconds
call 1 → allowed
call 2 → allowed
call 3 → allowed
call 4 → RuntimeError: Rate limit exceeded
```

Useful for staying within API rate limits without cluttering business logic.

## The key insight

The caller never changes — it just calls `chat()`. Whether it hits a lazy proxy, a protected proxy, or a rate-limited proxy is transparent. You can stack proxies just like decorators:

```python
client = ClaudeClient()
client = RateLimitedLLMProxy(client, max_calls=10, window_seconds=60)
client = ProtectedLLMProxy(client, allowed_roles={"admin"})
```

## Proxy vs Decorator

They look identical in code — both wrap an object behind the same interface. The difference is intent:

| | Proxy | Decorator |
|---|---|---|
| Intent | Control access to the object | Add behavior to the object |
| Examples | Lazy init, auth, rate limiting | Logging, caching, retry |
| Knows about real object | Yes — controls it | Yes — extends it |

In practice the line is blurry. The pattern name signals intent to the reader.

## Why it matters for AI engineering

- **Virtual proxy**: don't load the LLM client until the first request — faster startup
- **Protection proxy**: enforce which users or services can call expensive models
- **Rate limiting proxy**: stay within API quotas without touching pipeline code
- All three can be stacked and the calling code never changes

## The structure

| Role | In this example |
|---|---|
| Subject interface | `LLMClient` |
| Real subject | `ClaudeClient` |
| Proxies | `LazyLLMProxy`, `ProtectedLLMProxy`, `RateLimitedLLMProxy` |

## Files

- `proxy.py` — three proxy types demonstrated on a Claude client

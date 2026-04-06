# schedulifyx

Official Python SDK for [SchedulifyX API](https://app.schedulifyx.com/docs/) — Three-tier API access for social media integration.

## Architecture

SchedulifyX uses a **Three-Tier API Access Model**:

| Tier | Access | Cost |
|------|--------|------|
| **Tier 1 — Embed** (default) | Tenants, webhooks, pre-built UI components | Free |
| **Tier 2 — Publishing API** | Posts, accounts, analytics, queue, profiles | Free (approval required) |
| **Tier 3 — Full Engagement** | Inbox, comments, mentions + all Tier 2 | $149/year |

- **This SDK** (server-side): Manage tenants, generate client tokens, configure webhooks (all tiers). With Tier 2+ keys, also access posts, accounts, analytics, and more via REST.
- **Embed SDK** (`@schedulifyx/embed`, client-side): Render pre-built UI components — available on all tiers, no approval needed.

## Installation

```bash
pip install schedulifyx
```

## Quick Start

```python
from schedulifyx import SchedulifyX, Tenant, ClientToken

client = SchedulifyX('sk_live_YOUR_API_KEY')

# 1. Create a tenant (maps to a user in your app)
tenant: Tenant = client.tenants.create(
    external_id='user_123',
    email='user@example.com',
    name='John Doe'
)

# 2. Generate a client token for embedding UI components
token: ClientToken = client.tenants.generate_client_token(
    tenant.id,
    components=['post-creator', 'accounts', 'analytics'],
    expires_in=3600
)

# 3. Send token.token to your frontend for the Embed SDK
print(token.token)        # The JWT string
print(token.expires_at)   # ISO timestamp
```

## Configuration

```python
from schedulifyx import SchedulifyX

# Simple initialization
client = SchedulifyX('sk_live_YOUR_API_KEY')

# With options
client = SchedulifyX(
    api_key='sk_live_YOUR_API_KEY',
    base_url='https://api.schedulifyx.com',  # optional, default
    timeout=30  # optional, in seconds, default 30
)
```

## API Reference

### Tenants

Tenants represent users in your application. Each tenant can connect social accounts and use embedded components.

```python
# Create a tenant
tenant = client.tenants.create(
    external_id='user_123',
    email='user@example.com',
    name='John Doe',
    metadata={'plan': 'pro'}
)

# List tenants
tenants = client.tenants.list(limit=20, search='john')

# Get single tenant
t = client.tenants.get('tenant_uuid')

# Update tenant
client.tenants.update('tenant_uuid', name='Jane Doe')

# Delete tenant (removes all their data)
client.tenants.delete('tenant_uuid')
```

### Social Account Connection

Accounts are connected permanently via OAuth — they survive client token expiry.

```python
# Get OAuth URL for tenant to connect a platform
response = client.tenants.get_connect_url('tenant_uuid', 'instagram',
    redirect_uri='https://yourapp.com/callback'
)
# Returns a dict (not a dataclass) — access the URL directly
# Redirect user's browser to response['data']['url']

# List tenant's connected accounts
accounts = client.tenants.list_accounts('tenant_uuid')

# Disconnect an account
client.tenants.disconnect_account('tenant_uuid', 'account_uuid')

# Connect Bluesky (no OAuth, uses app password)
client.tenants.connect_bluesky('tenant_uuid',
    identifier='user.bsky.social',
    app_password='xxxx-xxxx-xxxx-xxxx'
)

# Connect Mastodon (token-based)
client.tenants.connect_mastodon('tenant_uuid',
    instance_url='https://mastodon.social',
    access_token='token_here'
)
```

### Client Tokens

Generate short-lived tokens for your frontend to render embedded UI components.

```python
# Generate client token (max 1 hour TTL)
token = client.tenants.generate_client_token('tenant_uuid',
    components=['post-creator', 'accounts', 'inbox', 'analytics'],
    expires_in=3600,
    allowed_origins=['https://yourapp.com']
)

print(token.token)        # Pass to frontend Embed SDK
print(token.expires_at)   # ISO timestamp
print(token.components)   # List of allowed component names
```

### Webhooks

```python
# Create a webhook
webhook = client.webhooks.create(
    name='My Webhook',
    url='https://your-server.com/webhooks',
    events=['post.published', 'post.failed', 'account.connected']
)

# List webhooks
webhooks = client.webhooks.list()

# Update a webhook
client.webhooks.update('wh_123', events=['post.published'], is_active=False)

# Rotate secret
rotated = client.webhooks.rotate_secret('wh_123')

# Test a webhook
client.webhooks.test('wh_123', event_type='post.published')

# Get event history
events = client.webhooks.get_events('wh_123')

# Get available event types
types = client.webhooks.get_event_types()

# Delete a webhook
client.webhooks.delete('wh_123')
```

### Usage

```python
usage = client.usage()
print(f"{usage.monthly_requests}/{usage.monthly_limit} monthly requests used")
print(f"{usage.monthly_remaining} remaining this month")
```

## Error Handling

```python
from schedulifyx import SchedulifyX, SchedulifyXError

client = SchedulifyX('sk_live_YOUR_API_KEY')

try:
    client.tenants.create(external_id='user_123')
except SchedulifyXError as e:
    print(f'API Error: {e.code} - {e.message}')
    print(f'Status: {e.status}')
    print(f'Details: {e.details}')
```

## Type Hints

Most API methods return **typed dataclass instances** (not raw dicts). The SDK automatically
converts camelCase API responses to snake_case dataclass fields.

> **Note:** `get_connect_url()`, `delete()`, and `disconnect_account()` return raw
> `Dict[str, Any]` since their responses are simple confirmations or redirect URLs.

```python
from schedulifyx import (
    SchedulifyX,
    SchedulifyXError,
    Tenant,
    TenantAccount,
    ClientToken,
    Webhook,
    WebhookEvent,
    WebhookEventType,
    Usage,
    PaginatedResponse,
)
```

## Migration from v1.x

v2.0 introduced the three-tier access model. Direct data API methods were removed from the default (Tier 1) SDK, but are now available again with higher-tier API keys:

| Method | Tier 1 (Embed) | Tier 2 (Publishing) | Tier 3 (Engagement) |
|---|---|---|---|
| `client.posts.*` | Use embedded component | ✅ REST API | ✅ REST API |
| `client.accounts.*` | Use embedded component | ✅ REST API | ✅ REST API |
| `client.analytics.*` | Use embedded component | ✅ REST API | ✅ REST API |
| `client.queue.*` | Use embedded component | ✅ REST API | ✅ REST API |
| `client.x_twitter.*` | Use embedded component | ✅ REST API | ✅ REST API |
| `client.profiles.*` | Use embedded component | ✅ REST API | ✅ REST API |
| `client.comments.*` | Use embedded component | — | ✅ REST API |
| `client.inbox.*` | Use embedded component | — | ✅ REST API |
| `client.mentions.*` | Use embedded component | — | ✅ REST API |

**New in v2.0:**
- `client.tenants.generate_client_token()` — Generate tokens for embed SDK
- Persistent account connections via OAuth (accounts survive token expiry)
- Request Tier 2/3 access from your [API Keys dashboard](https://app.schedulifyx.com/settings/api)

See the [Embed Components documentation](https://app.schedulifyx.com/docs/embed-components) for frontend integration or the [Publishing API docs](https://app.schedulifyx.com/docs/api-posts) for REST access.

## License

MIT

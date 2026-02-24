# schedulifyx

Official Python SDK for [SchedulifyX API](https://app.schedulifyx.com/docs/) - Social media scheduling made easy.

## Installation

```bash
pip install schedulifyx
```

## Quick Start

```python
from schedulifyx import SchedulifyX

client = SchedulifyX('sk_live_YOUR_API_KEY')

# List all posts
posts = client.posts.list()
print(posts['data'])

# Create a scheduled post
post = client.posts.create(
    content='Hello from the SDK! 🚀',
    platforms=[{'platform': 'twitter', 'accountId': 'acc_123'}],
    scheduled_for='2024-12-20T10:00:00Z'
)

# Publish immediately
client.posts.publish(post['data']['id'])
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

### Posts

```python
# List posts with filters
posts = client.posts.list(
    status='scheduled',
    account_id='acc_123',
    limit=20,
    offset=0
)

# Get single post
post = client.posts.get('post_123')

# Create post
new_post = client.posts.create(
    content='Hello world!',
    platforms=[
        {'platform': 'twitter', 'accountId': 'acc_123'},
        {'platform': 'instagram', 'accountId': 'acc_456'}
    ],
    scheduled_for='2024-12-20T10:00:00Z',
    media_urls=['https://example.com/image.jpg']
)

# Update post
client.posts.update('post_123', content='Updated content', scheduled_for='2024-12-21T10:00:00Z')

# Delete post
client.posts.delete('post_123')

# Publish immediately
client.posts.publish('post_123')
```

### Accounts

```python
# List all connected accounts
accounts = client.accounts.list()

# Filter by platform
instagram_accounts = client.accounts.list(platform='instagram')

# Get single account
account = client.accounts.get('acc_123')

# Get Pinterest boards
boards = client.accounts.get_pinterest_boards('acc_pinterest_123')
```

### Profiles

```python
# List publishing profiles
profiles = client.profiles.list()

# Create a profile
profile = client.profiles.create(
    name='Morning Posts',
    description='Profile for morning content',
    color='#3B82F6'
)

# Update a profile
client.profiles.update('profile_123', name='Updated Name')

# Delete a profile
client.profiles.delete('profile_123')
```

### Analytics

```python
# Get overview
overview = client.analytics.overview()

# Get account-specific analytics
account_analytics = client.analytics.for_account('acc_123', days=30)

# Get all analytics
all_analytics = client.analytics.list(
    start_date='2024-01-01',
    end_date='2024-12-31'
)
```

### Queue

```python
# Get queue schedule
queue = client.queue.get_slots('acc_123')

# Set queue schedule
client.queue.set_slots(
    account_id='acc_123',
    timezone='America/New_York',
    slots=[
        {'dayOfWeek': 1, 'time': '09:00'},
        {'dayOfWeek': 1, 'time': '15:00'},
        {'dayOfWeek': 3, 'time': '12:00'}
    ],
    is_active=True
)

# Get next available slot
next_slot = client.queue.get_next_slot('acc_123')

# Preview upcoming slots
preview = client.queue.preview('acc_123', count=10)

# Get all queue schedules
all_queues = client.queue.get_all()

# Delete queue schedule
client.queue.delete_slots('acc_123')
```

### Webhooks

```python
# Create a webhook
webhook = client.webhooks.create(
    name='My Webhook',
    url='https://your-server.com/webhooks',
    events=['post.published', 'post.failed']
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

### Comments

```python
comments = client.comments.list(sentiment='positive', limit=20)
comment = client.comments.get('comment_123')
replies = client.comments.get_replies('comment_123')
client.comments.reply('comment_123', message='Thanks!')
stats = client.comments.stats()
```

### Inbox

```python
conversations = client.inbox.list(status='open', has_unread=True)
messages = client.inbox.get_messages('conv_123')
client.inbox.reply('conv_123', message='Thanks for reaching out!')
inbox_stats = client.inbox.stats()
```

### Mentions

```python
mentions = client.mentions.list(platform='instagram', status='unread')
mention_stats = client.mentions.stats()
```

### X/Twitter BYOK

```python
config = client.x_twitter.get_config()
client.x_twitter.set_credentials(
    api_key='...', api_secret='...',
    access_token='...', access_token_secret='...'
)
client.x_twitter.switch_mode(account_id='acc_123', mode='byok')
```

### Usage

```python
usage = client.usage()
print(f"{usage['data']['requestsToday']}/{usage['data']['dailyLimit']} daily requests used")
```

### Multi-Tenant

```python
# Create a tenant
tenant = client.tenants.create(
    external_id='user_123',
    email='user@example.com',
    name='John Doe'
)

# Get OAuth URL for tenant
response = client.tenants.get_connect_url(tenant['data']['id'], 'instagram')

# List tenant's accounts
accounts = client.tenants.list_accounts(tenant['data']['id'])

# Connect Bluesky for tenant
client.tenants.connect_bluesky(
    tenant['data']['id'],
    identifier='user.bsky.social',
    app_password='xxxx-xxxx-xxxx-xxxx'
)

# Disconnect account
client.tenants.disconnect_account(tenant['data']['id'], 'acc_123')
```

## Error Handling

```python
from schedulifyx import SchedulifyX, SchedulifyXError

client = SchedulifyX('sk_live_YOUR_API_KEY')

try:
    client.posts.create(
        content='Test',
        platforms=[{'platform': 'twitter', 'accountId': 'acc_123'}]
    )
except SchedulifyXError as e:
    print(f'API Error: {e.code} - {e.message}')
    print(f'Status: {e.status}')
    print(f'Details: {e.details}')
```

## Type Hints

The SDK includes type hints and dataclasses:

```python
from schedulifyx import (
    SchedulifyX,
    SchedulifyXError,
    Post,
    Account,
    Profile,
    Analytics,
    AnalyticsOverview,
    Usage,
    Tenant,
    QueueSlot,
    QueueSchedule,
    Webhook,
    Comment,
    CommentStats,
    Conversation,
    InboxMessage,
    InboxStats,
    Mention,
    MentionStats,
    PaginatedResponse,
)
```

## License

MIT
